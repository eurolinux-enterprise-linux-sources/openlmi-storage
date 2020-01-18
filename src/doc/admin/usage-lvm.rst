Logical Volume management
=========================

Volume Groups (VG) are represented by,
:ref:`LMI_VGStoragePool <LMI-VGStoragePool>` class.


Every :ref:`LMI_VGStoragePool <LMI-VGStoragePool>` instance has associated one
instance of :ref:`LMI_VGStorageSetting <LMI-VGStorageSetting>` representing its
configuration (e.g. volume group extent size) and one instance of
:ref:`LMI_LVStorageCapabilities <LMI-LVStorageCapabilities>`, representing its
ability to create logical volumes (for SMI-S applications).

Physical Volumes (PV) are associated to VGs using
:ref:`LMI_VGAssociatedComponentExtent <LMI-VGAssociatedComponentExtent>`
association.

Logical Volumes (LV) are represented by
:ref:`LMI_LVStorageExtent <LMI-LVStorageExtent>` class. Each
:ref:`LMI_LVStorageExtent <LMI-LVStorageExtent>` instance is associated to its
VG using :ref:`LMI_LVAllocatedFromStoragePool <LMI-LVAllocatedFromStoragePool>`
association.

In addition, LVs are associated to all PVs using
:ref:`LMI_LVBasedOn <LMI-LVBasedOn>` association.


.. _diagram:

Following instance diagram shows one Volume Group ``/dev/myGroup`` based on
three Physical Volumes ``/dev/sda1``, ``/dev/sdb1 `` and ``/dev/sdc1`` and two
Logical Volumes ``myVol1`` and ``myVol2``.

.. figure:: pic/lvm-instance.svg

Note that the diagram is simplified and does not show
:ref:`LMI_LVBasedOn <LMI-LVBasedOn>` association, which associates every
``myVolY`` to ``/dev/sdX1``.

Currently the LVM support is limited to creation and removal of VGs and LVs. It
is not possible to modify existing VG or LV, e.g. add or remove devices to/from
VG and/or resize LVs. In future OpenLMI may be extended to have more
configuration options in :ref:`LMI_VGStorageSetting <LMI-VGStorageSetting>` and
:ref:`LMI_LVStorageSetting <LMI-LVStorageSetting>`.

Useful methods
--------------

:ref:`CreateOrModifyVG <LMI-StorageConfigurationService-CreateOrModifyVG>`
  Creates a Volume Group with given devices. The devices are automatically
  formatted with Physical Volume metadata. Optionally, the Volume Group extent
  size can be specified by using Goal parameter of the method.

:ref:`CreateOrModifyStoragePool <LMI-StorageConfigurationService-CreateOrModifyStoragePool>`
  Creates a Volume Group in SMI-S way.

:ref:`CreateVGStorageSetting <LMI-VGStorageCapabilities-CreateVGStorageSetting>`
  This is helper method to calculate
  :ref:`LMI_VGStorageSetting <LMI-VGStorageSetting>` for given list of devices
  for
  :ref:`CreateOrModifyStoragePool <LMI-StorageConfigurationService-CreateOrModifyStoragePool>`
  method.

:ref:`CreateOrModifyLV <LMI-StorageConfigurationService-CreateOrModifyLV>`
  Creates a Logical Volume from given VG.

:ref:`CreateOrModifyElementFromStoragePool <LMI-StorageConfigurationService-CreateOrModifyElementFromStoragePool>`
  Creates a Logical Volume in SMI-S way.

:ref:`DeleteLV <LMI-StorageConfigurationService-DeleteLV>`
  Destroys a Logical Volume.

:ref:`ReturnToStoragePool <CIM-StorageConfigurationService-ReturnToStoragePool>`
  Destroys a Logical Volume in SMI-S way.

:ref:`DeleteVG <LMI-StorageConfigurationService-DeleteVG>`
  Destroys a Volume Group.

:ref:`DeleteStoragePool <CIM-StorageConfigurationService-DeleteStoragePool>`
  Destroys a Volume Group in SMI-S way.

Use cases
---------

Create Volume Group
^^^^^^^^^^^^^^^^^^^

