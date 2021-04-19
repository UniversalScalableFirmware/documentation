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

   This is the generic HOB header for GUID type HOB.

   | https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiHob.h

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
--------------------------

   | https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Guid/GraphicsInfoHob.h

   | https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Protocol/GraphicsOutput.h

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

   | https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Guid/GraphicsInfoHob.h

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

   | https://github.com/tianocore/edk2/blob/master/MdePkg/Include/Pi/PiHob.h

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
