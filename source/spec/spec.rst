Universal interface between bootloader and payload
===================================================

   | Version 0.7 Draft
   | 9/25/2020

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


**Contents**

`Unified interface between bootloader and payload
1 <#unified-interface-between-bootloader-and-payload>`__

`1 Introduction 4 <#introduction>`__

`1.1 Purpose 4 <#purpose>`__

`1.2 Intended Audience 4 <#intended-audience>`__

`1.3 Related Documents 4 <#related-documents>`__

`2 Overview 5 <#overview>`__

`2.1 Bootloaders 6 <#bootloaders>`__

`2.2 Payloads 7 <#payloads>`__

`2.3 Current Bootloader and Payload interfaces
8 <#current-bootloader-and-payload-interfaces>`__

`2.4 OS interfaces 10 <#os-interfaces>`__

`2.4.1 OS Boot protocols 10 <#os-boot-protocols>`__

`2.4.2 Data interface 10 <#data-interface>`__

`2.5 Payload principle 11 <#payload-principle>`__

`2.6 Security 12 <#security>`__

`3 Payload Image Format 12 <#payload-image-format>`__

`3.1 Payload Image Standard Header
13 <#payload-image-standard-header>`__

`3.2 Payload Image Relocation Table
15 <#payload-image-relocation-table>`__

`3.3 Payload Image Authentication Table
16 <#payload-image-authentication-table>`__

`4 Hand-off state 18 <#hand-off-state>`__

`4.1 IA-32 and x64 Platforms 18 <#ia-32-and-x64-platforms>`__

`4.1.1 State of silicon 18 <#state-of-silicon>`__

`4.1.2 Instruction execution environment
18 <#instruction-execution-environment>`__

`4.2 ARM Platforms 19 <#arm-platforms>`__

`4.3 RISC-V Platforms 19 <#risc-v-platforms>`__

`5 Payload Interfaces 19 <#payload-interfaces>`__

`5.1 ACPI tables 20 <#acpi-tables>`__

`5.2 HOB List 20 <#hob-list>`__

`5.2.1 Resource Descriptor HOB 21 <#resource-descriptor-hob>`__

`5.2.2 System Table info HOB 21 <#acpi-table-hob>`__

`5.2.3 Graphics information HOB 22 <#graphics-information-hob>`__

`5.2.4 Serial Debug Information HOB 22 <#_Toc49419802>`__

`5.2.5 CPU INFO HOB 24 <#cpu-info-hob>`__

`5.2.6 Optional HOBs 25 <#optional-hobs>`__

`6 Appendix A – HOB Data Structures
26 <#appendix-a-hob-data-structures>`__

`6.1 Base Data Type 26 <#base-data-type>`__

`6.2 EFI HOB TYPE 26 <#efi-hob-type>`__

`6.3 EFI_HOB_GENERIC_HEADER 26 <#efi_hob_generic_header>`__

`6.4 HOB List Header 27 <#hob-list-header>`__

`6.4.1 EFI_HOB_HANDOFF_INFO_TABLE 27 <#efi_hob_handoff_info_table>`__

`6.4.2 EFI_HOB_HANDOFF_TABLE_VERSION
28 <#efi_hob_handoff_table_version>`__

`6.4.3 EFI_BOOT_MODE 28 <#efi_boot_mode>`__

`6.5 EFI_HOB_GUID_TYPE 29 <#efi_hob_guid_type>`__

`6.6 EFI_PEI_GRAPHICS_INFO_HOB 29 <#efi_pei_graphics_info_hob>`__

`6.7 EFI_PEI_GRAPHICS_DEVICE_INFO_HOB
32 <#efi_pei_graphics_device_info_hob>`__

`6.8 EFI_HOB_RESOURCE_DESCRIPTOR 32 <#efi_hob_resource_descriptor>`__

`6.8.1 EFI_RESOURCE_TYPE 32 <#efi_resource_type>`__

`6.8.2 EFI_RESOURCE_ATTRIBUTE_TYPE 32 <#efi_resource_attribute_type>`__

`6.8.3 EFI_HOB_RESOURCE_DESCRIPTOR
34 <#efi_hob_resource_descriptor-1>`__

`6.9 EFI_HOB_MEMORY_ALLOCATION 35 <#efi_hob_memory_allocation>`__

`6.9.1 EFI_MEMORY_TYPE 35 <#efi_memory_type>`__

*Introduction*
==============

  Purpose 
----------

   The purpose of this document is to describe the architecture and
   interfaces between the bootloader and the payload. Bootloader or
   payload implementation specific details are outside the scope of this
   document. 

  Intended Audience 
--------------------

   This document is targeted at all platform and system developers
   who need the bootloader or the payload supports the
   unified bootloader and payload interface. This includes, but is not
   limited to: BIOS developers, bootloader developers, system
   integrators, as well as end users. 

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

Overview
========

   Most modern platforms rely on system Firmware to initialize the
   hardware and launch an Operating System (OS). The system firmware is
   responsible for initializing the platform hardware including CPU and
   other silicon functional blocks, detecting and initializing the
   memory subsystem, boot media initialization and setting up hardware
   abstractions for use by the operating systems.

   While newer architectural enhancements (e.g. - PCI, PCIe, USB, etc.)
   are developed at an industrial scale, there are vendor specific
   micro-architectural enhancements that happens at a much faster pace.
   Silicon vendors differentiate through these microarchitectural
   enhancements and these features are often considered intellectual
   property and rely on system specific firmware initialization. The
   system firmware thus provides the necessary abstraction and allows a
   generic operating system to run on different platform configurations
   and technologies without needing any changes to the operating system
   itself.

   A design methodology of viewing system firmware functionality as made
   up of **two distinct phases** – **initialization** and **OS boot
   logic** is gaining traction resulting in newer implementations of
   system firmware. This approach calls for modular phases with an
   initialization phase (bootloader) which completes the system
   initialization and gets the hardware to a usable state and then a
   payload phase. The payload can provide/implement many different
   functionalities including media and file system drivers, operating
   system boot, diagnostics, etc.

   While certain system firmware implementations implement both the
   initialization and OS boot logic in a single code base, the
   distinction lies in the functionality provided.

   This specification is used to describe the interface between the
   bootloader phase that initializes the system hardware and the payload
   phase. It includes how to pass parameters to payload and parameter
   format, payload image format, payload boot mode and stack usage, etc.
   The intent for this specification is to provide interoperability
   between spec compliant bootloaders and spec compliant payloads.

   .. image:: /images/design.png

Opens: Do we need a wrapper table on existing FV, PE/COFF, ELF?

Yes.

Should we put the wrapper inside the existing payload?

Open.

Bootloaders
-----------

   Bootloaders are primarily responsible for initializing the system
   hardware including, but not limited to CPU initialization, memory
   detection and initialization, initialization of silicon functional
   units (IO controllers), bus topology configuration, etc. In addition
   to the initialization itself, bootloader is responsible for providing
   the system configuration information to the subsequent stages in the
   boot process. In addition to proprietary options, there are many open
   sourced bootloaders available.

   **EDKII**

   EDK II is a modern, feature-rich, cross-platform firmware development
   environment for the UEFI and UEFI Platform Initialization (PI)
   specifications. EDKII performs both first stage (hardware
   initialization) and second stage booting.

   Reference implementations for many platforms are also available in
   open source under BSD + Patents license.

   https://www.tianocore.org/

   **Slim Bootloader**

   Slim Bootloader is an open source system firmware implementation that
   adopts the modular initialization followed by payload launch approach
   of system firmware design. Slim Bootloader project provides both the
   initialization phases as well as the OsLoader payload, but it also
   supports launching of different payloads. Open source Slim Bootloader
   uses BSD + Patents License.

   https://slimbootloader.github.io/

   **coreboot**

   coreboot is a project to develop open source boot firmware for
   various architectures. It follows the design philosophy of minimum
   necessary initialization followed by payload. coreboot is released
   under GNU's General Public License (GPL).

   https://www.coreboot.org/

   **U-Boot**

   U-Boot is an open-source, primary boot loader used in embedded
   devices. U-Boot performs both first stage (hardware initialization)
   and second stage booting. U-boot is released under GNU's General
   Public License (GPL)

   https://www.denx.de/wiki/U-Boot/WebHome

Payloads
--------

   After initializing the system hardware, bootloaders launch the
   payload modules. Payloads ideally are modular and platform
   independent. Payloads depend on the abstract interfaces (scope of
   this document) to be platform independent.

   While OS boot protocol is one of the main functionalities provided by
   payloads, there could be other functionalities (e.g - diagnostics)
   that can be enabled by payloads.

   From a design point of view, a payload is different from a boot image
   based on its relationship with the system firmware. Payloads are
   considered part of system firmware and is typically in the flash
   while boot images are not considered part of system firmware (not
   within the trusted firmware boundary) and is often in a boot media.

   Also, as mentioned earlier, while certain system firmware
   implementations implement both the initialization and OS boot logic
   in a single code base, the distinction lies in the functionality
   provided. This leads to use cases where some system firmware
   implementations can act as a payload providing OS boot capability
   while relying on an underlying bootloader layer for system hardware
   initialization. Examples of such payloads include EDKII and Uboot.
   Both EDKII and uboot implementations implement both phases of system
   firmware functionality and can also be launched as payloads by other
   bootloaders.

   There are many payloads currently available including EDK2 payload
   providing UEFI services, Linux as a payload, uboot payload and other
   custom implementations.

   **EDK II Payload**

   EDK II DXE and BDS stages can be launched by bootloaders as an UEFI
   payload. The EDKII payload provides the required UEFI specification
   defined architectural protocols and can launch an UEFI aware OS.

   **SBL OsLoader**

   SBL’s payload implementation that supports Linux boot protocol and
   can also launch ELF or PE executables. It also supports launching OS
   compliant with the MultiBoot specification.

   **Linux Payload**

   LinuxBoot is a firmware for modern servers that replaces specific
   firmware functionality like the UEFI DXE phase with a Linux kernel
   and runtime.

   https://www.linuxboot.org/