Use :ref:`CreateOrModifyVG <LMI-StorageConfigurationService-CreateOrModifyVG>`
method. Following example creates a VG '/dev/myGroup' with three members and
with default extent size (4MiB):: 
    
    # Find the devices we want to add to VG
    # (filtering one CIM_StorageExtent.instances()
    # call would be faster, but this is easier to read)
    sda1 = ns.CIM_StorageExtent.first_instance({"Name": "/dev/sda1"})
    sdb1 = ns.CIM_StorageExtent.first_instance({"Name": "/dev/sdb1"})
    sdc1 = ns.CIM_StorageExtent.first_instance({"Name": "/dev/sdc1"})

    # Create the VG
    (ret, outparams, err) = storage_service.SyncCreateOrModifyVG(
            ElementName="myGroup",
            InExtents=[sda1, sdb1, sdc1])
    vg = outparams['Pool'].to_instance()
    print "VG", vg.PoolID, \
            "with extent size", vg.ExtentSize, \
            "and",  vg.RemainingExtents, "free extents created." 

The resulting VG is the same as shown in diagram_ above, except it does not have
any LVs yet.

Create Volume Group in SMI-S way
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

SMI-S applications can use
:ref:`CreateOrModifyStoragePool <LMI-StorageConfigurationService-CreateOrModifyStoragePool>`
method. Following example creates a VG '/dev/myGroup' with three members and
with default extent size (4MiB):: 
    
    # Find the devices we want to add to VG
    # (filtering one CIM_StorageExtent.instances()
    # call would be faster, but this is easier to read)
    sda1 = ns.CIM_StorageExtent.first_instance({"Name": "/dev/sda1"})
    sdb1 = ns.CIM_StorageExtent.first_instance({"Name": "/dev/sdb1"})
    sdc1 = ns.CIM_StorageExtent.first_instance({"Name": "/dev/sdc1"})

    # Create the VG
    (ret, outparams, err) = storage_service.SyncCreateOrModifyStoragePool(
            InExtents=[sda1, sdb1, sdc1],
            ElementName="myGroup")
    vg = outparams['Pool'].to_instance()
    print "VG", vg.PoolID, \
            "with extent size", vg.ExtentSize, \
            "and",  vg.RemainingExtents, "free extents created." 

The resulting VG is the same as shown in diagram_ above, except it does not have
any LVs yet.


Create Volume Group with specific extent size
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use
:ref:`CreateVGStorageSetting <LMI-VGStorageCapabilities-CreateVGStorageSetting>`
to create :ref:`LMI_VGStorageSetting <LMI-VGStorageSetting>`, modify its
:ref:`ExtentSize <LMI-VGStorageSetting-ExtentSize>` property with desired
extent size and finally call
:ref:`CreateOrModifyVG <LMI-StorageConfigurationService-CreateOrModifyVG>` with
the setting as ``Goal`` parameter. Following example creates a VG
'/dev/myGroup' with three members and with 1MiB extent size (4MiB)::

    # Find the devices we want to add to VG
    # (filtering one CIM_StorageExtent.instances()
    # call would be faster, but this is easier to read)
    sda1 = ns.CIM_StorageExtent.first_instance({"Name": "/dev/sda1"})
    sdb1 = ns.CIM_StorageExtent.first_instance({"Name": "/dev/sdb1"})
    sdc1 = ns.CIM_StorageExtent.first_instance({"Name": "/dev/sdc1"})

    # Create the LMI_VGStorageSetting
    vg_caps = ns.LMI_VGStorageCapabilities.first_instance()
    (ret, outparams, err) = vg_caps.CreateVGStorageSetting(
            InExtents = [sda1, sdb1, sdc1])
    setting = outparams['Setting'].to_instance()
    # Modify the LMI_VGStorageSetting
    setting.ExtentSize = MEGABYTE
    settinh.push()

    # Create the VG
    # (either of CreateOrModifyStoragePool or CreateOrModifyVG
    # can be used with the same result) 
    (ret, outparams, err) = storage_service.SyncCreateOrModifyStoragePool(
            InExtents=[sda1, sdb1, sdc1],
            ElementName="myGroup",
            Goal=setting)
    vg = outparams['Pool'].to_instance()
    print "VG", vg.PoolID, \
            "with extent size", vg.ExtentSize, \
            "and",  vg.RemainingExtents, "free extents created." 
    
