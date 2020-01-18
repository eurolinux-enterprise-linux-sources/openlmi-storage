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

import blivet.devices
from lmi.storage.ExtentProvider import ExtentProvider
import lmi.providers.cmpi_logging as cmpi_logging

class LMI_LUKSStorageExtent(ExtentProvider):
    """
        Provider of LMI_LUKSStorageExtent class.
    """

    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_LUKSStorageExtent, self).__init__(
            classname='LMI_LUKSStorageExtent',
            *args, **kwargs)

    @cmpi_logging.trace_method
    def provides_device(self, device):
        """
            Returns True, if this class is provider for given Anaconda
            StorageDevice class.
        """
        if  isinstance(device, blivet.devices.LUKSDevice):
            return device.status
        return False

    @cmpi_logging.trace_method
    def enumerate_devices(self):
        """
            Enumerate all StorageDevices, that this provider provides.
        """
        for device in self.storage.devicetree.getDevicesByInstance(blivet.devices.LUKSDevice):
            if device.status:
                yield device

