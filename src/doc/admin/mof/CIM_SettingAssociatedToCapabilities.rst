.. _CIM-SettingAssociatedToCapabilities:

CIM_SettingAssociatedToCapabilities
-----------------------------------

Class reference
===============
Subclass of :ref:`CIM_Dependency <CIM-Dependency>`

This association defines settings that can be used to create or modify elements. Unlike ElementSettingData, these settings are not used to express the characteristics of existing managed elements. 

Typically, the capabilities associated with this class define the characteristics of a service in creating or modifying elements that are dependent on the service directly or indirectly. A CIM Client may use this association to find SettingData instances that can be used to create or modify these dependent elements.


Key properties
^^^^^^^^^^^^^^

| :ref:`Dependent <CIM-Dependency-Dependent>`
| :ref:`Antecedent <CIM-Dependency-Antecedent>`

Local properties
^^^^^^^^^^^^^^^^

.. _CIM-SettingAssociatedToCapabilities-Dependent:

:ref:`CIM_SettingData <CIM-SettingData>` **Dependent**

    The Setting.

    
.. _CIM-SettingAssociatedToCapabilities-Antecedent:

:ref:`CIM_Capabilities <CIM-Capabilities>` **Antecedent**

    The Capabilities.

    
.. _CIM-SettingAssociatedToCapabilities-DefaultSetting:

``boolean`` **DefaultSetting**

    If an element whose characteristics are described by the associated Capabilities instance has a dependent element created or modified without specifying an associated SettingData instance, then the default SettingData will be used in that operation.

    

Local methods
^^^^^^^^^^^^^

*None*

Inherited properties
^^^^^^^^^^^^^^^^^^^^

*None*

Inherited methods
^^^^^^^^^^^^^^^^^

*None*

