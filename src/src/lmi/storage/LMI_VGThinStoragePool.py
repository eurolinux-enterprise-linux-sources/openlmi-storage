# Copyright (C) 2012-2014 Red Hat, Inc.  All rights reserved.
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
#          Jan Synacek  <jsynacek@redhat.com>
# -*- coding: utf-8 -*-
"""
Module for LMI_VGThinStoragePool class.

LMI_VGThinStoragePool
-----------------

.. autoclass:: LMI_VGThinStoragePool
    :members:

"""

import pywbem
import blivet
import lmi.providers.cmpi_logging as cmpi_logging
from  lmi.storage.util import storage
from lmi.storage.VGStoragePoolProvider import VGStoragePoolProvider
from lmi.storage.SettingManager import StorageSetting
from lmi.storage.util import units
import math

LOG = cmpi_logging.get_logger(__name__)

class LMI_VGThinStoragePool(VGStoragePoolProvider):
    """
        Provider of LMI_VGThinStoragePool.
    """
    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_VGThinStoragePool, self).__init__(
                classname="LMI_VGThinStoragePool",
                setting_classname='LMI_LVStorageSetting',
                *args, **kwargs)

    @cmpi_logging.trace_method
    def enumerate_devices(self):
        """
            Returns Anaconda StorageDevices managed by this provider.
        """
        return self.storage.vgs

    @cmpi_logging.trace_method
    def provides_device(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        if isinstance(device, blivet.devices.LVMThinPoolDevice):
            return True
        return False

    @cmpi_logging.trace_method
    # pylint: disable-msg=W0221
    def get_instance(self, env, model, device=None):
        """
            Provider implementation of GetInstance intrinsic method.
            It fills all VGStoragePool properties.
        """
        if not self.provides_name(model):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Wrong keys.")
        if not device:
            device = self.get_device_for_name(model)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find the VG.")

        model = super(LMI_VGThinStoragePool, self).get_instance(env, model,
                device)
        model['ElementName'] = device.lvname
        model['TotalManagedSpace'] = pywbem.Uint64(storage.from_blivet_size(device.size))
        # workaround for #1034721
        freespace = storage.from_blivet_size(device.freeSpace)
        if freespace < 0:
            model['RemainingManagedSpace'] = pywbem.Uint64(0)
        else:
            model['RemainingManagedSpace'] = pywbem.Uint64(freespace)
        model['SpaceLimit'] = pywbem.Uint64(storage.from_blivet_size(device.size))
        model['SpaceLimitDetermination'] = self.Values.SpaceLimitDetermination.Limitless
        model['ThinProvisionMetaDataSpace'] = pywbem.Uint64(storage.from_blivet_size(device.metaDataSize))
        return model


    @cmpi_logging.trace_method
    def cim_method_getsupportedsizerange(self, env, object_name,
                                         param_minimumvolumesize=None,
                                         param_maximumvolumesize=None,
                                         param_elementtype=None,
                                         param_volumesizedivisor=None,
                                         param_goal=None):
        """Implements LMI_VGThinStoragePool.GetSupportedSizeRange()
        param_minimumvolumesize --  The input parameter MinimumVolumeSize (type pywbem.Uint64)
            The minimum size for a volume/pool in bytes.

        param_maximumvolumesize --  The input parameter MaximumVolumeSize (type pywbem.Uint64)
            The maximum size for a volume/pool in bytes.

        param_elementtype --  The input parameter ElementType (type pywbem.Uint16 self.Values.GetSupportedSizeRange.ElementType)
            The type of element for which supported size ranges are
            reported. The Thin Provision values are only supported when
            the Thin Provisioning Profile is supported; the resulting
            StorageVolues/LogicalDisk shall have ThinlyProvisioned set to
            true.

        param_volumesizedivisor --  The input parameter VolumeSizeDivisor (type pywbem.Uint64)
            A volume/pool size must be a multiple of this value which is
            specified in bytes.

        param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='CIM_StorageSetting', ...))
            The StorageSetting for which supported size ranges should be
            reported for.

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.GetSupportedSizeRange)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        MinimumVolumeSize -- (type pywbem.Uint64)
            The minimum size for a volume/pool in bytes.

        MaximumVolumeSize -- (type pywbem.Uint64)
            The maximum size for a volume/pool in bytes.

        VolumeSizeDivisor -- (type pywbem.Uint64)
            A volume/pool size must be a multiple of this value which is
            specified in bytes.

        Possible Errors:
        CIM_ERR_ACCESS_DENIED
        CIM_ERR_INVALID_PARAMETER (including missing, duplicate,
            unrecognized or otherwise incorrect parameters)
        CIM_ERR_NOT_FOUND (the target CIM Class or instance does not
            exist in the specified namespace)
        CIM_ERR_METHOD_NOT_AVAILABLE (the CIM Server is unable to honor
            the invocation request)
        CIM_ERR_FAILED (some other unspecified error occurred)

        """
        if not self.provides_name(object_name):
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND, "Wrong keys.")
        device = self.get_device_for_name(object_name)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find the VG.")

        # we support only thin logical volume
        etypes = self.Values.GetSupportedSizeRange.ElementType
        if (param_elementtype
                and param_elementtype != etypes.Thin_Provisioned_Logical_Disk):
            ret = self.Values.GetSupportedSizeRange.Invalid_Element_Type
            return (ret, [])

        # there are no limits on thin LVs
        out_params = []
        out_params += [pywbem.CIMParameter('minimumvolumesize', type='uint64',
                           value=None)]
        out_params += [pywbem.CIMParameter('maximumvolumesize', type='uint64',
                           value=None)]
        out_params += [pywbem.CIMParameter('volumesizedivisor', type='uint64',
                           value=pywbem.Uint64(1))]
        rval = pywbem.Uint32(
            self.Values.GetSupportedSizeRange.Method_completed_OK)
        return (rval, out_params)

    @cmpi_logging.trace_method
    def _get_setting_for_device(self, device, setting_provider):
        """ Return setting for given device """
        _id = storage.get_persistent_name(device)
        setting = self.setting_manager.create_setting(
                self.setting_classname,
                StorageSetting.TYPE_CONFIGURATION,
                setting_provider.create_setting_id(_id),
                class_to_create=StorageSetting)
        setting.set_setting(self.get_redundancy(device))
        setting['ElementName'] = device.path
        setting['SpaceLimit'] = storage.from_blivet_size(device.size)
        setting['ThinProvisionedPoolType'] = \
            self.Values.ThinProvisionedPoolType.ThinlyProvisionedLimitlessStoragePool
        return setting


