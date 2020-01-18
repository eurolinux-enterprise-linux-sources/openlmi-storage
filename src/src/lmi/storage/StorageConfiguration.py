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
# -*- coding: utf-8 -*-
"""
Module for StorageConfiguration class.

StorageConfiguration
--------------------

.. autoclass:: StorageConfiguration
    :members:

"""

import ConfigParser
import socket
from lmi.base.BaseConfiguration import BaseConfiguration
import lmi.providers.cmpi_logging as cmpi_logging

class StorageConfiguration(BaseConfiguration):
    """
        Configuration class specific to storage providers.
        OpenLMI configuration file should reside in
        /etc/openlmi/storage/storage.conf.
    """

    PERSISTENT_PATH = '/var/lib/openlmi-storage/'
    SETTINGS_DIR = 'settings/'

    @classmethod
    def provider_prefix(cls):
        return "storage"

    @classmethod
    def default_options(cls):
        """ :rtype: (``dict``) Dictionary of default values. """
        defaults = BaseConfiguration.default_options().copy()
        defaults['DebugBlivet'] = 'false'
        defaults['TempDir'] = '/tmp'
        return defaults

    @property
    def blivet_tracing(self):
        """ Return True if blivet tracing is enabled."""
        return self.config.getboolean('Log', 'DebugBlivet')

    @property
    def temp_dir(self):
        """ Return path to temporary directory."""
        return self.get_safe('Storage', 'TempDir', fallback='/tmp')
