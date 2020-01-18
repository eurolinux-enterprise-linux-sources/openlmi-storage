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
# -*- coding: utf-8 -*-
"""
Module for LMI_MDRAIDStorageCapabilities class.

LMI_MDRAIDStorageCapabilities
-----------------------------

.. autoclass:: LMI_MDRAIDStorageCapabilities
    :members:

"""

from lmi.storage.CapabilitiesProvider import CapabilitiesProvider
from lmi.storage.SettingManager import Setting
import pywbem
import lmi.providers.cmpi_logging as cmpi_logging
import lmi.storage.util.units as units
from lmi.storage.DeviceProvider import DeviceProvider

class LMI_MDRAIDStorageCapabilities(CapabilitiesProvider):
    """
        LMI_MDRAIDStorageCapabilities provider implementation.
    """

    INSTANCE_ID = "LMI:LMI_MDRAIDStorageCapabilities:Global"

    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_MDRAIDStorageCapabilities, self).__init__(
                "LMI_MDRAIDStorageCapabilities", *args, **kwargs)

        parity = LMI_MDRAIDStorageCapabilities.Values.ParityLayoutDefault
        self.instances = [
            {
                    'InstanceID': LMI_MDRAIDStorageCapabilities.INSTANCE_ID,
                    'ElementName': LMI_MDRAIDStorageCapabilities.INSTANCE_ID,
                    'DataRedundancyDefault': pywbem.Uint16(1),
                    'DataRedundancyMax': pywbem.Uint16(units.MAXINT16),
                    'DataRedundancyMin': pywbem.Uint16(1),
                    'NoSinglePointOfFailure': True,
                    'NoSinglePointOfFailureDefault': False,
                    'ExtentStripeLengthDefault': pywbem.Uint16(1),
                    'PackageRedundancyDefault': pywbem.Uint16(0),
                    'PackageRedundancyMax': pywbem.Uint16(units.MAXINT16),
                    'PackageRedundancyMin': pywbem.Uint16(0),
                    'ParityLayoutDefault': parity.Rotated_Parity
            },
    ]

    @cmpi_logging.trace_method
    def enumerate_capabilities(self):
        """
            Return an iterable with all capabilities instances, i.e.
            dictionaries property_name -> value.
            If the capabilities are the default ones, it must have
            '_default' as a property name.
        """

        return self.instances

    @cmpi_logging.trace_method
    # pylint: disable-msg=W0221
    def create_setting_for_capabilities(self, capabilities, default=False):
        """
            Create LMI_MDRAIDStorageSetting for given capabilities.
            Return CIMInstanceName of the setting or raise CIMError on error.
        """
        setting_id = self.setting_manager.allocate_id(
                'LMI_MDRAIDStorageSetting')
        if not setting_id:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Failed to allocate setting InstanceID")

        setting = self.setting_manager.create_setting(
                'LMI_MDRAIDStorageSetting',
                Setting.TYPE_TRANSIENT,
                setting_id)

        if default:
            setting['DataRedundancyGoal'] = pywbem.Uint16(
                    capabilities['DataRedundancyDefault'])
            setting['DataRedundancyMax'] = pywbem.Uint16(
                    capabilities['DataRedundancyDefault'])
            setting['DataRedundancyMin'] = pywbem.Uint16(
                    capabilities['DataRedundancyDefault'])
            setting['ExtentStripeLength'] = pywbem.Uint16(
                    capabilities['ExtentStripeLengthDefault'])
            setting['ExtentStripeLengthMax'] = pywbem.Uint16(
                    capabilities['ExtentStripeLengthDefault'])
            setting['ExtentStripeLengthMin'] = pywbem.Uint16(
                    capabilities['ExtentStripeLengthDefault'])
            setting['NoSinglePointOfFailure'] = \
                    capabilities['NoSinglePointOfFailureDefault']
            setting['PackageRedundancyGoal'] = pywbem.Uint16(
                    capabilities['PackageRedundancyDefault'])
            setting['PackageRedundancyMax'] = pywbem.Uint16(
                    capabilities['PackageRedundancyDefault'])
            setting['PackageRedundancyMin'] = pywbem.Uint16(
                    capabilities['PackageRedundancyDefault'])
            if capabilities['ParityLayoutDefault']:
                setting['ParityLayout'] = pywbem.Uint16(
                        capabilities['ParityLayoutDefault'] - 1)
            else:
                setting['ParityLayout'] = None
        else:
            setting['DataRedundancyGoal'] = pywbem.Uint16(
                    capabilities['DataRedundancyDefault'])
            setting['DataRedundancyMax'] = pywbem.Uint16(
                    capabilities['DataRedundancyMax'])
            setting['DataRedundancyMin'] = pywbem.Uint16(
                    capabilities['DataRedundancyMin'])
            setting['ExtentStripeLength'] = pywbem.Uint16(
                    capabilities['ExtentStripeLengthDefault'])
            setting['ExtentStripeLengthMax'] = pywbem.Uint16(
                    capabilities['ExtentStripeLengthDefault'])
            setting['ExtentStripeLengthMin'] = pywbem.Uint16(
                    capabilities['ExtentStripeLengthDefault'])
            setting['NoSinglePointOfFailure'] = \
                    capabilities['NoSinglePointOfFailureDefault']
            setting['PackageRedundancyGoal'] = pywbem.Uint16(
                    capabilities['PackageRedundancyDefault'])
            setting['PackageRedundancyMax'] = pywbem.Uint16(
                    capabilities['PackageRedundancyMax'])
            setting['PackageRedundancyMin'] = pywbem.Uint16(
                    capabilities['PackageRedundancyMin'])
            if capabilities['ParityLayoutDefault']:
                setting['ParityLayout'] = pywbem.Uint16(
                        capabilities['ParityLayoutDefault'] - 1)
            else:
                setting['ParityLayout'] = None

        setting['ElementName'] = 'CreatedFrom' + capabilities['InstanceID']
        self.setting_manager.set_setting('LMI_MDRAIDStorageSetting', setting)
        return pywbem.CIMInstanceName(
                classname='LMI_MDRAIDStorageSetting',
                namespace=self.config.namespace,
                keybindings={'InstanceID': setting_id})


    @cmpi_logging.trace_method
    # pylint: disable-msg=W0221
    def cim_method_createsetting(self, env, object_name,
            param_settingtype=None):
        """
            Implements LMI_MDRAIDStorageCapabilities.CreateSetting()

            Method to create and populate a StorageSetting instance from a
            StorageCapability instance. This removes the need to populate
            default settings and other settings in the context of each
            StorageCapabilities (which could be numerous). If the underlying
            instrumentation supports the StorageSettingWithHints subclass,
            then an instance of that class will be created instead.
        """
        default = False
        if param_settingtype:
            setting_types = self.Values.CreateSetting.SettingType
            if param_settingtype == setting_types.Default:
                default = True
            elif param_settingtype == setting_types.Goal:
                default = False
            else:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                        "Parameter SettingType has invalid value.")

        capabilities = self.get_capabilities_for_id(object_name['InstanceID'])
        if not capabilities:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find the Capabilities.")

        setting_name = self.create_setting_for_capabilities(
                capabilities, default)

        outparams = [pywbem.CIMParameter('newsetting', type='reference',
                           value=setting_name)]
        rval = self.Values.CreateSetting.Success
        return (rval, outparams)

    @cmpi_logging.trace_method
    def cim_method_createmdraidstoragesetting(self, env, object_name,
                                          param_inextents=None,
                                          param_level=None):
        """
            Implements LMI_MDRAIDStorageCapabilities.CreateMDRAIDStorageSetting()

            This method creates new instance of LMI_MDRAIDStorageSetting.
            Applications then do not need to calculate DataRedundancy,
            PackageRedundancy and ExtentStripeLength.
        """
        if not param_inextents:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Parameter InExtents is mandatory.")

        if param_level is not None:
            level = param_level
        else:
            level = self.Values.CreateMDRAIDStorageSetting.Level.RAID0
        if level not in (
                self.Values.CreateMDRAIDStorageSetting.Level.RAID0,
                self.Values.CreateMDRAIDStorageSetting.Level.RAID1,
                self.Values.CreateMDRAIDStorageSetting.Level.RAID4,
                self.Values.CreateMDRAIDStorageSetting.Level.RAID5,
                self.Values.CreateMDRAIDStorageSetting.Level.RAID6,
                self.Values.CreateMDRAIDStorageSetting.Level.RAID10):
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Invalid value of parameter Level.")

        # create list of redundancies of all input devices
        redundancies = []
        for device_name in param_inextents:
            provider = self.provider_manager.get_device_provider_for_name(
                    device_name)
            if not provider:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                        "Cannot find provider for one of the input extents.")
            device = provider.get_device_for_name(device_name)
            if not device:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                        "Cannot find device for one of the input extents.")
            redundancy = provider.get_redundancy(device)
            redundancies.append(redundancy)

        final_redundancy = DeviceProvider.Redundancy.get_common_redundancy_list(
                redundancies, level)

        setting_id = self.setting_manager.allocate_id(
                'LMI_MDRAIDStorageSetting')
        if not setting_id:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Failed to allocate setting InstanceID")

        setting = self.setting_manager.create_setting(
                'LMI_MDRAIDStorageSetting',
                Setting.TYPE_TRANSIENT,
                setting_id)
        setting['DataRedundancyGoal'] = pywbem.Uint16(
                final_redundancy.data_redundancy)
        setting['DataRedundancyMax'] = pywbem.Uint16(
                final_redundancy.data_redundancy)
        setting['DataRedundancyMin'] = pywbem.Uint16(
                final_redundancy.data_redundancy)
        setting['ExtentStripeLength'] = pywbem.Uint16(
                final_redundancy.stripe_length)
        setting['ExtentStripeLengthMax'] = pywbem.Uint16(
                final_redundancy.stripe_length)
        setting['ExtentStripeLengthMin'] = pywbem.Uint16(
                final_redundancy.stripe_length)
        setting['NoSinglePointOfFailure'] = \
                final_redundancy.no_single_point_of_failure
        setting['PackageRedundancyGoal'] = pywbem.Uint16(
                final_redundancy.package_redundancy)
        setting['PackageRedundancyMax'] = pywbem.Uint16(
                final_redundancy.package_redundancy)
        setting['PackageRedundancyMin'] = pywbem.Uint16(
                final_redundancy.package_redundancy)
        setting['ElementName'] = 'CreatedFrom' + object_name['InstanceID']
        if final_redundancy.parity_layout:
            setting['ParityLayout'] = pywbem.Uint16(
                    final_redundancy.parity_layout)
        else:
            setting['ParityLayout'] = None
        self.setting_manager.set_setting('LMI_MDRAIDStorageSetting', setting)

        outparams = [ pywbem.CIMParameter('setting', type='reference',
                           value=pywbem.CIMInstanceName(
                                   classname='LMI_MDRAIDStorageSetting',
                                   namespace=self.config.namespace,
                                   keybindings={'InstanceID': setting_id}))]
        return (self.Values.CreateMDRAIDStorageSetting.Success, outparams)

    class Values(CapabilitiesProvider.Values):
        class CreateSetting(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unspecified_Error = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535
            class SettingType(object):
                Default = pywbem.Uint16(2)
                Goal = pywbem.Uint16(3)

        class CreateMDRAIDStorageSetting(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Failed = pywbem.Uint32(4)
            class Level(object):
                RAID0 = pywbem.Uint16(0)
                RAID1 = pywbem.Uint16(1)
                RAID4 = pywbem.Uint16(4)
                RAID5 = pywbem.Uint16(5)
                RAID6 = pywbem.Uint16(6)
                RAID10 = pywbem.Uint16(10)

        class ParityLayoutDefault(object):
            Non_Rotated_Parity = pywbem.Uint16(2)
            Rotated_Parity = pywbem.Uint16(3)
