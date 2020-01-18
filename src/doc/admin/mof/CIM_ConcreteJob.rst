.. _CIM-ConcreteJob:

CIM_ConcreteJob
---------------

Class reference
===============
Subclass of :ref:`CIM_Job <CIM-Job>`

A concrete version of Job. This class represents a generic and instantiable unit of work, such as a batch or a print job.


Key properties
^^^^^^^^^^^^^^

| :ref:`InstanceID <CIM-ConcreteJob-InstanceID>`

Local properties
^^^^^^^^^^^^^^^^

.. _CIM-ConcreteJob-InstanceID:

``string`` **InstanceID**

    Within the scope of the instantiating Namespace, InstanceID opaquely and uniquely identifies an instance of this class. In order to ensure uniqueness within the NameSpace, the value of InstanceID SHOULD be constructed using the following 'preferred' algorithm: 

    <OrgID>:<LocalID> 

    Where <OrgID> and <LocalID> are separated by a colon ':', and where <OrgID> must include a copyrighted, trademarked or otherwise unique name that is owned by the business entity that is creating or defining the InstanceID, or that is a registered ID that is assigned to the business entity by a recognized global authority. (This requirement is similar to the <Schema Name>_<Class Name> structure of Schema class names.) In addition, to ensure uniqueness <OrgID> must not contain a colon (':'). When using this algorithm, the first colon to appear in InstanceID must appear between <OrgID> and <LocalID>. 

    <LocalID> is chosen by the business entity and should not be re-used to identify different underlying (real-world) elements. If the above 'preferred' algorithm is not used, the defining entity must assure that the resulting InstanceID is not re-used across any InstanceIDs produced by this or other providers for the NameSpace of this instance. 

    For DMTF defined instances, the 'preferred' algorithm must be used with the <OrgID> set to 'CIM'.

    
.. _CIM-ConcreteJob-JobOutParameters:

