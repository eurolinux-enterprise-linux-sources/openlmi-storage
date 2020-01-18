# Copyright (C) 2012-2013 Red Hat, Inc.  All rights reserved.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Authors: Jan Safranek <jsafrane@redhat.com>
"""
    Support functions for Blivet.
"""

import subprocess
import os
import parted
import pywbem
import blivet
import lmi.providers.cmpi_logging as cmpi_logging

GPT_TABLE_SIZE = 34 * 2  # there are two copies
MBR_TABLE_SIZE = 1

LOG = cmpi_logging.get_logger(__name__)

def _align_up(address, alignment):
    """ Align address to nearest higher address divisible by alignment."""
    return (address / alignment + 1) * alignment

def _align_down(address, alignment):
    """ Align address to nearest lower address divisible by alignment."""
    return (address / alignment) * alignment

@cmpi_logging.trace_function
def get_logical_partition_start(partition):
    """
        Return starting sector of logical partition metadata, relative to
        extended partition start.
    """
    disk = partition.disk
    ext = disk.format.partedDisk.getExtendedPartition()
    if not ext:
        raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                'Cannot find extended partition.')

    metadata = None
    part = ext.nextPartition()
    while part is not None:
        if (part.type & parted.PARTITION_LOGICAL
                and part.type & parted.PARTITION_METADATA):
            metadata = part
        if part.path == partition.path:
            break
        part = part.nextPartition()

    if not part:
        raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                'Cannot find the partition on the disk.')
    if not metadata:
        raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                'Cannot find metadata for the partition.')

    return metadata.geometry.start

@cmpi_logging.trace_function
def get_partition_table_size(device):
    """
        Return size of partition table (in blocks) for given Anaconda
        StorageDevice instance.
    """
    if device.format:
        fmt = device.format
        if fmt.labelType == "gpt":
            return GPT_TABLE_SIZE * 2
        if fmt.labelType == "msdos":
            return MBR_TABLE_SIZE
    return 0

@cmpi_logging.trace_function
def get_available_sectors(device):
    """
        Return (start, end), where start is the first usable sector after
        partition table and end is the last usable sector before any
        partition table copy
    """
    size = device.partedDevice.length
    if device.format:
        fmt = device.format
        alignment = device.partedDevice.optimumAlignment.grainSize
        if fmt.labelType == "gpt":
            return (
                    _align_up(GPT_TABLE_SIZE, alignment),
                    _align_down(size - GPT_TABLE_SIZE - 1, alignment))
        if fmt.labelType == "msdos":
            return(
                    _align_up(MBR_TABLE_SIZE, alignment),
                    _align_down(size - 1, alignment))

    if isinstance(device, blivet.devices.PartitionDevice):
        if device.isExtended:
            return(
                    _align_up(0, alignment),
                    _align_down(size - 1, alignment))

    return (0, size - 1)

@cmpi_logging.trace_function
def remove_partition(storage, device):
    """
        Remove PartitionDevice from system, i.e. delete a partition.
    """
    action = blivet.deviceaction.ActionDestroyDevice(device)
    do_storage_action(storage, [action])

