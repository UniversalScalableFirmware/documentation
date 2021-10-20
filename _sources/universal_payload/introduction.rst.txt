.. _intro:

Introduction
=============

THIS SPECIFICATION IS PROVIDED "AS IS" WITH NO WARRANTIES WHATSOEVER, 
INCLUDING ANY WARRANTY OF MERCHANTABILITY, NONINFRINGEMENT, FITNESS 
FOR ANY PARTICULAR PURPOSE, OR ANY WARRANTY OTHERWISE ARISING OUT OF 
ANY PROPOSAL, SPECIFICATION OR SAMPLE. 

This specification is an intermediate draft for comment only and is
subject to change without notice. Readers should not design products
based on this document.

The **Universal Payload Project Team** provides the content on this site under a 
**Creative Commons Attribution 4.0 International license** (https://spdx.org/licenses/CC-BY-4.0.html) 
except where otherwise noted.

\*Other names and brands may be claimed as the property of others.

Purpose
---------

The purpose of this document is to describe the architecture and interfaces between the bootloader and the payload. Bootloader or payload implementation specific details are outside the scope of this document.

Intended Audience
-------------------

This document is targeted at all platform and system developers who need the bootloader or the payload supports the unified bootloader and payload interface. This includes, but is not limited to: BIOS developers, bootloader developers, system integrators, as well as end users.

Related Documents
-------------------

-  Unified Extensible Firmware Interface (UEFI) Specification

   http://www.uefi.org/specifications

-  Platform Initialization (PI) Specification v1.7
   https://uefi.org/sites/default/files/resources/PI_Spec_1_7_final_Jan_2019.pdf

-  Portable Executable (PE) and Common Object File Format (COFF)

   https://docs.microsoft.com/en-us/windows/win32/debug/pe-format

-  PE authentication

   https://download.microsoft.com/download/9/c/5/9c5b2167-8017-4bae-9fde-d599bac8184a/Authenticode_PE.docx

-  ACPI DBG2 table

   http://download.microsoft.com/download/9/4/5/945703CA-EF1F-496F-ADCF-3332CE5594FD/microsoft-debug-port-table-2-CP.docx

-  ACPI specification 6.3

   https://uefi.org/sites/default/files/resources/ACPI_6_3_final_Jan30.pdf

-  Device tree specification

   https://buildmedia.readthedocs.org/media/pdf/devicetree-specification/latest/devicetree-specification.pdf