Current Bootloader and Payload interfaces
-----------------------------------------

   **Coreboot Payload Interface**:

   **Reference**: https://www.coreboot.org/API

   **Reference**: https://doc.coreboot.org/lib/abi-data-consumption.html

   **Reference**:
   https://github.com/tianocore/edk2/blob/master/UefiPayloadPkg/Library/CbParseLib/CbParseLib.c

   coreboot passes information to downstream users (payloads and/or
   operating systems) using **coreboot tables**.

   The table usually sits in memory around address 0x500. However, some
   bootloaders seem to overwrite low memory area, thus destroying the
   coreboot table integrity, rendering the table useless. So, the
   coreboot tables were moved to the high tables area.

   When coreboot tables were moved to high memory, a 40 bytes mini
   coreboot table with a single sub table is placed at 0x500/0x530 that
   points to the real coreboot table. This is comparable to the ACPI
   RSDT or the MP floating table.

   Coreboot tables is a series of data records packed back to back and
   each encoding both type and size. This is something similar to a UEFI
   HOB list. Coreboot tables provide information about

-  **memory map**

-  **Graphics Info**

-  Pointers to certain CBMEM structures (**ACPI, SMBIOS**, etc)

..

   How to fill the gap with current coreboot and payload requirement?

   Use a library in coreboot to convert the new interface.

   **Slim Bootloader (SBL) Payload Interface**:

   **Reference**:
   https://slimbootloader.github.io/developer-guides/payload.html

   **Reference**:
   https://uefi.org/sites/default/files/resources/PI_Spec_1_7_final_Jan_2019.pdf

   **Reference**:
   https://github.com/tianocore/edk2/blob/master/UefiPayloadPkg/Library/SblParseLib/SblParseLib.c

   SBL supports “loosely coupled payload” which basically refers to
   payloads built independently (no source sharing). SBL builds a series
   of data structures called the Hand Off Blocks (HOBs) and provides a
   pointer to this HOB List to the payloads. These data structures
   conform to the HOB format as described in the Platform Initialization
   (PI) Specification.

   **PEI to DXE Interface**:

   **Reference**:
   https://uefi.org/sites/default/files/resources/PI_Spec_1_7_final_Jan_2019.pdf

   PEI must also provide a mechanism for components of DXE and the DXE
   Foundation to discover the state of the system when the DXE
   Foundation is invoked. Certain aspects of the system state at handoff
   are architectural, while other system state information may vary and
   hence must be described to DXE components.

   The DXE IPL PPI passes the Hand-Off Block (HOB) list from PEI to the
   DXE Foundation when it invokes the DXE Foundation. The handoff state
   is described in the form of HOBs in the HOB list.

+----------------------------------+----------------------------------+
| Required HOB Type                | Usage                            |
+==================================+==================================+
| Phase Handoff Information Table  | This HOB is required.            |
| (PHIT) HOB                       |                                  |
+----------------------------------+----------------------------------+
| One or more Resource Descriptor  | The DXE Foundation will use this |
| HOB(s) describing physical       | physical system memory for DXE.  |
| system memory                    |                                  |
+----------------------------------+----------------------------------+
| Boot-strap processor (BSP) Stack | The DXE Foundation needs to know |
| HOB                              | the current stack location so    |
|                                  | that it can move it if           |
|                                  | necessary, based upon its        |
|                                  | desired memory address map. This |
|                                  | HOB will be of type              |
|                                  | EfiConventionalMemory            |
+----------------------------------+----------------------------------+
| One or more Resource Descriptor  | The DXE Foundation will place    |
| HOB(s) describing firmware       | this into the GCD.               |
| devices                          |                                  |
+----------------------------------+----------------------------------+
| One or more Firmware Volume      | The DXE Foundation needs this    |
| HOB(s)                           | information to begin loading     |
|                                  | other drivers in the platform.   |
+----------------------------------+----------------------------------+
| A Memory Allocation Module HOB   | This HOB tells the DXE           |
|                                  | Foundation where it is when      |
|                                  | allocating memory into the       |
|                                  | initial system address map.      |
+----------------------------------+----------------------------------+

OS interfaces
-------------

   While this specification aims to document the bootloader to payload
   interface, the payload to OS interface is briefly discussed just for
   the sake of completeness.

OS Boot protocols
~~~~~~~~~~~~~~~~~

   **UEFI**

   UEFI stands for "Unified Extensible Firmware Interface." The UEFI
   Specification defines a new model for the interface between
   personal-computer operating systems and platform firmware. The
   interface consists of data tables that contain platform-related
   information, plus boot and runtime service calls that are available
   to the operating system and its loader. Together, these provide a
   standard environment for booting an operating system and running
   pre-boot applications.

   https://uefi.org/specifications

   **Linux Boot Protocol**

   Linux kernel can itself be a bootable image without needing a
   separate OS Loader. The Linux boot protocol defines the requirements
   required to launch Linux kernel as a boot target.

   https://www.kernel.org/doc/html/latest/x86/boot.html

   **Multiboot Protocol**

   The Multiboot specification is an open standard describing how a boot
   loader can load an x86 operating system kernel. The specification
   allows any compliant boot-loader implementation to boot any compliant
   operating-system kernel. Thus, it allows different operating systems
   and boot loaders to work together and interoperate, without the need
   for operating system–specific boot loaders.

   https://www.gnu.org/software/grub/manual/multiboot2/multiboot.html

Data interface
~~~~~~~~~~~~~~

   Modern buses and devices (PCI, PCIe, USB, SATA, etc.) support
   software detection, enumeration and configuration, providing true
   plug and play capabilities, there still exists some devices that are
   not enumerable through software.

   Examples:

-  PCI Host Bridge

-  GPIO

-  Serial interfaces like I2C, HS-UART, etc.

-  Graphics framebuffer

-  Device Management information including manufacturer name, etc.

..

   While it is possible to write platform specific device drivers to
   support such devices/interfaces, it is efficient for the platform
   specific firmware to provide information to the platform independent
   operating system.

   There are two data protocols that are used extensively for this
   purpose – ACPI and Device Tree.

   **ACPI**

   Advanced Configuration and Power Interface (**ACPI**) provides an
   open standard that operating systems can use to discover and
   configure computer hardware components, to perform power management
   by (for example) putting unused components to sleep, and to perform
   status monitoring. In October 2013, ACPI Special Interest Group (ACPI
   SIG), the original developers of the ACPI standard, agreed to
   transfer all assets to the UEFI Forum, in which all future
   development will take place.

   **SMBIOS**

   System Management BIOS (**SMBIOS**) is the premier standard for
   delivering management information via system firmware.

   https://uefi.org/specifications

   https://www.dmtf.org/standards/smbios

   **DEVICE TREE**

   The devicetree is a data structure for describing hardware. A
   devicetree is a tree data structure with nodes that describe the
   devices in a system. Each node has property/value pairs that describe
   the characteristics of the device being represented.

   https://www.devicetree.org/

Payload principle
-----------------

   | Keep interface as clean and simple as possible.
   | The payload should encapsulate the boot abstractions for a given
     technology, such as UEFI payload or LinuxBoot. The Payload should
     vie to be portable to different platform implementations (PI), such
     as coreboot, Slim bootloader, or an EDKII style firmware.
   | The payload should elide strong dependencies on the payload
     launching code (e.g., coreboot versus EDKII versus slimboot) and
     also avoid board-specific dependencies. The payload behavior should
     be parameterized by the data input block.

   | **Open**\ *: Should Payload return back to bootloader if payload
     fail?*
   | *Answer: No for first generation. No callbacks into payload
     launcher.*

   **Open**\ *: Do we need callback from payload to bootloader? Avoid it
   if possible*

   | **Open**\ *: How to support SMM for booloader and Payload? Where is
     trust boundary.*
   | *Answer: SMM should be either part of the payload for present
     generation Management Mode (MM) PI drivers, but longer term the
     EDKII PI independent MM modules should be used. The latter are a
     class of SMM drivers (or TrustZone drivers for ARM) that are not
     launched via DXE. For coreboot SMM can be loaded from ramstage, the
     PI payload launcher, or elided from ramstage and use the portable
     MM handlers.*
   | If there is an existing standard it will be used (e.g., ACPI table
     that’s simple to parse).

Security
--------

Payload is part of system firmware TCB

   Today the payload is provisioned as part of the platform
   initialization code. As such, the payload is protected and updated by
   the platform manufacturer (PM). The payload should be covered by a
   digital signature generated by the PM. The platform owner (PO) should
   not be able to update the payload independently of the PM.

   | The platform initialization (PI) code should be the platform root
     of trust for update, measurement, and verification. As such, the PI
     code that launches the payload should verify the payload using
     payload Hash or using a key to verify its signature. The PI code
     should also provide a measurement into a Trusted Platform Module
     (TPM) of the payload into a TPM Platform Configuration Register
     (e.g., PCR[0]). The payload may continue the measured boot actions
     by recording code executed in the payload phase into PCR’s (e.g.,
     UEFI driver into PCR[2], UEFI OS loader into PCR[4]).
   | *Open: Do we need a capability boot to say if payload
     supports/requires measured/verified boot?*

Payload Image Format
====================

   Payload, as a standalone component, usually needs to be loaded by a
   bootloader into memory properly prior to execution. In this loading
   process, some additional process might be required, such as rebasing,
   assembling, etc.

   The following information might be required by a bootloader to load
   a payload image:
