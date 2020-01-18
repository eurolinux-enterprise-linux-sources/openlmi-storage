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
# Authors: Jan Synacek  <jsynacek@redhat.com>
# -*- coding: utf-8 -*-
"""
Module for LMI_VGAllocatedFromStoragePool class.

LMI_VGAllocatedFromStoragePool
------------------------------

.. autoclass:: LMI_VGAllocatedFromStoragePool
    :members:

"""

from lmi.storage.BaseProvider import BaseProvider
import pywbem
import lmi.providers.cmpi_logging as cmpi_logging

class LMI_VGAllocatedFromStoragePool(BaseProvider):
    """
        Implementation of LMI_VGAllocatedFromStoragePool class.
    """
    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_VGAllocatedFromStoragePool, self).__init__(*args, **kwargs)

    @cmpi_logging.trace_method
    def _get_provider_for_device(self, device):
        if device is None:
            path = "None"
        else:
            path = device.path
        provider = self.provider_manager.get_provider_for_device(device)
        if provider is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Cannot find provider for device " + path)
        return provider

    @cmpi_logging.trace_method
    def enum_instances(self, env, model, keys_only):
        model.path.update({'Dependent': None, 'Antecedent': None})

        for vg in self.storage.vgs:
            vgprovider = self._get_provider_for_device(vg)

            for tp in vg.thinpools:
                tpprovider = self._get_provider_for_device(tp)

                model['Antecedent'] = vgprovider.get_name_for_device(vg)
                model['Dependent']  = tpprovider.get_name_for_device(tp)

                yield model

    @cmpi_logging.trace_method
    def references(self, env, object_name, model, result_class_name, role,
                   result_role, keys_only):
        """Instrument Associations."""
        return self.simple_references(env, object_name, model,
                result_class_name, role, result_role, keys_only,
                "CIM_StoragePool",
                "CIM_StoragePool")
