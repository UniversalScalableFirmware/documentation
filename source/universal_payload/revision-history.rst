Universal Payload Revision History
=====================================

========  =================================================  ======
Revision  Description                                        Date
========  =================================================  ======
0.75      - Changed payload image format to ELF.             Jun 9, 2021
          - Updated ACPI table requirement.
          - Separate new interfaces to a new chapter.
          - Reuse CPU HOB from PI Spec.
          - Add required interfaces regarding memory usage
            information.
          - Add PLD_GENERIC_HEADER as the common header for
            new interfaces.
          - Add PLD_GENERIC_HEADER.Length.
          - Add PLD_PCI_ROOT_BRIDGES definition.
          - Change prefix of interface definitions from
            'PLD\_' to 'UNIVERSAL_PAYLOAD\_'.
          - Change prefix of GUIDs from
            'gPld' to 'gUniversalPayload'.
          - Change 'PldHeader' to 'Header'.
0.7       Initial draft.                                     Sep 19, 2020
========  =================================================  ======