@cmpi_logging.trace_function
def do_storage_action(storage, actions):
    """
        Perform array Anaconda DeviceActions on given Storage instance.
    """
    do_partitioning = False
    need_reset = False

    for action in actions:
        LOG().trace_info("Running action " + str(action))
        LOG().trace_info("    on device " + repr(action.device))

        if (isinstance(action.device, blivet.devices.PartitionDevice)
                and isinstance(action,
                        blivet.deviceaction.ActionCreateDevice)):
            do_partitioning = True

        if (isinstance(action.device, blivet.devices.PartitionDevice) and not
                isinstance(action, blivet.deviceaction.ActionDestroyFormat)):
            # The action is partition manipulation action, Blivet needs reload
            # to get parted devices right
            need_reset = True
        elif not isinstance(action,
                    (blivet.deviceaction.ActionDestroyFormat,
                    blivet.deviceaction.ActionDestroyDevice)):
            # The action is device creation/manipulation, Blivet needs reload
            # to get new/changed device properties (like udev symlinks,
            # uuid etc.)
            need_reset = True

        storage.devicetree.registerAction(action)
    try:
        if do_partitioning:
            # this must be called when creating a partition
            LOG().trace_verbose("Running doPartitioning()")
            blivet.partitioning.doPartitioning(storage=storage)

        storage.devicetree.processActions(dryRun=False)

        for action in actions:
            if not isinstance(action,
                    blivet.deviceaction.ActionDestroyDevice):
                LOG().trace_verbose(
                        "Result: " + repr(action.device))

    finally:
        if need_reset:
            os.system('udevadm trigger --subsystem-match block')
            os.system('udevadm settle')
            storage.reset()

def log_storage_call(msg, args):
    """
        Log a storage action to log.
        INFO level will be used. The message should have format
        'CREATE <type>' or 'DELETE <type>', where <type> is type of device
        (PARTITION, MDRAID, VG, LV, ...). The arguments will be printed
        after it in no special orded, only StorageDevice instances
        will be replaced with device.path.
    """
    print_args = {}
    for (key, value) in args.iteritems():
        if isinstance(value, blivet.devices.StorageDevice):
            value = value.path
        if key == 'parents':
            value = [d.path for d in value]
        print_args[key] = value

    LOG().info(msg + ": " + str(print_args))

@cmpi_logging.trace_function
def get_persistent_name(device):
    """
    Return stable device name of given device.

    Current order of significance: by-id, by-partuuid, by-path, by-uuid, /dev

    :param device: (``StorageDevice``) The device.
    :returns: ``string``
    """
    prefixes = ["/dev/disk/by-id/", "/dev/disk/by-partuuid/",
            "/dev/disk/by-path/", "/dev/disk/by-uuid/"]
    links = device.deviceLinks
    found = False
    # Find a symlink which matches the topmost prefix"
    for prefix in prefixes:
        for link in links:
            if link.startswith(prefix):
                found = True
                break
        if found:
            break
    if found:
        return link
    return device.path

@cmpi_logging.trace_function
def get_device_for_persistent_name(_blivet, name):
    """
    Return device for given device name or device symlink name as returned
    by get_persistent_name.

    :param _blivet: (``Blivet``) Blivet instance.
    :param name: (``string``) Name of the device or device symlink.
    :returns: ``StorageDevice`` or ``None``, if no device matches the name.
    """
    for device in _blivet.devices:
        if name == device.path:
            return device
        if name in device.deviceLinks:
            return device
    return None

@cmpi_logging.trace_function
def check_empty_parameters(**kwargs):
    """
    Check for empty parameters. Throw an error if there are any.
    """
    for p, a in kwargs.items():
        if a is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                  "Empty parameter: %s." % p)

@cmpi_logging.trace_function
def assert_unused(_blivet, devices):
    """
    Check that given devices are not used. Throw pywbem.CIMError if so.

    'Used' means that the device is either mounted or other device depends on
    it.

    :param _blivet: (``Blivet``) Blivet instance.
    :param devices: (array of ``StorageDevice``s) Devices to check.
    :returns None:
    """
    for device in devices:
        fs = device.format
        if fs:
            try:
                mountpoint = fs.mountpoint
            except AttributeError:
                mountpoint = None
            if mountpoint:
                # The device has mounted filesystem -> it is used.
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Device %s is mounted at %s." % (device.path, mountpoint))

        children = _blivet.deviceDeps(device)
        for child in children:
            # Members of stopped stopped MD RAID and other stopped devices
            # are unused.
            if not child.status:
                continue

            # Unmounted BTRFs formats are unused.
            if isinstance(child, blivet.devices.BTRFSVolumeDevice):
                assert_unused(_blivet, [child])
                continue

            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                "Device %s is used by %s." % (device.path, child.path))
