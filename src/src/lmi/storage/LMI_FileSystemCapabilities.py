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
# Authors: Jan Safranek <jsafrane@redhat.com>
# -*- coding: utf-8 -*-
"""
Module for LMI_FileSystemCapabilities class.

LMI_FileSystemCapabilities
---------------------------------------

.. autoclass:: LMI_FileSystemCapabilities
    :members:

"""

from lmi.storage.CapabilitiesProvider import CapabilitiesProvider
import pywbem
import lmi.providers.cmpi_logging as cmpi_logging

class LMI_FileSystemCapabilities(CapabilitiesProvider):
    """
        LMI_FileSystemCapabilities provider implementation.
    """

    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_FileSystemCapabilities, self).__init__(
                "LMI_FileSystemCapabilities", *args, **kwargs)

        vals = self.Values
        self.instances = [
            {
                'InstanceID': 'LMI:LMI_FileSystemCapabilities:ext2',
                'ActualFileSystemType':
                    vals.ActualFileSystemType.EXT2,
                'SupportedPersistenceTypes':
                    [ vals.SupportedPersistenceTypes.Persistent ],
                'SupportedProperties':
                    [
                            vals.SupportedProperties.DataExtentsSharing,
                            vals.SupportedProperties.FilenameCaseAttributes,
                            vals.SupportedProperties.FilenameFormats,
                            vals.SupportedProperties.Persistence,
                    ],
            },
            {
                'InstanceID': 'LMI:LMI_FileSystemCapabilities:ext3',
                'ActualFileSystemType':
                    vals.ActualFileSystemType.EXT3,
                'SupportedPersistenceTypes':
                    [ vals.SupportedPersistenceTypes.Persistent ],
                'SupportedProperties':
                    [
                            vals.SupportedProperties.DataExtentsSharing,
                            vals.SupportedProperties.FilenameCaseAttributes,
                            vals.SupportedProperties.FilenameFormats,
                            vals.SupportedProperties.Persistence,
                    ],
            },
            {
                'InstanceID': 'LMI:LMI_FileSystemCapabilities:ext4',
                'ActualFileSystemType':
                    vals.ActualFileSystemType.EXT4,
                'SupportedPersistenceTypes':
                    [ vals.SupportedPersistenceTypes.Persistent ],
                'SupportedProperties':
                    [
                            vals.SupportedProperties.DataExtentsSharing,
                            vals.SupportedProperties.FilenameCaseAttributes,
                            vals.SupportedProperties.FilenameFormats,
                            vals.SupportedProperties.Persistence,
                    ],
            },
            {
                'InstanceID': 'LMI:LMI_FileSystemCapabilities:btrfs',
                'ActualFileSystemType':
                    vals.ActualFileSystemType.BTRFS,
                'SupportedPersistenceTypes':
                    [ vals.SupportedPersistenceTypes.Persistent ],
                'SupportedProperties':
                    [
                            vals.SupportedProperties.DataExtentsSharing,
                            vals.SupportedProperties.FilenameCaseAttributes,
                            vals.SupportedProperties.FilenameFormats,
                            vals.SupportedProperties.Persistence,
                    ],
            },
            {
                'InstanceID': 'LMI:LMI_FileSystemCapabilities:xfs',
                'ActualFileSystemType':
                    vals.ActualFileSystemType.XFS,
                'SupportedPersistenceTypes':
                    [ vals.SupportedPersistenceTypes.Persistent ],
                'SupportedProperties':
                    [
                            vals.SupportedProperties.DataExtentsSharing,
                            vals.SupportedProperties.FilenameCaseAttributes,
                            vals.SupportedProperties.FilenameFormats,
                            vals.SupportedProperties.Persistence,
                    ],
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
    def create_setting_for_capabilities(self, capabilities):
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                "Application-specific FileSystemSetting is not yet supported.")

    class Values(CapabilitiesProvider.Values):
        class ActualFileSystemType(object):
            Unknown = pywbem.Uint16(0)
            UFS = pywbem.Uint16(2)
            HFS = pywbem.Uint16(3)
            FAT = pywbem.Uint16(4)
            FAT16 = pywbem.Uint16(5)
            FAT32 = pywbem.Uint16(6)
            NTFS4 = pywbem.Uint16(7)
            NTFS5 = pywbem.Uint16(8)
            XFS = pywbem.Uint16(9)
            AFS = pywbem.Uint16(10)
            EXT2 = pywbem.Uint16(11)
            EXT3 = pywbem.Uint16(12)
            REISERFS = pywbem.Uint16(13)
            # DMTF_Reserved = ..
            EXT4 = pywbem.Uint16(32769)
            BTRFS = pywbem.Uint16(32770)
            JFS = pywbem.Uint16(32771)
            TMPFS = pywbem.Uint16(32772)
            VFAT = pywbem.Uint16(32773)

        class SupportedPersistenceTypes(object):
            Other = pywbem.Uint16(1)
            Persistent = pywbem.Uint16(2)
            Temporary = pywbem.Uint16(3)
            External = pywbem.Uint16(4)

        class SupportedProperties(object):
            DataExtentsSharing = pywbem.Uint16(2)
            CopyTarget = pywbem.Uint16(3)
            FilenameCaseAttributes = pywbem.Uint16(4)
            FilenameStreamFormats = pywbem.Uint16(5)
            FilenameFormats = pywbem.Uint16(6)
            LockingSemantics = pywbem.Uint16(7)
            AuthorizationProtocols = pywbem.Uint16(8)
            AuthenticationProtocols = pywbem.Uint16(9)
            Persistence = pywbem.Uint16(10)
            # DMTF_Reserved = ..
            # Vendor_Defined = 0x8000..
