#!/usr/bin/python
# -*- Coding:utf-8 -*-
#
# Copyright (C) 2013 Red Hat, Inc.  All rights reserved.
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
# Authors: Jan Synacek <jsynacek@redhat.com>


from test_base import StorageTestBase
import unittest
import pywbem
import subprocess
import time
import re

MEGABYTE = 1024 * 1024

class TestMounting(StorageTestBase):
    @classmethod
    def setUpClass(cls):
        super(TestMounting, cls).setUpClass()
        cls.mnt_partitions = {}
        i = 0
        for fstype in ["ext2", "ext3", "ext4", "btrfs", "xfs"]:
            cls.mnt_partitions[fstype] = cls.partitions[i]
            if fstype in ["btrfs", "xfs"]:
                subprocess.check_call(["mkfs." + fstype, "-f", cls.partitions[i]])
            else:
                subprocess.check_call(["mkfs." + fstype, cls.partitions[i]])
            i += 1
        TestMounting._restart_cim()

    @classmethod
    def tearDownClass(cls):
        for partition in cls.mnt_partitions.itervalues():
            subprocess.check_call(["wipefs", "-a", partition])
        # other tests might run afterwards, so restart cimom to reset blivet
        TestMounting._restart_cim()

    @classmethod
    def _restart_cim(cls):
        subprocess.check_call(["systemctl", "restart", cls.cimom])
        time.sleep(1)

    def setUp(self):
        super(TestMounting, self).setUp()
        self.service = self.wbemconnection.EnumerateInstanceNames("LMI_MountConfigurationService")[0]
        self.capability = self.wbemconnection.EnumerateInstanceNames("LMI_MountedFileSystemCapabilities")[0]

    def tearDown(self):
        super(TestMounting, self).tearDown()

    def _create_setting(self):
        (ret, outparams) = self.wbemconnection.InvokeMethod('CreateSetting', self.capability)
        self.assertEqual(ret, 0)
        return outparams['setting']

    def _mount(self, mnt_point, partition, fstype, setting_name=None):
        assoc_elems = self.wbemconnection.ExecQuery("WQL",
                                                    'select * from LMI_FileSystemSetting where \
                                                    InstanceID="LMI:LMI_FileSystemSetting:%s"' % (partition))
        if not assoc_elems:
            self.fail("No associations with '%s'" % (partition))

        fs_name = self.wbemconnection.AssociatorNames(assoc_elems[0].path)[0]

        kwargs = {"FileSystemType":fstype,
                  "Mode"          :pywbem.Uint16(32768),
                  "FileSystem"    :fs_name,
                  "MountPoint"    :mnt_point,
                  "FileSystemSpec":partition}
        if setting_name is not None:
            kwargs["Goal"] = setting_name

        (ret, outparams) = self.invoke_async_method(
            "CreateMount",
            self.service,
            int,
            **kwargs)

        # 0 - Completed with no error
        # 4096 - Method parameters checked, job started
        self.assertIn(ret, (0, 4096))
        # XXX outparams is always {} here, even though mounting was successful. BUG?

    def _modify_mount(self, something):
        # TBI
        pass

    def _umount(self, mnt_point, partition, fstype='ext4'):
        mnt_name = pywbem.CIMInstanceName(classname='LMI_MountedFileSystem',
                                          namespace='root/cimv2',
                                          keybindings={'MountPointPath':mnt_point,
                                                       'FileSystemType':fstype,
                                                       'FileSystemSpec':partition})

        (ret, outparams) = self.invoke_async_method("DeleteMount",
                                                    self.service,
                                                    int,
                                                    Mount=mnt_name,
                                                    Mode=pywbem.Uint16(32769)
                                                    )

        self.assertEqual(ret, 0)
        self.assertEqual(outparams, {})

    def _grep_mount(self, partition):
        p1 = subprocess.Popen(["mount"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", partition], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        return p2.communicate()[0]

    def _check_partition_is_mounted(self, partition):
        out = self._grep_mount(partition)
        self.assertRegexpMatches(out, partition + " on " + self.mnt_dir)

    def _check_partition_is_unmounted(self, partition):
        out = self._grep_mount(partition)
        self.assertEquals(out, "")

    def _create_id(self, spec, path):
        return spec + '|' + path

    def test_simple_mount_and_umount(self):
        for fstype, partition in self.mnt_partitions.iteritems():
            # mount
            try:
                self._mount(self.mnt_dir, partition, fstype)
            except pywbem.CIMError as pe:
                self.fail(pe[1])
            out = self._grep_mount(partition)
            self._check_partition_is_mounted(partition)

            # check the default setting
            sid = partition + "|" + self.mnt_dir
            assoc_elems = self.wbemconnection.ExecQuery("WQL",
                                                        'select * from LMI_MountedFileSystemSetting where \
                                                        InstanceID="LMI:LMI_MountedFileSystemSetting:%s"' % (sid))
            if not assoc_elems:
                self.fail("No associations with '%s'" % (partition))
            self.assertTrue(assoc_elems[0]['AllowWrite'])
            self.assertTrue(assoc_elems[0]['UpdateRelativeAccessTimes'])
            # we do not check OtherOptions because we don't know what the options are

            # unmount
            try:
                self._umount(self.mnt_dir, partition, fstype)
            except pywbem.CIMError as pe:
                self.fail(pe[1])
            out = self._grep_mount(partition)
            self._check_partition_is_unmounted(partition)

    def test_mount_and_umount_wrong_dir(self):
        for fstype, partition in self.mnt_partitions.iteritems():
            self.assertRaises(pywbem.CIMError,
                              self._mount,
                              '/no/such/dir',
                              partition,
                              fstype
                              )
            self.assertRaises(pywbem.CIMError,
                              self._umount,
                              '/no/such/dir',
                              partition,
                              fstype
                              )

    def test_mount_and_umount_wrong_partition(self):
        self.assertRaisesRegexp(AssertionError,
                                '^No associations with .*$',
                                self._mount,
                                self.mnt_dir,
                                '/no/such/partition',
                                'not_important'
                                 )

        self.assertRaises(pywbem.CIMError,
                          self._umount,
                          self.mnt_dir,
                          '/no/such/partition',
                          'not_important'
                          )

    def test_mount_and_umount_wrong_fstype(self):
        self.assertRaises(pywbem.CIMError,
                          self._mount,
                          self.mnt_dir,
                          self.mnt_partitions['ext4'],
                          'no-such-fs'
                          )

        self.assertRaises(pywbem.CIMError,
                          self._umount,
                          self.mnt_dir,
                          self.mnt_partitions['btrfs'],
                          'no-such-fs'
                          )

    def test_mount_own_simple_setting_ext4(self):
        setting_name = self._create_setting()
        setting = self.wbemconnection.GetInstance(setting_name)
        setting['AllowWrite'] = False
        setting['InterpretDevices'] = False
        otheropts = ['max_batch_time=30', 'nobarrier', 'journal_async_commit']
        setting['OtherOptions'] = otheropts
        self.wbemconnection.ModifyInstance(setting)

        fstype = 'ext4'
        partition = self.mnt_partitions[fstype]
        # mount
        try:
            self._mount(self.mnt_dir, partition, fstype, setting.path)
        except pywbem.CIMError as pe:
            self.fail(pe[1])
        out = self._grep_mount(partition)
        self._check_partition_is_mounted(partition)

        # check if settings are correctly set
        out = self._grep_mount(partition)
        # parse mount options in grep output (options are in parens):
        # /dev/vda7 on /mnt type ext4 (ro,nodev,...)
        opts = re.findall("\((.+),?\)", out)[0].split(',')

        # check if all expected options are in place
        self.assertIn('ro', opts)
        self.assertIn('nodev', opts)
        map(lambda o: self.assertIn(o, opts), otheropts)

        # unmount
        try:
            self._umount(self.mnt_dir, partition, fstype)
        except pywbem.CIMError as pe:
            self.fail(pe[1])
        out = self._grep_mount(partition)
        self._check_partition_is_unmounted(partition)

    def _test_device_mount(self, devicename):
        # format it
        EXT3 = 12  # LMI_FileSystemSetting.ActualFileSystemType
        fs_service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_FileSystemConfigurationService")[0]
        (ret, outparams) = self.invoke_async_method(
                "LMI_CreateFileSystem",
                fs_service,
                int, "theelement",
                InExtents=[devicename],
                FileSystemType=pywbem.Uint16(EXT3))
        self.assertEqual(ret, 0)
        fsname = outparams['theelement']
        fs = self.wbemconnection.GetInstance(fsname)

        self._mount(self.mnt_dir, fs['ElementName'], "ext3")

        # check it is really mounted
        mounted_fss = self.wbemconnection.AssociatorNames(fsname, ResultClass="LMI_MountedFileSystem")
        self.assertEqual(len(mounted_fss), 1)

        # unmount
        self._umount(self.mnt_dir, fs['ElementName'], "ext3")

    def test_raid_mount(self):
        """
        Test mounting of MD RAID.
        This tests rhbz#1057666.
        """
        # create MD RAID
        raidname = self._create_mdraid(self.partition_names[-2:], 0);
        try:
            self._test_device_mount(raidname)
        finally:
            try:
                if raidname:
                    self._delete_mdraid(raidname)
            except Exception, ex:
                # ignore any error, we want the original exception
                print "Error cleaning up RAID:", ex
                pass

    def test_lv_mount(self):
        """
        Test mounting of a logical volume.
        """
        lvname = None
        # create VG
        storage_service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_StorageConfigurationService")[0]
        (ret, outparams) = self.invoke_async_method(
                "CreateOrModifyVG",
                storage_service,
                int, "pool",
                InExtents=self.partition_names[-2:],
                ElementName="myVG")
        self.assertEqual(ret, 0)
        vgname = outparams['pool']

        try:
            # create LV
            (retval, outparams) = self.invoke_async_method(
                    "CreateOrModifyLV",
                    storage_service,
                    int, "TheElement",
                    InPool=vgname,
                    Size=pywbem.Uint64(20 * MEGABYTE))
            self.assertEqual(retval, 0)
            lvname = outparams['TheElement']

            self._test_device_mount(lvname)
        finally:
            try:
                if lvname:
                    self.invoke_async_method("DeleteLV", storage_service,
                            int, None, TheElement=lvname)
                if vgname:
                    self.invoke_async_method("DeleteVG", storage_service, int,
                            None, Pool=vgname)
            except Exception, ex:
                # ignore any error, we want the original exception
                print "Error cleaning up LVM:", ex

    def test_luks_mount(self):
        """
        Test mounting of a luks volume.
        """
        passphrase = "23rnv0as0df23n"
        luks_service = self.wbemconnection.EnumerateInstanceNames(
                "LMI_ExtentEncryptionConfigurationService")[0]

        (ret, outparams) = self.invoke_async_method("CreateEncryptionFormat",
                luks_service,
                int,
                InExtent=self.partition_names[-1],
                Passphrase=passphrase)
        self.assertEquals(ret, 0)
        luksfmt = outparams['Format']

        (ret, outparams) = self.invoke_async_method(
                "OpenEncryptionFormat",
                luks_service,
                int,
                ElementName='opened',
                Passphrase=passphrase,
                Format=luksfmt)
        luksname = outparams['Extent']

        self.assertEquals(ret, 0)
        try:
            self._test_device_mount(luksname)
        finally:
            try:
                (ret, outparams) = self.invoke_async_method(
                    "CloseEncryptionFormat",
                    luks_service,
                    int,
                    Format=luksfmt)
            except Exception, ex:
                # ignore any error, we want the original exception
                print "Error cleaning up LUKS:", ex


    # TODO more settings coverage for various filesystem types
    # more advanced settings tests

if __name__ == '__main__':
    unittest.main()
