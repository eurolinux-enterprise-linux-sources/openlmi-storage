.. _LMI-LUKSFormatSetting:

LMI_LUKSFormatSetting
---------------------

Class reference
===============
Subclass of :ref:`LMI_EncryptionFormatSetting <LMI-EncryptionFormatSetting>`

Parameters used to create LUKS format by LMI_LUKSConfigurationService. This class is currently not implemented and may be changed in future released on OpenLMI.


Key properties
^^^^^^^^^^^^^^

| :ref:`InstanceID <CIM-ManagedElement-InstanceID>`

Local properties
^^^^^^^^^^^^^^^^

.. _LMI-LUKSFormatSetting-OtherChainMode:

``string`` **OtherChainMode**

    Name of other block cipher encryption mode if ChainMode property has value of "Other".

    
.. _LMI-LUKSFormatSetting-IVMode:

``uint16`` **IVMode**

    Initialization Vector (IV) used for selected block mode (if block mode requires IV).

    
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
    
.. _LMI-LUKSFormatSetting-ChainMode:

``uint16`` **ChainMode**

    Block cipher encryption mode.

    
    ======== ======
    ValueMap Values
    ======== ======
    0        CBC   
    1        XTS   
    2        Other 
    ======== ======
    
.. _LMI-LUKSFormatSetting-OtherIVMode:

``string`` **OtherIVMode**

    Name of other initialization vector if IVMode property has value of "Other".

    
.. _LMI-LUKSFormatSetting-OtherCipher:

``string`` **OtherCipher**

    Name of other encryption block cipher if Cipher property has value of "Other".

    
.. _LMI-LUKSFormatSetting-Cipher:

``uint16`` **Cipher**

    Encryption block cipher.

    
    ======== ========
    ValueMap Values  
    ======== ========
    0        Blowfish
    1        Serpent 
    2        AES     
    65535    Other   
    ======== ========
    
.. _LMI-LUKSFormatSetting-ESSIVHashAlhorithm:

``uint16`` **ESSIVHashAlhorithm**

    Hash algorithm used to derive initial vector. Used only if IVMode has value of "ESSIV"

    
    ======== ======
    ValueMap Values
    ======== ======
    0        SHA256
    1        SHA1  
    2        MD5   
    3        Other 
    ======== ======
    
.. _LMI-LUKSFormatSetting-KeySize:

``uint16`` **KeySize**

    Master key size in bits. The argument has to be a multiple of 8.

    
.. _LMI-LUKSFormatSetting-OtherESSIVHashAlhorithm:

``string`` **OtherESSIVHashAlhorithm**

    Name of other hash algorithm to derive initial vector if ESSIVHashAlhorithm has value of "Other".

    

Local methods
^^^^^^^^^^^^^

*None*

Inherited properties
^^^^^^^^^^^^^^^^^^^^

| ``string`` :ref:`ElementName <CIM-SettingData-ElementName>`
| ``string`` :ref:`InstanceID <CIM-SettingData-InstanceID>`
| ``string`` :ref:`Caption <CIM-ManagedElement-Caption>`
| ``string`` :ref:`ConfigurationName <CIM-SettingData-ConfigurationName>`
| ``uint64`` :ref:`Generation <CIM-ManagedElement-Generation>`
| ``uint16`` :ref:`ChangeableType <CIM-SettingData-ChangeableType>`
| ``string`` :ref:`Description <CIM-ManagedElement-Description>`

Inherited methods
^^^^^^^^^^^^^^^^^

*None*

