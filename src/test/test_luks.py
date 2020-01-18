#!/usr/bin/python
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
#          Jan Safranek <jsafrane@redhat.com>

from test_base import StorageTestBase, short_tests_only
import unittest
import pywbem
import subprocess
import sys
import traceback

class TestLUKS(StorageTestBase):
    @classmethod
    def setUpClass(cls):
        super(TestLUKS, cls).setUpClass()
        cls.luks_partition = cls.partition_names[-1]
        cls.luks_passphrase = '23rnv0as0df23n'
        cls.luks_newpassphrase = 'v939tnmnopxc09'
        cls.luks_elementname = 'luks-cim-test'

    def setUp(self):
        super(TestLUKS, self).setUp()
        self.service = self.wbemconnection.EnumerateInstanceNames("LMI_ExtentEncryptionConfigurationService")[0]

    def _create_luks(self, device, passphrase):
        """
        Create LUKS format on given device.
        
        :param device: CIMInstanceName
        :param passphrase: string
        :returns: LMI_EncryptionFormat
        """
        (ret, outparams) = self.invoke_async_method("CreateEncryptionFormat",
                self.service,
               int,
                InExtent=device,
                Passphrase=passphrase)
        self.assertEquals(ret, 0)
        return outparams['Format']

    def test_create_encryption_format(self):
        """
        Test to create, open, close and delete one LUKS.
        """
        fmt = self._create_luks(self.luks_partition, self.luks_passphrase)
        self.assertTrue(fmt)
        opened = False

        try:
            # check the returned format
            self.assertEquals(fmt['CSName'], self.SYSTEM_NAME)
            self.assertEquals(fmt['CSCreationClassName'], self.SYSTEM_CLASS_NAME)
            self.assertTrue(fmt['Name'].startswith("UUID="))
            self.assertEquals(fmt['CreationClassName'], "LMI_LUKSFormat")

            # check it's associated to the original device
            devices = self.wbemconnection.AssociatorNames(fmt, AssocClass="LMI_ResidesOnExtent")
            self.assertEquals(len(devices), 1)
            device = devices[0]
            self.assertCIMNameEquals(device, self.luks_partition)

            # open it using our password
            (ret, outparams) = self.invoke_async_method(
                    "OpenEncryptionFormat",
                    self.service,
                    int,
                    ElementName=self.luks_elementname,
                    Passphrase=self.luks_passphrase,
                    Format=fmt)
            self.assertEquals(ret, 0)
            opened = True
            extent_name = outparams['Extent']
            self.assertTrue(extent_name)
            extent = self.wbemconnection.GetInstance(extent_name)

            self.assertEquals(extent['ElementName'], self.luks_elementname)
            self.assertEquals(extent['SystemName'], self.SYSTEM_NAME)
            self.assertEquals(extent['SystemCreationClassName'], self.SYSTEM_CLASS_NAME)
            self.assertEquals(extent['CreationClassName'], "LMI_LUKSStorageExtent")

            # check the extent is associated properly
            basedons = self.wbemconnection.AssociatorNames(extent_name, AssocClass="LMI_LUKSBasedOn")
            self.assertEquals(len(basedons), 1)
            basedon = basedons[0]
            self.assertCIMNameEquals(basedon, device)

        except:
            # print the exception so it's not overwritten by any new exception
            # in 'finally' block
            print >> sys.stderr, "test_create_encryption_format failed:"
            print >> sys.stderr, traceback.format_exc()
            raise

        finally:
            # close the device
            if opened:
                (ret, outparams) = self.invoke_async_method(
                        "CloseEncryptionFormat",
                        self.service,
                        int,
                        Format=fmt)
                self.assertEquals(ret, 0)


    def test_add_and_delete_passphrase(self):
        """
        Test adding and removing passphrases.
        """
        USED = 1  # LMI_LUKSFormat.SlotStatus.used
        UNUSED = 0
        passphrases = [self.luks_newpassphrase + str(x) for x in range(7)]

        fmt = self._create_luks(self.luks_partition, self.luks_passphrase)
        self.assertTrue(fmt)

        # add 7 different passwords
        for i in xrange(7):
            f = self.wbemconnection.GetInstance(fmt)
            self.assertListEqual(f['SlotStatus'], [USED] * (i + 1) + [UNUSED] * (7 - i))
            (ret, outparams) = self.wbemconnection.InvokeMethod(
                "AddPassphrase",
                self.service,
                NewPassphrase=passphrases[i],
                Passphrase=self.luks_passphrase,
                Format=fmt)
            self.assertEquals(ret, 0)
        f = self.wbemconnection.GetInstance(fmt)
        self.assertListEqual(f['SlotStatus'], [USED] * 8)

        # add 9th password -> error
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "AddPassphrase",
                self.service,
                NewPassphrase=self.luks_newpassphrase * 2,
                Passphrase=self.luks_passphrase,
                Format=fmt)

        # remove the added passwords
        for i in xrange(7):
            f = self.wbemconnection.GetInstance(fmt)
            self.assertListEqual(f['SlotStatus'], [USED] + [UNUSED] * i + [USED] * (7 - i))
            (ret, outparams) = self.wbemconnection.InvokeMethod(
                "DeletePassphrase",
                self.service,
                Passphrase=passphrases[i],
                Format=fmt)
            self.assertEquals(ret, 0)

        f = self.wbemconnection.GetInstance(fmt)
        self.assertListEqual(f['SlotStatus'], [USED] + [UNUSED] * 7)

        # remove removed password -> error
        self.assertRaises(pywbem.CIMError, self.wbemconnection.InvokeMethod,
                "DeletePassphrase",
                self.service,
                Passphrase=passphrases[0],
                Format=fmt)


    def test_delete_wrong_passphrase(self):
        """
        Test removal of wrong passphrase.
        """
        fmt = self._create_luks(self.luks_partition, self.luks_passphrase)
        self.assertTrue(fmt)

        self.assertRaises(
            pywbem.CIMError,
            self.wbemconnection.InvokeMethod,
            "DeletePassphrase",
            self.service,
            Passphrase='NoSuchPassword',
            Format=fmt)

    def test_double_open_encryption_format(self):
        """
        Test opening already opened LUKS.
        """
        fmt = self._create_luks(self.luks_partition, self.luks_passphrase)
        self.assertTrue(fmt)

        (ret, outparams) = self.invoke_async_method(
                "OpenEncryptionFormat",
                self.service,
                int,
                ElementName=self.luks_elementname,
                Passphrase=self.luks_passphrase,
                Format=fmt)
        self.assertEquals(ret, 0)

        try:
            self.assertRaises(
                    pywbem.CIMError,
                    self.invoke_async_method,
                    "OpenEncryptionFormat",
                    self.service,
                    int,
                    ElementName=self.luks_elementname,
                    Passphrase=self.luks_passphrase,
                    Format=fmt)
        except:
            # print the exception so it's not overwritten by any new exception
            # in 'finally' block
            print >> sys.stderr, "test_create_encryption_format failed:"
            print >> sys.stderr, traceback.format_exc()
            raise

        finally:
            (ret, outparams) = self.invoke_async_method(
                    "CloseEncryptionFormat",
                    self.service,
                    int,
                    Format=fmt)
            self.assertEquals(ret, 0)


    def test_double_close_encryption_format(self):
        """
        Test closing already closed LUKS.
        """
        fmt = self._create_luks(self.luks_partition, self.luks_passphrase)
        self.assertTrue(fmt)

        (ret, outparams) = self.invoke_async_method(
                "OpenEncryptionFormat",
                self.service,
                int,
                ElementName=self.luks_elementname,
                Passphrase=self.luks_passphrase,
                Format=fmt)
        self.assertEquals(ret, 0)

        (ret, outparams) = self.invoke_async_method(
                "CloseEncryptionFormat",
                self.service,
                int,
                Format=fmt)
        self.assertEquals(ret, 0)

        self.assertRaises(
            pywbem.CIMError,
            self.invoke_async_method,
            "CloseEncryptionFormat",
            self.service,
            int,
            Format=fmt)


if __name__ == '__main__':
    unittest.main()
