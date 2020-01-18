# Copyright (C) 2014 Red Hat, Inc.  All rights reserved.
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
Module for LMI_MediaPresent class.

LMI_MediaPresent
---------------------------

.. autoclass:: LMI_MediaPresent
    :members:

"""

import blivet.formats
from lmi.providers.ComputerSystem import get_system_name
from lmi.storage.BaseProvider import BaseProvider
import pywbem
import lmi.providers.cmpi_logging as cmpi_logging

class LMI_MediaPresent(BaseProvider):
    """
        LMI_MediaPresent provider implementation.
    """

    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_MediaPresent, self).__init__(*args, **kwargs)

    @cmpi_logging.trace_method
    def get_drive_name(self, device):
        """
        Returns CIMInstanceName for given blivet device.
        """
        return pywbem.CIMInstanceName(
            classname='LMI_DiskDrive',
            namespace=self.config.namespace,
            keybindings={
                'CreationClassName' : "LMI_DiskDrive",
                'DeviceID' : device.path,
                'SystemName' : get_system_name(),
                'SystemCreationClassName' : self.config.system_class_name,
        })

    @cmpi_logging.trace_method
    def get_instance(self, env, model):
        """
            Provider implementation of GetInstance intrinsic method.
        """
        device = self.provider_manager.get_device_for_name(model['Dependent'])
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find Dependent extent.")

        name = self.get_drive_name(device)
        if name != model['Antecedent']:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Antecedent is not associated with Dependent instance.")

        return model

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        """
            Provider implementation of EnumerateInstances intrinsic method.
        """
        model.path.update({'Dependent': None, 'Antecedent': None})

        for device in self.storage.disks:
            if device.type != 'disk':
                continue
            model['Antecedent'] = self.get_drive_name(device)
            model['Dependent'] = self.provider_manager.get_name_for_device(
                    device)
            yield model


    @cmpi_logging.trace_method
    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        """Instrument Associations."""
        return self.simple_references(env, object_name, model,
                result_class_name, role, result_role, keys_only,
                "CIM_StorageExtent",
                "CIM_MediaAccessDevice")
