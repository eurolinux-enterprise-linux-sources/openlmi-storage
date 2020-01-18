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
# -*- coding: utf-8 -*-
"""
Python Provider for LMI_MountPoint

LMI_MountPoint
--------------

.. autoclass:: LMI_MountPoint
    :members:

"""

import pywbem
import blivet
from lmi.storage.MountingProvider import MountingProvider
import lmi.providers.cmpi_logging as cmpi_logging
from lmi.providers.ComputerSystem import get_system_name

class LMI_MountPoint(MountingProvider):
    """Instrument the CIM class LMI_MountPoint

    CIM_Dependency is a generic association used to establish dependency
    relationships between ManagedElements.

    """
    @cmpi_logging.trace_method
    def __init__ (self, *args, **kwargs):
        super(LMI_MountPoint, self).__init__(*args, **kwargs)
        self.classname = 'LMI_MountPoint'

    @cmpi_logging.trace_method
    def get_instance(self, env, model):
        """
            Provider implementation of GetInstance intrinsic method.
        """
        directory = model['Antecedent']
        if (directory['CSCreationClassName'] != self.config.system_class_name or
            directory['CSName'] != get_system_name()):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                                  "Wrong Antecedent keys.")

        spec = model['Dependent']['FileSystemSpec']
        path = model['Dependent']['MountPointPath']

        device = self.storage.devicetree.getDeviceByPath(spec)
        self.check_get_instance(device, spec, path)

        return model

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        """Enumerate instances.
        """
        model.path.update({'Dependent': None, 'Antecedent': None})
        for device in self.storage.devices:
            if isinstance(device, blivet.devices.NoDevice):
                paths = [device.format.mountpoint]
            else:
                paths = blivet.util.get_mount_paths(device.path)

            for path in paths:
                provider = self.provider_manager.get_provider_for_format(device, device.format)
                if provider is None:
                    raise pywbem.CIMError(pywbem.CIM_ERR_FAILED, "Could not get provider for %s" % path)
                fs = provider.get_name_for_format(device, device.format)

                model['Antecedent'] = pywbem.CIMInstanceName(
                    classname='LMI_UnixDirectory',
                    namespace=self.config.namespace,
                    keybindings={
                        'CSCreationClassName': self.config.system_class_name,
                        'CSName' : get_system_name(),
                        'CreationClassName': 'LMI_UnixDirectory',
                        'FSCreationClassName': fs['CreationClassName'],
                        'FSName': fs['Name'],
                        'Name': path
                        })
                model['Dependent'] = pywbem.CIMInstanceName(
                    classname='LMI_MountedFileSystem',
                    namespace=self.config.namespace,
                    keybindings={
                        'FileSystemSpec' : device.path,
                        'MountPointPath' : path
                        })
                yield model

    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        return self.simple_references(env, object_name, model,
                                      result_class_name, role, result_role, keys_only,
                                      "LMI_MountedFileSystem",
                                      "CIM_Directory")
