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
