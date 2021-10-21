.. _security:

Security 
========

Security Overview
-----------------

There are various security considerations for the POL, sFSP, and the
payloads. This section will describe the various overall concerns and
technology specific aspects.

Protection
~~~~~~~~~~

Critical Resource Lock (hardware)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The platform shall always lock the important resource before it exits
the platform manufacture phase.

The important resource includes but is not limited to flash part, SMRAM,
SMRR, silicon register such as lockable BAR register,

Critical Service Close (software)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The platform shall always close the service that may impact the system
resource.

The service includes but is not limited to SMM registration service,
flash update service.

Critical Resource Access
^^^^^^^^^^^^^^^^^^^^^^^^

The platform shall only allow the critical resource access in the
trusted execution environment such as SMM.

.. _update-1:

Update
^^^^^^

The platform shall only allow firmware update only in the trusted
execution environment such as SMM, or before existing the platform
manufacture phase.

The update must check the secure version number to prevent rollback.

Detection
~~~~~~~~~

Secure Boot (verified boot)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The platform shall enable secure boot. The early boot component shall
verify the next component.

Care must be taken for Time-of-check/Time-of-use (TOC/TOU) attack.

The early component shall copy the next component to a trusted execution
environment, verify and use.

Secure Configuration (data verification)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the configuration has security property, such as lock/unlock policy.
It shall be protected and verified.

The secure configuration may be treated as code and verified together
with secure boot.

Or the secure configuration may be protected by the variable
enhancement, such as RPMB or RPMC.

Recovery
~~~~~~~~

Recovery trigger
^^^^^^^^^^^^^^^^

A platform should have a watchdog to auto trigger recovery process
automatically. Otherwise, it should notify the end user that a manual
recovery is required.

Known good image
^^^^^^^^^^^^^^^^

The recovery process may load a known good image. The known good image
itself shall be protected and follow the detection flow.

The known good image shall be up to date as well, to resist rollback
attack – recovery to an old known bad image.

Attestation
~~~~~~~~~~~

Trusted Boot (measured boot)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The platform shall enable trusted boot. The early boot component shall
measure the next component before transfer control to it, to create a
trust chain.

Completeness
^^^^^^^^^^^^

The platform shall follow TCG specification to measure all required
component. For example, the platform shall measure every boot component.
The platform shall measure any security-related boot configuration.