-  Version information
-  Architecture
-  Entry point
-  Relocation information
-  Preferred base
-  Verification

Opens:

   There are several options here for bootloader on how to load a
   payload. Inputs are required to decide which option might be the best
   approach.

-  Option 1: Use a new standard header for payload loading.

..

   For example, as current proposed in section 3.1, providing a new
   standard information header for payload loading. In this way the
   bootloader implementation could be much simpler since it does not
   need to understand the different PE, ELF, FV or other formats.
   Meanwhile, a standard tool can be used to facilitate generating the
   payload image header from existing formats to reduce the effort
   required by the payloads. The downside of this approach is that it
   will introduce yet another layer of image wrapper on top of the
   native format. It might cause concerns of more fragmentation on image
   format.

-  Option 2: Converge into one existing format.

..

   This approach is to converge all different payload formats into a
   single well-known format, such as PE or ELF. It makes bootloader
   simpler to only support one known format. On the other side, it needs
   every payload to generate this new well-known format if it is not
   already in this format. Sometimes, it might be challenges. For
   example, producing ELF format from a UEFI FV image.

   .efi format with Linux support:
   https://www.kernel.org/doc/html/latest/admin-guide/efi-stub.html

   UBOOT supports EFI:
   https://www.xypron.de/u-boot/uefi/u-boot_on_efi.html#:~:text=U%2DBoot%20supports%20running%20as,bit%20or%2064%2Dbit%20EFI

-  Option 3: Reuse current different payload image formats.

..

   This approach requires bootloader to support all different payload
   formats including PE, COFF, FV, etc, and handle them separately
   during the loading process. The advantage is that the industry
   standard formats are followed. However, it does introduce overhead to
   every bootloader to be able to handle these formats.

..

   This specification is open to other options. Below it used the
   proposaled option 1 as of now.

   Today, many payloads use their own image formats (PE, ELF, FV, RAW,
   …), and it makes it difficult for a bootloader to identify and
   understand how to load a payload. To address this, a small common
   payload image header is introduced at the beginning of the payload
   image to describe necessary information required for loading.

Payload Image Standard Header
-----------------------------

   This section defines the payload image primary header format.

   Table 1. PAYLOAD_INFO_HEADER

+-------------+---------------+------------------+------------------+
| Byte Offset | Size in Bytes | Field            | Description      |
+=============+===============+==================+==================+
| 0           | 4             | Identifier       | ‘PLDH’.          |
|             |               |                  | Identifier for   |
|             |               |                  | the              |
|             |               |                  | PAYL             |
|             |               |                  | OAD_INFO_HEADER. |
+-------------+---------------+------------------+------------------+
| 4           | 4             | HeaderLength     | Length of the    |
|             |               |                  | PAY              |
|             |               |                  | LOAD_INFO_HEADER |
|             |               |                  | header in bytes. |
+-------------+---------------+------------------+------------------+
| 8           | 1             | HeaderRevision   | Revision of the  |
|             |               |                  | header. The      |
|             |               |                  | current value    |
|             |               |                  | for this field   |
|             |               |                  | is 1.            |
+-------------+---------------+------------------+------------------+
| 9           | 3             | Reserved         | Not used for     |
|             |               |                  | now.             |
+-------------+---------------+------------------+------------------+
|             |               |                  |                  |
+-------------+---------------+------------------+------------------+
| 12          | 8             | ProducerId       | An OEM-supplied  |
|             |               |                  | ASCII string     |
|             |               |                  | that identifies  |
|             |               |                  | the payload      |
|             |               |                  | producer.        |
+-------------+---------------+------------------+------------------+
| 20          | 8             | ImageId          | ASCII string     |
|             |               |                  | that identifies  |
|             |               |                  | the payload ID   |
|             |               |                  | name. It can     |
|             |               |                  | provide          |
|             |               |                  | indication to    |
|             |               |                  | bootloader on    |
|             |               |                  | what kind of     |
|             |               |                  | payload it is,   |
|             |               |                  | such as UEFI     |
|             |               |                  | payload, Linux   |
|             |               |                  | payload, etc.    |
+-------------+---------------+------------------+------------------+
| 28          | 4             | Revision         | Revision of the  |
|             |               |                  | Payload binary.  |
|             |               |                  | Major.Mino       |
|             |               |                  | r.Revision.Build |
|             |               |                  |                  |
|             |               |                  | The              |
|             |               |                  | ImageRevision    |
|             |               |                  | can be decoded   |
|             |               |                  | as follows:      |
|             |               |                  |                  |
|             |               |                  | 7 : 0 - Build    |
|             |               |                  | Number           |
|             |               |                  |                  |
|             |               |                  | 15 : 8 -         |
|             |               |                  | Revision         |
|             |               |                  |                  |
|             |               |                  | 23 : 16 - Minor  |
|             |               |                  | Version          |
|             |               |                  |                  |
|             |               |                  | 31 : 24 - Major  |
|             |               |                  | Version          |
+-------------+---------------+------------------+------------------+
| 32          | 4             | Length           | The length of    |
|             |               |                  | the full payload |
|             |               |                  | binary image     |
|             |               |                  | including        |
|             |               |                  | primary header,  |
|             |               |                  | extended headers |
|             |               |                  | and the actual   |
|             |               |                  | payload itself.  |
+-------------+---------------+------------------+------------------+
|             |               |                  |                  |
+-------------+---------------+------------------+------------------+
| 36          | 4             | Svn              | Security version |
|             |               |                  | number of the    |
|             |               |                  | Payload binary.  |
|             |               |                  | This is used for |
|             |               |                  | anti-roll back   |
|             |               |                  | protection.      |
+-------------+---------------+------------------+------------------+
| 40          | 2             | Reserved         | Not used. Must   |
|             |               |                  | be 0 for this    |
|             |               |                  | revision.        |
+-------------+---------------+------------------+------------------+
| 42          | 2             | Machine          | Target machine   |
|             |               |                  | type as defined  |
|             |               |                  | in PE/COFF. This |
|             |               |                  | can be used by   |
|             |               |                  | bootloader to    |
|             |               |                  | determine if the |
|             |               |                  | targeted payload |
|             |               |                  | is suitable for  |
|             |               |                  | current          |
|             |               |                  | proccesor        |
|             |               |                  | architecture or  |
|             |               |                  | execution mode.  |
|             |               |                  | For example, if  |
|             |               |                  | the payload      |
|             |               |                  | image is ARM     |
|             |               |                  | arch, and        |
|             |               |                  | bootloader is    |
|             |               |                  | x86, bootloader  |
|             |               |                  | should jump to   |
|             |               |                  | error flow       |
|             |               |                  | instead of       |
|             |               |                  | jumping into     |
|             |               |                  | payload entry    |
|             |               |                  | point.           |
|             |               |                  | Similarly, if    |
|             |               |                  | current          |
|             |               |                  | processor is in  |
|             |               |                  | x86 mode, but    |
|             |               |                  | the payload      |
|             |               |                  | image indicates  |
|             |               |                  | x64, bootloader  |
|             |               |                  | need to handle   |
|             |               |                  | it accordingly.  |
+-------------+---------------+------------------+------------------+
| 44          | 4             | Capability       | Capabilities for |
|             |               |                  | the payload      |
|             |               |                  | images           |
|             |               |                  |                  |
|             |               |                  | -  Bit 0 –       |
|             |               |                  |    Support       |
|             |               |                  |    position      |
|             |               |                  |    independent   |
|             |               |                  |    code (PIC).   |
|             |               |                  |                  |
|             |               |                  | -  Bit 1 –       |
|             |               |                  |    Support       |
|             |               |                  |    relocation.   |
|             |               |                  |    If this bit   |
|             |               |                  |    is set and    |
|             |               |                  |    PIC is not    |
|             |               |                  |    set, a        |
|             |               |                  |    relocation    |
|             |               |                  |    table should  |
|             |               |                  |    exist in the  |
|             |               |                  |    extended      |
|             |               |                  |    table.        |
|             |               |                  |                  |
|             |               |                  | -  Bit 2 –       |
|             |               |                  |    Support       |
|             |               |                  |                  |
|             |               |                  |  authentication. |
|             |               |                  |    If this bit   |
|             |               |                  |    is set, an    |
|             |               |                  |                  |
|             |               |                  |   authentication |
|             |               |                  |    table should  |
|             |               |                  |    exist in the  |
|             |               |                  |    extended      |
|             |               |                  |    table.        |
+-------------+---------------+------------------+------------------+
| 48          | 4             | ImageOffset      | Actual payload   |
|             |               |                  | image start      |
|             |               |                  | offset relative  |
|             |               |                  | to this          |
|             |               |                  | structure start. |
+-------------+---------------+------------------+------------------+
| 52          | 4             | ImageLength      | Actual payload   |
|             |               |                  | image size       |
|             |               |                  | starting from    |
|             |               |                  | ImageOffset.     |
+-------------+---------------+------------------+------------------+
| 56          | 8             | ImageBase        | Preferred actual |
|             |               |                  | payload image    |
|             |               |                  | base address for |
|             |               |                  | execution. If    |
|             |               |                  | relocation is    |
|             |               |                  | not supported,   |
|             |               |                  | the image must   |
|             |               |                  | be loaded at     |
|             |               |                  | this required    |
|             |               |                  | base.            |
+-------------+---------------+------------------+------------------+
| 64          | 4             | ImageAlignment   | Required image   |
|             |               |                  | alignment for    |
|             |               |                  | execution. The   |
|             |               |                  | value needs to   |
|             |               |                  | be power of 2. 0 |
|             |               |                  | indicates no     |
|             |               |                  | special          |
|             |               |                  | alignment        |
|             |               |                  | requirements.    |
|             |               |                  | This field can   |
|             |               |                  | be used to       |
|             |               |                  | select proper    |
|             |               |                  | loading base     |
|             |               |                  | when relocation  |
|             |               |                  | is supported.    |
+-------------+---------------+------------------+------------------+
| 64          | 4             | EntryPointOffset | Payload entry    |
|             |               |                  | point offset     |
|             |               |                  | relative to the  |
|             |               |                  | Payload image    |
|             |               |                  | base address.    |
+-------------+---------------+------------------+------------------+

