.. _openlmi-config:

Configuration
=============

Configuration files
-------------------

Configuration is stored in ``/etc/openlmi/storage/storage.conf`` and
``/etc/openlmi/openlmi.conf``. ``storage.conf`` is parsed first and
only missing options are parsed from ``openlmi.conf``.

File format
-----------

This file has simple .ini syntax, with ``#`` or ``;`` used for comments.


Default configuration::

     [CIM]
     Namespace=root/cimv2
     SystemClassName=PG_ComputerSystem
     
     [Log]
     Level=ERROR
     Stderr=false
     DebugBlivet=false

======= =================== ==================== ===========
Section Option name         Default value        Desciption
======= =================== ==================== ===========
``CIM`` ``Namespace``       root/cimv2           Namespace where OpenLMI-Storage providers are registered.
``CIM`` ``SystemClassName`` PG_ComputerSystem    Name of CIM_ComputerSystem class, which is used to represent the computer system. It will be used as ``SystemClassName`` property value of various classes.
``Log`` ``Level``           ERROR                Chooses which messages are logged, either to CIMOM and (if configured) to standard error output. Available levels (sorted by severity) are:

                                                    * CRITICAL
                                                    * ERROR
                                                    * WARNING
                                                    * INFO
                                                    * DEBUG
                                                    * TRACE_WARNING
                                                    * TRACE_INFO
                                                    * TRACE_VERBOSE

                                                 Levels below INFO (= TRACE_WARNING, TRACE_INFO and DEBUG) are useful mainly for debugging and bug reporting.
``Log`` ``Stderr``          false                Toggles sending of log messages to standard error output of the CIMOM.
``Log`` ``DebugBlivet``     false                Toggles logging of detailed debug messages in Blivet.
======= =================== ==================== ===========

Persistent setting
------------------

OpenLMI-Storage stores persistent data in ``/var/lib/openlmi-storage/``.
Typically, various :ref:`CIM_SettingData <CIM-SettingData>` instances with
:ref:`ChangeableType <CIM-SettingData-ChangeableType>`
``Changeable - Persistent`` are stored here.

Logging
=======

By default, all log messages with level INFO and above are sent to CIMOM using
standard CMPI ``CMLogMessage`` function. Consult documentation of your CIMOM
how to enable output of these messages into CIMOM logs.

With ``Stderr`` configuration option enabled, all logs are sent both to CIMOM
and to the standard error output of the CIMOM.

Messages with TRACE_WARNING and below are sent to CIMOM using ``CMTraceMessage``
and should be visible in CIMOM tracing log. Again, please consult your CIMOM
documentation how to enable tracing logs.
