# Copyright (C) 2012-2014 Red Hat, Inc.  All rights reserved.
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
#          Jan Synacek  <jsynacek@redhat.com>
# -*- coding: utf-8 -*-
"""
Module for VGStoragePoolProvider class.

VGStoragePoolProvider
-----------------

.. autoclass:: VGStoragePoolProvider
    :members:

"""

from lmi.storage.DeviceProvider import DeviceProvider
import pywbem
import blivet
import lmi.providers.cmpi_logging as cmpi_logging
from lmi.storage.SettingHelper import SettingHelper
from lmi.storage.SettingManager import StorageSetting
import lmi.storage.util.units as units
import lmi.storage.util.storage as storage
import math
from lmi.storage.SettingProvider import SettingProvider

LOG = cmpi_logging.get_logger(__name__)

class VGStoragePoolProvider(DeviceProvider, SettingHelper):
    """
        Abstract provider of Pools.
    """
    @cmpi_logging.trace_method
    def __init__(self, classname, *args, **kwargs):
        super(VGStoragePoolProvider, self).__init__(
                setting_classname='LMI_LVStorageSetting',
                *args, **kwargs)
        self.classname = classname

    @cmpi_logging.trace_method
    def provides_name(self, object_name):
        """
            Returns True, if this class is provider for given CIM InstanceName.
        """
        if not object_name.has_key('InstanceID'):
            return False

        instance_id = object_name['InstanceID']
        if instance_id is None:
            return False
        parts = instance_id.split(":")
        if len(parts) != 3:
            return False
        if parts[0] != "LMI":
            return False
        if parts[1] != self.classname:
            return False
        return True

    @cmpi_logging.trace_method
    def provides_device(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        return False

    @cmpi_logging.trace_method
    def get_device_for_name(self, object_name):
        """
            Returns Anaconda StorageDevice for given CIM InstanceName or
            None if no device is found.
        """
        if self.provides_name(object_name):
            instance_id = object_name['InstanceID']
            parts = instance_id.split(":")
            vgname = parts[2]
            for vg in self.enumerate_devices():
                if vg.name == vgname:
                    return vg
            return None

    @cmpi_logging.trace_method
    def enumerate_devices(self):
        """
            Returns Anaconda StorageDevices managed by this provider.
        """
        return []

    @cmpi_logging.trace_method
    def get_name_for_device(self, device):
        """
            Returns CIM InstanceName for given Anaconda StorageDevice.
            None if no device is found.
        """
        vgname = device.name
        name = pywbem.CIMInstanceName(self.classname,
                namespace=self.config.namespace,
                keybindings={
                    'InstanceID' : "LMI:%s:%s" % (self.classname, vgname)
                })
        return name

    @cmpi_logging.trace_method
    # pylint: disable-msg=W0221
    def get_instance(self, env, model, device=None):
        """
            Provider implementation of GetInstance intrinsic method.
            It fills all VGStoragePool properties.
        """
        if not self.provides_name(model):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Wrong keys.")
        if not device:
            device = self.get_device_for_name(model)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find the VG.")

        model['Primordial'] = False

        model['PoolID'] = device.name
        model['Name'] = device.path
        model['UUID'] = device.uuid

        return model

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        """Enumerate instances.

        The WBEM operations EnumerateInstances and EnumerateInstanceNames
        are both mapped to this method.
        This method is a python generator

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        model -- A template of the pywbem.CIMInstances to be generated.
            The properties of the model are already filtered according to
            the PropertyList from the request.  Only properties present in
            the model need to be given values.  If you prefer, you can
            always set all of the values, and the instance will be filtered
            for you.
        keys_only -- A boolean.  True if only the key properties should be
            set on the generated instances.

        Possible Errors:
        CIM_ERR_FAILED (some other unspecified error occurred)

        """
        model.path.update({'InstanceID': None})

        for device in self.enumerate_devices():
            name = self.get_name_for_device(device)
            model['InstanceID'] = name['InstanceID']
            if keys_only:
                yield model
            else:
                yield self.get_instance(env, model, device)

    @cmpi_logging.trace_method
    def cim_method_getsupportedsizes(self, env, object_name,
                                     param_elementtype=None,
                                     param_goal=None,
                                     param_sizes=None):
        """Implements VGStoragePoolProvider.GetSupportedSizes() """
        rval = self.Values.GetSupportedSizes.Use_GetSupportedSizes_instead
        return (rval, [])

    @cmpi_logging.trace_method
    def enumerate_settings(self, setting_provider):
        """
            This method returns iterable with all instances of LMI_*Setting
            as Setting instances.
        """
        for vg in self.enumerate_devices():
            yield self._get_setting_for_device(vg, setting_provider)

    @cmpi_logging.trace_method
    def get_setting_for_id(self, setting_provider, instance_id):
        """
            Return Setting instance, which corresponds to LMI_*Setting with
            given InstanceID.
            Return None if there is no such instance.

            Subclasses must override this method.
        """
        path = setting_provider.parse_setting_id(instance_id)
        if not path:
            return None
        device = storage.get_device_for_persistent_name(self.storage, path)
        if not path:
            return None
        return self._get_setting_for_device(device, setting_provider)

    @cmpi_logging.trace_method
    def get_associated_element_name(self, setting_provider, instance_id):
        """
            Return CIMInstanceName of ManagedElement for ElementSettingData
            association for setting with given ID.
            Return None if no such ManagedElement exists.
        """
        path = setting_provider.parse_setting_id(instance_id)
        if not path:
            return None
        device = storage.get_device_for_persistent_name(self.storage, path)
        if not device:
            return None
        return self.get_name_for_device(device)

    @cmpi_logging.trace_method
    def get_supported_setting_properties(self, setting_provider):
        """
            Return hash property_name -> constructor.
                constructor is a function which takes string argument
                and returns CIM value. (i.e. pywbem.Uint16
                or bool or string etc).
            This hash will be passed to SettingProvider.__init__
        """
        return {
                'ExtentSize': pywbem.Uint64,
                'DataRedundancyGoal': pywbem.Uint16,
                'DataRedundancyMax': pywbem.Uint16,
                'DataRedundancyMin': pywbem.Uint16,
                'ExtentStripeLength' : pywbem.Uint16,
                'ExtentStripeLengthMax' : pywbem.Uint16,
                'ExtentStripeLengthMin' : pywbem.Uint16,
                'NoSinglePointOfFailure' : SettingProvider.string_to_bool,
                'PackageRedundancyGoal' : pywbem.Uint16,
                'PackageRedundancyMax' : pywbem.Uint16,
                'PackageRedundancyMin' : pywbem.Uint16,
                'ParityLayout' : pywbem.Uint16,
                'SpaceLimit': pywbem.Uint64,
                'ThinProvisionedInitialReserve': pywbem.Uint64,
                'ThinProvisionedPoolType': pywbem.Uint16,
        }

    @cmpi_logging.trace_method
    def get_setting_ignore(self, setting_provider):
        return {
                'CompressedElement': False,
                'CompressionRate': 1,
                'InitialSynchronization': 0,
                'UseReplicationBuffer': 0,
        }

    @cmpi_logging.trace_method
    def get_setting_validators(self, setting_provider):
        return {
                'ExtentSize': self._check_extent_size
        }


    @cmpi_logging.trace_method
    def _check_extent_size(self, value):
        """
            Check if the given value is acceptable as
            VGStorageSetting.ExtentSize.
        """
        # lowest value is 1MB
        if value < units.MEGABYTE:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Property ExtentSize must be at least 1MiB")
        # must be power of 2
        exp = math.log(value, 2)
        if math.floor(exp) != exp:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Property ExtentSize must be power of 2")
        return True


    @cmpi_logging.trace_method
    def do_delete_instance(self, device):
        storage.log_storage_call("DELETE VG",
                {'device': device})
        action = blivet.deviceaction.ActionDestroyDevice(device)
        storage.do_storage_action(self.storage, [action])


    class Values(DeviceProvider.Values):
        class GetSupportedSizeRange(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedSizes_instead = pywbem.Uint32(2)
            Invalid_Element_Type = pywbem.Uint32(3)
            class ElementType(object):
                Storage_Pool = pywbem.Uint16(2)
                Storage_Volume = pywbem.Uint16(3)
                Logical_Disk = pywbem.Uint16(4)
                Thin_Provisioned_Volume = pywbem.Uint16(5)
                Thin_Provisioned_Logical_Disk = pywbem.Uint16(6)

        class GetSupportedSizes(object):
            Method_completed_OK = pywbem.Uint32(0)
            Method_not_supported = pywbem.Uint32(1)
            Use_GetSupportedSizes_instead = pywbem.Uint32(2)
            Invalid_Element_Type = pywbem.Uint32(3)
            class ElementType(object):
                Storage_Pool = pywbem.Uint16(2)
                Storage_Volume = pywbem.Uint16(3)
                Logical_Disk = pywbem.Uint16(4)
                Thin_Provisioned_Volume = pywbem.Uint16(5)
                Thin_Provisioned_Logical_Disk = pywbem.Uint16(6)

        class SpaceLimitDetermination(object):
            Allocated = pywbem.Uint16(2)
            Quote = pywbem.Uint16(3)
            Limitless = pywbem.Uint16(4)

        class ThinProvisionedPoolType(object):
            ThinlyProvisionedAllocatedStoragePool = pywbem.Uint16(7)
            ThinlyProvisionedQuotaStoragePool = pywbem.Uint16(8)
            ThinlyProvisionedLimitlessStoragePool = pywbem.Uint16(9)