List Physical Volumes of a Volume Group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enumerate :ref:`VGAssociatedComponentExtent <LMI-VGAssociatedComponentExtent>`
associations of the VG.

Following code lists all PVs of ``/dev/myGroup``::

    # Find the VG
    vg = ns.LMI_VGStoragePool.first_instance({"Name": "/dev/mapper/myGroup"})
    pvs = vg.associators(AssocClass="LMI_VGAssociatedComponentExtent")
    for pv in pvs:
        print "Found PV", pv.DeviceID

Create Logical Volume
^^^^^^^^^^^^^^^^^^^^^

Use :ref:`CreateOrModifyLV <LMI-StorageConfigurationService-CreateOrModifyLV>`
method. Following example creates two 100MiB volumes:: 
    
    # Find the VG
    vg = ns.LMI_VGStoragePool.first_instance({"Name": "/dev/mapper/myGroup"})

    # Create the LV
    (ret, outparams, err) = storage_service.SyncCreateOrModifyLV(
            ElementName="Vol1",
            InPool=vg,
            Size=100 * MEGABYTE)
    lv = outparams['TheElement'].to_instance()
    print "LV", lv.DeviceID, \
            "with", lv.BlockSize * lv.NumberOfBlocks,\
            "bytes created."

    # Create the second LV
    (ret, outparams, err) = storage_service.SyncCreateOrModifyLV(
            ElementName="Vol2",
            InPool=vg,
            Size=100 * MEGABYTE)
    lv = outparams['TheElement'].to_instance()
    print "LV", lv.DeviceID, \
            "with", lv.BlockSize * lv.NumberOfBlocks, \
            "bytes created."

The resulting LVs are the same as shown in diagram_ above.


Create Logical Volume in SMI-S way
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use
:ref:`CreateOrModifyElementFromStoragePool <LMI-StorageConfigurationService-CreateOrModifyElementFromStoragePool>`
method. The code is the same as in previous sample, just different method is
used::

    # Find the VG
    vg = ns.LMI_VGStoragePool.first_instance({"Name": "/dev/mapper/myGroup"})

    # Create the LV
    (ret, outparams, err) = storage_service.SyncCreateOrModifyElementFromStoragePool(
            ElementName="Vol1",
            InPool=vg,
            Size=100 * MEGABYTE)
    lv = outparams['TheElement'].to_instance()
    print "LV", lv.DeviceID, \
            "with", lv.BlockSize * lv.NumberOfBlocks,\
            "bytes created."

    # Create the second LV
    (ret, outparams, err) = storage_service.SyncCreateOrModifyElementFromStoragePool(
            ElementName="Vol2",
            InPool=vg,
            Size=100 * MEGABYTE)
    lv = outparams['TheElement'].to_instance()
    print "LV", lv.DeviceID, \
            "with", lv.BlockSize * lv.NumberOfBlocks, \
            "bytes created."

Delete VG
^^^^^^^^^

Call :ref:`DeleteVG <LMI-StorageConfigurationService-DeleteVG>` method::

    vg = ns.LMI_VGStoragePool.first_instance({"Name": "/dev/mapper/myGroup"})
    (ret, outparams, err) = storage_service.SyncDeleteVG(
            Pool = vg)

Delete LV
^^^^^^^^^

Call :ref:`DeleteLV <LMI-StorageConfigurationService-DeleteLV>` method::

   lv = ns.LMI_LVStorageExtent.first_instance({"Name": "/dev/mapper/myGroup-Vol2"})
   (ret, outparams, err) = storage_service.SyncDeleteLV(
           TheElement=lv)

Future direction
----------------

In future, we might implement:

* Modification of existing VGs and LVs, for example adding/removing devices
  and resizing LVs.

* LVs with stripping and mirroring.

* Clustered VGs and LVs.

* Thin pools and volumes.

* Snapshots.

* Indications of various events.

