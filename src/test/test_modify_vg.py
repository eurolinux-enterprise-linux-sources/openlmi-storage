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

from test_base import StorageTestBase, blivet_version
import unittest
import pywbem


MEGABYTE = 1024 * 1024

@unittest.skipIf(not blivet_version(0, 52, 0), reason="Old blivet does not support VG modification.")
class TestModifyVG(StorageTestBase):
    """
        Test LMI_StorageConfigurationService.CreateOrModifyVG
        (modify only).
    """

    VG_CLASS = "LMI_VGStoragePool"
    STYLE_EMBR = 4100
    STYLE_MBR = 2
    STYLE_GPT = 3
    PARTITION_CLASS = "LMI_GenericDiskPartition"

    def setUp(self):
        """ Find storage service. """
        super(TestModifyVG, self).setUp()
        self.service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_StorageConfigurationService")[0]
        self.vgname = self._create_vg()

    def tearDown(self):
        self._destroy_vg(self.vgname)

    def _get_disk_size(self, devicename):
        """ Return size of given device, in bytes."""
        disk = self.wbemconnection.GetInstance(devicename)
        return disk['NumberOfBlocks'] * disk['BlockSize']

    def _create_vg(self, lvsize=0):
        """
        Create one VG with one PV and one LV on it with given size
        Use lvsize = None to disable lv creation.
        Use lvsize = 0 to use max. lv size
        """
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                InExtents=self.partition_names[:1],
                ElementName='tstName')
        self.assertEqual(ret, 0)
        self.assertEqual(len(outparams), 2)
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[0]),
                delta=4 * MEGABYTE)
        vgname = outparams['pool']
        vg = self.wbemconnection.GetInstance(vgname)

        if lvsize == 0:
            # Use almost all space, just with ~4MB delta in case the test
            # partitions have variable size. Subsequent tests will move the
            # LV to different PVs and we want to be sure it fits there.
            lvsize = vg['RemainingManagedSpace'] - vg['ExtentSize']
        if lvsize:
            # create LV with given size
            (retval, outparams) = self.invoke_async_method(
                "CreateOrModifyLV",
                self.service,
                int, "TheElement",
                InPool=vgname,
                Size=pywbem.Uint64(lvsize))
        return vgname

    def _destroy_vg(self, vgname):
        """ Destroy VG and all its LVs """
        lvs = self.wbemconnection.AssociatorNames(vgname,
                AssocClass="LMI_LVAllocatedFromStoragePool")

        for lv in lvs:
            self.invoke_async_method("DeleteLV", self.service, int, None,
                    TheElement=lv)

        (ret, outparams) = self.invoke_async_method(
                'DeleteVG',
                self.service,
                int, None,
                Pool=vgname)
        self.assertEquals(ret, 0)

    def test_extend_1pv(self):
        """ Extend a VG with one additional PV."""
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                Pool = self.vgname,
                InExtents=self.partition_names[:2])
        self.assertEquals(ret, 0)
        vg = self.wbemconnection.GetInstance(outparams['pool'])

        # check the output params
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[0]) + self._get_disk_size(self.partition_names[1]),
                delta=8 * MEGABYTE)

        # check the vg is larger
        self.assertEquals(vg['TotalManagedSpace'], outparams['size'])

        self.assertAlmostEqual(
                vg['RemainingManagedSpace'],
                self._get_disk_size(self.partition_names[1]),
                delta=4 * MEGABYTE)
        self.assertEquals(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])

    def test_extend_reduce_1pv(self):
        """ Extend a VG with one additional PV and then reduce it. pvmove is expected."""
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                Pool = self.vgname,
                InExtents=self.partition_names[:2])
        self.assertEquals(ret, 0)
        vg = self.wbemconnection.GetInstance(outparams['pool'])

        # check the output params
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[0]) + self._get_disk_size(self.partition_names[1]),
                delta=8 * MEGABYTE)

        # check the vg is larger
        self.assertEquals(vg['TotalManagedSpace'], outparams['size'])

        self.assertAlmostEqual(
                vg['RemainingManagedSpace'],
                self._get_disk_size(self.partition_names[1]),
                delta=4 * MEGABYTE)
        self.assertEquals(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])

        # reduce it by one PV
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                Pool = self.vgname,
                InExtents=self.partition_names[1:2])
        self.assertEquals(ret, 0)
        vg = self.wbemconnection.GetInstance(outparams['pool'])

        # check the output params
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[1]),
                delta=4 * MEGABYTE)

        # check the vg is smaller
        self.assertEquals(vg['TotalManagedSpace'], outparams['size'])

        self.assertAlmostEqual(
                vg['TotalManagedSpace'],
                self._get_disk_size(self.partition_names[1]),
                delta=4 * MEGABYTE)
        self.assertEquals(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])

    def test_move_1pv(self):
        """ Exchange all vg's PV in one call."""
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                Pool = self.vgname,
                InExtents=self.partition_names[1:2])
        self.assertEquals(ret, 0)
        vg = self.wbemconnection.GetInstance(outparams['pool'])

        # check the output params
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[1]),
                delta=4 * MEGABYTE)

        # check the vg is smaller
        self.assertEquals(vg['TotalManagedSpace'], outparams['size'])

        self.assertAlmostEqual(
                vg['TotalManagedSpace'],
                self._get_disk_size(self.partition_names[1]),
                delta=4 * MEGABYTE)
        self.assertEquals(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])

    def test_move_pool_1pv(self):
        """ Exchange all vg's PV in one call, using CreateOrModifyStoragePool."""
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyStoragePool",
                self.service,
                int, "pool",
                Pool = self.vgname,
                InExtents=self.partition_names[1:2])
        self.assertEquals(ret, 0)
        vg = self.wbemconnection.GetInstance(outparams['pool'])

        # check the output params
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[1]),
                delta=4 * MEGABYTE)

        # check the vg is smaller
        self.assertEquals(vg['TotalManagedSpace'], outparams['size'])

        self.assertAlmostEqual(
                vg['TotalManagedSpace'],
                self._get_disk_size(self.partition_names[1]),
                delta=4 * MEGABYTE)
        self.assertEquals(
                vg['ExtentSize'] * vg['TotalExtents'],
                vg['TotalManagedSpace'])

    def test_reduce_fail(self):
        """ Reduce a VG under its lv size -> error."""
        # extend the vg to 2 partitions
        (ret, outparams) = self.invoke_async_method(
            "CreateOrModifyVG",
            self.service,
            int, "pool",
            Pool = self.vgname,
            InExtents=self.partition_names[:2])
        self.assertEquals(ret, 0)
        vg = self.wbemconnection.GetInstance(outparams['pool'])

        # check the output params
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[0]) + self._get_disk_size(self.partition_names[1]),
                delta=8 * MEGABYTE)

        # create a new LV there
        (retval, outparams) = self.invoke_async_method(
            "CreateOrModifyLV",
            self.service,
            int, "TheElement",
            InPool=self.vgname,
            Size=pywbem.Uint64(vg['RemainingManagedSpace']))

        # try to reduce the vg
        self.assertRaises(pywbem.CIMError, self.invoke_async_method,
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                Pool = self.vgname,
                InExtents=self.partition_names[1:2])

    def test_move_2pv(self):
        """ Exchange all vg's PV in one call."""

        # extend the vg to 2 partitions
        (ret, outparams) = self.invoke_async_method(
            "CreateOrModifyVG",
            self.service,
            int, "pool",
            Pool = self.vgname,
            InExtents=self.partition_names[:2])
        self.assertEquals(ret, 0)
        vg = self.wbemconnection.GetInstance(outparams['pool'])

        # check the output params
        self.assertAlmostEqual(
                outparams['size'],
                self._get_disk_size(self.partition_names[0]) + self._get_disk_size(self.partition_names[1]),
                delta=8 * MEGABYTE)

        # create a new LV there
        (retval, outparams) = self.invoke_async_method(
            "CreateOrModifyLV",
            self.service,
            int, "TheElement",
            InPool=self.vgname,
            Size=pywbem.Uint64(vg['RemainingManagedSpace']))

        # sequentially move the VG to different VGs
        for i in xrange(len(self.partitions)/2 - 1):
            print "Moving to:", self.partitions[i*2+2:i*2+4]
            new_partitions = self.partition_names[i*2+2:i*2+4]
            (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                self.service,
                int, "pool",
                Pool = self.vgname,
                InExtents=new_partitions)
            self.assertEquals(ret, 0)

            # check the associations to PVs
            pvs = self.wbemconnection.AssociatorNames(self.vgname,
                    AssocClass='LMI_VGAssociatedComponentExtent')
            for pv in pvs:
                self.assertIn(pv, new_partitions)


if __name__ == '__main__':
    unittest.main()
