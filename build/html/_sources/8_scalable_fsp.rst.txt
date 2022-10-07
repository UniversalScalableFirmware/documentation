.. _scalable-fsp:

Scalable FSP 
============

The scalable FSP is an evolution of the Intel Firmware Support Package
detailed at `www.intel.com/fsp <http://www.intel.com/fsp>`__.

Interfaces
----------

| There are a plurality of interfaces to the FSP, including C and
  RUST-based.
| These interfaces allow for the POL to have a generic means by which to
  interface with the scalable FSP.

C API’s include

For EDKII -

https://github.com/tianocore/edk2/tree/master/IntelFsp2WrapperPkg/Include/Library

`FspMeasurementLib.h <https://github.com/tianocore/edk2/blob/master/IntelFsp2WrapperPkg/Include/Library/FspMeasurementLib.h>`__

`FspWrapperApiLib.h <https://github.com/tianocore/edk2/blob/master/IntelFsp2WrapperPkg/Include/Library/FspWrapperApiLib.h>`__

`FspWrapperApiTestLib.h <https://github.com/tianocore/edk2/blob/master/IntelFsp2WrapperPkg/Include/Library/FspWrapperApiTestLib.h>`__

`FspWrapperHobProcessLib.h <https://github.com/tianocore/edk2/blob/master/IntelFsp2WrapperPkg/Include/Library/FspWrapperHobProcessLib.h>`__

`FspWrapperPlatformLib.h <https://github.com/tianocore/edk2/blob/master/IntelFsp2WrapperPkg/Include/Library/FspWrapperPlatformLib.h>`__

Details of some of the interfaces can be found in
https://www.intel.com/content/dam/develop/external/us/en/documents/a-tour-beyond-bios-using-the-intel-firmware-support-package-with-the-efi-developer-kit-ii-fsp2-0-820293.pdf.

RUST variants include

https://github.com/jyao1/rust-firmware/tree/master/rust-fsp-wrapper

coreboot FSP

https://github.com/coreboot/coreboot/tree/master/src/drivers/intel/fsp2_0

`api.h <https://github.com/coreboot/coreboot/blob/master/src/drivers/intel/fsp2_0/include/fsp/api.h>`__

`debug.h <https://github.com/coreboot/coreboot/blob/master/src/drivers/intel/fsp2_0/include/fsp/debug.h>`__

`graphics.h <https://github.com/coreboot/coreboot/blob/master/src/drivers/intel/fsp2_0/include/fsp/graphics.h>`__

`info_header.h <https://github.com/coreboot/coreboot/blob/master/src/drivers/intel/fsp2_0/include/fsp/info_header.h>`__

`soc_binding.h <https://github.com/coreboot/coreboot/blob/master/src/drivers/intel/fsp2_0/include/fsp/soc_binding.h>`__

`upd.h <https://github.com/coreboot/coreboot/blob/master/src/drivers/intel/fsp2_0/include/fsp/upd.h>`__

`util.h <https://github.com/coreboot/coreboot/blob/master/src/drivers/intel/fsp2_0/include/fsp/util.h>`__

Additional details can be found in
https://github.com/coreboot/coreboot/tree/master/Documentation/soc/intel/fsp
and https://link.springer.com/chapter/10.1007/978-1-4842-0070-4_4

sFSP interactions
-----------------

The Intel Firmware Support Package has various evolutions for the Next
Generation Firmware program. These are tentatively described by the
specification evolution.

Since the POL uses FSP as its SOC abstraction, the POL considerations
for the various permutations of the FSP are described below.

FSP 2.2
~~~~~~~

Multiple notifications, bootloader debug/status code + FSP 2.1

FSP 2.3
~~~~~~~

FSP 2.2, large HOB support, versioning update

FSP 2.next.next
~~~~~~~~~~~~~~~

FSP2.3, SOC ACPI Abstraction, FSP-V, 64-bit, SMM loading

FSP 3.0 or FSP2.next.next
~~~~~~~~~~~~~~~~~~~~~~~~~

FSP-at-Reset (“bootable FSP”), FSP-R (FSP-Runtime)

