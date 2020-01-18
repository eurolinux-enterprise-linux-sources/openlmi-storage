#!/usr/bin/python
# -*- Coding:utf-8 -*-
#
# Copyright (C) 2012 Red Hat, Inc.  All rights reserved.
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
#

""" Base module for all storage tests. """

import os
import unittest
import pywbem
import subprocess
import pyudev
import time
import socket
import Queue
import threading
import blivet

class StorageTestBase(unittest.TestCase):
    """
        This is base class of OpenLMI storage tests.
        It monitors all devices created between setUp and tearDown
        and tries to remove them in tearDown.
    """

    SYSTEM_CLASS_NAME = "PG_ComputerSystem"
    DISK_CLASS = "LMI_StorageExtent"

    DEFAULT_JOB_TIMEOUT = 5  # seconds

    JOB_CREATED = 4096  # usual value of Method Parameters Checked - Job Started

    @classmethod
    def setUpClass(cls):
        cls.url = os.environ.get("LMI_CIMOM_URL", "https://localhost:5989")
        cls.username = os.environ.get("LMI_CIMOM_USERNAME", "root")
        cls.password = os.environ.get("LMI_CIMOM_PASSWORD", "")
        cls.disk = os.environ.get("LMI_STORAGE_DISK", "")
        cls.partitions = os.environ.get("LMI_STORAGE_PARTITIONS", "").split()
        cls.cimom = os.environ.get("LMI_CIMOM_BROKER", "sblim-sfcb")
        cls.clean = os.environ.get("LMI_STORAGE_CLEAN", "Yes")
        cls.verbose = os.environ.get("LMI_STORAGE_VERBOSE", None)
        cls.mnt_dir = os.environ.get("LMI_STORAGE_MNT_DIR", "/mnt")
        cls.mydir = os.path.dirname(__file__)
        cls.wbemconnection = pywbem.WBEMConnection(cls.url, (cls.username, cls.password))

        elems = cls.wbemconnection.ExecQuery("WQL",
                    'select * from CIM_StorageExtent where Name="'
                    + cls.disk + '"')
        if elems:
            cls.disk_name = elems[0].path

        cls.partition_names = []
        for device in cls.partitions:
            elems = cls.wbemconnection.ExecQuery("WQL",
                    'select * from CIM_StorageExtent where Name="'
                    + device + '"')
            if elems:
                cls.partition_names.append(elems[0].path)

        # get correct system name
        cls.SYSTEM_NAME = cls.disk_name['SystemName']

    def setUp(self):
        self.start_udev_monitor()

    def start_udev_monitor(self):
        # pylint: disable-msg=W0201
        self.udev_context = pyudev.Context()
        self.udev_monitor = pyudev.Monitor.from_netlink(self.udev_context)
        self.udev_monitor.filter_by('block')
        self.udev_observer = pyudev.MonitorObserver(
                self.udev_monitor, self.udev_event)
        self.devices = []
        self.udev_observer.start()

    def stop_udev_monitor(self):
        self.udev_observer.stop()

    def udev_event(self, action, device):
        if action == 'change':
            return

        if self.verbose:
            print "UDEV event:", action, device.device_node
        if action == 'add':
            self.devices.append(device.device_node)
        if action == 'remove':
            if device.device_node in self.devices:
                self.devices.remove(device.device_node)

    def destroy_created(self):
        """
            Destroy all devices created during the tests as recorded by the
            udev. It returns nr. of removed items.
        """
        count = 0

        # remove them in reverse order
        while self.devices:
            device = self.devices.pop()
            udev_device = pyudev.Device.from_device_file(
                    self.udev_context, device)
            if self.verbose:
                print "Destroying %s:%s" % (device, udev_device.device_type)

            if udev_device.device_type == 'partition':
                count += 1
                self.destroy_mbr(udev_device.parent.device_node)
            if udev_device.device_type == 'disk':
                # is it RAID?
                try:
                    if udev_device['MD_LEVEL']:
                        count += 1
                        self.destroy_md(device)
                except KeyError:
                    pass  # it's not RATD

            # TODO: add LVM
        return count


    def destroy_vg(self, vgname):
        """
            Destroy given volume group, not using CIM.
            This method should be called when a test fails and wants to clean
            up its mess.
        """
        return self.log_run(["vgremove", "-f", "/dev/mapper/" + vgname])

    def destroy_md(self, md_device_id):
        """
            Destroy given RAID, not using CIM.
            This method should be called when a test fails and wants to clean
            up its mess.
        """
        return self.log_run([self.mydir + "/tools/mdremove", md_device_id])

    def destroy_mbr(self, disk_device_id):
        """
            Destroy any partition table on given device.
            This method should be called when a test fails and wants to clean
            up its mess.
        """
        return self.log_run([self.mydir + "/tools/mbrremove", disk_device_id])

    def restart_cim(self):
        """
            Restart CIMOM
        """
        ret = self.log_run(["systemctl", "restart", self.cimom])
        time.sleep(1)
        if ret == 0:
            self.wbemconnection = pywbem.WBEMConnection(
                    self.url, (self.username, self.password))
        return ret



    def log_run(self, args):
        """
            Print arguments and run them.
            args must be prepared for subprocess.call()
        """
        print "Running:", " ".join(args)
        return subprocess.call(args)


    def tearDown(self):
        """
            Default teardown. It destroys any devices created since setUp().
            It restarts CIMOM if any devices were destroyed.
            
            Each test should clean after itself!
        """
        # try to destroy everything and restart CIMOM
        self.stop_udev_monitor()
        if self.clean:
            if self.destroy_created():
                self.restart_cim()

    def _check_redundancy(self, extent, setting,
            data_redundancy=None,
            stripe_legtht=None,
            package_redundancy=None,
            parity_layout=None,
            check_parity_layout=False,
            nspof=None
            ):
        """
            Check if redundancy setting of StorageExtent and StorageSetting
            match and have requested values. Assert if not.
            If any value is None, it will not be checked, except parity_layout.
            If check_parity_layout is True, parity_layout will be checked
            against setting['ParityLayout'] even if it is None 
            Both extent and setting must be CIMInstance.
        """
        self.assertEqual(
                setting['DataRedundancyGoal'], extent['DataRedundancy'])
        self.assertEqual(
                setting['DataRedundancyMin'], extent['DataRedundancy'])
        self.assertEqual(
                setting['DataRedundancyMax'], extent['DataRedundancy'])
        self.assertEqual(
                setting['ExtentStripeLength'], extent['ExtentStripeLength'])
        self.assertEqual(
                setting['ExtentStripeLengthMin'], extent['ExtentStripeLength'])
        self.assertEqual(
                setting['ExtentStripeLengthMax'], extent['ExtentStripeLength'])
        self.assertEqual(
                setting['NoSinglePointOfFailure'],
                extent['NoSinglePointOfFailure'])
        self.assertEqual(
                setting['PackageRedundancyGoal'], extent['PackageRedundancy'])
        self.assertEqual(
                setting['PackageRedundancyMin'], extent['PackageRedundancy'])
        self.assertEqual(
                setting['PackageRedundancyMax'], extent['PackageRedundancy'])

        if data_redundancy:
            self.assertEqual(extent['DataRedundancy'], data_redundancy)
        if stripe_legtht:
            self.assertEqual(extent['ExtentStripeLength'], stripe_legtht)
        if package_redundancy:
            self.assertEqual(extent['PackageRedundancy'], package_redundancy)
        if check_parity_layout or parity_layout:
            self.assertEqual(setting['ParityLayout'], parity_layout)
        if nspof is not None:
            self.assertEqual(setting['NoSinglePointOfFailure'], nspof)

    def finish_job(self, jobname, return_constructor=int,
            affected_output_name=None):
        """
        Wait until the job finishes and return (ret, outparams) as if
        InvokeMethod without a job was returned.
        
        It's hard to reconstruct these outparams, since the embedded instances/
        ojects do not work in our CIMOMS, therefore special care is needed.
        
        When affected_output_name is specified, this methods finds the first
        element associated to the job using LMI_AffestedStorageJobElement and
        puts it into oputparams as affected_output_name entry.
        
        :param jobname: (``CIMInstanceName``) Name of the job.
        :param return_constructor: (function) Function, which converts
            string to the right type, for example int.
        :param affected_output_name: (``string``) If the output parameter of
            the method can discovered using LMI_<name>AffectedMethodElement
            association, this is the name of output parameter, which corresponds
            to this affected element.
        """
        # Use busy loop for now
        # TODO: rework to something sane
        while True:
            job = self.wbemconnection.GetInstance(jobname)
            if job['JobState'] > 5:  # all states higher than 5 are final
                break
            time.sleep(0.1)

        # get the MethodResult
        resultname = self.wbemconnection.AssociatorNames(jobname,
                AssocClass="LMI_AssociatedStorageJobMethodResult")[0]
        result = self.wbemconnection.GetInstance(resultname)
        ind = result['PostCallIndication']
        # check for error
        if ind['Error'] is not None:
            err = ind['Error'][0]
            code = err['CIMStatusCode']
            msg = err['Message']
            raise pywbem.CIMError(code, msg)

        ret = return_constructor(ind['ReturnValue'])

        # convert output parameters to format returned by InvokeMethod
        outparams = pywbem.NocaseDict()
        try:
            params = ind['MethodParameters']
        except KeyError:
            params = {}
        if params:
            for (key, value) in params.iteritems():
                outparams[key] = value

        return (ret, outparams)

    def _compare_cim_name(self, first, second):
        """
        Compare two CIMInstanceNames. Their hostname is not checked.
        """
        first_host = first.host
        first.host = None
        second_host = second.host
        second.host = None

        equals = first == second
        first.host = first_host
        second.host = second_host
        return equals

    def assertCIMNameEquals(self, first, second):
        """
        Compare two CIMInstanceNames. Their hostname is not checked.
        """
        self.assertTrue(self._compare_cim_name(first, second))

    def assertCIMNameIn(self, name, candidates):
        """
        Checks that given CIMInstanceName is in given set. It compares all
        properties except hostname.
        """
        for candidate in candidates:
            if self._compare_cim_name(name, candidate):
                return
        self.assertTrue(False, "name is not in candidates")

    def assertNocaseDictEqual(self, a, b, msg=None):
        a1 = {}
        for (key, value) in a.iteritems():
            a1[key.lower()] = value

        b1 = {}
        for (key, value) in b.iteritems():
            b1[key.lower()] = value

        self.assertDictEqual(a1, b1, msg)

    def invoke_async_method(self,
            method_name,
            object_name,
            return_constructor=int,
            affected_output_name=None,
            *args, **kwargs):
        """
        Invoke a method and if it returns a job, wait for the job.
        Return (retvalue, outparams) in the same way as finish_method() would.

        :param method_name: (``string``) Name of the method.
        :param object_name: (``CIMInstanceName``) Instance, on which the method
            should be invoked.
        :param return_constructor: (function) Function, which converts
            string to the right type, for example int.
        :param affected_output_name: (``string``) If the output parameter of
            the method can discovered using LMI_<name>AffectedMethodElement
            association, this is the name of output parameter, which corresponds
            to this affected element.
        """
        (ret, outparams) = self.wbemconnection.InvokeMethod(
                method_name,
                object_name,
                *args,
                **kwargs)
        if ret == self.JOB_CREATED:
            # wait for the job
            jobname = outparams['Job']
            (ret, outparams) = self.finish_job(jobname,
                    return_constructor,
                    affected_output_name)
        return (ret, outparams)


    def _create_mdraid(self, devicenames, level):
        """
        Create MD RAID device from given devices.

        :param devicenames: (``array of CIMInstanceNames``) RAID member devices.
        :param level: (int) RAID level

        :returns: ``CIMInstanceName`` of the RAID.
        """
        storage_service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_StorageConfigurationService")[0]
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyMDRAID",
                storage_service,
                int, "theelement",
                InExtents=devicenames,
                Level=pywbem.Uint16(level))
        self.assertEqual(ret, 0)
        return outparams['theelement']


    def _delete_mdraid(self, raidname):
        """
        Delete MD RAID.

        :param raidname: (``CIMInstanceName``) RAID to delete.
        """
        storage_service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_StorageConfigurationService")[0]
        (ret, _outparams) = self.invoke_async_method(
                "DeleteMDRAID",
                storage_service,
                int,
                TheElement=raidname)
        self.assertEquals(ret, 0)


def short_tests_only():
    """
        Returns True, if only short test should be executed, i.e.
        LMI_STORAGE_SHORT_ONLY is set.
    """
    if os.environ.get("LMI_STORAGE_SHORT_ONLY", None):
        return True
    return False

def blivet_version(major, minor, patch):
    """
        Returns True, if installed blivet version is at least the given one.
    """
    ver = blivet.__version__.split('.')
    if len(ver) > 3:
        ver = ver[:3]
    ver = map(int, ver)
    while len(ver) < 3:
        ver.append(0)
    
    return list(ver) >= list((major, minor, patch))
