.. image:: images/image1.jpeg
   :width: 6.5in
   :height: 4.0625in

Universal Scalable Firmware (USF) Specification

**Version 0.7**

**October 2021**

© Copyright Content on document licensed under a Creative Commons 
Attribution 4.0 International license


Terminology
===========

   There has been a lot of confusion regarding the terminologies
   surrounding firmware and BIOS. This section describes these
   terminologies as used in this specification. Just like “Operating
   System” (OS) is a generic name for the concept of Post-Boot
   Environment, “Basic Input Output System” (BIOS) is a generic name for
   the concept of Pre-Boot Environment. Just like there are multiple
   implementations of the concept of OS, such as Linux, there are
   various implementations of the concept of BIOS, such as UEFI FW,
   u-boot, coreboot, Slim bootloader etc.

   Tiano, EDKII and Min Platform are all implementations based on the
   “Universal Extensible Firmware Interface” (UEFI) and “Platform
   Initialization” (PI) interface specifications (uefi.org).

   This Specification uses the terminology Firmware/System Firmware/BIOS
   interchangeably to indicate the Pre-Boot environment

Motivation for Universal Scalable Firmware
---------------------------------------------

   UEFI and PI Spec based BIOS implementations such as Tiano and EDKII
   has served the industry well for the past couple of decades. The goal
   is to evolve the goodness of modularity to scale for IP FW
   development model, with emphasis on simplicity, scalability,
   debuggability, readability and determinism.

Simplicity, Determinisim and Debuggability
---------------------------------------------

   All the three attributes – Simplicity, Determinism and Debuggability
   go together. BIOS plays a major role in debugging hardware, silicon
   features and various technologies (Security, Power Management, IO,
   Virtualization, RAS etc.) and should lend itself to readability and
   determining the sequence of operations by reading the source code.
   BIOS is the abstraction layer and it often times have to deal with
   unstable hardware and Silicon workarounds. A simple, debug (hardware
   debug, not just software) friendly infrastructure is called for.

   Today’s platform and SoC complexity calls for a model of replaceable
   IP Modules, with the associated FW components traveling with that IP.

   The layers of the Universal Scalable Firmware are described in the
   following diagram.

.. image:: images/image2.jpg
   :alt: A picture containing graphical user interface
   :width: 6.5in
   :height: 6.85208in

Figure 1 USF stack

   From the top of the stack we have the following.

OS interface
---------------

   These are well-known interfaces, such as ACPI, UEFI, Kexec, or
   Multiboot, that provide a means to interact with pre-OS and runtimes.

Universal Payload
-----------------------

Universal Payload API for different OS payloads (i.e., UEFI, LinuxBoot, ACRN embedded hypervisor), and support for various bootloaders (i.e., tianocore/EDKII, coreboot, slim bootloader, and u-boot.

Platform Orchestration Layer (POL)
-------------------------------------

   Simplified ACPI support, common libraries for various bootloaders &
   Rust language, standard binary configuration through YAML, support
   for FW attestation, authentication, measurement, and modern update.

Scalable Firmware Support Package (sFSP)
--------------------------------------------

   Scalable Firmware Support Package (sFSP) support for 64-bit reset
   vector, SMM encapsulation, various domain modules, authentication,
   unified configuration, and SOC level validation.