..

   One or more Payload Image Extend Header can immediately follow the
   payload image primary header in back to back order. The extended
   header needs to be aligned at 4-bytes boundary and must start with a
   payload image common header. If the offset of the next extended
   header is equal or greater than “\ *PAYLOAD_INFO_HEADER.
   ImageOffset”* field, it indicates the end of all extended headers.
   The only exception is the authentication table, it with be located at
   the very end of the whole image in order to facilitate the image
   hashing calculation. Please refer to section 3.3 for more details.

Payload Image Relocation Table
------------------------------

   In order to provide a unified way for bootloader to rebase an image,
   an optional extended header is provided to provide the relocation
   information. When *PAYLOAD_INFO_HEADER.Capability* [BIT1] is set,
   this table must exist in the extended header.

   Table 1. PAYLOAD_RELOCATION_HEADER

+-------------+---------------+------------------+------------------+
| Byte Offset | Size in Bytes | Field            | Description      |
+=============+===============+==================+==================+
| 0           | 4             | Identifier       | ‘PLDR’.          |
|             |               |                  | Identifier for   |
|             |               |                  | the              |
|             |               |                  | PAYL             |
|             |               |                  | OAD_INFO_HEADER. |
+-------------+---------------+------------------+------------------+
| 4           | 4             | HeaderLength     | Length of the    |
|             |               |                  | header in bytes. |
+-------------+---------------+------------------+------------------+
| 8           | 1             | HeaderRevision   | Revision of the  |
|             |               |                  | header. The      |
|             |               |                  | current value    |
|             |               |                  | for this field   |
|             |               |                  | is 1.            |
+-------------+---------------+------------------+------------------+
| 9           | 3             | Reserved         | Not used for     |
|             |               |                  | now.             |
+-------------+---------------+------------------+------------------+
| 12          | 1             | RelocFmt         | Relocation Format|
|             |               |                  | 0: RAW - The     |
|             |               |                  | relocation block |                  
|             |               |                  | data starts from |                  
|             |               |                  | end of header.   |                  
|             |               |                  | 1: POINTER       |
|             |               |                  | PE Relocation    |                  
|             |               |                  | block header is  |                  
|             |               |                  | located at end   |                  
|             |               |                  | of the  header.  |                  
|             |               |                  |                  |                  
+-------------+---------------+------------------+------------------+
| 13          | 1             | Reserved         | Reserved         |
+-------------+---------------+------------------+------------------+
| 14          | 2             | RelocImgStripped | Size in bytes    |
|             |               |                  | to be adjusted   |
|             |               |                  | from Relocation  |
|             |               |                  | Image.           |
+-------------+---------------+------------------+------------------+
| 16          | 4             | RelocImgOffset   | Relocation       |
|             |               |                  | Image Offset     |
|             |               |                  | from Payload Base|
|             |               |                  | address.         |
+-------------+---------------+------------------+------------------+
| 20          | *             |*RelocationBlocks*| If RelocFmt is   |
|             |               |                  | RAW, Relocation  |
|             |               |                  | Blocks Data      |
|             |               |                  | starts here      |
|             |               |                  | If RelocFmt is   |
|             |               |                  | POINTER,         |
|             |               |                  | it defines the   |
|             |               |                  | Relative Virtual |
|             |               |                  | address (RVA) and|
|             |               |                  | size of the      |
|             |               |                  | relocation block |
|             |               |                  | as stated        |
|             |               |                  | by IMAGE_DATA_   |
|             |               |                  | DIRECTORY of     |
|             |               |                  | PE format.       |
+-------------+---------------+------------------+------------------+

   *RelocationBlocks* follows the Base Relocation Block defined in PE
   format listed below:

   https://docs.microsoft.com/en-us/windows/win32/debug/pe-format

Payload Image Authentication Table
----------------------------------

   Multiple Base Relocation Blocks might present back to back. If the
   next Base Relocation Block start offset is equal or greater than the
   “\ *PAYLOAD_RELOCATION_HEADER.HeaderLength*\ ” field, it indicates
   the end of all relocation blocks. In order to provide a unified way
   for bootloader to authenticate an image, an optional extended header
   is provided to provide the authentication information. When
   Capability BIT2 is 1, this table must exist in the extended headers.
   This extended table, if exists, will show up at the end of the full
   image located by offset (*PAYLOAD_INFO_HEADER. ImageOffset* +
   *PAYLOAD_INFO_HEADER. ImageLength*)

   Table 1.PAYLOAD_AUTHENTICATION_HEADER

+-------------+---------------+------------------+------------------+
| Byte Offset | Size in Bytes | Field            | Description      |
+=============+===============+==================+==================+
| 0           | 4             | Signature        | ‘PLDA’.          |
|             |               |                  | Signature for    |
|             |               |                  | the              |
|             |               |                  | PAYL             |
|             |               |                  | OAD_INFO_HEADER. |
+-------------+---------------+------------------+------------------+
| 4           | 4             | HeaderLength     | Length of the    |
|             |               |                  | header in bytes. |
+-------------+---------------+------------------+------------------+
| 8           | 1             | HeaderRevision   | Revision of the  |
|             |               |                  | header. The      |
|             |               |                  | current value    |
|             |               |                  | for this field   |
|             |               |                  | is 1.            |
+-------------+---------------+------------------+------------------+
| 9           | 3             | Reserved         | Not used for     |
|             |               |                  | now.             |
|             |               |                  |                  |
|             |               |                  | Open: Add        |
|             |               |                  | authentication   |
|             |               |                  | type?            |
+-------------+---------------+------------------+------------------+
|             |               |                  |                  |
+-------------+---------------+------------------+------------------+
| 12          | \*            |AuthenticationData| Defined by       |
|             |               |                  | PAYLOAD_AUT      |
|             |               |                  | HENTICATION_DATA |
|             |               |                  | structure        |
+-------------+---------------+------------------+------------------+

..

   Table 2. PAYLOAD_AUTHENTICATION_DATA

+-------------+---------------+------------------+------------------+
| Byte Offset | Size in Bytes | Field            | Description      |
+=============+===============+==================+==================+
| 0           | 4             | PubKeyId         | ‘PUBK’           |
+-------------+---------------+------------------+------------------+
| 4           | 2             | PubKeySize       | Public key       |
|             |               |                  | structure size   |
|             |               |                  | from the         |
|             |               |                  | beginning of     |
|             |               |                  | PubKeyId to the  |
|             |               |                  | end of           |
|             |               |                  | PubKeyData.      |
+-------------+---------------+------------------+------------------+
| 6           | 1             | PubKeyType       | Public key type. |
|             |               |                  |                  |
|             |               |                  | 0- RSA 1-ECDSA   |
+-------------+---------------+------------------+------------------+
| 7           | 1             | Reserved         | Not used for now |
|             |               |                  |                  |
+-------------+---------------+------------------+------------------+
| 8           | \*            | PubKeyData       | Public key data  |
|             |               |                  | buffer. The size |
|             |               |                  | is indicated by  |
|             |               |                  | PubKeySize - 8   |
+-------------+---------------+------------------+------------------+
| i           | 4             | SignatureId      | ‘SIGN’           |
+-------------+---------------+------------------+------------------+
| i+4         | 2             | SignatureSize    | The signature    |
|             |               |                  | structure size   |
|             |               |                  | from the         |
|             |               |                  | beginning of     |
|             |               |                  | SignatureId to   |
|             |               |                  | the end of the   |
|             |               |                  | SignatureData.   |
+-------------+---------------+------------------+------------------+
| i+6         | 1             | SignatureType    | 0- RSA 1-RSA-PSS |
|             |               |                  | 2 - ECDSA        |
+-------------+---------------+------------------+------------------+
| i+7         | 1             | SignatureHashAlg | HASH algorithm   |
|             |               |                  | used for         |
|             |               |                  | signature        |
|             |               |                  | calculation.     |
|             |               |                  | Same definitions |
|             |               |                  | as PubKeyHashAlg |
+-------------+---------------+------------------+------------------+
| i+8         | \*            | SignatureData    | Signature data.  |
|             |               |                  | The length is    |
|             |               |                  | indicated by     |
|             |               |                  | SignatureSize -  |
|             |               |                  | 8                |
+-------------+---------------+------------------+------------------+

The current spec defined PKCS 1.5 and 2.1 support. Other standards can
be extended by adding new AuthenticationType.

This signature calculation should cover data starting from offset 0 of
*PAYLOAD_INFO_HEADER*

to the end of the actual payload image indicated by offset
(*PAYLOAD_INFO_HEADER. ImageOffset* + *PAYLOAD_INFO_HEADER.
ImageLength*) excluding the *PAYLOAD_AUTHENTICATION_HEADER.* It is the
responsibility of the bootlaoder to verify the fields in
PAYLOAD_AUTHENTICATION_HEADER and PAYLOAD_AUTHENTICATION_DATA are valid
before conducting the authentication. For example, if for security
reason, SHA2_256 is not accepted, the authentication should just fail
even though the signature might be valid.

-

-

