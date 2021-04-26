Payload Image Format
====================

Payload, as a standalone component, usually needs to be loaded by a
bootloader into memory properly prior to execution. In this loading
process, additional process might be required, such as assembling,
rebasing, authenticating, etc. Today, many payloads use
their own image formats (PE, ELF, FV, RAW, etc.), and it is very
challenging for a bootloader to identify and support all of them.  

To address this, a common payload image format is desired to
facilitate the payload loading process. Instead of defining a new
image format for payloads, it is preferred to reuse an already-existing
format, such as ELF (Executable and Linkable Format) and PE (Portable
Executable). This specification selects the ELF image format as the
common universal payload image format since it is is flexible, extensible,
and cross-platform. It is also adopted by many different operating systems
on many different hardware platforms.

For detailed information on the ELF image format, please see
`ELF Specification <https://refspecs.linuxfoundation.org/elf/elf.pdf>`_ .


Payload Image Sections
----------------------
To use ELF image as universal payload image format, it is required to define
a simple way for bootloader to differenciate a universal payload image from
a regular ELF image. On the other side, a universal payload might aslo need
addtional image information to proceed with the boot flow. This specifciation
requires the universal payload image to provide these addtional requried
inforamtion through new defined ELF sections, *Universal Payload Information
Section* and *Universal Payload Loaded Image Section*.


Universal Payload Information Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This specification requires a mandatory ELF universal payload information section
to indicate the ELF image conforms to this specification. If this section is found
inside the ELF image and is valid, the bootloader can retrieve universal payload
specific information from this section, such as payload version, payload ID, etc.
And the bootloader shall use the interfaces defined in this specification to handoff
the control to the payload.

This Universal Payload Information section must:

-  Have section name defined as ".upld_info"

-  Have section aligned at 4-byte boundary within the ELF image.

-  Contain UNIVERSAL_PAYLOAD_INFO structure in its section, as
   defined as below:

**UNIVERSAL_PAYLOAD_INFO Strcuture**

+-----------------+-----------------+-----------------+-----------------+
| **              | Size in Bytes   | Field           | Description     |
| **              |                 |                 |                 |
| Byte Offset     |                 |                 |                 |
+=================+=================+=================+=================+
| 0               | 4               | Identifier      | 'PLDH'          |
|                 |                 |                 | Identifier for  |
|                 |                 |                 | the unverial    |
|                 |                 |                 | payload info.   |
+-----------------+-----------------+-----------------+-----------------+
| 4               | 4               | HeaderLength    | Length of the   |
|                 |                 |                 | structure in    |
|                 |                 |                 | bytes.          |
+-----------------+-----------------+-----------------+-----------------+
| 8               | 2               | SpecRevision    | Indicates       |
|                 |                 |                 | compliance with |
|                 |                 |                 | a revision of   |
|                 |                 |                 | this            |
|                 |                 |                 | specification   |
|                 |                 |                 | in the BCD      |
|                 |                 |                 | format.         |
|                 |                 |                 |                 |
|                 |                 |                 | 7 : 0 - Minor   |
|                 |                 |                 | Version         |
|                 |                 |                 |                 |
|                 |                 |                 | 15 : 8 - Major  |
|                 |                 |                 | Version         |
|                 |                 |                 |                 |
|                 |                 |                 | For revision    |
|                 |                 |                 | v0.75 the value |
|                 |                 |                 | will be 0x0075. |
+-----------------+-----------------+-----------------+-----------------+
| 10              | 2               | Reserved        | Reserved for    |
|                 |                 |                 | future use.     |
+-----------------+-----------------+-----------------+-----------------+
| 12              | 4               | Revision        | Revision of the |
|                 |                 |                 | Payload         |
|                 |                 |                 | binary.         |
|                 |                 |                 | Major.Minor     |
|                 |                 |                 | .Revision.Build |
|                 |                 |                 |                 |
|                 |                 |                 | The             |
|                 |                 |                 | ImageRevision   |
|                 |                 |                 | can be decoded  |
|                 |                 |                 | as follows:     |
|                 |                 |                 |                 |
|                 |                 |                 |  7 : 0  - Build |
|                 |                 |                 | Number          |
|                 |                 |                 |                 |
|                 |                 |                 | 15 :8  -        |
|                 |                 |                 | Revision        |
|                 |                 |                 |                 |
|                 |                 |                 | 23 :16 - Minor  |
|                 |                 |                 | Version         |
|                 |                 |                 |                 |
|                 |                 |                 | 31 :24 - Major  |
|                 |                 |                 | Version         |
+-----------------+-----------------+-----------------+-----------------+
| 16              | 4               | Attribute       | Bit-field       |
|                 |                 |                 | attribute       |
|                 |                 |                 | indicator of    |
|                 |                 |                 | the payload     |
|                 |                 |                 | image.          |
|                 |                 |                 |                 |
|                 |                 |                 | BIT 0: Build    |
|                 |                 |                 | Type.           |
|                 |                 |                 |                 |
|                 |                 |                 | 0: Release Build|
|                 |                 |                 |                 |
|                 |                 |                 | 1: Debug Build  |
+-----------------+-----------------+-----------------+-----------------+
| 20              | 4               | Capability      | Bit-field       |
|                 |                 |                 | capability      |
|                 |                 |                 | indicator that  |
|                 |                 |                 | the payload     |
|                 |                 |                 | image can       |
|                 |                 |                 | support.        |
|                 |                 |                 |                 |
|                 |                 |                 | BIT 0: Support  |
|                 |                 |                 | SMM rebase      |
+-----------------+-----------------+-----------------+-----------------+
| 24              | 16              | ProducerId      | A               |
|                 |                 |                 | null-terminated |
|                 |                 |                 | OEM-supplied    |
|                 |                 |                 | string that     |
|                 |                 |                 | identifies the  |
|                 |                 |                 | payload         |
|                 |                 |                 | producer.       |
+-----------------+-----------------+-----------------+-----------------+
| 40              | 16              | ImageId         | A               |
|                 |                 |                 | null-terminated |
|                 |                 |                 | ASCII string    |
|                 |                 |                 | that identifies |
|                 |                 |                 | the payload     |
|                 |                 |                 | name.           |
+-----------------+-----------------+-----------------+-----------------+


Universal Payload Loaded Image Section
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are many cases that a payload might need extra images to proceed the
boot flow. For example, UEFI payload might need additional FV images, Linux
payload might need additional InitRd image, u-boot might need additional
device tree blob, etc. In these cases, it is desired to pass this additional
image information from bootloader to payload so that payload can consume these
images later.

This specification defines optional universal payload extra image sections. 
If exist, they holds extra image information to be passed into the universal
payload. Please note, multiple extra image sections might exist in single
universal payload ELF image.

If an universal payload extra image section needs to be provided, it
must:

-  Have unique section name defined as ".upld.*". The full section name string
   length needs to be less than 16. Here, ‘*’ can be any ASCII string.

-  Have section aligned at proper boundary within the ELF file as required by
   the nature of the extra image itself. For example, FV and InitRd might need
   4KB page-aligned.

-  Contain the raw extra image data in its section.

During payload image loading, the bootloader shall build these extra images into
HOB. And the universal payload can locate the information from the HOB and find
required extra image information for consumption. 

