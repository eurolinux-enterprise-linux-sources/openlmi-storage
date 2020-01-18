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
"""
Python Provider for LMI_LUKSFormat

LMI_LUKSFormat
---------------------

.. autoclass:: LMI_LUKSFormat
    :members:

"""

import pywbem
import blivet.formats.luks
from lmi.storage.FormatProvider import FormatProvider
from lmi.storage.util import storage
import lmi.providers.cmpi_logging as cmpi_logging

class LMI_LUKSFormat(FormatProvider):
    """Instrument the CIM class LMI_LUKSFormat

    Class representing LUKS data.

    """

    @cmpi_logging.trace_method
    def __init__ (self, *args, **kwargs):
        super(LMI_LUKSFormat, self).__init__(
            "LMI_LUKSFormat",
            "luks",
            *args, **kwargs)

    @cmpi_logging.trace_method
    def provides_format(self, device, fmt):
        if  isinstance(fmt, blivet.formats.luks.LUKS):
            return True
        return False

    # XXX temporary, remove when blivet can do that
    @cmpi_logging.trace_method
    def _get_luks_key_slot_statuses(self, path):
        import subprocess
        import re
        out = subprocess.check_output(['cryptsetup', 'luksDump', path])
        return map(lambda s: s == 'ENABLED', re.findall('Key Slot \d:\s*(\w+)', out))

    @cmpi_logging.trace_method
    def get_instance(self, env, model, fmt=None):
        model = super(LMI_LUKSFormat, self).get_instance(
                env, model, fmt)
        if not fmt:
            (device, fmt) = self.get_format_for_id(model['Name'])

        model['InstanceID'] = 'luks:' + fmt.device
        if fmt.uuid:
            model['UUID'] = fmt.uuid
        statuses = self._get_luks_key_slot_statuses(fmt.device)
        model['SlotStatus'] = pywbem.CIMProperty(name='SlotStatus',
                                                 value=statuses,
                                                 type='uint16',
                                                 array_size=len(statuses),
                                                 is_array=True)

        return model