``string`` **JobOutParameters**

    The output, (including inout), parameters of the Job, formatted as an EmbeddedObject (with a predefined class name of "__JobOutParameters". 

    This property shall be NULL unless JobStatus has the value Completed.

    In the case where a Job represents an intrinsic operation or an extrinsic method call, this property contains the parameters and return value of that call.Each parameter is mapped to a corresponding property of the same type. The returnvalue is mapped to a property with the name __ReturnValue of the same type.

    The value of each embedded property shall be the value of the corresponding output pararmeter or ReturnValue at the time the job completed.

    
.. _CIM-ConcreteJob-JobState:

``uint16`` **JobState**

    JobState is an integer enumeration that indicates the operational state of a Job. It can also indicate transitions between these states, for example, 'Shutting Down' and 'Starting'. Following is a brief description of the states: 

    New (2) indicates that the job has never been started. 

    Starting (3) indicates that the job is moving from the 'New', 'Suspended', or 'Service' states into the 'Running' state. 

    Running (4) indicates that the Job is running. 

    Suspended (5) indicates that the Job is stopped, but can be restarted in a seamless manner. 

    Shutting Down (6) indicates that the job is moving to a 'Completed', 'Terminated', or 'Killed' state. 

    Completed (7) indicates that the job has completed normally. 

    Terminated (8) indicates that the job has been stopped by a 'Terminate' state change request. The job and all its underlying processes are ended and can be restarted (this is job-specific) only as a new job. 

    Killed (9) indicates that the job has been stopped by a 'Kill' state change request. Underlying processes might have been left running, and cleanup might be required to free up resources. 

    Exception (10) indicates that the Job is in an abnormal state that might be indicative of an error condition. Actual status might be displayed though job-specific objects. 

    Service (11) indicates that the Job is in a vendor-specific state that supports problem discovery, or resolution, or both.

    Query pending (12) waiting for a client to resolve a query

    
    ============ ===============
    ValueMap     Values         
    ============ ===============
    2            New            
    3            Starting       
    4            Running        
    5            Suspended      
    6            Shutting Down  
    7            Completed      
    8            Terminated     
    9            Killed         
    10           Exception      
    11           Service        
    12           Query Pending  
    13..32767    DMTF Reserved  
    32768..65535 Vendor Reserved
    ============ ===============
    
.. _CIM-ConcreteJob-TimeOfLastStateChange:

``datetime`` **TimeOfLastStateChange**

    The date or time when the state of the Job last changed. If the state of the Job has not changed and this property is populated, then it must be set to a 0 interval value. If a state change was requested, but rejected or not yet processed, the property must not be updated.

    
.. _CIM-ConcreteJob-Name:

``string`` **Name**

    The user-friendly name for this instance of a Job. In addition, the user-friendly name can be used as a property for a search or query. (Note: Name does not have to be unique within a namespace.)

    
.. _CIM-ConcreteJob-MethodName:

``string`` **MethodName**

    If not NULL, the name of the intrinsic operation or extrinsic method for which this Job represents an invocation.

    When not NULL, and if an extrinsic method, the format shall be <classPath>.MethodName, where classPath is a WBEM-URI-TypedClassPath or a WBEM-URI-UntypedClassPath as defined by DSP0207. And where methodName is a method of that class.

    When not NULL, and if an intrinsic operation, the format shall be <namespacePath>.OperationName, where namespacePath is a WBEM-URI-TypedNamespacePath or a WBEM-URI-UntypedNamespacePath as defined by DSP0207. And where OperationName is either the name of a generic operation as defined in DSP0223 or is the name of a protocol specific operation as defined for the protocol used to retrieve the instance.

    
.. _CIM-ConcreteJob-JobInParameters:

``string`` **JobInParameters**

    The input, (including inout), parameters of the Job, formatted as an EmbeddedObject (with a predefined class name of "__JobInParameters". In the case where a Job represents an intrinsic operation or an extrinsic method call, this property contains the input parameters of that call.Each input parameter is mapped to a corresponding property of the same type.

    The value of each embedded property shall be the value of the corresponding input pararmeter at the time the job was started.

    
.. _CIM-ConcreteJob-TimeBeforeRemoval:

``datetime`` **TimeBeforeRemoval**

    The amount of time that the Job is retained after it has finished executing, either succeeding or failing in that execution. The job must remain in existence for some period of time regardless of the value of the DeleteOnCompletion property. 

    The default is five minutes.

    

Local methods
^^^^^^^^^^^^^

    .. _CIM-ConcreteJob-RequestStateChange:

``uint32`` **RequestStateChange** (``uint16`` RequestedState, ``datetime`` TimeoutPeriod)

    Requests that the state of the job be changed to the value specified in the RequestedState parameter. Invoking the RequestStateChange method multiple times could result in earlier requests being overwritten or lost. 

    If 0 is returned, then the task completed successfully. Any other return code indicates an error condition.

    
    ============ ==============================================
    ValueMap     Values                                        
    ============ ==============================================
    0            Completed with No Error                       
    1            Not Supported                                 
    2            Unknown/Unspecified Error                     
    3            Can NOT complete within Timeout Period        
    4            Failed                                        
    5            Invalid Parameter                             
    6            In Use                                        
    ..           DMTF Reserved                                 
    4096         Method Parameters Checked - Transition Started
    4097         Invalid State Transition                      
    4098         Use of Timeout Parameter Not Supported        
    4099         Busy                                          
    4100..32767  Method Reserved                               
    32768..65535 Vendor Specific                               
    ============ ==============================================
    
    **Parameters**
    
        *IN* ``uint16`` **RequestedState**
            RequestStateChange changes the state of a job. The possible values are as follows: 

            Start (2) changes the state to 'Running'. 

            Suspend (3) stops the job temporarily. The intention is to subsequently restart the job with 'Start'. It might be possible to enter the 'Service' state while suspended. (This is job-specific.) 

            Terminate (4) stops the job cleanly, saving data, preserving the state, and shutting down all underlying processes in an orderly manner. 

            Kill (5) terminates the job immediately with no requirement to save data or preserve the state. 

            Service (6) puts the job into a vendor-specific service state. It might be possible to restart the job.

            
            ============ ===============
            ValueMap     Values         
            ============ ===============
            2            Start          
            3            Suspend        
            4            Terminate      
            5            Kill           
            6            Service        
            7..32767     DMTF Reserved  
            32768..65535 Vendor Reserved
            ============ ===============
            
        
        *IN* ``datetime`` **TimeoutPeriod**
            A timeout period that specifies the maximum amount of time that the client expects the transition to the new state to take. The interval format must be used to specify the TimeoutPeriod. A value of 0 or a null parameter indicates that the client has no time requirements for the transition. 

            If this property does not contain 0 or null and the implementation does not support this parameter, a return code of 'Use Of Timeout Parameter Not Supported' must be returned.

            
        
    
    .. _CIM-ConcreteJob-GetErrors:

``uint32`` **GetErrors** (``string[]`` Errors)

    If JobState is "Completed" and Operational Status is "Completed" then no instance of CIM_Error is returned. 

    If JobState is "Exception" then GetErrors may return intances of CIM_Error related to the execution of the procedure or method invoked by the job.

    If Operatational Status is not "OK" or "Completed"then GetErrors may return CIM_Error instances related to the running of the job.

    
    ============ =================
    ValueMap     Values           
    ============ =================
    0            Success          
    1            Not Supported    
    2            Unspecified Error
    3            Timeout          
    4            Failed           
    5            Invalid Parameter
    6            Access Denied    
    ..           DMTF Reserved    
    32768..65535 Vendor Specific  
    ============ =================
    
    **Parameters**
    
        *OUT* ``string[]`` **Errors**
            If the OperationalStatus on the Job is not "OK", then this method will return one or more CIM Error instance(s). Otherwise, when the Job is "OK", null is returned.

            
        
    
    .. _CIM-ConcreteJob-GetError:

``uint32`` **GetError** (``string`` Error)

    GetError is deprecated because Error should be an array,not a scalar.

    When the job is executing or has terminated without error, then this method returns no CIM_Error instance. However, if the job has failed because of some internal problem or because the job has been terminated by a client, then a CIM_Error instance is returned.

    
    ============ =================
    ValueMap     Values           
    ============ =================
    0            Success          
    1            Not Supported    
    2            Unspecified Error
    3            Timeout          
    4            Failed           
    5            Invalid Parameter
    6            Access Denied    
    ..           DMTF Reserved    
    32768..65535 Vendor Specific  
    ============ =================
    
    **Parameters**
    
        *OUT* ``string`` **Error**
            If the OperationalStatus on the Job is not "OK", then this method will return a CIM Error instance. Otherwise, when the Job is "OK", null is returned.

            
        
    

Inherited properties
^^^^^^^^^^^^^^^^^^^^

| ``uint16`` :ref:`HealthState <CIM-ManagedSystemElement-HealthState>`
| ``string[]`` :ref:`StatusDescriptions <CIM-ManagedSystemElement-StatusDescriptions>`
| ``uint32`` :ref:`Priority <CIM-Job-Priority>`
| ``uint16`` :ref:`CommunicationStatus <CIM-ManagedSystemElement-CommunicationStatus>`
| ``uint32`` :ref:`JobRunTimes <CIM-Job-JobRunTimes>`
| ``string`` :ref:`OtherRecoveryAction <CIM-Job-OtherRecoveryAction>`
| ``string`` :ref:`Status <CIM-ManagedSystemElement-Status>`
| ``datetime`` :ref:`UntilTime <CIM-Job-UntilTime>`
| ``string`` :ref:`Description <CIM-ManagedElement-Description>`
| ``sint8`` :ref:`RunDay <CIM-Job-RunDay>`
| ``uint8`` :ref:`RunMonth <CIM-Job-RunMonth>`
| ``uint16`` :ref:`ErrorCode <CIM-Job-ErrorCode>`
| ``uint16`` :ref:`RecoveryAction <CIM-Job-RecoveryAction>`
| ``uint16`` :ref:`PercentComplete <CIM-Job-PercentComplete>`
| ``uint16`` :ref:`LocalOrUtcTime <CIM-Job-LocalOrUtcTime>`
| ``uint16`` :ref:`DetailedStatus <CIM-ManagedSystemElement-DetailedStatus>`
| ``datetime`` :ref:`InstallDate <CIM-ManagedSystemElement-InstallDate>`
| ``sint8`` :ref:`RunDayOfWeek <CIM-Job-RunDayOfWeek>`
| ``string`` :ref:`ElementName <CIM-ManagedElement-ElementName>`
| ``string`` :ref:`JobStatus <CIM-Job-JobStatus>`
| ``datetime`` :ref:`ElapsedTime <CIM-Job-ElapsedTime>`
| ``string`` :ref:`Caption <CIM-ManagedElement-Caption>`
| ``boolean`` :ref:`DeleteOnCompletion <CIM-Job-DeleteOnCompletion>`
| ``datetime`` :ref:`TimeSubmitted <CIM-Job-TimeSubmitted>`
| ``uint16`` :ref:`PrimaryStatus <CIM-ManagedSystemElement-PrimaryStatus>`
| ``string`` :ref:`ErrorDescription <CIM-Job-ErrorDescription>`
| ``datetime`` :ref:`RunStartInterval <CIM-Job-RunStartInterval>`
| ``uint64`` :ref:`Generation <CIM-ManagedElement-Generation>`
| ``datetime`` :ref:`ScheduledStartTime <CIM-Job-ScheduledStartTime>`
| ``uint16[]`` :ref:`OperationalStatus <CIM-ManagedSystemElement-OperationalStatus>`
| ``uint16`` :ref:`OperatingStatus <CIM-ManagedSystemElement-OperatingStatus>`
| ``string`` :ref:`Notify <CIM-Job-Notify>`
| ``datetime`` :ref:`StartTime <CIM-Job-StartTime>`
| ``string`` :ref:`Owner <CIM-Job-Owner>`

Inherited methods
^^^^^^^^^^^^^^^^^

| :ref:`KillJob <CIM-Job-KillJob>`

