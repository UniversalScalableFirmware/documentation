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

Open: Do we need a set of configuration data to config payload?

  We do not believe so.

Open: Do we need pass data from payload to bootloader to impact bootloader behavior in next boot?

  Keep it open now.

Open: will payload be run in S3 path?

  Suggest skipping payload.

.. _acpi_tables:

ACPI tables
-----------

ACPI table is required to boot modern operation system, especially to boot windows operating system.
The bootloader should provide a ACPI RSDP HOB. In the ACPI table least RSDT, FADT and MCFG should be available to the payload.
Payload could remove/add/modify the ACPI table passed from the bootloader if required.

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
`http://www.pcisig.com <http://www.pcisig.com/>`.

And another example is on the debug device info. The bootloader might
report debug device following up ACPI Debug Port Table 2 (DBG2). If a
fully 16550-compatible serial device is specified in the ACPI DBG2,
bootloader should provide a Serial Debug Information HOB in the HOB
list so that the payload could use same debug device with same
setting. If the ACPI DBG2 table could not be found, the payload
should use serial device provided by the Serial Debug Information HOB
as the default debug device.


.. hob_list:

HOB List
--------

The bootloader should build a HOB list and pass the HOB list header
to payload when passing control to payload. The HOB format is
described in the *Platform Initialization (PI) Specification - Volume
3: Shared Architectural Elements*.

There are two sections below describing the HOBs produced by the
bootloader and consumed by the payload for providing the system
architecturally information.

First section describes the HOBs defined in *Platform Initialization
Specification Volume 3: Shared Architectural elements*.

Second section defines the new HOBs.

Reusing Interfaces in Platform Initialization Specification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PHIT(Phase Handoff Info Table) HOB
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The bootloader should report the general state information through
the HOB following EFI_HOB_HANDOFF_INFO_TABLE format defined in
*Platform Initialization Specification Volume 3: Shared Architectural
elements*.

CPU HOB
^^^^^^^

The bootloader should report the processor information including address space
and I/O space capabilities to the payload through the HOB following
EFI_HOB_CPU format defined in *Platform Initialization Specification Volume 3:
Shared Architectural elements*.

Resource Descriptor HOB
^^^^^^^^^^^^^^^^^^^^^^^

The bootloader should report the system resources through the HOB
following EFI_HOB_RESOURCE_DESCRIPTOR format defined in *Platform
Initialization Specification Volume 3: Shared Architectural
elements*.

For example, any physical memory found in bootloader should be
reported using resource type EFI_RESOURCE_SYSTEM_MEMORY, and the
reserved memory used by bootloader should be reported using resource
type EFI_RESOURCE_MEMORY_RESERVED.

I/O and memory mapped I/O resource should also be reported using
resource type EFI_RESOURCE_IO and EFI_RESOURCE_MEMORY_MAPPED_IO.

Memory Allocation HOB
^^^^^^^^^^^^^^^^^^^^^

The bootloader should report the memory usages that exist outside the
HOB list through the HOB following EFI_HOB_MEMORY_ALLOCATION format defined
in *Platform Initialization Specification Volume 3: Shared Architectural
elements*.

Boot-Strap Processor (BSP) Stack Memory Allocation HOB
''''''''''''''''''''''''''''''''''''''''''''''''''''''

The bootloader should report the initial stack prepared for payload through
the HOB following EFI_HOB_MEMORY_ALLOCATION_STACK format defined in *Platform
Initialization Specification Volume 3: Shared Architectural elements*.

