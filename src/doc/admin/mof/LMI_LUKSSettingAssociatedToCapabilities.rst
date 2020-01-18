.. _LMI-LUKSSettingAssociatedToCapabilities:

LMI_LUKSSettingAssociatedToCapabilities
---------------------------------------

Class reference
===============
Subclass of :ref:`CIM_SettingAssociatedToCapabilities <CIM-SettingAssociatedToCapabilities>`

This association defines settings that can be used to create or modify elements. Unlike ElementSettingData, these settings are not used to express the characteristics of existing managed elements. 

Typically, the capabilities associated with this class define the characteristics of a service in creating or modifying elements that are dependent on the service directly or indirectly. A CIM Client may use this association to find SettingData instances that can be used to create or modify these dependent elements.


Key properties
^^^^^^^^^^^^^^

| :ref:`Dependent <CIM-Dependency-Dependent>`
| :ref:`Antecedent <CIM-Dependency-Antecedent>`

Local properties
^^^^^^^^^^^^^^^^

*None*

Local methods
^^^^^^^^^^^^^

*None*

Inherited properties
^^^^^^^^^^^^^^^^^^^^

| :ref:`CIM_SettingData <CIM-SettingData>` :ref:`Dependent <CIM-SettingAssociatedToCapabilities-Dependent>`
| :ref:`CIM_Capabilities <CIM-Capabilities>` :ref:`Antecedent <CIM-SettingAssociatedToCapabilities-Antecedent>`
| ``boolean`` :ref:`DefaultSetting <CIM-SettingAssociatedToCapabilities-DefaultSetting>`

Inherited methods
^^^^^^^^^^^^^^^^^

*None*

