Inheritance tree
================

.. |nbsp| unicode:: 0xA0
    :trim:

| \* :ref:`CIM_AbstractComponent <CIM-AbstractComponent>`
|    \|--- \* :ref:`CIM_Component <CIM-Component>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_AssociatedComponentExtent <CIM-AssociatedComponentExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_VGAssociatedComponentExtent <LMI-VGAssociatedComponentExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_SystemComponent <CIM-SystemComponent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_HostedFileSystem <CIM-HostedFileSystem>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_HostedFileSystem <LMI-HostedFileSystem>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_SystemDevice <CIM-SystemDevice>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_SystemStorageDevice <LMI-SystemStorageDevice>`
| \* :ref:`CIM_AbstractElementStatisticalData <CIM-AbstractElementStatisticalData>`
|    \|--- \* :ref:`CIM_ElementStatisticalData <CIM-ElementStatisticalData>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_StorageElementStatisticalData <LMI-StorageElementStatisticalData>`
| \* :ref:`CIM_AffectedJobElement <CIM-AffectedJobElement>`
|    \|--- \* :ref:`LMI_AffectedJobElement <LMI-AffectedJobElement>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_AffectedStorageJobElement <LMI-AffectedStorageJobElement>`
| \* :ref:`CIM_AssociatedBlockStatisticsManifestCollection <CIM-AssociatedBlockStatisticsManifestCollection>`
|    \|--- \* :ref:`LMI_AssociatedBlockStatisticsManifestCollection <LMI-AssociatedBlockStatisticsManifestCollection>`
| \* :ref:`CIM_AssociatedJobMethodResult <CIM-AssociatedJobMethodResult>`
|    \|--- \* :ref:`LMI_AssociatedJobMethodResult <LMI-AssociatedJobMethodResult>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_AssociatedStorageJobMethodResult <LMI-AssociatedStorageJobMethodResult>`
| \* :ref:`CIM_Dependency <CIM-Dependency>`
|    \|--- \* :ref:`CIM_AbstractBasedOn <CIM-AbstractBasedOn>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_BasedOn <CIM-BasedOn>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MDRAIDBasedOn <LMI-MDRAIDBasedOn>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_PartitionBasedOn <LMI-PartitionBasedOn>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LVBasedOn <LMI-LVBasedOn>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LUKSBasedOn <LMI-LUKSBasedOn>`
|    \|--- \* :ref:`CIM_SettingAssociatedToCapabilities <CIM-SettingAssociatedToCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LUKSSettingAssociatedToCapabilities <LMI-LUKSSettingAssociatedToCapabilities>`
|    \|--- \* :ref:`LMI_MountPoint <LMI-MountPoint>`
|    \|--- \* :ref:`CIM_AbstractElementAllocatedFromPool <CIM-AbstractElementAllocatedFromPool>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_ElementAllocatedFromPool <CIM-ElementAllocatedFromPool>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_AllocatedFromStoragePool <CIM-AllocatedFromStoragePool>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LVAllocatedFromStoragePool <LMI-LVAllocatedFromStoragePool>`
|    \|--- \* :ref:`LMI_AttachedFileSystem <LMI-AttachedFileSystem>`
|    \|--- \* :ref:`LMI_HostedMount <LMI-HostedMount>`
|    \|--- \* :ref:`CIM_ResidesOnExtent <CIM-ResidesOnExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_ResidesOnExtent <LMI-ResidesOnExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MDRAIDFormatResidesOnExtent <LMI-MDRAIDFormatResidesOnExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_PVFormatResidesOnExtent <LMI-PVFormatResidesOnExtent>`
|    \|--- \* :ref:`CIM_HostedDependency <CIM-HostedDependency>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_HostedService <CIM-HostedService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_HostedStorageService <LMI-HostedStorageService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_HostedCollection <CIM-HostedCollection>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_HostedStorageStatisticsCollection <LMI-HostedStorageStatisticsCollection>`
|    \|--- \* :ref:`CIM_InstalledPartitionTable <CIM-InstalledPartitionTable>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_InstalledPartitionTable <LMI-InstalledPartitionTable>`
| \* :ref:`CIM_ElementCapabilities <CIM-ElementCapabilities>`
|    \|--- \* :ref:`LMI_BlockStorageStatisticsElementCapabilities <LMI-BlockStorageStatisticsElementCapabilities>`
|    \|--- \* :ref:`LMI_MDRAIDElementCapabilities <LMI-MDRAIDElementCapabilities>`
|    \|--- \* :ref:`LMI_EncryptionElementCapabilities <LMI-EncryptionElementCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LUKSElementCapabilities <LMI-LUKSElementCapabilities>`
|    \|--- \* :ref:`LMI_LVElementCapabilities <LMI-LVElementCapabilities>`
|    \|--- \* :ref:`LMI_MountElementCapabilities <LMI-MountElementCapabilities>`
|    \|--- \* :ref:`LMI_VGElementCapabilities <LMI-VGElementCapabilities>`
|    \|--- \* :ref:`LMI_DiskPartitionElementCapabilities <LMI-DiskPartitionElementCapabilities>`
|    \|--- \* :ref:`LMI_FileSystemConfigurationElementCapabilities <LMI-FileSystemConfigurationElementCapabilities>`
| \* :ref:`CIM_ElementSettingData <CIM-ElementSettingData>`
|    \|--- \* :ref:`LMI_FileSystemElementSettingData <LMI-FileSystemElementSettingData>`
|    \|--- \* :ref:`LMI_MDRAIDElementSettingData <LMI-MDRAIDElementSettingData>`
|    \|--- \* :ref:`LMI_EncryptionElementSettingData <LMI-EncryptionElementSettingData>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LUKSElementSettingData <LMI-LUKSElementSettingData>`
|    \|--- \* :ref:`LMI_LVElementSettingData <LMI-LVElementSettingData>`
|    \|--- \* :ref:`LMI_DiskPartitionElementSettingData <LMI-DiskPartitionElementSettingData>`
|    \|--- \* :ref:`LMI_VGElementSettingData <LMI-VGElementSettingData>`
|    \|--- \* :ref:`LMI_MountedFileSystemElementSettingData <LMI-MountedFileSystemElementSettingData>`
| \* :ref:`CIM_Indication <CIM-Indication>`
|    \|--- \* :ref:`CIM_InstIndication <CIM-InstIndication>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_InstModification <CIM-InstModification>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_StorageInstModification <LMI-StorageInstModification>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_InstCreation <CIM-InstCreation>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_StorageInstCreation <LMI-StorageInstCreation>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_InstMethodCall <CIM-InstMethodCall>`
| \* :ref:`CIM_ManagedElement <CIM-ManagedElement>`
|    \|--- \* :ref:`LMI_MountedFileSystem <LMI-MountedFileSystem>`
|    \|--- \* :ref:`CIM_MethodResult <CIM-MethodResult>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MethodResult <LMI-MethodResult>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_StorageMethodResult <LMI-StorageMethodResult>`
|    \|--- \* :ref:`CIM_Capabilities <CIM-Capabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_EncryptionFormatCapabilities <LMI-EncryptionFormatCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LUKSFormatCapabilities <LMI-LUKSFormatCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_FileSystemCapabilities <CIM-FileSystemCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_FileSystemCapabilities <LMI-FileSystemCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_FileSystemConfigurationCapabilities <CIM-FileSystemConfigurationCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_FileSystemConfigurationCapabilities <LMI-FileSystemConfigurationCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_StatisticsCapabilities <CIM-StatisticsCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_BlockStatisticsCapabilities <CIM-BlockStatisticsCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_BlockStatisticsCapabilities <LMI-BlockStatisticsCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MountedFileSystemCapabilities <LMI-MountedFileSystemCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_StorageCapabilities <CIM-StorageCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_VGStorageCapabilities <LMI-VGStorageCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LVStorageCapabilities <LMI-LVStorageCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MDRAIDStorageCapabilities <LMI-MDRAIDStorageCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_DiskPartitionConfigurationCapabilities <CIM-DiskPartitionConfigurationCapabilities>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_DiskPartitionConfigurationCapabilities <LMI-DiskPartitionConfigurationCapabilities>`
|    \|--- \* :ref:`CIM_ManagedSystemElement <CIM-ManagedSystemElement>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_LogicalElement <CIM-LogicalElement>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_LogicalFile <CIM-LogicalFile>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_Directory <CIM-Directory>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_EnabledLogicalElement <CIM-EnabledLogicalElement>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_DataFormat <LMI-DataFormat>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_PVFormat <LMI-PVFormat>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_EncryptionFormat <LMI-EncryptionFormat>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LUKSFormat <LMI-LUKSFormat>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MDRAIDFormat <LMI-MDRAIDFormat>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_LogicalDevice <CIM-LogicalDevice>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_StorageExtent <CIM-StorageExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_LogicalDisk <CIM-LogicalDisk>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_MediaPartition <CIM-MediaPartition>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_GenericDiskPartition <CIM-GenericDiskPartition>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_DiskPartition <CIM-DiskPartition>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_DiskPartition <LMI-DiskPartition>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_VTOCDiskPartition <CIM-VTOCDiskPartition>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_GPTDiskPartition <CIM-GPTDiskPartition>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_GenericDiskPartition <LMI-GenericDiskPartition>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_StorageExtent <LMI-StorageExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LVStorageExtent <LMI-LVStorageExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_EncryptionExtent <LMI-EncryptionExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LUKSStorageExtent <LMI-LUKSStorageExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MDRAIDStorageExtent <LMI-MDRAIDStorageExtent>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_FileSystem <CIM-FileSystem>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_LocalFileSystem <CIM-LocalFileSystem>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LocalFileSystem <LMI-LocalFileSystem>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_TransientFileSystem <LMI-TransientFileSystem>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_Service <CIM-Service>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_StorageConfigurationService <CIM-StorageConfigurationService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_StorageConfigurationService <LMI-StorageConfigurationService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_DiskPartitionConfigurationService <CIM-DiskPartitionConfigurationService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_DiskPartitionConfigurationService <LMI-DiskPartitionConfigurationService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_FileSystemConfigurationService <CIM-FileSystemConfigurationService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_FileSystemConfigurationService <LMI-FileSystemConfigurationService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_ExtentEncryptionConfigurationService <LMI-ExtentEncryptionConfigurationService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_StatisticsService <CIM-StatisticsService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_BlockStatisticsService <CIM-BlockStatisticsService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_BlockStatisticsService <LMI-BlockStatisticsService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MountConfigurationService <LMI-MountConfigurationService>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_ResourcePool <CIM-ResourcePool>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_StoragePool <CIM-StoragePool>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_VGStoragePool <LMI-VGStoragePool>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_Job <CIM-Job>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_ConcreteJob <CIM-ConcreteJob>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_ConcreteJob <LMI-ConcreteJob>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_StorageJob <LMI-StorageJob>`
|    \|--- \* :ref:`CIM_Collection <CIM-Collection>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_SystemSpecificCollection <CIM-SystemSpecificCollection>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_BlockStatisticsManifestCollection <CIM-BlockStatisticsManifestCollection>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_BlockStatisticsManifestCollection <LMI-BlockStatisticsManifestCollection>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_StatisticsCollection <CIM-StatisticsCollection>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_StorageStatisticsCollection <LMI-StorageStatisticsCollection>`
|    \|--- \* :ref:`CIM_StatisticalData <CIM-StatisticalData>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_BlockStorageStatisticalData <CIM-BlockStorageStatisticalData>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_BlockStorageStatisticalData <LMI-BlockStorageStatisticalData>`
|    \|--- \* :ref:`CIM_SettingData <CIM-SettingData>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_FileSystemSetting <CIM-FileSystemSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_FileSystemSetting <LMI-FileSystemSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_DiskPartitionConfigurationSetting <LMI-DiskPartitionConfigurationSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_EncryptionFormatSetting <LMI-EncryptionFormatSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LUKSFormatSetting <LMI-LUKSFormatSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MountedFileSystemSetting <LMI-MountedFileSystemSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`CIM_StorageSetting <CIM-StorageSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_StorageSetting <LMI-StorageSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_VGStorageSetting <LMI-VGStorageSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_MDRAIDStorageSetting <LMI-MDRAIDStorageSetting>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_LVStorageSetting <LMI-LVStorageSetting>`
|    \|--- \* :ref:`CIM_BlockStatisticsManifest <CIM-BlockStatisticsManifest>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_BlockStatisticsManifest <LMI-BlockStatisticsManifest>`
| \* :ref:`CIM_MemberOfCollection <CIM-MemberOfCollection>`
|    \|--- \* :ref:`LMI_MemberOfStorageStatisticsCollection <LMI-MemberOfStorageStatisticsCollection>`
|    \|--- \* :ref:`LMI_MemberOfBlockStatisticsManifestCollection <LMI-MemberOfBlockStatisticsManifestCollection>`
| \* :ref:`CIM_OwningJobElement <CIM-OwningJobElement>`
|    \|--- \* :ref:`LMI_OwningJobElement <LMI-OwningJobElement>`
|    \| |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp|  |nbsp| \|--- \* :ref:`LMI_OwningStorageJobElement <LMI-OwningStorageJobElement>`