Memory Allocation Module HOB
''''''''''''''''''''''''''''

The bootloader should report the payload memory location and entry point
through the HOB following EFI_HOB_MEMORY_ALLOCATION_MODULE format defined
in *Platform Initialization Specification Volume 3: Shared Architectural
elements*.

Graphics information HOB
^^^^^^^^^^^^^^^^^^^^^^^^

If bootloader initializes the graphics device, the bootloader might
report graphics mode and framebuffer information through
EFI_PEI_GRAPHICS_INFO_HOB, and graphics hardware information
through EFI_PEI_GRAPHICS_DEVICE_INFO_HOB.

EFI_PEI_GRAPHICS_INFO_HOB and EFI_PEI_GRAPHICS_DEVICE_INFO_HOB provide the basic information
for the graphics display. These HOBs are described in the *PI Specification.*

Please refer Appendix 6.6 EFI_PEI_GRAPHICS_INFO_HOB and 6.7 EFI_PEI_GRAPHICS_DEVICE_INFO_HOB for the details.

New Interfaces
~~~~~~~~~~~~~~

Common Payload Header
^^^^^^^^^^^^^^^^^^^^^^^^^

All new interfaces are GUID type HOBs starting with ``EFI_HOB_GUID_TYPE`` defined in the PI Specification.

The HOB data starts with a common header defined as below::

  #pragma pack(1)
  
  typedef struct {
    UINT8                Revision;
    UINT8                Reserved[3];
  } PLD_GENERIC_HEADER;

  #pragma pack()

HOB data for different interfaces is defined in following sections.

ACPI Table HOB
^^^^^^^^^^^^^^

The bootloader should pass ACPI table through the GUID HOB to the payload. So that the payload could get the platform information from the ACPI table.

Build the different HOBs for different table using standard defined GUID.

**HOB GUID**::

  #define EFI_ACPI_TABLE_GUID  {0x8868e871, 0xe4f1, 0x11d3, {0xbc, 0x22, 0x0, 0x80, 0xc7, 0x3c, 0x88, 0x81}}

.. Note:: This GUID reuses the same GUID defined in UEFI spec chapter 4.6 EFI Configuration Table

**Hob Interface Structure**

Payload ACPI table HOB::

  #pragma pack (1)

  typedef struct {
    EFI_HOB_GUID_TYPE   Header;
    UINT64              TableAddress;
  } ACPI_TABLE_HOB;

  #pragma pack()

**Member Description**

``Header``

Header.Name set to EFI_ACPI_TABLE_GUID. See section 6.5
EFI_HOB_GUID_TYPE.

``TableAddress``

Point to the ACPI RSDP table. The ACPI table need follow ACPI specification verson 2.0 or above.

SMBIOS Table HOB
^^^^^^^^^^^^^^^^

The bootloader might pass SMBIOS table through the GUID HOB to the
payload. So that the payload could get the platform information from
the table.

**HOB GUID**::

  #define    SMBIOS_TABLE_GUID    {0xeb9d2d31, 0x2d88, 0x11d3, {0x9a, 0x16, 0x0, 0x90, 0x27, 0x3f, 0xc1, 0x4d}}

  #define    SMBIOS3_TABLE_GUID   {0xf2fd1544, 0x9794, 0x4a2c, {0x99, 0x2e, 0xe5, 0xbb, 0xcf, 0x20, 0xe3, 0x94}}

.. Note:: These GUIDs reuse the same GUIDs defined in UEFI spec chapter 4.6 EFI Configuration Table

**Hob Interface Structure**::

  #pragma pack (1)

  //
  // Bootloader SMBIOS table hob
  //
  typedef struct {
    EFI_HOB_GUID_TYPE   Header;
    UINT64              TableAddress;
  } SMBIOS_TABLE_HOB;

  #pragma pack()

**Member Description**

``Header``

Header.Name set to SMBIOS_TABLE_GUID if SMBIOS table from
TableAddress follows the format defined by SMBIOS_TABLE_ENTRY_POINT,
or set to SMBIOS3_TABLE_GUID if SMBIOS table from TableAddress
follows the format defied by SMBIOS_TABLE_3_0_ENTRY_POINT. See
section 6.5 EFI_HOB_GUID_TYPE.

``AcpiTableAddress``

Point to the SMBIOS table entry point.

DEVICE TREE HOB
^^^^^^^^^^^^^^^

The bootloader might pass Device Tree through the GUID HOB to the
payload. So that the payload could get the platform information from
the table.

**HOB GUID**::

  #define    DEVICE_TREE_GUID    {0x6784b889, 0xb13c, 0x4c3b, {0xae, 0x4b, 0xf, 0xa, 0x2e, 0x32, 0xe, 0xa3}}

**Hob Interface Structure**::

  #pragma pack (1)

  //
  // Bootloader Device Tree hob
  //
  typedef struct {
    EFI_HOB_GUID_TYPE     Header;
    UINT64                DeviceTreeAddress;
  } DEVICE_TREE_HOB;

  #pragma pack()

**Member Description**

``Header``

Header.Name set to DEVICE_TREE_GUID. See section 6.5 EFI_HOB_GUID_TYPE.

``DeviceTreeAddress``

Point to the Device Tree entry point.

Serial Information HOB
^^^^^^^^^^^^^^^^^^^^^^

If the debug device type and subtype are specified in DBG2, the
bootloader should pass SERIAL_PORT_INFO hob to payload. This hob
provides 16550 compatible serial debug port information from
bootloader to payload.

**Opens: Should we let bootloader provide debug callback** **for debug?**

**HOB GUID**::

  #define    SERIAL_INFO_GUID    {0xaa7e190d, 0xbe21, 0x4409, {0x8e, 0x67, 0xa2, 0xcd, 0xf, 0x61, 0xe1, 0x70}}

**Hob Interface Structure**::

  #pragma pack(1)

  typedef struct {
    UINT16     Reversion;
    BOOLEAN    UseMmio;
    UINT8      RegisterWidth;
    UINT32     BaudRate;
    UINT64     RegisterBase;
  } SERIAL_PORT_INFO;

  #pragma pack()

**Member Description**

``UseMmio``

Indicates the 16550 serial port registers are in MMIO space, or in I/O space.

``Reversion``

Use 0 for this spec

``RegisterWidth``

Indicates the access width for 16550 serial port registers, e.g.:

  8 - serial port registers are accessed in 8-bit width.

  32 - serial port registers are accessed in 32-bit width.

``RegisterBase``

Base address of 16550 serial port registers in MMIO or I/O space.

``BaudRate``

Baud rate for the 16550 compatible serial port.

It could be 921600, 460800, 230400, 115200, 57600, 38400, 19200,
9600, 7200, 4800, 3600, 2400, 2000, 1800, 1200, 600, 300, 150, 134,
110, 75, 50

Set to 0 to use the default baud rate 115200.

Optional Interfaces
~~~~~~~~~~~~~~~~~~~

Some more HOBs could be built by bootloaders for advanced features. e.g.:

  Support FVs (also other format) from bootloader to payload

  Add debug log as HOB to payload

**Opens**: Does the bootloader need report IO info to payload?

      Better let the bootloader to report it,

**Opens**: does the HOB List need a checksum?

      It looks not too much value. Keep it open if we really need it.

**Opens**: For some information it is already in ACPI table, should bootloader build HOB for same info?

      Payload could have a check to ACPI table to get basic info they need.

