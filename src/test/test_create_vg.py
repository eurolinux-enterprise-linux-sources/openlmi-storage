#!/usr/bin/python
# -*- Coding:utf-8 -*-
#
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

from test_base import StorageTestBase, short_tests_only
import unittest
import pywbem


MEGABYTE = 1024 * 1024

class TestCreateVG(StorageTestBase):
    """
        Test LMI_StorageConfigurationService.CreateOrModifyVG
        (create only).
    """

    VG_CLASS = "LMI_VGStoragePool"
    STYLE_EMBR = 4100
    STYLE_MBR = 2
    STYLE_GPT = 3
    PARTITION_CLASS = "LMI_GenericDiskPartition"


    def setUp(self):
        """ Find storage service. """
        super(TestCreateVG, self).setUp()
        self.service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_StorageConfigurationService")[0]
        self.part_service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_DiskPartitionConfigurationService")[0]
        self.capabilities = self.wbemconnection.EnumerateInstanceNames(
                "LMI_VGStorageCapabilities")[0]

    def _get_disk_size(self, devicename):
        """ Return size of given device, in bytes."""
        disk = self.wbemconnection.GetInstance(devicename)
        return disk['NumberOfBlocks'] * disk['BlockSize']

    def test_create_1pv(self):
        """ Test CreateOrModifyVG with one PV."""
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                InExtents=self.partition_names[:1],
                ElementName='tstName')
        if len(outparams) == 1:
            # there is no Size returned, Pegasus does not support it yet
            # TODO: remove when pegasus supports embedded objects of unknown
            # types, rhbz#920763
            if outparams.has_key('pool'):
                vg = self.wbemconnection.GetInstance(outparams['pool'])
                outparams['size'] = vg['TotalExtents'] * vg['ExtentSize']

        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[0]),
                delta=4 * MEGABYTE)
        vgname = outparams['pool']
        vg = self.wbemconnection.GetInstance(vgname)
        self.assertEqual(vg['TotalManagedSpace'], outparams['size'])
        self.assertEqual(vg['PoolID'], 'tstName')
        self.assertEqual(vg['ElementName'], 'tstName')
        self.assertNotEqual(vg['UUID'], '')
        self.assertNotEqual(vg['UUID'], None)
        self.assertEqual(vg['ExtentSize'], 4 * MEGABYTE)
        self.assertEqual(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])
        self.assertEqual(
                vg['ExtentSize'] * vg['RemainingExtents'],
                vg['RemainingManagedSpace'])

        # check LVStorageCapabilities
        caps = self.wbemconnection.Associators(vgname, ResultClass="LMI_LVStorageCapabilities")
        self.assertEqual(len(caps), 1)
        cap = caps[0]
        self.assertEqual(cap['DataRedundancyDefault'], 1)
        self.assertEqual(cap['DataRedundancyMin'], 1)
        self.assertEqual(cap['DataRedundancyMax'], 1)
        self.assertEqual(cap['PackageRedundancyDefault'], 0)
        self.assertEqual(cap['PackageRedundancyMin'], 0)
        self.assertEqual(cap['PackageRedundancyMax'], 0)
        self.assertIsNone(cap['ParityLayoutDefault'])
        self.assertEqual(cap['ExtentStripeLengthDefault'], 1)

        (ret, outparams) = self.invoke_async_method(
                'DeleteVG',
                self.service,
                int, None,
                Pool=vgname)
        self.assertEquals(ret, 0)

    @unittest.skipIf(short_tests_only(), "Running short tests only.")
    def test_create_10pv(self):
        """ Test CreateOrModifyVG with 10 PVs."""
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                InExtents=self.partition_names[:10])

        vg = self.wbemconnection.GetInstance(outparams['pool'])

        if len(outparams) == 1:
            # there is no Size returned, Pegasus does not support it yet
            # TODO: remove when pegasus supports embedded objects of unknown
            # types, rhbz#920763
            outparams['size'] = vg['TotalExtents'] * vg['ExtentSize']

        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        sizes = map(lambda p: self._get_disk_size(p), self.partition_names[:10])
        pv_unusable = sum(map(lambda s: s % vg['ExtentSize'], sizes))
        self.assertEqual(
                outparams['size'],
                sum(sizes) - pv_unusable)
        vg = outparams['pool']

        (ret, outparams) = self.invoke_async_method(
                'DeleteVG',
                self.service,
                int, None,
                Pool=vg)
        self.assertEquals(ret, 0)

    @unittest.skipIf(short_tests_only(), "Running short tests only.")
    def test_create_10vg(self):
        """ Test CreateOrModifyVG with 10 VGs."""
        vgs = []
        for part in self.partition_names[:10]:
            (ret, outparams) = self.invoke_async_method(
                    "CreateOrModifyVG",
                    self.service,
                    int, "pool",
                    InExtents=[part])
            if len(outparams) == 1:
                # there is no Size returned, Pegasus does not support it yet
                # TODO: remove when pegasus supports embedded objects of unknown
                # types, rhbz#920763
                if outparams.has_key('pool'):
                    vg = self.wbemconnection.GetInstance(outparams['pool'])
                    outparams['size'] = vg['TotalExtents'] * vg['ExtentSize']
            self.assertEqual(ret, 0)
            self.assertEqual(len(outparams), 2)
            vg = outparams['pool']
            vgs.append(vg)

        for vg in vgs:
            (ret, outparams) = self.invoke_async_method(
                    'DeleteVG',
                    self.service,
                    int, None,
                    Pool=vg)
            self.assertEquals(ret, 0)

    def _create_disposable_vg(self, element_name):
        (ret, outparams) = self.invoke_async_method(
            'CreateOrModifyVG',
            self.service,
            int, 'pool',
            InExtents=[self.partition_names[-1]],
            ElementName=element_name)
        self.assertEquals(ret, 0)
        return (ret, outparams)

    def _delete_vg(self, vgname):
        (ret, outparams) = self.invoke_async_method(
                'DeleteVG',
                self.service,
                int, None,
                Pool=vgname)
        self.assertEquals(ret, 0)
        return (ret, outparams)

    def _delete_lv(self, lvname):
        (ret, outparams) = self.invoke_async_method(
                'DeleteLV',
                self.service,
                int, None,
                TheElement=lvname)
        self.assertEquals(ret, 0)
        return (ret, outparams)

    def test_create_thin_pool(self):
        """
        Test CreateOrModifyThinPool.
        """
        (ret, outparams) = self._create_disposable_vg('tstThinPoolVG')
        vg = outparams['pool']

        # create
        (ret, outparams) = self.invoke_async_method(
            'CreateOrModifyThinPool',
            self.service,
            int, 'pool',
            InPool=vg,
            ElementName='tstThinPool',
            Size=pywbem.Uint64(32 * MEGABYTE))
        self.assertEquals(ret, 0)
        tp = outparams['pool']

        self._delete_vg(tp)
        self._delete_vg(vg)

    def test_create_thin_lv(self):
        """
        Test CreateOrModifyThinLV.
        """
        (ret, outparams) = self._create_disposable_vg('tstThinPoolVG')
        vg = outparams['pool']

        # create thinpool
        (ret, outparams) = self.invoke_async_method(
            'CreateOrModifyThinPool',
            self.service,
            int, 'pool',
            InPool=vg,
            ElementName='tstThinPool',
            Size=pywbem.Uint64(32 * MEGABYTE))
        self.assertEquals(ret, 0)
        tp = outparams['pool']

        (ret, outparams) = self.invoke_async_method(
            'CreateOrModifyThinLV',
            self.service,
            int, 'theelement',
            ThinPool=tp,
            ElementName='tstThinLV',
            Size=pywbem.Uint64(MEGABYTE * MEGABYTE)) # way overcommited
        self.assertEquals(ret, 0)
        tlv = outparams['theelement']

        self._delete_lv(tlv)
        self._delete_vg(tp)
        self._delete_vg(vg)

    def _invoke_create_or_modify_sp(self, **kwargs):
        """
        Wrapper around invoke_async_method, that calls CreateOrModifyStoragePool
        with arguments passed in `kwargs'.

        By default, if pywbem.CIMError is caught, the test fails. If `kwargs'
        contains a special argument 'Fail' set to True, the test does not fail
        and any exception risen by CreateOrModifyStoragePool is re-thrown.
        """
        fail = kwargs.pop('Fail', True)
        try:
            (ret, outparams) = self.invoke_async_method(
                'CreateOrModifyStoragePool',
                self.service,
                int, 'pool',
                **kwargs)
        except pywbem.CIMError as pe:
            if fail:
                self.fail(pe[1])
            else:
                raise pe
        return (ret, outparams)

    def test_thin_pool_using_create_or_modify_storage_pool(self):
        str_inextents = map(str, self.partition_names[:2])
        (ret, outparams) = self._invoke_create_or_modify_sp(
            ElementName='tstName',
            InExtents=str_inextents)

        vg = outparams['pool']
        str_inpools = map(str, [vg])

        goal = self._create_setting()
        # ThinlyProvisionedLimitlessStoragePool = 9
        goal['ThinProvisionedPoolType'] = pywbem.Uint16(9)
        self.wbemconnection.ModifyInstance(goal)

        (ret, outparams) = self._invoke_create_or_modify_sp(
            ElementName='tstThinPool',
            Goal=goal.path,
            InPools=str_inpools,
            Size=pywbem.Uint64(32 * MEGABYTE))
        self.assertEquals(ret, 0)
        tp = outparams['pool']

        # try to rename the thin pool
        self.assertRaisesRegexp(pywbem.CIMError,
                                "Rename of thin pool is not yet supported",
                                self._invoke_create_or_modify_sp,
                                Fail=False,
                                ElementName='tstThinPool-rename',
                                Goal=goal.path,
                                Pool=tp)

        # try to resize the thin pool
        self.assertRaisesRegexp(pywbem.CIMError,
                                "device is not resizable",
                                self._invoke_create_or_modify_sp,
                                Fail=False,
                                Goal=goal.path,
                                Pool=tp,
                                Size=pywbem.Uint64(64 * MEGABYTE))

        self._delete_vg(tp)
        self._delete_vg(vg)

    def test_create_vg_using_create_or_modify_storage_pool(self):
        """
        Create a VG from 2 PV using the standard SMI-S method.

        CreateOrModifyStoragePool uses an array of strings for the InExtents
        parameter.
        """
        str_inextents = map(str, self.partition_names[:2])

        try:
            (ret, outparams) = self.invoke_async_method(
                'CreateOrModifyStoragePool',
                self.service,
                int, 'pool',
                InExtents=str_inextents,
                ElementName='tstName')
        except pywbem.CIMError as pe:
            self.fail(pe[1])

        vg = self.wbemconnection.GetInstance(outparams['pool'])

        if len(outparams) == 1:
            # there is no Size returned, Pegasus does not support it yet
            # TODO: remove when pegasus supports embedded objects of unknown
            # types, rhbz#920763
            outparams['size'] = vg['TotalExtents'] * vg['ExtentSize']

        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)

        vg = outparams['pool']
        (ret, outparams) = self.invoke_async_method(
            'DeleteVG',
            self.service,
            int, None,
            Pool=vg)
        self.assertEquals(ret, 0)

    def test_create_unknown_setting(self):
        """ Test CreateOrModifyVG with non-existing setting."""
        goal = pywbem.CIMInstanceName(
                classname=" LMI_VGStorageSetting",
                keybindings={
                        'InstanceID' : 'LMI:LMI_VGStorageSetting:not-existing'
                })
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                    "CreateOrModifyVG",
                    self.service,
                    InExtents=self.partition_names[:1],
                    Goal=goal
                    )

    def test_create_wrong_setting_class(self):
        """ Test CreateOrModifyVG with non-existing setting."""
        goal = pywbem.CIMInstanceName(
                classname=" LMI_LVStorageSetting",
                keybindings={
                        'InstanceID' : 'LMI:LMI_LVStorageSetting:not-existing'
                })
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                    "CreateOrModifyVG",
                    self.service,
                    InExtents=self.partition_names[:1],
                    Goal=goal
                    )

    def _create_setting(self):
        """ Create a VGStorageSetting and return CIMInstance of it."""
        (retval, outparams) = self.wbemconnection.InvokeMethod(
                "CreateSetting",
                self.capabilities)
        self.assertEqual(retval, 0)
        self.assertEqual(len(outparams), 1)

        setting_name = outparams['newsetting']
        setting = self.wbemconnection.GetInstance(setting_name)
        return setting

    def _delete_setting(self, setting_name):
        """ Delete given setting. """
        self.wbemconnection.DeleteInstance(setting_name)

    def test_create_default_setting(self):
        """
            Test CreateOrModifyVG with default setting from 
            VGStroageCapabilities.CreateSetting.
        """
        goal = self._create_setting()

        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                InExtents=self.partition_names[:1],
                Goal=goal.path)
        if len(outparams) == 1:
            # there is no Size returned, Pegasus does not support it yet
            # TODO: remove when pegasus supports embedded objects of unknown
            # types, rhbz#920763
            if outparams.has_key('pool'):
                vg = self.wbemconnection.GetInstance(outparams['pool'])
                outparams['size'] = vg['TotalExtents'] * vg['ExtentSize']

        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[0]),
                delta=4 * MEGABYTE)
        vgname = outparams['pool']
        vg = self.wbemconnection.GetInstance(vgname)
        self.assertEqual(vg['TotalManagedSpace'], outparams['size'])
        self.assertNotEqual(vg['ElementName'], '')
        self.assertNotEqual(vg['ElementName'], None)
        self.assertNotEqual(vg['UUID'], '')
        self.assertNotEqual(vg['UUID'], None)
        self.assertEqual(vg['ExtentSize'], 4 * MEGABYTE)
        self.assertEqual(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])
        self.assertEqual(
                vg['ExtentSize'] * vg['RemainingExtents'],
                vg['RemainingManagedSpace'])

        # check it has a setting associated
        settings = self.wbemconnection.Associators(
                vgname,
                AssocClass="LMI_VGElementSettingData")
        self.assertEqual(len(settings), 1)
        setting = settings[0]
        self.assertEqual(setting['ExtentSize'], goal['ExtentSize'])
        self.assertEqual(setting['DataRedundancyGoal'], goal['DataRedundancyGoal'])
        self.assertLessEqual(setting['DataRedundancyMax'], goal['DataRedundancyMax'])
        self.assertGreaterEqual(setting['DataRedundancyMin'], goal['DataRedundancyMin'])
        self.assertEqual(setting['ExtentStripeLength'], goal['ExtentStripeLength'])
        self.assertLessEqual(setting['ExtentStripeLengthMax'], goal['ExtentStripeLengthMax'])
        self.assertGreaterEqual(setting['ExtentStripeLengthMin'], goal['ExtentStripeLengthMin'])
        self.assertEqual(setting['NoSinglePointOfFailure'], goal['NoSinglePointOfFailure'])
        self.assertEqual(setting['PackageRedundancyGoal'], goal['PackageRedundancyGoal'])
        self.assertLessEqual(setting['PackageRedundancyMax'], goal['PackageRedundancyMax'])
        self.assertGreaterEqual(setting['PackageRedundancyMin'], goal['PackageRedundancyMin'])

        # check LVStorageCapabilities
        caps = self.wbemconnection.Associators(vgname, ResultClass="LMI_LVStorageCapabilities")
        self.assertEqual(len(caps), 1)
        cap = caps[0]
        self.assertEqual(cap['DataRedundancyDefault'], setting['DataRedundancyGoal'])
        self.assertEqual(cap['DataRedundancyMin'], setting['DataRedundancyMin'])
        self.assertEqual(cap['DataRedundancyMax'], setting['DataRedundancyMax'])
        self.assertEqual(cap['PackageRedundancyDefault'], setting['PackageRedundancyGoal'])
        self.assertEqual(cap['PackageRedundancyMin'], setting['PackageRedundancyMin'])
        self.assertEqual(cap['PackageRedundancyMax'], setting['PackageRedundancyMax'])
        self.assertEqual(cap['ParityLayoutDefault'], setting['ParityLayout'])
        self.assertEqual(cap['ExtentStripeLengthDefault'], goal['ExtentStripeLength'])

        (ret, outparams) = self.invoke_async_method(
                'DeleteVG',
                self.service,
                int, None,
                Pool=vgname)
        self.assertEquals(ret, 0)
        self._delete_setting(goal.path)

    def test_create_setting_1m(self):
        """
            Test CreateOrModifyVG with 2MiB ExtentSize.
        """
        goal = self._create_setting()
        goal['ExtentSize'] = pywbem.Uint64(MEGABYTE)
        self.wbemconnection.ModifyInstance(goal)

        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                InExtents=self.partition_names[:1],
                Goal=goal.path)
        if len(outparams) == 1:
            # there is no Size returned, Pegasus does not support it yet
            # TODO: remove when pegasus supports embedded objects of unknown
            # types, rhbz#920763
            if outparams.has_key('pool'):
                vg = self.wbemconnection.GetInstance(outparams['pool'])
                outparams['size'] = vg['TotalExtents'] * vg['ExtentSize']

        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[0]),
                delta=4 * MEGABYTE)
        vgname = outparams['pool']
        vg = self.wbemconnection.GetInstance(vgname)
        self.assertEqual(vg['TotalManagedSpace'], outparams['size'])
        self.assertNotEqual(vg['ElementName'], '')
        self.assertNotEqual(vg['ElementName'], None)
        self.assertNotEqual(vg['UUID'], '')
        self.assertNotEqual(vg['UUID'], None)
        self.assertEqual(vg['ExtentSize'], MEGABYTE)
        self.assertEqual(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])
        self.assertEqual(
                vg['ExtentSize'] * vg['RemainingExtents'],
                vg['RemainingManagedSpace'])

        # check it has a setting associated
        settings = self.wbemconnection.Associators(
                vgname,
                AssocClass="LMI_VGElementSettingData")
        self.assertEqual(len(settings), 1)
        setting = settings[0]
        self.assertEqual(setting['ExtentSize'], goal['ExtentSize'])
        self.assertEqual(setting['DataRedundancyGoal'], goal['DataRedundancyGoal'])
        self.assertLessEqual(setting['DataRedundancyMax'], goal['DataRedundancyMax'])
        self.assertGreaterEqual(setting['DataRedundancyMin'], goal['DataRedundancyMin'])
        self.assertEqual(setting['ExtentStripeLength'], goal['ExtentStripeLength'])
        self.assertLessEqual(setting['ExtentStripeLengthMax'], goal['ExtentStripeLengthMax'])
        self.assertGreaterEqual(setting['ExtentStripeLengthMin'], goal['ExtentStripeLengthMin'])
        self.assertEqual(setting['NoSinglePointOfFailure'], goal['NoSinglePointOfFailure'])
        self.assertEqual(setting['PackageRedundancyGoal'], goal['PackageRedundancyGoal'])
        self.assertLessEqual(setting['PackageRedundancyMax'], goal['PackageRedundancyMax'])
        self.assertGreaterEqual(setting['PackageRedundancyMin'], goal['PackageRedundancyMin'])

        (ret, outparams) = self.invoke_async_method(
                'DeleteVG',
                self.service,
                int, None,
                Pool=vgname)
        self.assertEquals(ret, 0)
        self._delete_setting(goal.path)

    def test_create_setting_64k(self):
        """
            Test CreateOrModifyVG with 64k ExtentSize.
        """
        goal = self._create_setting()
        goal['ExtentSize'] = pywbem.Uint64(64 * 1024)
        self.assertRaises(pywbem.CIMError, self.wbemconnection.ModifyInstance,
                goal)
        self._delete_setting(goal.path)

if __name__ == '__main__':
    unittest.main()
