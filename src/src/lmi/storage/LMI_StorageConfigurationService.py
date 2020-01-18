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
Module for LMI_StorageConfigurationService class.

LMI_StorageConfigurationService
-------------------------------

.. autoclass:: LMI_StorageConfigurationService
    :members:

"""

from lmi.storage.ServiceProvider import ServiceProvider
import pywbem
import blivet.formats
import lmi.providers.cmpi_logging as cmpi_logging
import lmi.storage.util.units as units
import lmi.storage.util.storage as storage
from lmi.storage.DeviceProvider import DeviceProvider
from lmi.storage.SettingProvider import SettingProvider
from lmi.providers.JobManager import Job
import time
import re
import subprocess

LOG = cmpi_logging.get_logger(__name__)

class LMI_StorageConfigurationService(ServiceProvider):
    """ Provider of LMI_StorageConfigurationService. """

    @cmpi_logging.trace_method
    def __init__(self, *args, **kwargs):
        super(LMI_StorageConfigurationService, self).__init__(
                classname="LMI_StorageConfigurationService",
                *args, **kwargs)

    @cmpi_logging.trace_method
    def _check_redundancy_setting(self, redundancy, setting):
        """
            Check that DeviceProvider.Redundancy matches Setting.
            Return None if so or string with error message if it does
            not match.
        """
        # Too many return statements, but it has a purpose.
        # pylint: disable-msg=R0911

        drmax = setting.get('DataRedundancyMax', None)
        drmin = setting.get('DataRedundancyMin', None)
        drgoal = setting.get('DataRedundancyGoal', None)

        if drmax is not None and int(drmax) < redundancy.data_redundancy:
            return "DataRedundancyMax is too low."
        if drmin is not None and int(drmin) > redundancy.data_redundancy:
            return "DataRedundancyMin is too high."
        if (drmax is None and drmin is None and drgoal is not None
                and int(drgoal) != redundancy.data_redundancy):
            # only goal is set - it must match
            return "DataRedundancyGoal does not match."

        esmax = setting.get('ExtentStripeLengthMax', None)
        esmin = setting.get('ExtentStripeLengthMin', None)
        esgoal = setting.get('ExtentStripeLength', None)
        if esmax is not None and int(esmax) < redundancy.stripe_length:
            return "ExtentStripeLengthMax is too low."
        if esmin is not None and int(esmin) > redundancy.stripe_length:
            return "ExtentStripeLengthMin is too high."
        if (esmax is None and esmin is None and esgoal is not None
                and int(esgoal) != redundancy.stripe_length):
            # only goal is set - it must match
            return "ExtentStripeLength does not match."

        prmax = setting.get('PackageRedundancyMax', None)
        prmin = setting.get('PackageRedundancyMin', None)
        prgoal = setting.get('PackageRedundancyGoal', None)
        if prmax is not None and int(prmax) < redundancy.package_redundancy:
            return "PackageRedundancyMax is too low."
        if prmin is not None and int(prmin) > redundancy.package_redundancy:
            return "PackageRedundancyMin is too high."
        if (prmax is None and prmin is None and prgoal is not None
                and prgoal != redundancy.package_redundancy):
            # only goal is set - it must match
            return "PackageRedundancyGoal does not match."

        nspof = setting.get('NoSinglePointOfFailure', None)
        if (nspof is not None
                and SettingProvider.string_to_bool(nspof)
                    != redundancy.no_single_point_of_failure):
            return "NoSinglePointOfFailure does not match."

        parity = setting.get('ParityLayout', None)
        if (parity is not None
                and int(parity) != redundancy.parity_layout):
            return "ParityLayout does not match."

        return None

    @cmpi_logging.trace_method
    def _check_redundancy_goal_setting(self, redundancy, setting):
        """
            Check that DeviceProvider.Redundancy matches Setting['*Goal'].
            Return None if so or string with error message if it does
            not match.

            If any of the *Goal property is missing, the min/max is checked
            if it fits.
        """
        drgoal = setting.get('DataRedundancyGoal', None)
        if (drgoal is not None
                and int(drgoal) != redundancy.data_redundancy):
            return "DataRedundancyGoal does not match."

        esgoal = setting.get('ExtentStripeLength', None)
        if (esgoal is not None
                and int(esgoal) != redundancy.stripe_length):
            return "ExtentStripeLength does not match."

        prgoal = setting.get('PackageRedundancyGoal', None)
        if (prgoal is not None
                and prgoal != redundancy.package_redundancy):
            return "PackageRedundancyGoal does not match."

        nspof = setting.get('NoSinglePointOfFailure', None)
        if (nspof is not None
                and SettingProvider.string_to_bool(nspof)
                    != redundancy.no_single_point_of_failure):
            return "NoSinglePointOfFailure does not match."

        parity = setting.get('ParityLayout', None)
        if (parity is not None
                and int(parity) != redundancy.parity_layout):
            return "ParityLayout does not match."

        return self._check_redundancy_setting(redundancy, setting)

    @cmpi_logging.trace_method
    def _modify_lv(self, job, devicename, name, size):
        """
            Really modify the logical volume, all parameters were checked.
        """
        device = storage.getRealDeviceByPath(devicename)
        if device is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Device %s disappeared." % (devicename,))

        if name is not None:
            # rename
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Rename of logical volume is not yet supported.")

        if size is not None:
            # resize

            # check PE size
            newsize = device.vg.align(storage.to_blivet_size(size), True)
            oldsize = device.vg.align(device.size, False)
            if newsize != oldsize:
                action = blivet.deviceaction.ActionResizeDevice(
                        device, newsize)
                storage.do_storage_action(self.storage, [action])
                self.storage.devicetree.processActions(dryRun=False)
                self.storage.reset()

        newsize = storage.from_blivet_size(device.size)
        outparams = {}
        outparams['Size'] = pywbem.Uint64(newsize)
        devname = self.provider_manager.get_name_for_device(device)
        outparams['TheElement'] = devname
        ret = self.Values.CreateOrModifyElementFromStoragePool \
                .Job_Completed_with_No_Error

        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                affected_elements=[devname],
                error=None)

    @cmpi_logging.trace_method
    def _create_lv(self, job, poolname, name, size):
        """
            Really create the logical volume, all parameters were checked.
        """
        pool = storage.getRealDeviceByPath(self.storage, poolname)
        if pool is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Pool %s disappeared." % (poolname,))
        args = {}
        args['parents'] = [pool]
        args['size'] = pool.align(storage.to_blivet_size(size), True)
        if name:
            args['name'] = name

        storage.log_storage_call("CREATE LV", args)

        lv = self.storage.newLV(**args)
        action = blivet.deviceaction.ActionCreateDevice(lv)
        storage.do_storage_action(self.storage, [action])
        # re-read the device from blivet, it should have all device links
        lv = storage.getRealDeviceByPath(self.storage, lv.path)
        newsize = storage.from_blivet_size(lv.size)
        lvname = self.provider_manager.get_name_for_device(lv)
        outparams = {
                'TheElement': lvname,
                'Size': pywbem.Uint64(newsize)
        }
        ret = self.Values.CreateOrModifyElementFromStoragePool \
                .Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                affected_elements=[lvname],
                error=None)

    @cmpi_logging.trace_method
    def _parse_goal(self, param_goal, classname):
        """
            Find Setting for given CIMInstanceName and check, that it is
            of given CIM class.
            Return None, if no Goal was given.
            Raise CIMError, if the Goal cannot be found.
        """
        if param_goal:
            instance_id = param_goal['InstanceID']
            goal = self.provider_manager.get_setting_for_id(
                instance_id, classname)
            if not goal:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    classname + " Goal was not found.")
            goal.touch()
        else:
            goal = None
        return goal

    @cmpi_logging.trace_method
    def _parse_element(self, param_theelement, classname, blivet_class):
        """
            Find StorageDevice for given CIMInstanceName.
            Return None if no CIMInstanceName was given.
            Raise CIMError if the device does not exist or is not of given
            class.
        """
        if not param_theelement:
            return None
        if param_theelement.classname != classname:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Expected %s as TheElement." % (classname))

        device = self.provider_manager.get_device_for_name(param_theelement)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Cannot find the TheElement device.")
        if not isinstance(device, blivet_class):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                "The TheElement parameter is not %s." % (classname,))
        return device


    @cmpi_logging.trace_method
    def _parse_pool(self, param_inpool):
        """
            Find LVMVolumeGroupDevice for given CIMInstanceName.
            Return None if no CIMInstanceName was given.
            Raise CIMError if the device does not exist or is not VG.
        """
        if not param_inpool:
            return None

        pool = self.provider_manager.get_device_for_name(param_inpool)
        if not pool:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Cannot find the InPool device.")
        return pool

    @cmpi_logging.trace_method
    def cim_method_createormodifylv(self, env, object_name,
                                    param_elementname=None,
                                    param_goal=None,
                                    param_theelement=None,
                                    param_inpool=None,
                                    param_size=None,
                                    input_arguments=None,
                                    method_name=None):
        """
            Implements LMI_StorageConfigurationService.CreateOrModifyLV()

            Create or modify Logical Volume. This method is shortcut to
            CreateOrModifyElementFromStoragePool with the right Goal. Lazy
            applications can use this method to create or modify LVs, without
            calculation of the Goal setting.
        """
        self.check_instance(object_name)

        # remember input parameters for job
        if not input_arguments:
            input_arguments = {
                'ElementName' : pywbem.CIMProperty(name='ElementName',
                        type='string',
                        value=param_elementname),
                'Goal' : pywbem.CIMProperty(name='Goal',
                        type='reference',
                        value=param_goal),
                'TheElement': pywbem.CIMProperty(name='TheElement',
                        type='reference',
                        value=param_theelement),
                'InPool': pywbem.CIMProperty(name='InPool',
                        type='reference',
                        value=param_inpool),
                'Size': pywbem.CIMProperty(name='Size',
                        type='uint64',
                        value=param_size),
            }
        if not method_name:
            method_name = 'CreateOrModifyLV'

        # check parameters
        goal = self._parse_goal(param_goal, "LMI_LVStorageSetting")
        device = self._parse_element(param_theelement, "LMI_LVStorageExtent",
                blivet.devices.LVMLogicalVolumeDevice)
        pool = self._parse_pool(param_inpool)

        # check if resize is needed
        if param_size and device:
            oldsize = storage.from_blivet_size(
                    device.vg.align(device.size, False))
            if param_size < oldsize:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                        "Shrinking of logical volumes is not supported.")
            if oldsize == param_size:
                # don't need to change the size
                param_size = None

        # check if rename is needed
        if device and device.name == param_elementname:
            # don't need to change the name
            param_elementname = None

        # pool vs goal
        if goal and pool:
            pool_provider = self.provider_manager.get_provider_for_device(pool)
            redundancy = pool_provider.get_redundancy(pool)
            error = self._check_redundancy_setting(redundancy, goal)
            if error:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "The Goal does not match InPool's capabilities: "
                            + error)

        # pool vs theelement
        if pool and device and device.vg != pool:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                        "InPool does not match TheElement's pool, modification"\
                        " of a pool is not supported.")

        if not device and not pool:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Either InPool or TheElement must be specified.")

        if not device and not param_size:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Parameter Size must be set when creating a logical"\
                    " volume.")

        # Schedule a job
        if device:
            jobname = "MODIFY LV %s" % (device.path)
            devname = device.path
            affected_elements = [devname]
        else:
            jobname = "CREATE LV %s FROM %s" % (param_elementname, pool.path)
            poolname = pool.path
            affected_elements = [poolname]

        job = Job(
                job_manager=self.job_manager,
                job_name=jobname,
                input_arguments=input_arguments,
                method_name=method_name,
                affected_elements=affected_elements,
                owning_element=self._get_instance_name())
        if device:
            job.set_execute_action(self._modify_lv,
                    job, devname, param_elementname, param_size)
        else:
            job.set_execute_action(self._create_lv,
                    job, poolname, param_elementname, param_size)

        # enqueue the job
        self.job_manager.add_job(job)

        outparams = [ pywbem.CIMParameter(
                name='job',
                type='reference',
                value=job.get_name())]
        return (self.Values.CreateOrModifyLV\
                .Method_Parameters_Checked___Job_Started, outparams)


    @cmpi_logging.trace_method
    def cim_method_createormodifythinlv(self, env, object_name,
                                        param_elementname=None,
                                        param_thinpool=None,
                                        param_theelement=None,
                                        param_size=None):
        # check parameters
        self.check_instance(object_name)

        if param_thinpool is None and param_theelement is None or \
           param_thinpool and param_theelement:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                                  "Either ThinPool or TheElement must be specified.")

        if param_thinpool:
            if param_size is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                                      "Size is required.")

            lv = self.provider_manager.get_device_for_name(param_thinpool)
            if lv is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "ThinPool was not found.")
            if lv.type != "lvmthinpool":
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "ThinPool must be a thin pool device (specified '%s')." % (lv.type))

            jobname = "CREATE THINLV %s FROM %s" % (param_elementname, lv.path)
            affected_elements = [lv.path]
            _method = self._create_thinlv

        if param_theelement:
            lv = self.provider_manager.get_device_for_name(param_theelement)
            if lv is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "Thin LV was not found.")
            if lv.type != "lvmthinlv":
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "TheElement must be a thin LV device (specified '%s')." % (lv.type))

            jobname = "MODIFY THINLV %s" % (lv.path)
            affected_elements = [lv.path]
            _method = self._modify_thinlv

        input_arguments = {
            'ElementName' : pywbem.CIMProperty(name='ElementName',
                                               type='string',
                                               value=param_elementname),
            'ThinPool': pywbem.CIMProperty(name='ThinPool',
                                         type='reference',
                                         value=param_thinpool),
            'TheElement': pywbem.CIMProperty(name='TheElement',
                                           type='reference',
                                             value=param_theelement),
            'Size': pywbem.CIMProperty(name='Size',
                                       type='uint64',
                                       value=param_size),
        }
        method_name = 'CreateOrModifyThinLV'

        job = Job(
                job_manager=self.job_manager,
                job_name=jobname,
                input_arguments=input_arguments,
                method_name=method_name,
                affected_elements=None,
                owning_element=self._get_instance_name())
        job.set_execute_action(_method, job, lv.path, param_elementname, param_size)
        self.job_manager.add_job(job)
        outparams = [pywbem.CIMParameter(name='job',
                                         type='reference',
                                         value=job.get_name())]

        return (self.Values.CreateOrModifyLV\
                .Method_Parameters_Checked___Job_Started, outparams)

    @cmpi_logging.trace_method
    def _create_thinlv(self, job, pool_path, name, size):

        thinpool = storage.getRealDeviceByPath(self.storage, pool_path)
        if thinpool is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Device %s disappeared." % (pool_path))

        args = {'parents'     : [thinpool],
                'name'        : name,
                'thin_volume' : True,
                'size'        : storage.to_blivet_size(size)}
        thinlv = self.storage.newLV(**args)
        action = blivet.deviceaction.ActionCreateDevice(thinlv)
        storage.do_storage_action(self.storage, [action])
        # re-read the device from blivet, it should have all device links
        thinlv = storage.getRealDeviceByPath(self.storage, thinlv.path)
        newsize = storage.from_blivet_size(thinlv.size)
        thinlvname = self.provider_manager.get_name_for_device(thinlv)
        outparams = {
                'TheElement': thinlvname,
                'Size': pywbem.Uint64(newsize)
        }
        ret = self.Values.CreateOrModifyElementFromStoragePool.Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                affected_elements=[thinlvname],
                error=None)

    @cmpi_logging.trace_method
    def _modify_thinlv(self, job, thinlv_path, name, size):
        thinlv = storage.getRealDeviceByPath(self.storage, thinlv_path)
        if thinlv is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Device %s disappeared." % (thinlv_path))
        thinlvname = self.provider_manager.get_name_for_device(thinlv)

        if name and name != thinlv.lvname:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Rename of thin LVs is not yet supported.")

        if size:
            # resize
            # check PE size
            newsize = thinlv.vg.align(storage.to_blivet_size(size), True)
            oldsize = thinlv.vg.align(thinlv.size, False)
            if newsize != oldsize:
                action = blivet.deviceaction.ActionResizeDevice(
                        thinlv, newsize)
                storage.do_storage_action(self.storage, [action])
                # XXX: blivet doesn't support this yet
                self.storage.devicetree.processActions(dryRun=False)
                self.storage.reset()

        outparams = {
            'Thinlv': thinlvname,
            'Size': pywbem.Uint64(newsize)
        }
        ret = self.Values.CreateOrModifyElementFromStoragePool.Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                affected_elements=[thinlvname],
                error=None)


    @cmpi_logging.trace_method
    # Too many arguments of generated method: pylint: disable-msg=R0913
    def cim_method_createormodifyelementfromstoragepool(self, env, object_name,
                                                        param_elementname=None,
                                                        param_goal=None,
                                                        param_inpool=None,
                                                        param_theelement=None,
                                                        param_elementtype=None,
                                                        param_size=None):
        """
            Implements LMI_StorageConfigurationService
                            .CreateOrModifyElementFromStoragePool()

            Start a job to create (or modify) a Logical Volume from a
            LMI_StoragePool. One of the parameters for this method is Size. As
            an input parameter, Size specifies the desired size of the
            element. As an output parameter, it specifies the size achieved.
            The Size is rounded to extent size of the Volume Group. Space is
            taken from the input StoragePool. The desired settings for the
            element are specified by the Goal parameter. If the requested size
            cannot be created, no action will be taken, and the Return Value
            will be 4097/0x1001. Also, the output value of Size is set to the
            nearest possible size.  This method supports renaming or resizing
            of a Logical Volume.  If 0 is returned, the function completed
            successfully and no ConcreteJob instance was required. If
            4096/0x1000 is returned, a ConcreteJob will be started to create
            the element. The Job's reference will be returned in the output
            parameter Job.
        """

        etype = self.Values.CreateOrModifyElementFromStoragePool.ElementType
        if param_elementtype is not None:
            if param_elementtype != etype.StorageExtent and \
               param_elementtype != etype.ThinlyProvisionedStorageVolume:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "Only StorageExtent (3) and ThinlyProvisionedStorageVolume (5) are allowed.")

        input_arguments = {
            'ElementName' : pywbem.CIMProperty(name='ElementName',
                    type='string',
                    value=param_elementname),
            'Goal' : pywbem.CIMProperty(name='Goal',
                    type='reference',
                    value=param_goal),
            'TheElement': pywbem.CIMProperty(name='TheElement',
                    type='reference',
                    value=param_theelement),
            'InPool': pywbem.CIMProperty(name='InPool',
                    type='reference',
                    value=param_inpool),
            'ElementType': pywbem.CIMProperty(name='ElementType',
                    type='uint16',
                    value=param_elementtype),
            'Size': pywbem.CIMProperty(name='Size',
                    type='uint64',
                    value=param_size),
        }

        inpool = self._parse_pool(param_inpool)
        if inpool is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                  "InPool was not found.")

        method_name = 'CreateOrModifyElementFromStoragePool'
        ret = None

        if inpool.type == 'lvmvg' and \
           param_elementtype == etype.StorageExtent:
            # create LV
            ret = self.cim_method_createormodifylv(env, object_name,
                                                   param_elementname,
                                                   param_goal,
                                                   param_theelement,
                                                   param_inpool,
                                                   param_size,
                                                   input_arguments=input_arguments,
                                                   method_name=method_name)
        elif inpool.type == 'lvmthinpool' and \
             param_elementtype == etype.ThinlyProvisionedStorageVolume:
            # create thin LV
            ret = self.cim_method_createormodifythinlv(env, object_name,
                                                       param_elementname,
                                                       param_inpool,
                                                       param_theelement,
                                                       param_size)
        else:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                  "Specified InPool and ElementType combination is not supported.")

        return ret


    @cmpi_logging.trace_method
    def _modify_vg(self, job, poolname, goal, devnames, name):
        """
            Modify existing Volume Group. The parameters were already checked.
            This method is called in context of JobManager worker thread.
        """
        devices = []
        for devname in devnames:
            device = storage.getRealDeviceByPath(self.storage, devname)
            if device is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Device %s disappeared." % (devname,))
            devices.append(device)

        pool = self.provider_manager.get_device_for_name(poolname)
        if not pool:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Pool %s disappeared." % (poolname,))

        if name is not None:
            # rename
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Rename of volume group is not yet supported.")

        # check extent size
        if goal and goal['ExtentSize'] != pool.peSize:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Changing ExtentSize is not supported.")

        # check for added and removed devices:
        actions = []
        pv = blivet.formats.getFormat('lvmpv')
        for device in devices:
            if device not in pool.pvs:
                storage.assert_unused(self.storage, [device])
                # create the pv format if necessary
                a1 = blivet.ActionCreateFormat(device, pv)
                actions.append(a1)

                try:
                    a2 = blivet.deviceaction.ActionAddMember(pool, device)
                except AttributeError:
                    raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                            "Adding devices to VG is not supported, "
                            "need blivet version > 0.46")

                actions.append(a2)
                storage.log_storage_call("MODIFY VG ADD MEMBER",
                        {'container': pool, 'device': device})


        need_remove_pv = []  # list of devices that need pvremove
        for device in pool.pvs:
            if device not in devices:
                try:
                    a = blivet.deviceaction.ActionRemoveMember(pool, device)
                except AttributeError:
                    raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                            "Removing devices from VG is not supported, "
                            "need blivet version > 0.46")
                storage.log_storage_call("MODIFY VG REMOVE MEMBER",
                        {'container': pool, 'device': device})
                actions.append(a)
                # Remember to destroy the PV metadata too; matches DeleteVG()
                # behavior.
                need_remove_pv.append(device.path)

        if actions:
            storage.do_storage_action(self.storage, actions)
            if need_remove_pv:
                # Destroy PV formats on removed devices in separate transaction,
                # blivet doesn't like ActionRemoveMember and ActionDestroyFormat
                # in one set.
                actions = []
                for devname in need_remove_pv:
                    # Re-read the device from blivet, there might be reset()
                    # called in previous do_storage_action()
                    device = storage.getRealDeviceByPath(self.storage, devname)
                    if device is None:
                        LOG().trace_warn('_modify_vg: Device %s lost', devname)
                        continue
                    a = blivet.deviceaction.ActionDestroyFormat(device)
                    actions.append(a)
                    LOG().trace_info('Removing PV format from %s', devname)
                storage.do_storage_action(self.storage, actions)
        else:
            # nothing to do !?
            LOG().info("CreateOrModifyVG with no action.")

        outparams = {}
        newsize = storage.from_blivet_size(pool.size)
        outparams['Size'] = pywbem.Uint64(newsize)
        outparams['Pool'] = poolname
        retval = self.Values.CreateOrModifyVG.Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=retval,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                affected_elements=[poolname],
                error=None)

    @cmpi_logging.trace_method
    def _create_vg(self, job, goal, devnames, name):
        """
            Create new  Volume Group. The parameters were already checked.
            This method is called in context of JobManager worker thread.
        """
        devices = []
        for devname in devnames:
            device = storage.getRealDeviceByPath(self.storage, devname)
            if device is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Device %s disappeared." % (devname,))
            devices.append(device)
        # Check the devices are unused
        storage.assert_unused(self.storage, devices)

        pv = blivet.formats.getFormat('lvmpv')
        for device in devices:
            if not (device.format
                    and isinstance(device.format,
                        blivet.formats.lvmpv.LVMPhysicalVolume)):
                # create the pv format there
                action = blivet.ActionCreateFormat(device, pv)
                self.storage.devicetree.registerAction(action)

        args = {}
        args['parents'] = devices
        if goal and goal['ExtentSize']:
            args['peSize'] = storage.to_blivet_size(int(goal['ExtentSize']))
        if name:
            args['name'] = name

        storage.log_storage_call("CREATE VG", args)

        vg = self.storage.newVG(**args)
        action = blivet.ActionCreateDevice(vg)
        storage.do_storage_action(self.storage, [action])

        poolname = self.provider_manager.get_name_for_device(vg)
        newsize = storage.from_blivet_size(vg.size)
        outparams = {
                'pool': poolname,
                'size':pywbem.Uint64(newsize),
        }
        retval = self.Values.CreateOrModifyVG.Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=retval,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                affected_elements=[poolname],
                error=None)

    @cmpi_logging.trace_method
    def _parse_inextents(self, param_inextents):
        """
            Find StorageDevices for given array of CIMInstanceNames and
            return couple (devices, redundancies), where devices
            is array of StorageDevices and redundancies is array
            of Redundancy of the devices.
            Return ([], []), if no InExtents were given.
            Raise CIMError, if any of the extents cannot be found.
        """

        def string_to_instance_name(string):
            m = re.search('(?://([^:.,]+)/)?([^:.,]+/[^:.,]+):(\w+)\.', string)
            (host, namespace, classname) = m.groups()
            kb = re.findall(r'(\w+)="(.*?)(?<!\\)"', string)

            return pywbem.CIMInstanceName(classname=classname,
                                          namespace=namespace,
                                          keybindings=kb,
                                          host=host)

        if not param_inextents:
            return ([], [])
        devices = []
        redundancies = []
        for extent_name in param_inextents:
            if isinstance(extent_name, str):
                extent_name = string_to_instance_name(extent_name)

            provider = self.provider_manager.get_device_provider_for_name(
                    extent_name)
            if not provider:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Cannot find provider for InExtent " + str(extent_name))
            device = provider.get_device_for_name(extent_name)
            if not provider:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Cannot find device for InExtent " + str(extent_name))
            devices.append(device)
            redundancies.append(provider.get_redundancy(device))

        return (devices, redundancies)

    def _parse_inpools(self, param_inpools):
        return self._parse_inextents(param_inpools)

    @cmpi_logging.trace_method
    def cim_method_createormodifyvg(self, env, object_name,
                                    param_elementname=None,
                                    param_goal=None,
                                    param_inextents=None,
                                    param_pool=None,
                                    input_arguments=None,
                                    method_name=None):
        """
            Implements LMI_StorageConfigurationService.CreateOrModifyVG()

            Create or modify Volume Group. This method is shortcut to
            CreateOrModifyStoragePool with the right Goal. Lazy applications
            can use this method to create or modify VGs, without calculation
            of the Goal setting.

            On implementation side, this method is called by
            CreateOrModifyStoragePool. If so, input_arguments and method_name
            parameters are set, so we can create proper Job here.
        """
        # check parameters
        self.check_instance(object_name)

        # remember input parameters for job
        if not input_arguments:
            input_arguments = {
                'ElementName' : pywbem.CIMProperty(name='ElementName',
                        type='string',
                        value=param_elementname),
                'Goal' : pywbem.CIMProperty(name='Goal',
                        type='reference',
                        value=param_goal),
                'InExtents': pywbem.CIMProperty(name='InExtents',
                        type='reference',
                        is_array=True,
                        value=param_inextents),
                'Pool': pywbem.CIMProperty(name='Pool',
                        type='reference',
                        value=param_pool),
            }
        if not method_name:
            method_name = 'CreateOrModifyVG'

        goal = self._parse_goal(param_goal, "LMI_VGStorageSetting")
        pool = self._parse_pool(param_pool)
        (devices, redundancies) = self._parse_inextents(param_inextents)

        # extents vs goal:
        if devices and goal:
            final_redundancy = DeviceProvider.Redundancy \
                    .get_common_redundancy_list(redundancies)
            error = self._check_redundancy_setting(final_redundancy, goal)
            if error:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "The Goal does not match InExtents' capabilities: "
                            + error)

        # elementname
        name = param_elementname
        if pool and param_elementname == pool.name:
            # no rename is needed
            name = None

        if not pool and not devices:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Either Pool or InExtents must be specified")

        # Schedule a job
        devnames = [device.path for device in devices]
        devpaths = [self.provider_manager.get_name_for_device(device)
                        for device in devices]
        if pool:
            jobname = "MODIFY VG %s" % (pool.name)
            poolname = self.provider_manager.get_name_for_device(pool)
        else:
            # Check the devices are unused
            storage.assert_unused(self.storage, devices)
            jobname = "CREATE VG %s FROM %s" % (name, ",".join(devnames))

        job = Job(
                job_manager=self.job_manager,
                job_name=jobname,
                input_arguments=input_arguments,
                method_name=method_name,
                affected_elements=devpaths,
                owning_element=self._get_instance_name())
        if pool:
            job.set_execute_action(self._modify_vg,
                    job, poolname, goal, devnames, name)
        else:
            job.set_execute_action(self._create_vg,
                    job, goal, devnames, name)

        # enqueue the job
        self.job_manager.add_job(job)

        outparams = [ pywbem.CIMParameter(
                name='job',
                type='reference',
                value=job.get_name())]
        return (self.Values.CreateOrModifyVG\
                .Method_Parameters_Checked___Job_Started, outparams)

    @cmpi_logging.trace_method
    def cim_method_createormodifythinpool(self, env, object_name,
                                          param_elementname=None,
                                          param_goal=None,
                                          param_inpool=None,
                                          param_pool=None,
                                          param_size=None):
        # check parameters
        self.check_instance(object_name)

        if param_goal:
            goal = self._parse_goal(param_goal, 'LMI_VGStorageSetting')
            if goal is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      'Invalid Goal.')

            # see LMI_VGStorageCapabilities.Values.SupportedStorageElementTypes
            ThinlyProvisionedLimitlessStoragePool = pywbem.Uint16(9)

            if goal['ThinProvisionedPoolType'] != str(ThinlyProvisionedLimitlessStoragePool):
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "Unsupported Goal value: %s." % (goal['ThinProvisionedPoolType']))

        input_arguments = {
            'ElementName' : pywbem.CIMProperty(name='ElementName',
                                               type='string',
                                               value=param_elementname),
            'Goal' : pywbem.CIMProperty(name='Goal',
                                        type='reference',
                                        value=param_goal),
            'InPool': pywbem.CIMProperty(name='InPool',
                                         type='reference',
                                         value=param_inpool),
            'Pool': pywbem.CIMProperty(name='Pool',
                                       type='reference',
                                       value=param_pool),
            'Size': pywbem.CIMProperty(name='Size',
                                       type='uint64',
                                       value=param_size),
        }

        method_name = 'CreateOrModifyThinPool'

        if param_inpool is None and param_pool is None or \
           param_inpool and param_pool:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                  "Either InPool or Pool must be specified.")

        if param_inpool:
            if param_size is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "Size is required.")

            pool = self.provider_manager.get_device_for_name(param_inpool)
            if pool is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "InPool was not found.")
            jobname = "CREATE THINPOOL %s FROM %s" % (param_elementname, pool.path)
            affected_elements = [pool.path]
            _method = self._create_thinpool

        if param_pool:
            pool = self.provider_manager.get_device_for_name(param_pool)
            if pool is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "ThinPool was not found.")
            jobname = "MODIFY THINPOOL %s" % (pool.path)
            affected_elements = [pool.path]
            _method = self._modify_thinpool

        job = Job(
                job_manager=self.job_manager,
                job_name=jobname,
                input_arguments=input_arguments,
                method_name=method_name,
                affected_elements=affected_elements,
                owning_element=self._get_instance_name())

        job.set_execute_action(_method, job, pool.path, param_elementname, param_size)

        self.job_manager.add_job(job)

        outparams = [pywbem.CIMParameter(name='job',
                                         type='reference',
                                         value=job.get_name())]

        return (self.Values.CreateOrModifyLV\
                .Method_Parameters_Checked___Job_Started, outparams)

    @cmpi_logging.trace_method
    def _create_thinpool(self, job, pool_path, name, size):
        vg = storage.getRealDeviceByPath(self.storage, pool_path)
        if vg is None:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                                  "Device %s disappeared." % (pool_path))
        args = {'parents'   : [vg],
                'name'      : name,
                'thin_pool' : True,
                'size'      : storage.to_blivet_size(size)}
        thinpool = self.storage.newLV(**args)
        action = blivet.deviceaction.ActionCreateDevice(thinpool)
        storage.do_storage_action(self.storage, [action])
        # re-read the device from blivet, it should have all device links
        thinpool = storage.getRealDeviceByPath(self.storage, thinpool.path)
        newsize = storage.from_blivet_size(thinpool.size)
        thinpoolname = self.provider_manager.get_name_for_device(thinpool)

        outparams = {
            'Pool': thinpoolname,
            'Size': pywbem.Uint64(newsize)
        }
        ret = self.Values.CreateOrModifyElementFromStoragePool.Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                affected_elements=[thinpoolname],
                error=None)

    @cmpi_logging.trace_method
    def _modify_thinpool(self, job, pool_path, name, size):
        thinpool = storage.getRealDeviceByPath(self.storage, pool_path)
        thinpoolname = self.provider_manager.get_name_for_device(thinpool)

        if name and name != thinpool.lvname:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Rename of thin pool is not yet supported.")

        if size:
            # resize
            # check PE size
            newsize = thinpool.vg.align(storage.to_blivet_size(size), True)
            oldsize = thinpool.vg.align(thinpool.size, False)
            if newsize != oldsize:
                action = blivet.deviceaction.ActionResizeDevice(
                        thinpool, newsize)
                storage.do_storage_action(self.storage, [action])
                # XXX: blivet raises 'device is not resizable' for now
                self.storage.devicetree.processActions(dryRun=False)
                self.storage.reset()

        outparams = {
            'Pool': thinpoolname,
            'Size': pywbem.Uint64(newsize)
        }
        ret = self.Values.CreateOrModifyElementFromStoragePool.Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                affected_elements=[thinpoolname],
                error=None)

    @cmpi_logging.trace_method
    # Too many aruments of generated method: pylint: disable-msg=R0913
    def cim_method_createormodifystoragepool(self, env, object_name,
                                             param_elementname=None,
                                             param_goal=None,
                                             param_inpools=None,
                                             param_inextents=None,
                                             param_pool=None,
                                             param_size=None):
        """
            Implements LMI_StorageConfigurationService.CreateOrModifyStoragePool()

            Starts a job to create (or modify) a StoragePool.Only Volume Groups
            can be created or modified using this method.\nLMI supports only
            creation of pools from whole StorageExtents, it is not possible to
            allocate only part of an StorageExtent.\nOne of the parameters for
            this method is Size. As an input parameter, Size specifies the
            desired size of the pool. It must match sum of all input extent
            sizes. Error will be returned if not, with correct Size output
            parameter value.\nAny InPools as parameter will result in
            error.\nThe capability requirements that the Pool must support are
            defined using the Goal parameter.\nThis method supports renaming
            of a Volume Group and adding and removing StorageExtents to/from a
            Volume Group.\nIf 0 is returned, then the task completed
            successfully and the use of ConcreteJob was not required. If the
            task will take some time to complete, a ConcreteJob will be
            created and its reference returned in the output parameter Job.\n
            This method automatically formats the StorageExtents added to a
            Volume Group as Physical Volumes.
        """
        # check parameters
        if param_inextents and param_inpools:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                  "InExtents and InPools are mutually exclusive.")

        if param_inpools:
            inpools = self._parse_inpools(param_inpools)[0]
            if inpools is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "InPools not found: %s." % (param_inpools[0]))

            inpool = self.provider_manager.get_name_for_device(inpools[0])
            if inpool is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "No InPool found for: %s." % (param_inpools[0]))

        if param_goal:
            goal = self._parse_goal(param_goal, 'LMI_VGStorageSetting')
            if goal is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "Invalid Goal.")

        if param_pool:
            pool = self._parse_pool(param_pool)
            if pool is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                      "Pool was not found.")

        method_name = 'CreateOrModifyStoragePool'
        input_arguments = {
            'ElementName' : pywbem.CIMProperty(name='ElementName',
                    type='string',
                    value=param_elementname),
            'Goal' : pywbem.CIMProperty(name='Goal',
                    type='reference',
                    value=param_goal),
            'InExtents': pywbem.CIMProperty(name='InExtents',
                    type='reference',
                    is_array=True,
                    value=param_inextents),
            'InPools': pywbem.CIMProperty(name='InPools',
                    type='reference',
                    is_array=True,
                    value=param_inpools),
            'Pool': pywbem.CIMProperty(name='Pool',
                    type='reference',
                    value=param_pool),
            'Size': pywbem.CIMProperty(name='Size',
                    type='uint64',
                    value=param_size),
        }

        if param_pool and pool:
            # modify pool
            if not param_inextents and param_goal and goal.has_key('ThinProvisionedPoolType'):
                # modify thin pool
                if param_inextents:
                    raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                                          "Unsupported combination of Goal and InExtents.")

                return self.cim_method_createormodifythinpool(env, object_name,
                                                              param_elementname, param_goal,
                                                              None, param_pool,
                                                              param_size)
            else:
                # modify vg
                if param_size:
                    LOG().trace_warn("Parameter without effect: Size")

                return self.cim_method_createormodifyvg(env, object_name,
                                                        param_elementname, param_goal,
                                                        param_inextents, param_pool,
                                                        input_arguments, method_name)
        # create thinpool
        if not param_inextents and param_goal and goal.has_key('ThinProvisionedPoolType'):
            # create thinpool
            return self.cim_method_createormodifythinpool(env, object_name,
                                                          param_elementname, param_goal,
                                                          inpool, None,
                                                          param_size)
        if param_size:
            LOG().trace_warn("Parameter without effect: Size")

        return self.cim_method_createormodifyvg(env, object_name,
                                                param_elementname, param_goal,
                                                param_inextents, None,
                                                input_arguments, method_name)

    @cmpi_logging.trace_method
    # Too many aruments of generated method: pylint: disable-msg=R0913
    def cim_method_createormodifyelementfromelements(self, env, object_name,
                                                     param_inelements,
                                                     param_elementtype,
                                                     param_elementname=None,
                                                     param_goal=None,
                                                     param_theelement=None,
                                                     param_size=None):
        """
            Implements LMI_StorageConfigurationService.CreateOrModifyElementFromElements()

            Start a job to create (or modify) a MD RAID from specified input
            StorageExtents. Only whole StorageExtents can be added to a
            RAID.\nAs an input parameter, Size specifies the desired size of
            the element and must match size of all input StorageVolumes
            combined in the RAID. Use null to avoid this calculation. As an
            output parameter, it specifies the size achieved.\nThe desired
            Settings for the element are specified by the Goal parameter.\n
            If 0 is returned, the function completed successfully and no
            ConcreteJob instance was required. If 4096/0x1000 is returned, a
            ConcreteJob will be started to create the element. The Job\'s
            reference will be returned in the output parameter Job.\nThis
            method does not support MD RAID modification for now.
        """
        # check parameters
        if param_size is not None:
            raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                    "Parameter Size is not supported.")

        if param_elementtype is not None:
            etypes = self.Values.CreateOrModifyElementFromElements.ElementType
            if param_elementtype != etypes.Storage_Extent:
                raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                        "Parameter ElementType must have value" \
                        " '3 - StorageExtent'.")
        input_arguments = {
                'InElements': pywbem.CIMProperty(name='InElements',
                        type='reference',
                        is_array=True,
                        value=param_inelements),
                'ElementType': pywbem.CIMProperty(name='ElementType',
                        type='int16',
                        value=param_elementtype),
                'ElementName' : pywbem.CIMProperty(name='ElementName',
                        type='string',
                        value=param_elementname),
                'TheElement': pywbem.CIMProperty(name='TheElement',
                        type='reference',
                        value=param_theelement),
                'Goal' : pywbem.CIMProperty(name='Goal',
                        type='reference',
                        value=param_goal),
                'Size' : pywbem.CIMProperty(name='Size',
                        type='uint64',
                        value=param_size),
        }

        return self.cim_method_createormodifymdraid(env, object_name,
                param_elementname=param_elementname,
                param_theelement=param_theelement,
                param_goal=param_goal,
                param_level=None,
                param_inextents=param_inelements,
                input_arguments=input_arguments,
                method_name='CreateOrModifyElementFromElements')

    @cmpi_logging.trace_method
    def _find_raid_level(self, redundancies, goal):
        """
           Find and return RAID level corresponding to given Goal and set of
           redundancies of input devices.
        """
        # find redundancies of the devices
        # try all possible RAID levels and take the best one
        # hash level -> redundancy of the RAID with given level
        levels = {
                0: DeviceProvider.Redundancy.get_common_redundancy_list(
                        redundancies, 0),
                1: DeviceProvider.Redundancy.get_common_redundancy_list(
                        redundancies, 1),
                4: DeviceProvider.Redundancy.get_common_redundancy_list(
                        redundancies, 4),
                5: DeviceProvider.Redundancy.get_common_redundancy_list(
                        redundancies, 5),
                6: DeviceProvider.Redundancy.get_common_redundancy_list(
                        redundancies, 6),
                10: DeviceProvider.Redundancy.get_common_redundancy_list(
                        redundancies, 10),
        }

        # hash RAID level number -> priority of the level
        # if more RAID levels matches the goal, the lowest priority is selected
        level_priorities = {
                1: 1,
                5: 2,
                6: 3,
                4: 4,
                10: 5,
                0: 6
        }

        # first, check the goal[*Goal] properties
        best_level = None
        for (level, redundancy) in levels.iteritems():
            err = self._check_redundancy_goal_setting(redundancy, goal)
            if err is None:
                # we have match which either completely satisfied goal[*Goal]
                # or the redundancy matches goal[*Min/Max] properties
                if not best_level:
                    best_level = level
                else:
                    if level_priorities[level] < level_priorities[best_level]:
                        best_level = level
                LOG().trace_info(
                        "Goal check: matching RAID%d, best level so far: %d",
                        level, best_level)
            else:
                LOG().trace_info("Goal check: skipping goal RAID%d: %s",
                            level, err)

        if best_level is not None:
            return best_level

        # then, find any that matches
        for (level, redundancy) in levels.iteritems():
            err = self._check_redundancy_setting(redundancy, goal)
            if err is None:
                if not best_level:
                    best_level = level
                else:
                    if level_priorities[level] < level_priorities[best_level]:
                        best_level = level
                LOG().trace_info(
                        "Any check: matching RAID%d, best level so far: %d",
                        level, best_level)
            else:
                LOG().trace_info("Any check: skipping RAID%d: %s", level, err)
        return best_level

    @cmpi_logging.trace_method
    def _schedule_create_mdraid(self, level, goal, devices, name,
            input_arguments, method_name):
        """
        Create the job to create a MD RAID.
        """
        devnames = [device.path for device in devices]
        devpaths = [self.provider_manager.get_name_for_device(device)
                        for device in devices]
        job = Job(
                job_manager=self.job_manager,
                job_name="CREATE MDRAID ON " + "+".join(devnames),
                input_arguments=input_arguments,
                method_name=method_name,
                affected_elements=devpaths,
                owning_element=self._get_instance_name())
        job.set_execute_action(self._create_mdraid,
                job, level, goal, devnames, name)

        # enqueue the job
        self.job_manager.add_job(job)

        outparams = [ pywbem.CIMParameter(
                name='job',
                type='reference',
                value=job.get_name())]
        return (self.Values.CreateOrModifyMDRAID\
                .Method_Parameters_Checked___Job_Started, outparams)

    @cmpi_logging.trace_method
    # pylint: disable-msg=W0613
    def _create_mdraid(self, job, level, goal, devicenames, name):
        """
            Create new  MD RAID. The parameters were already checked.
        """
        # Delete format on all devices first
        # This is workaround for #924245
        # TODO: remove when the bug is fixed
        actions = []
        for devname in devicenames:
            device = storage.getRealDeviceByPath(self.storage, devname)
            if device:
                actions.append(blivet.ActionDestroyFormat(device))
        storage.do_storage_action(self.storage, actions)
        # End of workaround


        # covert devices from strings to real devices
        devices = []
        for devname in devicenames:
            device = storage.getRealDeviceByPath(self.storage, devname)
            if device is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "Device %s disappeared." % (devname,))
            devices.append(device)
        # Check the devices are unused
        storage.assert_unused(self.storage, devices)

        # "format" the devices - this does just marks the devices as MD
        # members inside blivet
        fmt = blivet.formats.getFormat('mdmember')
        actions = []
        for device in devices:
            LOG().info("Formatting device %s with %s", device.name, fmt.name)
            action = blivet.ActionCreateFormat(device, fmt)
            self.storage.devicetree.registerAction(action)

        args = {}
        args['parents'] = devices
        if name:
            args['name'] = name
        args['level'] = str(level)
        args['memberDevices'] = len(devices)
        args['totalDevices'] = len(devices)

        storage.log_storage_call("CREATE MDRAID", args)

        raid = self.storage.newMDArray(**args)
        action = blivet.ActionCreateDevice(raid)
        storage.do_storage_action(self.storage, [action])

        # re-read the device from blivet, it should have all device links
        raid = storage.getRealDeviceByPath(self.storage, raid.path)
        newsize = storage.from_blivet_size(raid.size)
        raidname = self.provider_manager.get_name_for_device(raid)
        outparams = {
            'theelement': raidname,
            'size' : pywbem.Uint64(newsize)
        }
        retval = self.Values.CreateOrModifyMDRAID.Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=retval,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments=outparams,
                affected_elements=[raidname, ],
                error=None)

    @cmpi_logging.trace_method
    # pylint: disable-msg=W0613
    def _schedule_modify_mdraid(self, raid, level, goal, devices, name,
            input_parameters, method_name):
        """
            Modify existing MD RAID. The parameters were already checked.
        """
        raise pywbem.CIMError(pywbem.CIM_ERR_NOT_SUPPORTED,
                "MD RAID modification is not supported yet.")

    @cmpi_logging.trace_method
    def cim_method_createormodifymdraid(self, env, object_name,
                                        param_elementname=None,
                                        param_theelement=None,
                                        param_goal=None,
                                        param_level=None,
                                        param_inextents=None,
                                        input_arguments=None,
                                        method_name=None):
        """
            Implements LMI_StorageConfigurationService.CreateOrModifyMDRAID()

            Create or modify MD RAID array. This method is shortcut to
            CreateOrModifyElementFromElements with the right Goal. Lazy
            applications can use this method to create or modify MD RAID with
            the right level, without calculation of the Goal setting.\nEither
            Level or Goal must be specified. If both are specified, they must
            match.\nRAID modification is not yet supported.
        """
        # check parameters
        self.check_instance(object_name)

        # remember input parameters for job
        if not input_arguments:
            input_arguments = {
                    'ElementName' : pywbem.CIMProperty(name='ElementName',
                            type='string',
                            value=param_elementname),
                    'TheElement': pywbem.CIMProperty(name='TheElement',
                            type='reference',
                            value=param_theelement),
                    'Goal' : pywbem.CIMProperty(name='Goal',
                            type='reference',
                            value=param_goal),
                    'Level' : pywbem.CIMProperty(name='Level',
                            type='uint16',
                            value=param_level),
                    'InExtents': pywbem.CIMProperty(name='InExtents',
                            type='reference',
                            is_array=True,
                            value=param_inextents),
            }
        if not method_name:
            method_name = "CreateOrModifyMDRAID"

        # check the parameters
        goal = self._parse_goal(param_goal, "LMI_MDRAIDStorageSetting")
        raid = self._parse_element(param_theelement, "LMI_MDRAIDStorageExtent",
                blivet.devices.MDRaidArrayDevice)
        (devices, redundancies) = self._parse_inextents(param_inextents)

        # level
        if param_level is not None and param_level not in (
                self.Values.CreateOrModifyMDRAID.Level.RAID0,
                self.Values.CreateOrModifyMDRAID.Level.RAID1,
                self.Values.CreateOrModifyMDRAID.Level.RAID4,
                self.Values.CreateOrModifyMDRAID.Level.RAID5,
                self.Values.CreateOrModifyMDRAID.Level.RAID6,
                self.Values.CreateOrModifyMDRAID.Level.RAID10):
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Invalid value of parameter Level.")

        # goal vs level
        if goal and param_level is not None:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Only one of Level and Goal parameters may be used.")

        # extents vs goal:
        if devices and goal:
            # guess RAID level
            param_level = self._find_raid_level(redundancies, goal)
            if param_level is None:
                raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                        "The Goal does not match any RAID level for InExtents.")

        # nr. of devices vs level
        if ((param_level == 0
                or param_level == 1)
                    and len(devices) < 2):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "At least two devices are required for RAID level %d."
                    % (param_level))

        if (param_level == 5 or param_level == 4) and len(devices) < 3:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "At least three devices are required for RAID level" \
                    " 4 or 5.")
        if param_level == 6 and len(devices) < 4:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "At least four devices are required for RAID level 6.")
        if param_level == 10 and len(devices) < 2:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "At least two devices are required for RAID level 10.")

        name = param_elementname
        if raid and param_elementname == raid.name:
            # no rename is needed
            name = None

        if not raid and not devices:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Either TheElement or InExtents must be specified")

        if raid:
            return self._schedule_modify_mdraid(
                    raid, param_level, goal, devices, name, input_arguments,
                    method_name)
        else:
            # Check the devices are unused
            storage.assert_unused(self.storage, devices)
            return self._schedule_create_mdraid(
                    param_level, goal, devices, name, input_arguments,
                    method_name)

    @cmpi_logging.trace_method
    def _delete_mdraid(self, job, devicepath):
        """
        Really delete a MD RAID array. This method is called in context of
        JobManager worker thread.
        """
        device = storage.getRealDeviceByPath(self.storage, devicepath)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Cannot find device %s" % (devicepath,))
        if not isinstance(device, blivet.devices.MDRaidArrayDevice):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Device %s is not LMI_MDRAIDStorageExtent" % (devicepath,))

        # Check the device is unused
        storage.assert_unused(self.storage, [device])

        # finally delete it
        actions = []
        actions.append(blivet.ActionDestroyDevice(device))
        # Destroy also all formats on member devices.
        # TODO: remove when Blivet does this automatically.
        for parent in device.parents:
            actions.append(blivet.deviceaction.ActionDestroyFormat(parent))
        storage.do_storage_action(self.storage, actions)

        ret = self.Values.DeleteMDRAID.Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments={},
                affected_elements=[],
                error=None)

    @cmpi_logging.trace_method
    def cim_method_deletemdraid(self, env, object_name,
                                param_theelement=None):
        """Implements LMI_StorageConfigurationService.DeleteMDRAID()

        Delete MD RAID array. All members are detached from the array and
        all RAID metadata are erased.

        Keyword arguments:
        env -- Provider Environment (pycimmb.ProviderEnvironment)
        object_name -- A pywbem.CIMInstanceName or pywbem.CIMCLassName
            specifying the object on which the method DeleteMDRAID()
            should be invoked.
        param_theelement --  The input parameter TheElement (type REF (pywbem.CIMInstanceName(classname='LMI_MDRAIDStorageExtent', ...))
            The MD RAID device to destroy.


        Returns a two-tuple containing the return value (type pywbem.Uint32 self.Values.DeleteMDRAID)
        and a list of CIMParameter objects representing the output parameters

        Output parameters:
        Job -- (type REF (pywbem.CIMInstanceName(classname='CIM_ConcreteJob', ...))
            Reference to the job (may be null if job completed).


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
        # check parameters
        self.check_instance(object_name)

        # remember input parameters for job
        input_arguments = {
                'TheElement': pywbem.CIMProperty(name='TheElement',
                        type='reference',
                        value=param_theelement),
        }

        # check the parameters
        raid = self._parse_element(param_theelement, "LMI_MDRAIDStorageExtent",
                blivet.devices.MDRaidArrayDevice)
        if not raid:
            raise pywbem.CIMError(pywbem.CIM_ERR_INVALID_PARAMETER,
                    "Parameter TheElement must be specified an must be "
                    "reference to LMI_MDRAIDStorageExtent")
        # Check the device is unused
        storage.assert_unused(self.storage, [raid])

        # Schedule the job
        job = Job(
                job_manager=self.job_manager,
                job_name="DELETE MDRAID " + raid.path,
                input_arguments=input_arguments,
                method_name='DeleteMDRAID',
                affected_elements=[param_theelement],
                owning_element=self._get_instance_name())
        job.set_execute_action(self._delete_mdraid,
                job, raid.path)

        # enqueue the job
        self.job_manager.add_job(job)

        outparams = [ pywbem.CIMParameter(
                name='job',
                type='reference',
                value=job.get_name())]
        return (self.Values.CreateOrModifyMDRAID\
                .Method_Parameters_Checked___Job_Started, outparams)


    @cmpi_logging.trace_method
    def _delete_vg(self, job, poolpath):
        """
        Delete VG. This method is called in context of
        JobManager worker thread.
        """
        pool = storage.getRealDeviceByPath(self.storage, poolpath)
        if not pool:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Cannot find VG %s" % (poolpath,))

        # Check the device is unused
        storage.assert_unused(self.storage, [pool])

        # finally delete it
        actions = []
        actions.append(blivet.ActionDestroyDevice(pool))
        # Destroy also all formats on member devices.
        for parent in pool.parents:
            if parent.format and parent.format.type is not None:
                actions.append(blivet.deviceaction.ActionDestroyFormat(parent))
        storage.do_storage_action(self.storage, actions)

        ret = self.Values.DeleteVG.Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments={},
                affected_elements=[],
                error=None)

    @cmpi_logging.trace_method
    def cim_method_deletevg(self, env, object_name,
                            param_pool=None, input_arguments=None,
                            method_name=None):
        """Implements LMI_StorageConfigurationService.DeleteVG()

        Start a job to delete a Volume Group. If 0 is returned, the
        function completed successfully, and no ConcreteJob was required.
        If 4096/0x1000 is returned, a ConcreteJob will be started to
        delete the StoragePool. A reference to the Job is returned in the
        Job parameter.
        """
        self.check_instance(object_name)
        # remember input parameters for job
        if not input_arguments:
            input_arguments = {
                    'Pool': pywbem.CIMProperty(name='Pool',
                            type='reference',
                            value=param_pool),
            }
        if not method_name:
            method_name = "DeleteVG"

        # check the parameters
        pool = self._parse_pool(param_pool)
        if not pool:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Parameter Pool is mandatory and must be"
                    " LMI_VGStoragePool.")
        # Check the device is unused
        storage.assert_unused(self.storage, [pool])

        # Schedule the job
        job = Job(
                job_manager=self.job_manager,
                job_name="DELETE VG " + pool.path,
                input_arguments=input_arguments,
                method_name=method_name,
                affected_elements=[param_pool],
                owning_element=self._get_instance_name())
        job.set_execute_action(self._delete_vg,
                job, pool.path)

        # enqueue the job
        self.job_manager.add_job(job)

        outparams = [ pywbem.CIMParameter(
                name='job',
                type='reference',
                value=job.get_name())]
        return (self.Values.DeleteVG\
                .Method_Parameters_Checked___Job_Started, outparams)

    @cmpi_logging.trace_method
    def cim_method_deletestoragepool(self, env, object_name,
                                     param_pool=None):
        """Implements LMI_StorageConfigurationService.DeleteStoragePool()

        Start a job to delete a StoragePool. The freed space is returned
        source StoragePools (indicated by AllocatedFrom StoragePool) or
        back to underlying storage extents. If 0 is returned, the function
        completed successfully, and no ConcreteJob was required. If
        4096/0x1000 is returned, a ConcreteJob will be started to delete
        the StoragePool. A reference to the Job is returned in the Job
        parameter.

        Implementation just calls DeleteVG with the same arguments.
        """
        input_arguments = {
                'Pool': pywbem.CIMProperty(name='Pool',
                        type='reference',
                        value=param_pool),
        }
        return self.cim_method_deletevg(env, object_name, param_pool,
                input_arguments, "DeleteStoragePool")

    @cmpi_logging.trace_method
    def _delete_lv(self, job, devicepath):
        """
        Delete VG. This method is called in context of
        JobManager worker thread.
        """
        device = storage.getRealDeviceByPath(self.storage, devicepath)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Cannot find LV %s" % (devicepath,))
        if not isinstance(device, blivet.devices.LVMLogicalVolumeDevice):
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Device %s is not LMI_LVStorageExtent" % (devicepath,))

        # Check the device is unused
        storage.assert_unused(self.storage, [device])

        # finally delete it
        action = blivet.ActionDestroyDevice(device)
        storage.do_storage_action(self.storage, [action])

        ret = self.Values.DeleteLV.Job_Completed_with_No_Error
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=ret,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments={},
                affected_elements=[],
                error=None)

    @cmpi_logging.trace_method
    def cim_method_deletelv(self, env, object_name,
                            param_theelement=None,
                            input_arguments=None, method_name=None):
        """Implements LMI_StorageConfigurationService.DeleteLV()

        Start a job to delete a  Logical Volume. If 0 is returned, the
        function completed successfully and no ConcreteJob was required.
        If 4096/0x1000 is returned, a ConcreteJob will be started to
        delete the element. A reference to the Job is returned in the Job
        parameter. This method is alias of ReturnToStoragePool().
        """

        self.check_instance(object_name)
        # remember input parameters for job
        if not input_arguments:
            input_arguments = {
                    'TheElement': pywbem.CIMProperty(name='TheElement',
                            type='reference',
                            value=param_theelement),
            }
        if not method_name:
            method_name = "DeleteLV"

        # check the parameters
        device = self._parse_element(param_theelement, "LMI_LVStorageExtent",
                blivet.devices.LVMLogicalVolumeDevice)
        if not device:
            raise pywbem.CIMError(pywbem.CIM_ERR_FAILED,
                    "Parameter TheElement is mandatory and must be"
                    " LMI_LVStorageExtent.")
        # Check the device is unused
        storage.assert_unused(self.storage, [device])

        # Schedule the job
        job = Job(
                job_manager=self.job_manager,
                job_name="DELETE LV " + device.path,
                input_arguments=input_arguments,
                method_name=method_name,
                affected_elements=[param_theelement],
                owning_element=self._get_instance_name())
        job.set_execute_action(self._delete_lv,
                job, device.path)

        # enqueue the job
        self.job_manager.add_job(job)

        outparams = [ pywbem.CIMParameter(
                name='job',
                type='reference',
                value=job.get_name())]
        return (self.Values.DeleteLV\
                .Method_Parameters_Checked___Job_Started, outparams)

    @cmpi_logging.trace_method
    def cim_method_returntostoragepool(self, env, object_name,
                                       param_theelement=None):
        """Implements LMI_StorageConfigurationService.ReturnToStoragePool()

        Start a job to delete an element, i.e. Logical Volume, previously
        created from a StoragePool. The freed space is returned to the
        source StoragePool. If 0 is returned, the function completed
        successfully and no ConcreteJob was required. If 4096/0x1000 is
        returned, a ConcreteJob will be started to delete the element. A
        reference to the Job is returned in the Job parameter.
        """
        input_arguments = {
                'TheElement': pywbem.CIMProperty(name='TheElement',
                        type='reference',
                        value=param_theelement),
        }
        return self.cim_method_deletelv(env, object_name,
                param_theelement, input_arguments, "ReturnToStoragePool")

    @cmpi_logging.trace_method
    def _scan_scsi(self, job):
        """
        Scan SCSI and reload blivet.
        """
        try:
            out = subprocess.check_output(["/usr/bin/scsi-rescan", "-a"])
        except subprocess.CalledProcessError, ex:
            LOG().warn(ex.msg)
            raise
        LOG().trace_info("scsi-rescan output: %s", out)
        # reset the storage
        storage.storage_reset(self.storage)
        job.finish_method(
                Job.STATE_FINISHED_OK,
                return_value=self.Values.LMI_ScsiScan.Success,
                return_type=Job.ReturnValueType.Uint32,
                output_arguments={},
                affected_elements=[],
                error=None)


    @cmpi_logging.trace_method
    def cim_method_lmi_scsiscan(self, env, object_name):
        """Implements LMI_StorageConfigurationService.LMI_ScsiScan()

        This method requests that the system rescan SCSI devices for
        changes in their configuration. If called on a general-purpose
        host, the changes are reflected in the list of devices available
        to applications (for example, the UNIX 'device tree'. This method
        may also be used on a storage appliance to force rescanning of
        attached SCSI devices.   This operation can be disruptive;
        optional parameters allow the caller to limit the scan to a single
        or set of SCSI device elements. All parameters are optional; if
        parameters other Job are passed in as null, a full scan is
        invoked.
        """
        input_arguments = {
        }

        # Schedule the job
        job = Job(
                job_manager=self.job_manager,
                job_name="SCSI SCAN",
                input_arguments=input_arguments,
                method_name="LMI_ScsiScan",
                affected_elements=[],
                owning_element=self._get_instance_name())
        job.set_execute_action(self._scan_scsi, job)

        # enqueue the job
        self.job_manager.add_job(job)

        outparams = [ pywbem.CIMParameter(
                name='job',
                type='reference',
                value=job.get_name())]
        return (self.Values.LMI_ScsiScan\
                .Method_Parameters_Checked___Job_Started, outparams)


    class Values(ServiceProvider.Values):
        class CreateOrModifyElementFromStoragePool(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
            class ElementType(object):
                Unknown = pywbem.Uint16(0)
                Reserved = pywbem.Uint16(1)
                StorageVolume = pywbem.Uint16(2)
                StorageExtent = pywbem.Uint16(3)
                LogicalDisk = pywbem.Uint16(4)
                ThinlyProvisionedStorageVolume = pywbem.Uint16(5)
                ThinlyProvisionedLogicalDisk = pywbem.Uint16(6)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

        class CreateOrModifyLV(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535

        class CreateOrModifyVG(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)

        class CreateOrModifyStoragePool(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535

        class CreateOrModifyElementFromElements(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
            class ElementType(object):
                Unknown = pywbem.Uint16(0)
                Reserved = pywbem.Uint16(1)
                Storage_Volume = pywbem.Uint16(2)
                Storage_Extent = pywbem.Uint16(3)
                Storage_Pool = pywbem.Uint16(4)
                Logical_Disk = pywbem.Uint16(5)
                ThinlyProvisionedStorageVolume = pywbem.Uint16(6)
                ThinlyProvisionedLogicalDisk = pywbem.Uint16(7)
                # DMTF_Reserved = ..
                # Vendor_Specific = 32768..65535

        class CreateOrModifyMDRAID(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
            class Level(object):
                RAID0 = pywbem.Uint16(0)
                RAID1 = pywbem.Uint16(1)
                RAID4 = pywbem.Uint16(4)
                RAID5 = pywbem.Uint16(5)
                RAID6 = pywbem.Uint16(6)
                RAID10 = pywbem.Uint16(10)
        class DeleteMDRAID(object):
            Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Size_Not_Supported = pywbem.Uint32(4097)
            # Method_Reserved = 4098..32767
            # Vendor_Specific = 32768..65535
        class DeleteVG(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4097..32767
            # Vendor_Specific = 32768..65535
        class DeleteLV(object):
            Job_Completed_with_No_Error = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            In_Use = pywbem.Uint32(6)
            # DMTF_Reserved = ..
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            # Method_Reserved = 4097..32767
            # Vendor_Specific = 32768..65535
        class LMI_ScsiScan(object):
            Success = pywbem.Uint32(0)
            Not_Supported = pywbem.Uint32(1)
            Unknown = pywbem.Uint32(2)
            Timeout = pywbem.Uint32(3)
            Failed = pywbem.Uint32(4)
            Invalid_Parameter = pywbem.Uint32(5)
            # DMTF_Reserved = 6..4095
            Method_Parameters_Checked___Job_Started = pywbem.Uint32(4096)
            Invalid_Initiator = pywbem.Uint32(4097)
            No_matching_target_found = pywbem.Uint32(4098)
            No_matching_LUs_found = pywbem.Uint32(4099)
            Prohibited_by_name_binding_configuration = pywbem.Uint32(4100)
            # DMTF_Reserved = ..
            # Vendor_Specific = 32768..65535
