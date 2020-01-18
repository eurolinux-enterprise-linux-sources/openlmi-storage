.. _CIM-InstMethodCall:

CIM_InstMethodCall
------------------

Class reference
===============
Subclass of :ref:`CIM_InstIndication <CIM-InstIndication>`

CIM_InstMethodCall notifies when an instance's method is invoked.


Key properties
^^^^^^^^^^^^^^


Local properties
^^^^^^^^^^^^^^^^

.. _CIM-InstMethodCall-MethodName:

``string`` **MethodName**

    The name of the method invoked.

    
.. _CIM-InstMethodCall-ReturnValueType:

``uint16`` **ReturnValueType**

    The type of the method return value.

    
    ======== =============
    ValueMap Values       
    ======== =============
    2        boolean      
    3        string       
    4        char16       
    5        uint8        
    6        sint8        
    7        uint16       
    8        sint16       
    9        uint32       
    10       sint32       
    11       uint64       
    12       sint64       
    13       datetime     
    14       real32       
    15       real64       
    16       reference    
    ..       DMTF Reserved
    ======== =============
    
.. _CIM-InstMethodCall-MethodParameters:

``string`` **MethodParameters**

    The parameters of the method, formatted as an EmbeddedObject (with a predefined class name of "__MethodParameters".

    
.. _CIM-InstMethodCall-ReturnValue:

``string`` **ReturnValue**

    ReturnValue's data is dependent on the PreCall property. When PreCall is TRUE, this property is NULL describing that there is no method return value (since the method has not yet executed). When PreCall is FALSE, ReturnValue contains a string representation of the method's return value.

    
.. _CIM-InstMethodCall-Error:

``instance[]`` **Error**

    Error's data is dependent on the PreCall property. When PreCall is TRUE, this property is NULL describing that there is no method Error instances (since the method has not yet executed). When PreCall is FALSE, Error contains an array of zero or more entries containing CIM_ERROR instances represented as an array of Embedded Instances.

    
.. _CIM-InstMethodCall-PreCall:

``boolean`` **PreCall**

    Boolean indicating whether the Indication is sent before the method begins executing (TRUE) or when the method completes (FALSE). When TRUE, the inherited property SourceInstance contains the value of the instance (the properties defined by the Filter's Query clause), before execution of the method. When PreCall is FALSE, SourceInstance embeds the instance as it appears after the completion of the method.

    

Local methods
^^^^^^^^^^^^^

*None*

Inherited properties
^^^^^^^^^^^^^^^^^^^^

| ``string`` :ref:`IndicationFilterName <CIM-Indication-IndicationFilterName>`
| ``string`` :ref:`OtherSeverity <CIM-Indication-OtherSeverity>`
| ``sint64`` :ref:`SequenceNumber <CIM-Indication-SequenceNumber>`
| ``string`` :ref:`SourceInstanceHost <CIM-InstIndication-SourceInstanceHost>`
| ``datetime`` :ref:`IndicationTime <CIM-Indication-IndicationTime>`
| ``string`` :ref:`SourceInstance <CIM-InstIndication-SourceInstance>`
| ``string`` :ref:`SequenceContext <CIM-Indication-SequenceContext>`
| ``string[]`` :ref:`CorrelatedIndications <CIM-Indication-CorrelatedIndications>`
| ``uint16`` :ref:`PerceivedSeverity <CIM-Indication-PerceivedSeverity>`
| ``string`` :ref:`IndicationIdentifier <CIM-Indication-IndicationIdentifier>`
| ``string`` :ref:`SourceInstanceModelPath <CIM-InstIndication-SourceInstanceModelPath>`

Inherited methods
^^^^^^^^^^^^^^^^^

*None*

