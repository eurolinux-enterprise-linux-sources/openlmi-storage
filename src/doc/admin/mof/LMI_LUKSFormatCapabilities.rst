.. _LMI-LUKSFormatCapabilities:

LMI_LUKSFormatCapabilities
--------------------------

Class reference
===============
Subclass of :ref:`LMI_EncryptionFormatCapabilities <LMI-EncryptionFormatCapabilities>`

LMI_LUKSFormatCapabilities specifies combination of property values, which can be used to create a LUKS format using LMI_LUKSConfigurationService. This class is currently not implemented and may be changed in future released on OpenLMI.


Key properties
^^^^^^^^^^^^^^

| :ref:`InstanceID <CIM-ManagedElement-InstanceID>`

Local properties
^^^^^^^^^^^^^^^^

.. _LMI-LUKSFormatCapabilities-OtherChainModes:

``string[]`` **OtherChainModes**

    Array of names of supported encryption modes which have value "Other" in ChainModes property.

    
.. _LMI-LUKSFormatCapabilities-Ciphers:

``uint16[]`` **Ciphers**

    Array of supported encryption block ciphers.

    
    ======== ========
    ValueMap Values  
    ======== ========
    0        Blowfish
    1        Serpent 
    2        AES     
    65535    Other   
    ======== ========
    
.. _LMI-LUKSFormatCapabilities-OtherCiphers:

``string[]`` **OtherCiphers**

    Array of names of supported block ciphers for ciphers which have value "Other" in Ciphers property. Not every combination of Cipher and ChainMode is allowed. All possible combinations can be retrieved by GetSupportedChainModes() method.

    
.. _LMI-LUKSFormatCapabilities-OtherESSIVHashAlhorithms:

``string[]`` **OtherESSIVHashAlhorithms**

    Array of names of other hash algorithms to derive initial vector in "ESSIV" mode, which have value "Other" in ESSIVHashAlhorithms property.

    
.. _LMI-LUKSFormatCapabilities-ESSIVHashAlhorithms:

``uint16[]`` **ESSIVHashAlhorithms**

    Array of supported hash algorithms used to derive initial vector in "ESSIV" mode.

    
    ======== ======
    ValueMap Values
    ======== ======
    0        SHA256
    1        SHA1  
    2        MD5   
    3        Other 
    ======== ======
    
.. _LMI-LUKSFormatCapabilities-IVModes:

``uint16[]`` **IVModes**

    Array of supported initialization vector modes.

    
    ======== =======
    ValueMap Values 
    ======== =======
    0        Plain  
    1        Plain64
    2        ESSIV  
    3        BENBI  
    4        Null   
    5        LMK    
    65535    Other  
    ======== =======
    
.. _LMI-LUKSFormatCapabilities-ChainModes:

``uint16[]`` **ChainModes**

    Array of supported encryption modes.

    
    ======== ======
    ValueMap Values
    ======== ======
    0        CTR   
    1        CBC   
    2        ECB   
    3        XTR   
    4        LRW   
    5        PCBC  
    65535    Other 
    ======== ======
    

Local methods
^^^^^^^^^^^^^

    .. _LMI-LUKSFormatCapabilities-GetSupportedChainModes:

``uint32`` **GetSupportedChainModes** (``uint16`` Cipher, ``string`` OtherCipher, ``uint16[]`` ChainModes, ``string[]`` OtherChainModes, ``uint16[]`` KeySizeMin, ``uint16[]`` KeySizeMax)

    Discover all encryption modes which are supported for given block cipher. Minimum and maximum key sizes are also returned.

    
    **Parameters**
    
        *IN* ``uint16`` **Cipher**
            Encryption block cipher.

            
            ======== ========
            ValueMap Values  
            ======== ========
            0        Blowfish
            1        Serpent 
            2        AES     
            65535    Other   
            ======== ========
            
        
        *IN* ``string`` **OtherCipher**
            Name of other encryption block cipher if Cipher property has value of "Other".

            
        
        *OUT* ``uint16[]`` **ChainModes**
            Array of supported encryption modes for given cipher.

            
            ======== ======
            ValueMap Values
            ======== ======
            0        CTR   
            1        CBC   
            2        ECB   
            3        XTR   
            4        LRW   
            5        PCBC  
            65535    Other 
            ======== ======
            
        
        *OUT* ``string[]`` **OtherChainModes**
            Array of names of supported encryption modes which have value "Other" in ChainModes parameter.

            
        
        *OUT* ``uint16[]`` **KeySizeMin**
            Array of integers specifying the minimum key size in bytes corresponding to given block cipher and entry in ChainModes parameter.

            
        
        *OUT* ``uint16[]`` **KeySizeMax**
            Array of integers specifying the maximum key size in bytes corresponding to given block cipher and entry in ChainModes parameter.

            
        
    

Inherited properties
^^^^^^^^^^^^^^^^^^^^

| ``string`` :ref:`ElementName <CIM-Capabilities-ElementName>`
| ``string`` :ref:`Description <CIM-ManagedElement-Description>`
| ``string`` :ref:`InstanceID <CIM-Capabilities-InstanceID>`
| ``uint64`` :ref:`Generation <CIM-ManagedElement-Generation>`
| ``string`` :ref:`Caption <CIM-ManagedElement-Caption>`

Inherited methods
^^^^^^^^^^^^^^^^^

| :ref:`CreateGoalSettings <CIM-Capabilities-CreateGoalSettings>`