-

Hand-off state
==============

   The bootloader builds the Hand-Off Block (HOB) list containing
   platform specific information and passes the address of the HOB list
   to the payload.

   The prototype of payload entry point is defined as:

   | typedef
   | VOID
   | (__cdecl \*PAYLOAD_ENTRY) (
   | EFI_HOB_HANDOFF_INFO_TABLE \*HobList,
   | VOID \*ImageBase
   | );

   HOB List defines the detailed HOB list being used to transfer
   platform specific data from the bootloader to the payload.
   ImageBase defines the base address of the Payload Image. 

IA-32 and x64 Platforms
-----------------------

State of silicon
~~~~~~~~~~~~~~~~

   The bootloader initializes the processor and chipset through
   vendor-specific silicon initialization implementation. For example,
   FSP is a binary form of Intel silicon initialization implementation.
   Typically, when the control transfers to the payload:

-  The memory controller is initialized such that physical memory is
   available to use.

-  Processors (including application processors) are patched with
   microcode and initialized properly.

-  The PCI bus is assigned with proper bus numbers, IO/MMIO space.

-  The Graphics controller may be initialized properly.

..

   But the bootloader could do less silicon initialization if the
   responsibilities of the payload and the bootloader are well defined
   (out of the scope of this document).

Instruction execution environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Regardless of the environment where the bootloader runs, the
   processor is in 32bit protected mode when a 32bit payload starts, or
   in 64bit long-mode when a 64bit payload starts. The payload header
   contains the machine type information that the payload supports.

   The following sections provide a detailed description of the
   execution environment when the payload starts.

Registers
^^^^^^^^^

-  ESP + 4 points to the address of the HOB list for the 32bit payload.

-  RCX holds the address of the HOB list for the 64bit payload.

-  Direction flag in EFLAGs is clear so the string instructions process
   from low addresses to high addresses.

-  All other general-purpose register states are undefined.

-  Floating-point control word is initialized to 0x027F (all exceptions
   masked, double-precision, round-to-nearest).

-  | Multimedia-extensions control word (if supported) is initialized to
     0x1F80 (all exceptions
   | masked, round-to-nearest, flush to zero for masked underflow).

-  CR0.EM is clear.

-  CR0.TS is clear.

Interrupt
^^^^^^^^^

   Interrupt is disabled. The hardware is initialized by the boot loader
   such that no interrupt triggers even when the payload sets the
   Interrupt Enable flag in EFLAGs.

Page table
^^^^^^^^^^

   Selectors are set to be flat.

   Paging mode may be enabled for the 32bit payload. (have general term
   on how it could be enabled if enabling page mode).

   Paging mode is enabled for the 64bit payload.

   When paging is enabled, all memory space is identity mapped (virtual
   address equals physical address). The four-level page table is set
   up. The payload can choose to set up the five-level page table as
   needed.

Stack
^^^^^

   4KiB stack is available for the payload. The stack is 16-byte aligned
   and may be marked as non-executable in page table.

   discussion: Should payload declare its required stack size in the
   payload header?

   Payload could setup its own stack, there is no restriction to setup a
   new stack.

Application processors
^^^^^^^^^^^^^^^^^^^^^^

   Payload starts on the bootstrap processor. All application processors
   (on a multiple-processor system) are in halt state.

   Use mWait and mBox to wake up. (Follow ACPI table). How about the
   legacy bootloader? Assume something if ACPI is not there.

   TODO: take care about virtual platforms.

ARM Platforms
-------------

Need community inputs

RISC-V Platforms
----------------

Need community inputs

