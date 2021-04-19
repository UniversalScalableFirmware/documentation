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
   up of two distinct phases (**initialization** and **OS boot logic**)
   is gaining traction resulting in newer implementations of system
   firmware. This approach calls for modular phases with an
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

   It is SBL payload implementation that supports Linux boot protocol and
   can also launch ELF or PE executables. It also supports launching OS
   compliant with the MultiBoot specification.

   **Linux Payload**

   LinuxBoot is a firmware for modern servers that replaces specific
   firmware functionality like the UEFI DXE phase with a Linux kernel
   and runtime.

   https://www.linuxboot.org/

Bootloader interfaces
---------------------

Coreboot Payload Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Slim Bootloader (SBL) Payload Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Reference**:
   https://slimbootloader.github.io/developer-guides/payload.html

   **Reference**:
   https://uefi.org/sites/default/files/resources/PI_Spec_1_7_final_Jan_2019.pdf

   **Reference**:
   https://github.com/tianocore/edk2/blob/master/UefiPayloadPkg/Library/SblParseLib/SblParseLib.c

   SBL supports 'loosely coupled payload' which basically refers to
   payloads built independently (no source sharing). SBL builds a series
   of data structures called the Hand Off Blocks (HOBs) and provides a
   pointer to this HOB List to the payloads. These data structures
   conform to the HOB format as described in the Platform Initialization
   (PI) Specification.

PEI to DXE Interface
~~~~~~~~~~~~~~~~~~~~

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
   for operating system specific boot loaders.

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
   purpose: ACPI and Device Tree.

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
     that is simple to parse).

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
     by recording code executed in the payload phase into PCRs (e.g.,
     UEFI driver into PCR[2], UEFI OS loader into PCR[4]).
   | *Open: Do we need a capability boot to say if payload
     supports/requires measured/verified boot?*
