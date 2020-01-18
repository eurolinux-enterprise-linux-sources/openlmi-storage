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
    This module is the main entry from lmi.storage.CIMOM.

    All initialization must be done here.

    This module instantiates all providers and registers them in CIMOM.
"""

from lmi.storage.StorageConfiguration import StorageConfiguration
from lmi.storage.ProviderManager import ProviderManager
from lmi.storage.SettingManager import SettingManager

from lmi.storage.LMI_StorageExtent import LMI_StorageExtent
from lmi.storage.LMI_MDRAIDStorageExtent import LMI_MDRAIDStorageExtent
from lmi.storage.LMI_DiskPartition import LMI_DiskPartition
from lmi.storage.LMI_GenericDiskPartition import LMI_GenericDiskPartition
from lmi.storage.LMI_LVStorageExtent import LMI_LVStorageExtent
from lmi.storage.LMI_VGStoragePool import LMI_VGStoragePool
from lmi.storage.LMI_PartitionBasedOn import LMI_PartitionBasedOn
from lmi.storage.LMI_MDRAIDBasedOn import LMI_MDRAIDBasedOn
from lmi.storage.LMI_LVBasedOn import LMI_LVBasedOn
from lmi.storage.LMI_LVAllocatedFromStoragePool \
        import LMI_LVAllocatedFromStoragePool
from lmi.storage.LMI_VGAssociatedComponentExtent \
        import LMI_VGAssociatedComponentExtent
from lmi.storage.LMI_DiskPartitionConfigurationSetting \
        import LMI_DiskPartitionConfigurationSetting
from lmi.storage.SettingProvider \
        import ElementSettingDataProvider, SettingHelperProvider
from lmi.storage.LMI_DiskPartitioningConfigurationService \
        import LMI_DiskPartitionConfigurationService
from lmi.storage.LMI_HostedStorageService \
        import LMI_HostedStorageService
from lmi.storage.LMI_DiskPartitionConfigurationCapabilities \
        import LMI_DiskPartitionConfigurationCapabilities
from lmi.storage.CapabilitiesProvider import ElementCapabilitiesProvider
from lmi.storage.LMI_InstalledPartitionTable \
        import LMI_InstalledPartitionTable
from lmi.storage.LMI_LVStorageCapabilities \
        import LMI_LVStorageCapabilities, LMI_LVElementCapabilities
from lmi.storage.LMI_StorageConfigurationService \
        import LMI_StorageConfigurationService
from lmi.storage.LMI_VGStorageCapabilities import LMI_VGStorageCapabilities
from lmi.storage.LMI_MDRAIDStorageCapabilities \
        import LMI_MDRAIDStorageCapabilities
from lmi.storage.LMI_SystemStorageDevice import LMI_SystemStorageDevice
from lmi.storage.LMI_MDRAIDFormatProvider import LMI_MDRAIDFormatProvider
from lmi.storage.LMI_PVFormatProvider import LMI_PVFormatProvider
from lmi.storage.LMI_DataFormatProvider import LMI_DataFormatProvider
from lmi.storage.FormatProvider import LMI_ResidesOnExtent
from lmi.storage.LMI_LocalFileSystem import LMI_LocalFileSystem
from lmi.storage.LMI_FileSystemConfigurationService \
        import LMI_FileSystemConfigurationService
from lmi.storage.LMI_FileSystemConfigurationCapabilities \
        import LMI_FileSystemConfigurationCapabilities
from lmi.storage.LMI_FileSystemCapabilities \
        import LMI_FileSystemCapabilities
from lmi.providers.JobManager import JobManager
from lmi.providers.IndicationManager import IndicationManager
from lmi.storage.LMI_HostedFileSystem import LMI_HostedFileSystem
from lmi.storage.LMI_MountedFileSystem import LMI_MountedFileSystem
from lmi.storage.LMI_HostedMount import LMI_HostedMount
from lmi.storage.LMI_MountPoint import LMI_MountPoint
from lmi.storage.LMI_AttachedFileSystem import LMI_AttachedFileSystem
from lmi.storage.LMI_MountConfigurationService import LMI_MountConfigurationService
from lmi.storage.LMI_MountedFileSystemCapabilities import LMI_MountedFileSystemCapabilities
from lmi.providers.TimerManager import TimerManager
from lmi.storage.LMI_TransientFileSystem import LMI_TransientFileSystem
from lmi.storage.LMI_BlockStorageStatisticalData import \
    LMI_BlockStorageStatisticalData, LMI_StorageElementStatisticalData, \
    LMI_StorageStatisticsCollection, LMI_MemberOfStorageStatisticsCollection, \
    LMI_HostedStorageStatisticsCollection, \
    LMI_BlockStatisticsManifestCollection, LMI_BlockStatisticsManifest, \
    LMI_MemberOfBlockStatisticsManifestCollection, \
    LMI_AssociatedBlockStatisticsManifestCollection, \
    LMI_BlockStatisticsService, LMI_BlockStatisticsCapabilities
from lmi.storage.LMI_LUKSStorageExtent import LMI_LUKSStorageExtent
from lmi.storage.LMI_LUKSFormat import LMI_LUKSFormat
from lmi.storage.LMI_ExtentEncryptionConfigurationService import LMI_ExtentEncryptionConfigurationService
from lmi.storage.LMI_LUKSBasedOn import LMI_LUKSBasedOn

import lmi.providers.cmpi_logging as cmpi_logging
from lmi.providers.ComputerSystem import get_system_name
import blivet
import logging

timer_manager = None
indication_manager = None
job_manager = None

LOG = cmpi_logging.get_logger(__name__)

def init_anaconda(config):
    """ Initialize Anaconda storage module."""
    LOG().info("Initializing Anaconda")

    # enable discovery of non-device filesystems (procfs, tmpfs, ...)
    blivet.flags.include_nodev = True
    # set up storage class instance
    storage = blivet.Blivet()
    # identify the system's storage devices
    storage.reset()
    return storage

def get_providers(env):
    """
        CIMOM callback. Initialize OpenLMI and return dictionary of all
        providers we implement.
    """
    # allow **magic here
    # pylint: disable-msg=W0142

    config = StorageConfiguration.get_instance()
    cmpi_logging.setup(env, config)
    root_logger = logging.getLogger()
    anaconda_loggers = [
        logging.getLogger('blivet'),
        logging.getLogger('program')]
    for logger in anaconda_loggers:
        logger.setLevel(logging.DEBUG if config.blivet_tracing else logging.WARNING)
        for handler in root_logger.handlers:
            logger.addHandler(handler)
    LOG().info("Provider init.")

    # Initialize ComputerSystem.Name
    get_system_name(env)

    # initialize the timer manager
    global timer_manager
    timer_manager = TimerManager.get_instance(env)

    global indication_manager
    indication_manager = IndicationManager.get_instance(
            env, "Storage", config.namespace)

    manager = ProviderManager()
    setting_manager = SettingManager(config, timer_manager)
    setting_manager.load()
    storage = init_anaconda(config)

    global job_manager
    job_manager = JobManager('Storage', config.namespace,
            indication_manager, timer_manager)

    providers = {}
    # common construction options
    opts = {'storage': storage,
            'config': config,
            'provider_manager': manager,
            'setting_manager': setting_manager,
            'job_manager' : job_manager}

    # StorageDevice providers
    provider = LMI_StorageExtent(**opts)
    manager.add_device_provider(provider)
    providers['LMI_StorageExtent'] = provider

    provider = LMI_MDRAIDStorageExtent(**opts)
    manager.add_device_provider(provider)
    providers['LMI_MDRAIDStorageExtent'] = provider
    setting_provider = SettingHelperProvider(
            setting_helper=provider,
            setting_classname="LMI_MDRAIDStorageSetting",
            **opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_MDRAIDStorageSetting'] = setting_provider
    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="LMI_MDRAIDStorageExtent",
            setting_data_classname="LMI_MDRAIDStorageSetting",
            **opts)
    providers['LMI_MDRAIDElementSettingData'] = assoc_provider

    provider = LMI_DiskPartition(**opts)
    manager.add_device_provider(provider)
    providers['LMI_DiskPartition'] = provider

    provider = LMI_GenericDiskPartition(**opts)
    manager.add_device_provider(provider)
    providers['LMI_GenericDiskPartition'] = provider

    provider = LMI_LVStorageExtent(**opts)
    manager.add_device_provider(provider)
    providers['LMI_LVStorageExtent'] = provider
    setting_provider = SettingHelperProvider(
            setting_helper=provider,
            setting_classname="LMI_LVStorageSetting",
            **opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_LVStorageSetting'] = setting_provider
    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="LMI_LVStorageExtent",
            setting_data_classname="LMI_LVStorageSetting",
            **opts)
    providers['LMI_LVElementSettingData'] = assoc_provider

    provider = LMI_VGStoragePool(**opts)
    manager.add_device_provider(provider)
    providers['LMI_VGStoragePool'] = provider
    setting_provider = SettingHelperProvider(
            setting_helper=provider,
            setting_classname="LMI_VGStorageSetting",
            **opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_VGStorageSetting'] = setting_provider
    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="LMI_VGStoragePool",
            setting_data_classname="LMI_VGStorageSetting",
            **opts)
    providers['LMI_VGElementSettingData'] = assoc_provider
    cap_provider = LMI_LVStorageCapabilities(**opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_LVStorageCapabilities'] = cap_provider
    assoc_provider = LMI_LVElementCapabilities(
            "LMI_LVElementCapabilities",
            cap_provider, provider, **opts)
    providers['LMI_LVElementCapabilities'] = assoc_provider

    # mounting
    provider = LMI_MountedFileSystem(**opts)
    providers['LMI_MountedFileSystem'] = provider

    setting_provider = SettingHelperProvider(
            setting_helper=provider,
            setting_classname="LMI_MountedFileSystemSetting",
            **opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_MountedFileSystemSetting'] = setting_provider

    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="LMI_MountedFileSystem",
            setting_data_classname="LMI_MountedFileSystemSetting",
            **opts)
    providers['LMI_MountedFileSystemElementSettingData'] = assoc_provider

    provider = LMI_HostedMount(**opts)
    providers['LMI_HostedMount'] = provider

    provider = LMI_MountPoint(**opts)
    providers['LMI_MountPoint'] = provider

    provider = LMI_AttachedFileSystem(**opts)
    providers['LMI_AttachedFileSystem'] = provider

    service_provider = LMI_MountConfigurationService(**opts)
    manager.add_service_provider(service_provider)
    providers['LMI_MountConfigurationService'] = service_provider

    cap_provider = LMI_MountedFileSystemCapabilities(**opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_MountedFileSystemCapabilities'] = cap_provider

    assoc_provider = ElementCapabilitiesProvider(
            'LMI_MountElementCapabilities',
            cap_provider, service_provider, **opts)
    providers['LMI_MountElementCapabilities'] = assoc_provider

    # luks
    provider = LMI_LUKSStorageExtent(**opts)
    manager.add_device_provider(provider)
    providers['LMI_LUKSStorageExtent'] = provider

    provider = LMI_LUKSBasedOn(**opts)
    providers['LMI_LUKSBasedOn'] = provider

    provider = LMI_LUKSFormat(**opts)
    manager.add_format_provider(provider)
    providers['LMI_LUKSFormat'] = provider

    service_provider = LMI_ExtentEncryptionConfigurationService(**opts)
    manager.add_service_provider(service_provider)
    providers['LMI_ExtentEncryptionConfigurationService'] = service_provider

    # settings
    setting_provider = LMI_DiskPartitionConfigurationSetting(
            ** opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_DiskPartitionConfigurationSetting'] = setting_provider
    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="CIM_DiskPartition",
            setting_data_classname="LMI_DiskPartitionConfigurationSetting",
            **opts)
    providers['LMI_DiskPartitionElementSettingData'] = assoc_provider


    # services & capabilities
    service_provider = LMI_StorageConfigurationService(**opts)
    manager.add_service_provider(service_provider)
    providers['LMI_StorageConfigurationService'] = service_provider
    cap_provider = LMI_VGStorageCapabilities(**opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_VGStorageCapabilities'] = cap_provider
    assoc_provider = ElementCapabilitiesProvider(
            "LMI_VGElementCapabilities",
            cap_provider, service_provider, **opts)
    providers['LMI_VGElementCapabilities'] = assoc_provider

    cap_provider = LMI_MDRAIDStorageCapabilities(**opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_MDRAIDStorageCapabilities'] = cap_provider
    assoc_provider = ElementCapabilitiesProvider(
            "LMI_MDRAIDElementCapabilities",
            cap_provider, service_provider, **opts)
    providers['LMI_MDRAIDElementCapabilities'] = assoc_provider


    service_provider = LMI_DiskPartitionConfigurationService(
            ** opts)

    manager.add_service_provider(service_provider)
    providers['LMI_DiskPartitionConfigurationService'] = service_provider

    cap_provider = LMI_DiskPartitionConfigurationCapabilities(
            ** opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_DiskPartitionConfigurationCapabilities'] = cap_provider
    assoc_provider = ElementCapabilitiesProvider(
            "LMI_DiskPartitionElementCapabilities",
            cap_provider, service_provider, **opts)
    providers['LMI_DiskPartitionElementCapabilities'] = assoc_provider


    # Associations
    provider = LMI_PartitionBasedOn(**opts)
    providers['LMI_PartitionBasedOn'] = provider

    provider = LMI_MDRAIDBasedOn(**opts)
    providers['LMI_MDRAIDBasedOn'] = provider

    provider = LMI_LVBasedOn(**opts)
    providers['LMI_LVBasedOn'] = provider

    provider = LMI_LVAllocatedFromStoragePool(**opts)
    providers['LMI_LVAllocatedFromStoragePool'] = provider

    provider = LMI_VGAssociatedComponentExtent(**opts)
    providers['LMI_VGAssociatedComponentExtent'] = provider

    provider = LMI_HostedStorageService(**opts)
    providers['LMI_HostedStorageService'] = provider

    provider = LMI_SystemStorageDevice(**opts)
    providers['LMI_SystemStorageDevice'] = provider

    provider = LMI_InstalledPartitionTable(**opts)
    providers['LMI_InstalledPartitionTable'] = provider

    fmt = LMI_DataFormatProvider(**opts)
    manager.add_format_provider(fmt)
    providers['LMI_DataFormat'] = fmt

    fmt = LMI_MDRAIDFormatProvider(**opts)
    manager.add_format_provider(fmt)
    providers['LMI_MDRAIDFormat'] = fmt

    fmt = LMI_PVFormatProvider(**opts)
    manager.add_format_provider(fmt)
    providers['LMI_PVFormat'] = fmt

    fmt = LMI_LocalFileSystem(**opts)
    manager.add_format_provider(fmt)
    providers['LMI_LocalFileSystem'] = fmt
    setting_provider = SettingHelperProvider(
            setting_helper=fmt,
            setting_classname="LMI_FileSystemSetting",
            **opts)
    manager.add_setting_provider(setting_provider)
    providers['LMI_FileSystemSetting'] = setting_provider
    assoc_provider = ElementSettingDataProvider(
            setting_provider=setting_provider,
            managed_element_classname="LMI_LocalFileSystem",
            setting_data_classname="LMI_FileSystemSetting",
            **opts)
    providers['LMI_FileSystemElementSettingData'] = assoc_provider

    fmt = LMI_TransientFileSystem(**opts)
    manager.add_format_provider(fmt)
    providers['LMI_TransientFileSystem'] = fmt

    service_provider = LMI_FileSystemConfigurationService(**opts)
    manager.add_service_provider(service_provider)
    providers['LMI_FileSystemConfigurationService'] = service_provider
    cap_provider = LMI_FileSystemConfigurationCapabilities(
            ** opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_FileSystemConfigurationCapabilities'] = cap_provider
    assoc_provider = ElementCapabilitiesProvider(
            "LMI_FileSystemConfigurationElementCapabilities",
            cap_provider, service_provider, **opts)
    providers['LMI_FileSystemConfigurationElementCapabilities'] = assoc_provider

    cap_provider = LMI_FileSystemCapabilities(**opts)
    manager.add_capabilities_provider(cap_provider)
    providers['LMI_FileSystemCapabilities'] = cap_provider
    assoc_provider = ElementCapabilitiesProvider(
            "LMI_FileSystemElementCapabilities",
            cap_provider, service_provider, **opts)
    providers['LMI_FileSystemElementCapabilities'] = assoc_provider

    provider = LMI_ResidesOnExtent(**opts)
    providers['LMI_ResidesOnExtent'] = provider

    job_providers = job_manager.get_providers()
    providers.update(job_providers)

    provider = LMI_HostedFileSystem(**opts)
    providers['LMI_HostedFileSystem'] = provider

    # Block Statistics providers
    block_stat_provider = LMI_BlockStorageStatisticalData(**opts)
    providers['LMI_BlockStorageStatisticalData'] = block_stat_provider

    assoc_provider = LMI_StorageElementStatisticalData(
            block_stat_provider=block_stat_provider,
            **opts)
    providers['LMI_StorageElementStatisticalData'] = assoc_provider

    provider = LMI_StorageStatisticsCollection(**opts)
    providers['LMI_StorageStatisticsCollection'] = provider

    provider = LMI_MemberOfStorageStatisticsCollection(
            block_stat_provider=block_stat_provider,
            **opts)
    providers['LMI_MemberOfStorageStatisticsCollection'] = provider

    provider = LMI_HostedStorageStatisticsCollection(**opts)
    providers['LMI_HostedStorageStatisticsCollection'] = provider

    provider = LMI_BlockStatisticsManifestCollection(**opts)
    providers['LMI_BlockStatisticsManifestCollection'] = provider

    manifest_provider = LMI_BlockStatisticsManifest(**opts)
    providers['LMI_BlockStatisticsManifest'] = manifest_provider

    provider = LMI_MemberOfBlockStatisticsManifestCollection(
            manifest_provider=manifest_provider, **opts)
    providers['LMI_MemberOfBlockStatisticsManifestCollection'] = provider

    provider = LMI_AssociatedBlockStatisticsManifestCollection(**opts)
    providers['LMI_AssociatedBlockStatisticsManifestCollection'] = provider

    service_provider = LMI_BlockStatisticsService(
            block_stat_provider,
            **opts)
    providers['LMI_BlockStatisticsService'] = service_provider
    manager.add_service_provider(service_provider)

    cap_provider = LMI_BlockStatisticsCapabilities(**opts)
    providers['LMI_BlockStatisticsCapabilities'] = cap_provider

    assoc_provider = ElementCapabilitiesProvider(
            "LMI_BlockStorageStatisticsElementCapabilities",
            cap_provider, service_provider, **opts)
    providers['LMI_BlockStorageStatisticsElementCapabilities'] = assoc_provider

    LOG().trace_info("Registered providers: %s", str(providers))
    return providers

def authorize_filter(env, fltr, ns, classes, owner):
    """ CIMOM callback."""
    IndicationManager.get_instance().authorize_filter(
            env, fltr, ns, classes, owner)

def activate_filter (env, fltr, ns, classes, first_activation):
    """ CIMOM callback."""
    IndicationManager.get_instance().activate_filter(
            env, fltr, ns, classes, first_activation)

def deactivate_filter(env, fltr, ns, classes, last_activation):
    """ CIMOM callback."""
    IndicationManager.get_instance().deactivate_filter(
            env, fltr, ns, classes, last_activation)

def enable_indications(env):
    """ CIMOM callback."""
    IndicationManager.get_instance().enable_indications(env)

def disable_indications(env):
    """ CIMOM callback."""
    IndicationManager.get_instance().disable_indications(env)

def can_unload(_env):
    """ CIMOM callback."""
    LOG().trace_info("can_unload called")
    return job_manager.can_shutdown()

def shutdown(_env):
    """ CIMOM callback."""
    LOG().info("Provider shutdown.")
    # Job manager must be the first, it uses TimerManager and IndicationManager
    job_manager.shutdown()

    timer_manager.shutdown()
    indication_manager.shutdown()
