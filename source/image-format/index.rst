Payload Image Format
====================

   Payload, as a standalone component, usually needs to be loaded by a
   bootloader into memory properly prior to execution. In this loading
   process, some additional process might be required, such as rebasing,
   assembling, etc.

   Today, many payloads use their own image formats (PE, ELF, FV, RAW,
   …), and it makes it difficult for a bootloader to identify and
   understand how to load a payload. To address this, a small common
   payload image header is introduced at the beginning of the payload
   image to describe necessary information required for loading.

   The following information might be required by a bootloader to load
   payload image:

-

-  Version information

-  Architecture

-  Entry point

-  Relocation information

-  Preferred base

-  Verification

Opens:

   There are several options here for bootloader on how to load a
   payload. Inputs are required to decide which option might be the best
   approach. The current proposal used option 1.

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

a)

b)

c)

d)

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
