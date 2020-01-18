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
Python Provider for LMI_ExtentEncryptionConfigurationService

Instruments the CIM class LMI_ExtentEncryptionConfigurationService
"""

import pywbem
import blivet.devicelibs.crypto as crypto
import blivet.formats.luks
import blivet.devices
from blivet.errors import CryptoError
from lmi.storage.ServiceProvider import ServiceProvider
from lmi.storage.util.storage import *
from lmi.providers.JobManager import Job
import lmi.storage.util
import lmi.providers.cmpi_logging as cmpi_logging

class LMI_ExtentEncryptionConfigurationService(ServiceProvider):
    """Instrument the CIM class LMI_ExtentEncryptionConfigurationService

    A Service is a LogicalElement that represents the availability of
    functionality that can be managed. This functionality may be provided
    by a seperately modeled entity such as a LogicalDevice or a
    SoftwareFeature, or both. The modeled Service typically provides only
    functionality required for management of itself or the elements it
    affects.

    """

    @cmpi_logging.trace_method
    def __init__ (self, *args, **kwargs):
        super(LMI_ExtentEncryptionConfigurationService, self).__init__(
            classname="LMI_ExtentEncryptionConfigurationService",
            *args, **kwargs)

    @cmpi_logging.trace_method
    def cim_method_createencryptionformat(self, env, object_name,
                                          param_goal=None,
                                          param_inextent=None,
                                          param_passphrase=None):
        """Implements LMI_ExtentEncryptionConfigurationService.CreateEncryptionFormat()

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName
            specifying the object on which the method CreateEncryptionFormat()
            should be invoked.
        param_goal --  The input parameter Goal (type REF (pywbem.CIMInstanceName(classname='LMI_EncryptionFormatSetting', ...))
        param_inextent --  The input parameter InExtent (type REF (pywbem.CIMInstanceName(classname='CIM_StorageExtent', ...))
        param_passphrase --  The input parameter Passphrase (type unicode)

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))
        Format -- (type REF (pywbem.CIMInstanceName(classname='LMI_EncryptionFormat', ...))

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
        args = {'InExtent':param_inextent,
                'Passphrase':param_passphrase}
        check_empty_parameters(**args)

        device = self.provider_manager.get_device_for_name(param_inextent)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Can't find any device for %s." % param_inextent['DeviceID'])

        # remember input parameters for job
        input_arguments = {
            'Goal' : pywbem.CIMProperty(name='Goal',
                                        type='reference',
                                        value=param_goal),
            'InExtent' : pywbem.CIMProperty(name='InExtent',
                                            type='reference',
                                            value=param_inextent),
            'Passphrase' : pywbem.CIMProperty(name='Passphrase',
                                              type='string',
                                              value=param_passphrase)}

        # create Job
        job = Job(job_manager=self.job_manager,
                  job_name="LUKS FORMAT %s" % device.path,
                  input_arguments=input_arguments,
                  method_name="CreateEncryptionFormat",
                  affected_elements=[param_inextent],
                  owning_element=self._get_instance_name())
        job.set_execute_action(self._create_encryption_format, job,
                               param_inextent, param_passphrase)
        self.job_manager.add_job(job)

        rval = self.EncryptionFormatMethods.Method_Parameters_Checked___Job_Started
        outparams = [(pywbem.CIMParameter(
                name='Job',
                type='reference',
                value=job.get_name()))]
        return (rval, outparams)

    @cmpi_logging.trace_method
    def _create_encryption_format(self, job, devicename, passphrase):
        """
        Really create encryption format. All checks have been done.
        """
        device = self.provider_manager.get_device_for_name(devicename)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Device disappeared: " + devicename['DeviceID'])

        rval = self.EncryptionFormatMethods.Job_Completed_with_No_Error
        state = Job.STATE_FINISHED_OK
        err = None

        # destroy previous format
        destroyAction = blivet.ActionDestroyFormat(device)
        fmt = blivet.formats.luks.LUKS(device=device.path, passphrase=passphrase, mapName=None)
        action = blivet.ActionCreateFormat(device, fmt)
        lmi.storage.util.storage.do_storage_action(self.storage, [destroyAction, action])

        new_device = getRealDeviceByPath(self.storage, device.path)
        if not new_device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Cannot locate new format, was it removed?")
        # XXX after blivet.reset(), the device gets opened by blivet. see BUG #996118

        efname = self.provider_manager.get_name_for_format(new_device, new_device.format)
        outparams = {'Format' : efname}
        job.finish_method(
            state,
            return_value=rval,
            return_type=Job.ReturnValueType.Uint32,
            output_arguments=outparams,
            affected_elements=[efname],
            error=err)

    @cmpi_logging.trace_method
    def cim_method_openencryptionformat(self, env, object_name,
                                        param_elementname=None,
                                        param_passphrase=None,
                                        param_format=None):
        """Implements LMI_ExtentEncryptionConfigurationService.OpenEncryptionFormat()

        Opens a LUKS device. This usually means an entry accessible through
        the device mapper.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName
            specifying the object on which the method OpenEncryptionFormat()
            should be invoked.
        param_elementname --  The input parameter ElementName (type unicode)
        param_passphrase --  The input parameter Passphrase (type unicode)
        param_format --  The input parameter Format (type REF (pywbem.CIMInstanceName(classname='LMI_EncryptionFormat', ...))

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.OpenEncryptionFormat)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))
        Extent -- (type REF (pywbem.CIMInstanceName(classname='CIM_StorageExtent', ...))

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
        args = {'Format':param_format,
                'Passphrase':param_passphrase,
                'ElementName':param_elementname}
        check_empty_parameters(**args)

        provider = self.provider_manager.get_provider_for_format_name(param_format)
        (device, _) = provider.get_format_for_name(param_format)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Can't find any device for %s." % param_format['Name'])

        # remember input parameters for job
        input_arguments = {
            'ElementName' : pywbem.CIMProperty(name='ElementName',
                                               type='string',
                                               value=param_elementname),
            'Format' : pywbem.CIMProperty(name='Format',
                                            type='reference',
                                            value=param_format),
            'Passphrase' : pywbem.CIMProperty(name='Passphrase',
                                              type='string',
                                              value=param_passphrase)}

        # create Job
        job = Job(job_manager=self.job_manager,
                  job_name="LUKS OPEN %s" % device.path,
                  input_arguments=input_arguments,
                  method_name="OpenEncryptionFormat",
                  affected_elements=[param_format],
                  owning_element=self._get_instance_name())
        job.set_execute_action(self._open_encryption_format, job,
                               param_format, param_elementname, param_passphrase)
        self.job_manager.add_job(job)

        rval = self.EncryptionFormatMethods.Method_Parameters_Checked___Job_Started
        outparams = [(pywbem.CIMParameter(
                name='Job',
                type='reference',
                value=job.get_name()))]
        return (rval, outparams)


    @cmpi_logging.trace_method
    def _open_encryption_format(self, job, formatname, elementname, passphrase):
        """
        Really open encryption format. All checks have been done.
        """
        provider = self.provider_manager.get_provider_for_format_name(formatname)
        (device, fmt) = provider.get_format_for_name(formatname)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Device disappeared: " + formatname['Name'])
        if not fmt or not isinstance(fmt, blivet.formats.luks.LUKS):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "LUKS format disappeared from device: " + formatname['Name'])

        children = self.storage.devicetree.getChildren(device)
        if children:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "LUKS is already opened as %s" % (children[0]))

        rval = self.EncryptionFormatMethods.Job_Completed_with_No_Error
        state = Job.STATE_FINISHED_OK
        err = None

        device.format.mapName = elementname
        device.format.passphrase = passphrase
        luksdevice = blivet.devices.LUKSDevice(elementname,
                                               device.format,
                                               size=device.size,
                                               uuid=device.format.uuid,
                                               sysfsPath=device.sysfsPath,
                                               parents=[device],
                                               exists=False)
        # See BUG #996457.
        luksdevice.format.device = device.path
        action = blivet.ActionCreateDevice(luksdevice)
        lmi.storage.util.storage.do_storage_action(self.storage, [action])

        new_device = getRealDeviceByPath(self.storage, luksdevice.path)
        if not new_device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Cannot locate new format, was it removed?")

        extent = self.provider_manager.get_name_for_device(new_device)
        outparams = {'Extent' : extent}
        job.finish_method(
            state,
            return_value=rval,
            return_type=Job.ReturnValueType.Uint32,
            output_arguments=outparams,
            affected_elements=[extent],
            error=err)

    @cmpi_logging.trace_method
    def cim_method_closeencryptionformat(self, env, object_name,
                                         param_format=None):
        """Implements LMI_ExtentEncryptionConfigurationService.CloseEncryptionFormat()

        Closes a LUKS device.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName
            specifying the object on which the method CloseEncryptionFormat()
            should be invoked.
        param_format --  The input parameter Format (type REF (pywbem.CIMInstanceName(classname='LMI_EncryptionFormat', ...))

        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.CloseEncryptionFormat)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))

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
        args = {'Format':param_format}
        check_empty_parameters(**args)

        provider = self.provider_manager.get_provider_for_format_name(param_format)
        (device, _) = provider.get_format_for_name(param_format)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Can't find any device for %s." % param_format['Name'])

        # remember input parameters for job
        input_arguments = {'Format' : pywbem.CIMProperty(name='Format',
                                                         type='reference',
                                                         value=param_format)}

        # create Job
        job = Job(job_manager=self.job_manager,
                  job_name="LUKS CLOSE %s" % device.path,
                  input_arguments=input_arguments,
                  method_name="CloseEncryptionFormat",
                  affected_elements=[param_format],
                  owning_element=self._get_instance_name())
        job.set_execute_action(self._close_encryption_format, job, param_format)
        self.job_manager.add_job(job)

        rval = self.EncryptionFormatMethods.Method_Parameters_Checked___Job_Started
        outparams = [(pywbem.CIMParameter(
                name='Job',
                type='reference',
                value=job.get_name()))]
        return (rval, outparams)

    @cmpi_logging.trace_method
    def _close_encryption_format(self, job, formatname):
        """
        Really close encryption format. All checks have been done.
        """
        provider = self.provider_manager.get_provider_for_format_name(formatname)
        (device, fmt) = provider.get_format_for_name(formatname)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Device disappeared: " + formatname['Name'])
        if not fmt or not isinstance(fmt, blivet.formats.luks.LUKS):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "LUKS format disappeared from device: " + formatname['Name'])
        children = self.storage.devicetree.getChildren(device)
        if not children:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "No LUKS device opened: " + formatname['Name'])

        rval = self.EncryptionFormatMethods.Job_Completed_with_No_Error
        state = Job.STATE_FINISHED_OK
        err = None

        luksdevice = children[0]
        action = blivet.ActionDestroyDevice(luksdevice)
        lmi.storage.util.storage.do_storage_action(self.storage, [action])

        job.finish_method(
            state,
            return_value=rval,
            return_type=Job.ReturnValueType.Uint32,
            output_arguments={},
            affected_elements=[],
            error=err)

    @cmpi_logging.trace_method
    def cim_method_addpassphrase(self, env, object_name,
                                 param_newpassphrase=None,
                                 param_passphrase=None,
                                 param_format=None):
        """Implements LMI_ExtentEncryptionConfigurationService.AddPassphrase()

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName
            specifying the object on which the method AddPassphrase()
            should be invoked.
        param_newpassphrase --  The input parameter NewPassphrase (type unicode)
        param_passphrase --  The input parameter Passphrase (type unicode)
        param_format --  The input parameter Format (type REF (pywbem.CIMInstanceName(classname='LMI_EncryptionFormat', ...))
        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

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
        args = {'Format':param_format,
                'Passphrase':param_passphrase,
                'NewPassphrase':param_newpassphrase}
        check_empty_parameters(**args)

        provider = self.provider_manager.get_provider_for_format_name(param_format)
        if not provider:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find given Format.")

        (device, fmt) = provider.get_format_for_name(param_format)
        if not fmt:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find given Format.")

        try:
            crypto.luks_add_key(device.path, param_newpassphrase, param_passphrase)
        except CryptoError:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Can't add key to LUKS.")

        return (pywbem.Uint32(0), [])

    @cmpi_logging.trace_method
    def cim_method_deletepassphrase(self, env, object_name,
                                    param_passphrase=None,
                                    param_format=None):
        """Implements LMI_ExtentEncryptionConfigurationService.DeletePassphrase()

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName
            specifying the object on which the method DeletePassphrase()
            should be invoked.
        param_passphrase --  The input parameter Passphrase (type unicode)
        param_format --  The input parameter Format (type REF (pywbem.CIMInstanceName(classname='LMI_EncryptionFormat', ...))

        Returns a two-tuple containing the return value (type pywbem.Uint32)
        and a list of CIMParameter objects representing the output parameters

        Output parameters: none

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
        args = {'Format':param_format,
                'Passphrase':param_passphrase}
        check_empty_parameters(**args)

        provider = self.provider_manager.get_provider_for_format_name(param_format)
        if not provider:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find given Format.")

        (device, fmt) = provider.get_format_for_name(param_format)
        if not fmt:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_FOUND,
                    "Cannot find given Format.")

        try:
            crypto.luks_remove_key(device.path, None, param_passphrase)
        except CryptoError:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Can't remove key from LUKS.")

        return (pywbem.Uint32(0), [])

    class EncryptionFormatMethods(object):
        Job_Completed_with_No_Error = pywbem.Uint32(0)
        Not_Supported = pywbem.Uint32(1)
        Unknown = pywbem.Uint32(2)
        Timeout = pywbem.Uint32(3)
        Failed = pywbem.Uint32(4)
        Invalid_Parameter = pywbem.Uint32(5)
        In_Use = pywbem.Uint32(6)
        # DMTF_Reserved = ..
        Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
        # Method_Reserved = 4098..32767
        # Vendor_Specific = 32768..65535
