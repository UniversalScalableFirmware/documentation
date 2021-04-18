Payload Image Format
====================

   Payload, as a standalone component, usually needs to be loaded by a bootloader into memory properly prior to execution. In this loading
   process, some additional process might be required, such as authentication, rebasing, assembling, etc.

   Today, many payloads use their own image formats (PE, ELF, FV, RAW, etc.), and it makes it difficult for a bootloader to identify and
   support all of them. To address this, a common payload image format is required for payload authentication, loading and booting.

   Instead of defining a new image format for payloads, it is prefered to use an already-existing format.
   The well-known payload format has ELF (Executable and Linkable Format) and PE (Portable Executable).
   This specification selects the ELF image format as the common universal payload image format since it is widely supported by most bootloaders.

   It is the payload choice on how to implement the ELF image format. It is possible for the complexity payload (e.g. UEFI payload) to use other image
   format inside the payload. But from the bootloader view point, all the payloads should act as the standard ELF image for authentication, loading
   and booting.