Payload Interfaces
==================

   The bootloader provides platform information to payload through
   standard ACPI table, SMBIOS table, Device tree and a series of data
   structures called the Hand Off Blocks (HOBs). If the information is
   already defined in ACPI specification, SMBIOS specification or device
   tree, the payload could parse them to get the required information.
   For the platform information that is not defined in the standard
   tables, the bootloader should build a HOB list to pass it to the
   payload.

   All of them should be optional

   (Add device tree to reference:

   https://buildmedia.readthedocs.org/media/pdf/devicetree-specification/latest/devicetree-specification.pdf)

   Open: Do we need a set of configuration data to config payload?

   We don’t believe so.

   Open: Do we need pass data from payload to bootloader to impact
   bootloader behavior in next boot?

   Keep it open now.

   Open: will payload be run in S3 path?

   Suggest skipping payload.

ACPI tables
-----------

   ACPI table is required to boot modern operation system, especially to
   boot windows operating system. ACPI table should be provided by
   bootloader since most of the tables are platform specific. The
   payload might update some of the ACPI tables if required.

   The payload could parse the ACPI table to get some basic platform
   information. For example, the Fixed ACPI Description Table (FADT)
   defines various fixed hardware ACPI information to an ACPI compatible
   OS, such as the base address for the following hardware registers
   blocks: PM1a_CNT_BLK, PM_TMR_BLK, PM1a_EVT_BLK, GPE0_BLK,
   PM1b_EVT_BLK, PM1b_CNT_BLK, PM2_CNT_BLK, and GPE1_BLK. The payload
   could use them and other values (e.g. RESET_REG, RESET_VALUE) to make
   the payload platform independent.

   The other example is to get PCIE base address from ACPI memory mapped
   configuration space access table definition, defined in the PCI
   Firmware Specification.
   `http://www.pcisig.com <http://www.pcisig.com/>`__.

   And another example is on the debug device info. The bootloader might
   report debug device following up ACPI Debug Port Table 2 (DBG2). If a
   fully 16550-compatible serial device is specified in the ACPI DBG2,
   bootloader should provide a Serial Debug Information HOB in the HOB
   list so that the payload could use same debug device with same
   setting. If the ACPI DBG2 table could not be found, the payload
   should use serial device provided by the Serial Debug Information HOB
   as the default debug device.

   (ACPI DBG2 document.
   http://download.microsoft.com/download/9/4/5/945703CA-EF1F-496F-ADCF-3332CE5594FD/microsoft-debug-port-table-2-CP.docx)

HOB List
--------

   The bootloader should build a HOB list and pass the HOB list header
   to payload when passing control to payload. The HOB format is
   described in the *Platform Initialization (PI) Specification - Volume
   3: Shared Architectural Elements*. The payload could decide on how to
   consume the information passed from the bootloader.

   The sections below describe the HOBs from the bootloader to provide
   the system architecturally information. Additional bootloader
   specific HOB may be defined in the bootloader specific documents.

Resource Descriptor HOB
~~~~~~~~~~~~~~~~~~~~~~~

   The bootloader should report the system resources through the HOB
   following **EFI_HOB_RESOURCE_DESCRIPTOR** format defined in *Platform
   Initialization Specification Volume 3 – Shared Architectural
   elements*.

   For example, any physical memory found in bootloader should be
   reported using resource type **EFI_RESOURCE_SYSTEM_MEMORY**, and the
   reserved memory used by bootloader should be reported using resource
   type **EFI_RESOURCE_MEMORY_RESERVED**.

   I/O and memory mapped I/O resource should also be reported using
   resource type **EFI_RESOURCE_IO** and
   **EFI_RESOURCE_MEMORY_MAPPED_IO**.

   **Open**: should report payload in memory using the Boot Firmware
   Volume (BFV) HOB?

ACPI Table HOB
~~~~~~~~~~~~~~

   The bootloader should pass ACPI table through the GUID HOB to the
   payload. So that the payload could get the platform information from
   the ACPI table.

   Build the different HOBs for different table using standard defined
   GUID.

   | **HOB GUID**
   | **#define EFI_ACPI_TABLE_GUID \\**
   | **{0x8868e871, 0xe4f1, 0x11d3, {0xbc, 0x22, 0x0, 0x80, 0xc7, 0x3c,
     0x88, 0x81}}**

   **Note: This GUID reuses the same GUID defined in UEFI spec chapter
   4.6 EFI Configuration Table**

   **Hob Interface Structure**

   #pragma **pack**\ (1)

   | *///*
   | */// Bootloader acpi table hob*
   | *///*
   | typedef struct {
   | EFI_HOB_GUID_TYPE Header;

   | UINT64 TableAddress;
   | } ACPI_TABLE_HOB;

   #pragma pack()

   **Member Description**

   Header

   Header.Name set to EFI_ACPI_TABLE_GUID. See section 6.5
   EFI_HOB_GUID_TYPE.

   **TableAddress**

   Point to the ACPI RSDP table. The ACPI table need follow ACPI
   specification verson 2.0 or above.

SMBIOS Table HOB
~~~~~~~~~~~~~~~~

   The bootloader might pass SMBIOS table through the GUID HOB to the
   payload. So that the payload could get the platform information from
   the table.

   | **HOB GUID**
   | **#define SMBIOS_TABLE_GUID \\**
   | **{0xeb9d2d31, 0x2d88, 0x11d3, {0x9a, 0x16, 0x0, 0x90, 0x27, 0x3f,
     0xc1, 0x4d}}**

   | **#define SMBIOS3_TABLE_GUID \\**
   | **{0xf2fd1544, 0x9794, 0x4a2c, {0x99, 0x2e, 0xe5, 0xbb, 0xcf, 0x20,
     0xe3, 0x94}}**

   **Note: These GUIDs reuse the same GUIDs defined in UEFI spec chapter
   4.6 EFI Configuration Table**

   **Hob Interface Structure**

   #pragma **pack**\ (1)

   | *///*
   | */// Bootloader SMBIOS table hob*
   | *///*
   | typedef struct {
   | EFI_HOB_GUID_TYPE Header;

   | UINT64 TableAddress;
   | } SMBIOS_TABLE_HOB;

   #pragma pack()

   **Member Description**

   Header

   Header.Name set to SMBIOS_TABLE_GUID if SMBIOS table from
   TableAddress follows the format defined by SMBIOS_TABLE_ENTRY_POINT,
   or set to SMBIOS3_TABLE_GUID if SMBIOS table from TableAddress
   follows the format defied by SMBIOS_TABLE_3_0_ENTRY_POINT. See
   section 6.5 EFI_HOB_GUID_TYPE.

   **AcpiTableAddress**

   Point to the SMBIOS table entry point.

DEVICE TREE HOB
~~~~~~~~~~~~~~~

   The bootloader might pass Device Tree through the GUID HOB to the
   payload. So that the payload could get the platform information from
   the table.

   | **HOB GUID**
   | **#define DEVICE_TREE_GUID \\**
   | **{0x6784b889, 0xb13c, 0x4c3b, {0xae, 0x4b, 0xf, 0xa, 0x2e, 0x32,
     0xe, 0xa3}}**

   **Hob Interface Structure**

   #pragma **pack**\ (1)

   | *///*
   | */// Bootloader Device Tree hob*
   | *///*
   | typedef struct {
   | EFI_HOB_GUID_TYPE Header;

   | UINT64 DeviceTreeAddress;
   | } DEVICE_TREE_HOB;

   #pragma pack()

   **Member Description**

   Header

   Header.Name set to DEVICE_TREE_GUID. See section 6.5
   EFI_HOB_GUID_TYPE.

   DeviceTreeAddress

   Point to the Device Tree entry point.

Graphics information HOB
~~~~~~~~~~~~~~~~~~~~~~~~

   If bootloader initializes the graphics device, the bootloader might
   report graphics mode and framebuffer information through
   **EFI_PEI_GRAPHICS_INFO_HOB**, and graphics hardware information
   through **EFI_PEI_GRAPHICS_DEVICE_INFO_HOB**.

   **EFI_PEI_GRAPHICS_INFO_HOB** and
   **EFI_PEI_GRAPHICS_DEVICE_INFO_HOB** provide the basic information
   for the graphics display. These HOBs are described in the *PI
   Specification.*

   Please refer Appendix 6.6 EFI_PEI_GRAPHICS_INFO_HOB and 6.7
   **EFI_PEI_GRAPHICS_DEVICE_INFO_HOB** for the details.

Serial Information HOB
~~~~~~~~~~~~~~~~~~~~~~

   If the debug device type and subtype are specified in DBG2, the
   bootloader should pass SERIAL_PORT_INFO hob to payload. This hob
   provides 16550 compatible serial debug port information from
   bootloader to payload.

   **Opens: Should we let bootloader provide debug callback** **for
   debug?**

   | **HOB GUID**
   | **#define SERIAL_INFO_GUID \\**
   | **{0xaa7e190d, 0xbe21, 0x4409, {0x8e, 0x67, 0xa2, 0xcd, 0xf, 0x61,
     0xe1, 0x70}}**

   **Hob Interface Structure**

   **#pragma pack(1)**

   typedef struct {

   UINT16 Reversion;

   BOOLEAN UseMmio;

   UINT8 RegisterWidth;

   UINT32 BaudRate;

   UINT64 RegisterBase;

   } SERIAL_PORT_INFO;

   **#pragma pack()**

   **Member Description**

   **UseMmio**

   Indicates the 16550 serial port registers are in MMIO space, or in
   I/O space.

   Reversion

   Use 0 for this spec

   **RegisterWidth**

   Indicates the access width for 16550 serial port registers, e.g.:

   8 - serial port registers are accessed in 8-bit width.

   32 - serial port registers are accessed in 32-bit width.

   **RegisterBase**

   Base address of 16550 serial port registers in MMIO or I/O space.

   **BaudRate**

   Baud rate for the 16550 compatible serial port.

   It could be 921600, 460800, 230400, 115200, 57600, 38400, 19200,
   9600, 7200, 4800, 3600, 2400, 2000, 1800, 1200, 600, 300, 150, 134,
   110, 75, 50

   Set to 0 to use the default baud rate 115200.

CPU INFO HOB
~~~~~~~~~~~~

   The bootloader should build a CPU information HOB to the payload.

   | **HOB Type**
   | EFI_HOB_TYPE_CPU

   **Hob Interface Structure**

   #pragma **pack**\ (1)

   | *///*
   | */// CPU info Hob*
   | *///*
   | typedef struct {
   | UINT8 Revision;

   UINT8 Reserved;

   UINT8 SizeOfMemorySpace;

   | UINT8 SizeOfIoSpace;
   | } PAYLOAD_CPU_INFO;
   | #pragma pack()

   **Member Description**

   **Revision**

   Use 0 for this structure.

   **SizeOfMemorySpace**

   The maximum physical memory addressability of the processor.

   **SizeOfIoSpace**

   The maximum physical I/O addressability of the processor.

Optional HOBs
~~~~~~~~~~~~~

   Some more HOBs could be built by bootloaders for advanced features.

   e.g.:

   Support FVs (also other format) from bootloader to payload

   Add debug log as HOB to payload

   **Opens**: Does the bootloader need report IO info to payload?

   Better let the bootloader to report it,

   **Opens**: does the HOB List need a checksum?

   It looks not too much value. Keep it open if we really need it.

   **Opens**: For some information it is already in ACPI table, should
   bootloader build HOB for same info?

   Payload could have a check to ACPI table to get basic info they need.

Appendix A – HOB Data Structures
================================

   The declarations/definitions provided here are derived from the EDK2
   source available for download at https://github.com/tianocore/edk2

Base Data Type
--------------

   | `https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Base.h
      <https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Base.h>`__

     typedef struct {
       UINT32 Data1;
       UINT16 Data2;
       UINT16 Data3;
       UINT8 Data4[8];
     } GUID;


   `https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Uefi/UefiBaseType.h
    <https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Uefi/UefiBaseType.h>`__\

     typedef GUID EFI_GUID;
     typedef UINT64 EFI_PHYSICAL_ADDRESS;

EFI HOB TYPE
------------

   https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiHob.h

   //

   // HobType of EFI_HOB_GENERIC_HEADER.

   //

   #define EFI_HOB_TYPE_HANDOFF 0x0001

   #define EFI_HOB_TYPE_MEMORY_ALLOCATION 0x0002

   #define EFI_HOB_TYPE_RESOURCE_DESCRIPTOR 0x0003

   #define EFI_HOB_TYPE_GUID_EXTENSION 0x0004

   #define EFI_HOB_TYPE_FV 0x0005

   #define EFI_HOB_TYPE_CPU 0x0006

   #define EFI_HOB_TYPE_MEMORY_POOL 0x0007

   #define EFI_HOB_TYPE_FV2 0x0009

   #define EFI_HOB_TYPE_LOAD_PEIM_UNUSED 0x000A

   #define EFI_HOB_TYPE_UEFI_CAPSULE 0x000B

   #define EFI_HOB_TYPE_FV3 0x000C

   #define EFI_HOB_TYPE_UNUSED 0xFFFE

   #define EFI_HOB_TYPE_END_OF_HOB_LIST 0xFFFF

EFI_HOB_GENERIC_HEADER
----------------------

   https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiHob.h

   ///

   /// Describes the format and size of the data inside the HOB.

   /// All HOBs must contain this generic HOB header.

   ///

   typedef struct {

   ///

   /// Identifies the HOB data structure type.

   ///

   UINT16 HobType;

   ///

   /// The length in bytes of the HOB.

   ///

   UINT16 HobLength;

   ///

   /// This field must always be set to zero.

   ///

   UINT32 Reserved;

   } EFI_HOB_GENERIC_HEADER;

HOB List Header
---------------

   https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiHob.h

EFI_HOB_HANDOFF_INFO_TABLE
~~~~~~~~~~~~~~~~~~~~~~~~~~

   ///

   /// Contains general state information used by the HOB producer
   phase.

   /// This HOB must be the first one in the HOB list.

   ///

   typedef struct {

   ///

   /// The HOB generic header. Header.HobType = EFI_HOB_TYPE_HANDOFF.

   ///

   EFI_HOB_GENERIC_HEADER Header;

   ///

   /// The version number pertaining to the PHIT HOB definition.

   /// This value is four bytes in length to provide an 8-byte aligned
   entry

   /// when it is combined with the 4-byte BootMode.

   ///

   UINT32 Version;

   ///

   /// The system boot mode as determined during the HOB producer phase.

   ///

   EFI_BOOT_MODE BootMode;

   ///

   /// The highest address location of memory that is allocated for use
   by the HOB producer

   /// phase. This address must be 4-KB aligned to meet page
   restrictions of UEFI.

   ///

   EFI_PHYSICAL_ADDRESS EfiMemoryTop;

   ///

   /// The lowest address location of memory that is allocated for use
   by the HOB producer phase.

   ///

   EFI_PHYSICAL_ADDRESS EfiMemoryBottom;

   ///

   /// The highest address location of free memory that is currently
   available

   /// for use by the HOB producer phase.

   ///

   EFI_PHYSICAL_ADDRESS EfiFreeMemoryTop;

   ///

   /// The lowest address location of free memory that is available for
   use by the HOB producer phase.

   ///

   EFI_PHYSICAL_ADDRESS EfiFreeMemoryBottom;

   ///

   /// The end of the HOB list.

   ///

   EFI_PHYSICAL_ADDRESS EfiEndOfHobList;

   } EFI_HOB_HANDOFF_INFO_TABLE;

EFI_HOB_HANDOFF_TABLE_VERSION
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   ///

   /// Value of version in EFI_HOB_HANDOFF_INFO_TABLE.

   ///

   #define EFI_HOB_HANDOFF_TABLE_VERSION 0x0009

EFI_BOOT_MODE
~~~~~~~~~~~~~

   | https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiBootMode.h

   ///

   /// EFI boot mode

   ///

   typedef UINT32 EFI_BOOT_MODE;

   //

   // 0x21 - 0xf..f are reserved.

   //

   #define BOOT_WITH_FULL_CONFIGURATION 0x00

   #define BOOT_WITH_MINIMAL_CONFIGURATION 0x01

   #define BOOT_ASSUMING_NO_CONFIGURATION_CHANGES 0x02

   #define BOOT_WITH_FULL_CONFIGURATION_PLUS_DIAGNOSTICS 0x03

   #define BOOT_WITH_DEFAULT_SETTINGS 0x04

   #define BOOT_ON_S4_RESUME 0x05

   #define BOOT_ON_S5_RESUME 0x06

   #define BOOT_WITH_MFG_MODE_SETTINGS 0x07

   #define BOOT_ON_S2_RESUME 0x10

   #define BOOT_ON_S3_RESUME 0x11

   #define BOOT_ON_FLASH_UPDATE 0x12

   #define BOOT_IN_RECOVERY_MODE 0x20

 EFI_HOB_GUID_TYPE
-----------------

   | This is the generic HOB header for GUID type HOB.
   | `https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiHob.h
      <https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiHob.h>`__
     ///

   /// Allows writers of executable content in the HOB producer phase to

   /// maintain and manage HOBs with specific GUID.

   ///

   typedef struct {

   ///

   /// The HOB generic header. Header.HobType =
   EFI_HOB_TYPE_GUID_EXTENSION.

   ///

   EFI_HOB_GENERIC_HEADER Header;

   ///

   /// A GUID that defines the contents of this HOB.

   ///

   EFI_GUID Name;

   //

   // Guid specific data goes here

   //

   } EFI_HOB_GUID_TYPE;

 EFI_PEI_GRAPHICS_INFO_HOB
-------------------------

   `https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Guid/GraphicsInfoHob.h
    <https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Guid/GraphicsInfoHob.h>`__
   https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Protocol/GraphicsOutput.h

   | **HOB GUID**
   | #define EFI_PEI_GRAPHICS_INFO_HOB_GUID \\
   | {0x39f62cce, 0x6825, 0x4669, {0xbb, 0x56, 0x54, 0x1a, 0xba, 0x75,
     0x3a, 0x07}}

   **Hob Interface Structure**

   | typedef struct {
   | EFI_PHYSICAL_ADDRESS FrameBufferBase;
   | UINT32 FrameBufferSize;
   | EFI_GRAPHICS_OUTPUT_MODE_INFORMATION GraphicsMode;
   | } EFI_PEI_GRAPHICS_INFO_HOB;

   **Related Definitions**

   typedef struct {

   UINT32 RedMask;

   UINT32 GreenMask;

   UINT32 BlueMask;

   UINT32 ReservedMask;

   } EFI_PIXEL_BITMASK;

   | If a bit is set in *RedMask*, *GreenMask*, or *BlueMask* then those
     bits of the pixel represent the
   | corresponding color. Bits in *RedMask*, *GreenMask*, *BlueMask*,
     and *ReserverdMask* must not overlap bit
   | positions. The values for the red, green, and blue components in
     the bit mask represent the color
   | intensity. The color intensities must increase as the color values
     for each color mask increase with a
   | minimum intensity of all bits in a color mask clear to a maximum
     intensity of all bits in a color mask set.

   typedef enum {

   ///

   /// A pixel is 32-bits and byte zero represents red, byte one
   represents green,

   /// byte two represents blue, and byte three is reserved. This is the
   definition

   /// for the physical frame buffer. The byte values for the red,
   green, and blue

   /// components represent the color intensity. This color intensity
   value range

   /// from a minimum intensity of 0 to maximum intensity of 255.

   ///

   PixelRedGreenBlueReserved8BitPerColor,

   ///

   /// A pixel is 32-bits and byte zero represents blue, byte one
   represents green,

   /// byte two represents red, and byte three is reserved. This is the
   definition

   /// for the physical frame buffer. The byte values for the red,
   green, and blue

   /// components represent the color intensity. This color intensity
   value range

   /// from a minimum intensity of 0 to maximum intensity of 255.

   ///

   PixelBlueGreenRedReserved8BitPerColor,

   ///

   /// The Pixel definition of the physical frame buffer.

   ///

   PixelBitMask,

   ///

   /// This mode does not support a physical frame buffer.

   ///

   PixelBltOnly,

   ///

   /// Valid EFI_GRAPHICS_PIXEL_FORMAT enum values are less than this
   value.

   ///

   PixelFormatMax

   } EFI_GRAPHICS_PIXEL_FORMAT;

   typedef struct {

   ///

   /// The version of this data structure. A value of zero represents
   the

   /// EFI_GRAPHICS_OUTPUT_MODE_INFORMATION structure as defined in this
   specification.

   ///

   UINT32 Version;

   ///

   /// The size of video screen in pixels in the X dimension.

   ///

   UINT32 HorizontalResolution;

   ///

   /// The size of video screen in pixels in the Y dimension.

   ///

   UINT32 VerticalResolution;

   ///

   /// Enumeration that defines the physical format of the pixel. A
   value of PixelBltOnly

   /// implies that a linear frame buffer is not available for this
   mode.

   ///

   EFI_GRAPHICS_PIXEL_FORMAT PixelFormat;

   ///

   /// This bitmask is only valid if PixelFormat is set to
   PixelPixelBitMask.

   /// A bit being set defines what bits are used for what purpose such
   as Red, Green, Blue, or Reserved.

   ///

   EFI_PIXEL_BITMASK PixelInformation;

   ///

   /// Defines the number of pixel elements per video memory line.

   ///

   UINT32 PixelsPerScanLine;

   } EFI_GRAPHICS_OUTPUT_MODE_INFORMATION;

   **NOTE:** for performance reasons, or due to hardware restrictions,
   scan lines may be padded to an amount of memory alignment. These
   padding pixel elements are outside the area covered by
   *HorizontalResolution* and are not visible. For direct frame buffer
   access, this number is used as a span between starts of pixel lines
   in video memory. Based on the size of an individual pixel element and
   *PixelsPerScanline*, the offset in video memory from pixel element
   (x, y) to pixel element (x, y+1) has to be calculated as "sizeof(
   PixelElement ) \* PixelsPerScanLine", not "sizeof( PixelElement ) \*
   HorizontalResolution", though in many cases those values can
   coincide. This value can depend on video hardware and mode
   resolution. GOP implementation is responsible for providing accurate
   value for this field.

EFI_PEI_GRAPHICS_DEVICE_INFO_HOB
--------------------------------

   `https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Guid/GraphicsInfoHob.h
    <https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Guid/GraphicsInfoHob.h>`__
   **HOB GUID**

   | #define EFI_PEI_GRAPHICS_DEVICE_INFO_HOB_GUID \\
   | {0xe5cb2ac9, 0xd35d, 0x4430, {0x93, 0x6e, 0x1d, 0xe3, 0x32, 0x47,
     0x8d, 0xe7}}

   **Hob Interface Structure**

   typedef struct {

   UINT16 VendorId; ///< Ignore if the value is 0xFFFF.

   UINT16 DeviceId; ///< Ignore if the value is 0xFFFF.

   UINT16 SubsystemVendorId; ///< Ignore if the value is 0xFFFF.

   UINT16 SubsystemId; ///< Ignore if the value is 0xFFFF.

   UINT8 RevisionId; ///< Ignore if the value is 0xFF.

   UINT8 BarIndex; ///< Ignore if the value is 0xFF.

   } EFI_PEI_GRAPHICS_DEVICE_INFO_HOB;

 EFI_HOB_RESOURCE_DESCRIPTOR
---------------------------

   https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiHob.h

EFI_RESOURCE_TYPE
~~~~~~~~~~~~~~~~~

   ///

   /// The resource type

   ///

   typedef UINT32 EFI_RESOURCE_TYPE;

   ///

   /// Value of ResourceType in EFI_HOB_RESOURCE_DESCRIPTOR.

   ///

   #define EFI_RESOURCE_SYSTEM_MEMORY 0x00000000

   #define EFI_RESOURCE_MEMORY_MAPPED_IO 0x00000001

   #define EFI_RESOURCE_IO 0x00000002

   #define EFI_RESOURCE_FIRMWARE_DEVICE 0x00000003

   #define EFI_RESOURCE_MEMORY_MAPPED_IO_PORT 0x00000004

   #define EFI_RESOURCE_MEMORY_RESERVED 0x00000005

   #define EFI_RESOURCE_IO_RESERVED 0x00000006

   #define EFI_RESOURCE_MAX_MEMORY_TYPE 0x00000007

 EFI_RESOURCE_ATTRIBUTE_TYPE
~~~~~~~~~~~~~~~~~~~~~~~~~~~

   ///

   /// A type of recount attribute type.

   ///

   typedef UINT32 EFI_RESOURCE_ATTRIBUTE_TYPE;

   //

   // These types can be ORed together as needed.

   //

   // The following attributes are used to describe settings

   //

   #define EFI_RESOURCE_ATTRIBUTE_PRESENT 0x00000001

   #define EFI_RESOURCE_ATTRIBUTE_INITIALIZED 0x00000002

   #define EFI_RESOURCE_ATTRIBUTE_TESTED 0x00000004

   #define EFI_RESOURCE_ATTRIBUTE_READ_PROTECTED 0x00000080

   //

   // This is typically used as memory cacheability attribute today.

   // NOTE: Since PI spec 1.4, please use
   EFI_RESOURCE_ATTRIBUTE_READ_ONLY_PROTECTED

   // as Physical write protected attribute, and
   EFI_RESOURCE_ATTRIBUTE_WRITE_PROTECTED

   // means Memory cacheability attribute: The memory supports being
   programmed with

   // a writeprotected cacheable attribute.

   //

   #define EFI_RESOURCE_ATTRIBUTE_WRITE_PROTECTED 0x00000100

   #define EFI_RESOURCE_ATTRIBUTE_EXECUTION_PROTECTED 0x00000200

   #define EFI_RESOURCE_ATTRIBUTE_PERSISTENT 0x00800000

   //

   // The rest of the attributes are used to describe capabilities

   //

   #define EFI_RESOURCE_ATTRIBUTE_SINGLE_BIT_ECC 0x00000008

   #define EFI_RESOURCE_ATTRIBUTE_MULTIPLE_BIT_ECC 0x00000010

   #define EFI_RESOURCE_ATTRIBUTE_ECC_RESERVED_1 0x00000020

   #define EFI_RESOURCE_ATTRIBUTE_ECC_RESERVED_2 0x00000040

   #define EFI_RESOURCE_ATTRIBUTE_UNCACHEABLE 0x00000400

   #define EFI_RESOURCE_ATTRIBUTE_WRITE_COMBINEABLE 0x00000800

   #define EFI_RESOURCE_ATTRIBUTE_WRITE_THROUGH_CACHEABLE 0x00001000

   #define EFI_RESOURCE_ATTRIBUTE_WRITE_BACK_CACHEABLE 0x00002000

   #define EFI_RESOURCE_ATTRIBUTE_16_BIT_IO 0x00004000

   #define EFI_RESOURCE_ATTRIBUTE_32_BIT_IO 0x00008000

   #define EFI_RESOURCE_ATTRIBUTE_64_BIT_IO 0x00010000

   #define EFI_RESOURCE_ATTRIBUTE_UNCACHED_EXPORTED 0x00020000

   #define EFI_RESOURCE_ATTRIBUTE_READ_PROTECTABLE 0x00100000

   //

   // This is typically used as memory cacheability attribute today.

   // NOTE: Since PI spec 1.4, please use
   EFI_RESOURCE_ATTRIBUTE_READ_ONLY_PROTECTABLE

   // as Memory capability attribute: The memory supports being
   protected from processor

   // writes, and EFI_RESOURCE_ATTRIBUTE_WRITE_PROTEC TABLE means Memory
   cacheability attribute:

   // The memory supports being programmed with a writeprotected
   cacheable attribute.

   //

   #define EFI_RESOURCE_ATTRIBUTE_WRITE_PROTECTABLE 0x00200000

   #define EFI_RESOURCE_ATTRIBUTE_EXECUTION_PROTECTABLE 0x00400000

   #define EFI_RESOURCE_ATTRIBUTE_PERSISTABLE 0x01000000

   #define EFI_RESOURCE_ATTRIBUTE_READ_ONLY_PROTECTED 0x00040000

   #define EFI_RESOURCE_ATTRIBUTE_READ_ONLY_PROTECTABLE 0x00080000

   //

   // Physical memory relative reliability attribute. This

   // memory provides higher reliability relative to other

   // memory in the system. If all memory has the same

   // reliability, then this bit is not used.

   //

   #define EFI_RESOURCE_ATTRIBUTE_MORE_RELIABLE 0x02000000

.. _efi_hob_resource_descriptor-1:

 EFI_HOB_RESOURCE_DESCRIPTOR
~~~~~~~~~~~~~~~~~~~~~~~~~~~

   ///

   /// Describes the resource properties of all fixed,

   /// nonrelocatable resource ranges found on the processor

   /// host bus during the HOB producer phase.

   ///

   typedef struct {

   ///

   /// The HOB generic header. Header.HobType =
   EFI_HOB_TYPE_RESOURCE_DESCRIPTOR.

   ///

   EFI_HOB_GENERIC_HEADER Header;

   ///

   /// A GUID representing the owner of the resource. This GUID is used
   by HOB

   /// consumer phase components to correlate device ownership of a
   resource.

   ///

   EFI_GUID Owner;

   ///

   /// The resource type enumeration as defined by EFI_RESOURCE_TYPE.

   ///

   EFI_RESOURCE_TYPE ResourceType;

   ///

   /// Resource attributes as defined by EFI_RESOURCE_ATTRIBUTE_TYPE.

   ///

   EFI_RESOURCE_ATTRIBUTE_TYPE ResourceAttribute;

   ///

   /// The physical start address of the resource region.

   ///

   EFI_PHYSICAL_ADDRESS PhysicalStart;

   ///

   /// The number of bytes of the resource region.

   ///

   UINT64 ResourceLength;

   } EFI_HOB_RESOURCE_DESCRIPTOR;

 EFI_HOB_MEMORY_ALLOCATION
-------------------------

EFI_MEMORY_TYPE
~~~~~~~~~~~~~~~

   https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Uefi/UefiMultiPhase.h

   ///

   /// Enumeration of memory types introduced in UEFI.

   ///

   typedef enum {

   ///

   /// Not used.

   ///

   EfiReservedMemoryType,

   ///

   /// The code portions of a loaded application.

   /// (Note that UEFI OS loaders are UEFI applications.)

   ///

   EfiLoaderCode,

   ///

   /// The data portions of a loaded application and the default data
   allocation

   /// type used by an application to allocate pool memory.

   ///

   EfiLoaderData,

   ///

   /// The code portions of a loaded Boot Services Driver.

   ///

   EfiBootServicesCode,

   ///

   /// The data portions of a loaded Boot Serves Driver, and the default
   data

   /// allocation type used by a Boot Services Driver to allocate pool
   memory.

   ///

   EfiBootServicesData,

   ///

   /// The code portions of a loaded Runtime Services Driver.

   ///

   EfiRuntimeServicesCode,

   ///

   /// The data portions of a loaded Runtime Services Driver and the
   default

   /// data allocation type used by a Runtime Services Driver to
   allocate pool memory.

   ///

   EfiRuntimeServicesData,

   ///

   /// Free (unallocated) memory.

   ///

   EfiConventionalMemory,

   ///

   /// Memory in which errors have been detected.

   ///

   EfiUnusableMemory,

   ///

   /// Memory that holds the ACPI tables.

   ///

   EfiACPIReclaimMemory,

   ///

   /// Address space reserved for use by the firmware.

   ///

   EfiACPIMemoryNVS,

   ///

   /// Used by system firmware to request that a memory-mapped IO region

   /// be mapped by the OS to a virtual address so it can be accessed by
   EFI runtime services.

   ///

   EfiMemoryMappedIO,

   ///

   /// System memory-mapped IO region that is used to translate memory

   /// cycles to IO cycles by the processor.

   ///

   EfiMemoryMappedIOPortSpace,

   ///

   /// Address space reserved by the firmware for code that is part of
   the processor.

   ///

   EfiPalCode,

   ///

   /// A memory region that operates as EfiConventionalMemory,

   /// however it happens to also support byte-addressable
   non-volatility.

   ///

   EfiPersistentMemory,

   EfiMaxMemoryType

   } EFI_MEMORY_TYPE;

   https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiHob.h

**11.6.2 EFI_HOB_MEMORY_ALLOCATION_HEADER**

   /// EFI_HOB_MEMORY_ALLOCATION_HEADER describes the

   /// various attributes of the logical memory allocation. The type
   field will be used for

   /// subsequent inclusion in the UEFI memory map.

   ///

   typedef struct {

   ///

   /// A GUID that defines the memory allocation region's type and
   purpose, as well as

   /// other fields within the memory allocation HOB. This GUID is used
   to define the

   /// additional data within the HOB that may be present for the memory
   allocation HOB.

   /// Type EFI_GUID is defined in InstallProtocolInterface() in the
   UEFI 2.0

   /// specification.

   ///

   EFI_GUID Name;

   ///

   /// The base address of memory allocated by this HOB. Type

   /// EFI_PHYSICAL_ADDRESS is defined in AllocatePages() in the UEFI
   2.0

   /// specification.

   ///

   EFI_PHYSICAL_ADDRESS MemoryBaseAddress;

   ///

   /// The length in bytes of memory allocated by this HOB.

   ///

   UINT64 MemoryLength;

   ///

   /// Defines the type of memory allocated by this HOB. The memory type
   definition

   /// follows the EFI_MEMORY_TYPE definition. Type EFI_MEMORY_TYPE is
   defined

   /// in AllocatePages() in the UEFI 2.0 specification.

   ///

   EFI_MEMORY_TYPE MemoryType;

   ///

   /// Padding for Itanium processor family

   ///

   UINT8 Reserved[4];

   } EFI_HOB_MEMORY_ALLOCATION_HEADER;

**11.6.3 EFI_HOB_MEMORY_ALLOCATION**

   /// Describes all memory ranges used during the HOB producer

   /// phase that exist outside the HOB list. This HOB type

   /// describes how memory is used, not the physical attributes of
   memory.

   ///

   typedef struct {

   ///

   /// The HOB generic header. Header.HobType =
   EFI_HOB_TYPE_MEMORY_ALLOCATION.

   ///

   EFI_HOB_GENERIC_HEADER Header;

   ///

   /// An instance of the EFI_HOB_MEMORY_ALLOCATION_HEADER that
   describes the

   /// various attributes of the logical memory allocation.

   ///

   EFI_HOB_MEMORY_ALLOCATION_HEADER AllocDescriptor;

   //

   // Additional data pertaining to the "Name" Guid memory

   // may go here.

   //

   } EFI_HOB_MEMORY_ALLOCATION;
