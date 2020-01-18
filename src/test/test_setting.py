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

from test_base import StorageTestBase
import pywbem
import unittest

class TestSettings(StorageTestBase):
    """
        Test common features of settings.
         - it can be cloned
         - it can be modified
         - it can be persisted to disk
         - it can be removed
    """
    @classmethod
    def setUpClass(cls):
        super(TestSettings, cls).setUpClass()

        # find an instance we will clone
        settings = cls.wbemconnection.EnumerateInstanceNames('LMI_DiskPartitionConfigurationSetting')        
        if len(settings) < 1:
            raise unittest.SkipTest("There is no LMI_DiskPartitionConfigurationSetting on system. Add a partition!")
        cls.master = settings[0]

    def create_clone(self):
        """ Create and return a clone of master. """
        (ret, outvars) = self.wbemconnection.InvokeMethod(
                'CloneSetting',
                self.master)
        # check return parameters
        self.assertTrue(ret == 0)
        clone_path = outvars['Clone']
        self.assertTrue(clone_path)
        clone = self.wbemconnection.GetInstance(clone_path)
        return clone
        
    def test_clone(self):
        """ Test that master.clone works as expected """
        clone = self.create_clone()
        self.assertTrue(clone)
        
        # check the clone is the same as the master
        master = self.wbemconnection.GetInstance(self.master)
        self.assertEqual(master['Bootable'], clone['Bootable'])
        self.assertEqual(master['Caption'], clone['Caption'])
        self.assertEqual(master['ConfigurationName'], clone['ConfigurationName'])
        self.assertEqual(master['Description'], clone['Description'])
        self.assertEqual(master['ElementName'], clone['ElementName'])
        self.assertEqual(master['Hidden'], clone['Hidden'])
        self.assertEqual(master['PartitionType'], clone['PartitionType'])
        # check it has different ID
        self.assertNotEqual(self.master['InstanceID'], clone['InstanceID'])
        # check the clone is transient
        self.assertEqual(1, clone['ChangeableType'])
        
    def test_modify_transient(self):
        """ Test changing of transient instance. """
        clone = self.create_clone()
        self.assertTrue(clone)
        clone_path = clone.path
        # change Bootable, ElementName and PartitionType to initial values
        # (we don't know what clone values are)
        clone['Bootable'] = False
        clone['PartitionType'] = pywbem.Uint16(0) # unknown
        clone['ElementName'] = 'myElementName'
        self.wbemconnection.ModifyInstance(clone)

        clone = self.wbemconnection.GetInstance(clone_path)
        self.assertTrue(clone)
        self.assertEqual(clone['Bootable'], False)
        self.assertEqual(clone['ElementName'], 'myElementName')
        self.assertEqual(clone['PartitionType'], 0)

        # change Bootable, ElementName and PartitionType again
        clone['Bootable'] = True
        clone['PartitionType'] = pywbem.Uint16(1)
        clone['ElementName'] = 'myElementName2'
        self.wbemconnection.ModifyInstance(clone)
        clone = self.wbemconnection.GetInstance(clone_path)
        self.assertTrue(clone)
        self.assertEqual(clone['Bootable'], True)
        self.assertEqual(clone['ElementName'], 'myElementName2')
        self.assertEqual(clone['PartitionType'], 1)

        # change ChangeableType
        # not changeable - persistent -> error
        clone['ChangeableType'] = pywbem.Uint16(0) 
        self.assertRaises(pywbem.CIMError, self.wbemconnection.ModifyInstance, clone)

        # not changeable - transient -> error
        clone['ChangeableType'] = pywbem.Uint16(4) 
        self.assertRaises(pywbem.CIMError, self.wbemconnection.ModifyInstance, clone)

        # changeable - transient -> nothing happens
        clone['ChangeableType'] = pywbem.Uint16(1) 
        self.wbemconnection.ModifyInstance(clone)

    def test_restart_transient(self):
        """ Test that CIMOM restart removes all transient. """
        clone = self.create_clone()
        self.assertTrue(clone)
        clone_path = clone.path
        
        self.restart_cim()
        
        self.assertRaises(pywbem.CIMError,
                          self.wbemconnection.GetInstance,
                          clone_path)

    def test_delete_transient(self):
        """ Test that transient config can be removed. """
        clone = self.create_clone()
        self.assertTrue(clone)
        clone_path = clone.path
        
        self.wbemconnection.DeleteInstance(clone_path)
        
        self.assertRaises(pywbem.CIMError,
                          self.wbemconnection.GetInstance,
                          clone_path)

    def test_delete_persistent(self):
        """ Test that persistent config can be removed. """
        clone = self.create_clone()
        self.assertTrue(clone)
        clone_path = clone.path

        # changeable - persistent -> clone is stored
        clone['ChangeableType'] = pywbem.Uint16(2)
        self.wbemconnection.ModifyInstance(clone)
        
        self.wbemconnection.DeleteInstance(clone_path)        
        self.assertRaises(pywbem.CIMError,
                          self.wbemconnection.GetInstance,
                          clone_path)
                          
        # check the instance is gone also after restart
        self.restart_cim()
        self.assertRaises(pywbem.CIMError,
                          self.wbemconnection.GetInstance,
                          clone_path)
        
        
        
    def test_modify_persistent(self):
        """ 
            Test that persistent setting can be modified and the changes
            survive CIMOM restart.
        """
        clone = self.create_clone()
        self.assertTrue(clone)
        clone_path = clone.path
        # change Bootable, ElementName and PartitionType to initial values
        # (we don't know what clone values are)
        clone['Bootable'] = False
        clone['PartitionType'] = pywbem.Uint16(0) # unknown
        clone['ElementName'] = 'myElementName'
        
        self.wbemconnection.ModifyInstance(clone)
        # changeable - persistent -> clone is stored
        clone['ChangeableType'] = pywbem.Uint16(2)
        self.wbemconnection.ModifyInstance(clone)
        
        # restart the service and check the clone survived
        self.restart_cim()
        clone = self.wbemconnection.GetInstance(clone_path)
        self.assertTrue(clone)
        self.assertEqual(clone['Bootable'], False)
        self.assertEqual(clone['ElementName'], 'myElementName')
        self.assertEqual(clone['PartitionType'], 0)
        self.assertEqual(clone['ChangeableType'], 2)
        
        # try to change the clone
        clone['Bootable'] = True
        clone['PartitionType'] = pywbem.Uint16(1)
        clone['ElementName'] = 'myElementName1'
        self.wbemconnection.ModifyInstance(clone)

        clone = self.wbemconnection.GetInstance(clone_path)
        self.assertTrue(clone)
        self.assertEqual(clone['Bootable'], True)
        self.assertEqual(clone['ElementName'], 'myElementName1')
        self.assertEqual(clone['PartitionType'], 1)
        self.assertEqual(clone['ChangeableType'], 2)

        # change ChangeableType
        # not changeable - persistent -> error
        clone['ChangeableType'] = pywbem.Uint16(0) 
        self.assertRaises(pywbem.CIMError, self.wbemconnection.ModifyInstance, clone)

        # not changeable - transient -> error
        clone['ChangeableType'] = pywbem.Uint16(4) 
        self.assertRaises(pywbem.CIMError, self.wbemconnection.ModifyInstance, clone)

        # changeable - transient -> error
        clone['ChangeableType'] = pywbem.Uint16(1) 
        self.assertRaises(pywbem.CIMError, self.wbemconnection.ModifyInstance, clone)
        
        # changeable - persistent -> nothing happens
        clone['ChangeableType'] = pywbem.Uint16(2)
        self.wbemconnection.ModifyInstance(clone)
        
        # restart the service and check the clone survived
        self.restart_cim()
        clone = self.wbemconnection.GetInstance(clone_path)
        self.assertTrue(clone)
        self.assertEqual(clone['Bootable'], True)
        self.assertEqual(clone['ElementName'], 'myElementName1')
        self.assertEqual(clone['PartitionType'], 1)
        self.assertEqual(clone['ChangeableType'], 2)
        

if __name__ == '__main__':
    unittest.main()
