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
Module for LMI_LUKSBasedOn class.

LMI_LUKSBasedOn
-----------------

.. autoclass:: LMI_LUKSBasedOn
    :members:

"""

from lmi.storage.BasedOnProvider import BasedOnProvider
import pywbem
import lmi.providers.cmpi_logging as cmpi_logging
import blivet

class LMI_LUKSBasedOn(BasedOnProvider):
    """
        Implementation of BasedOn class.
    """
    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_LUKSBasedOn, self).__init__(*args, **kwargs)

    @cmpi_logging.trace_method
    def enumerate_devices(self):
        """
            Enumerate all devices, which are in this association as
            Dependent ones, i.e. all devices, which do not have any
            specialized BasedOn class
        """
        for dev in self.storage.devices:
            if isinstance(dev, blivet.devices.LUKSDevice):
                yield dev
