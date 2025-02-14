# Configuration Constants
#
from main.support.entry_point import EntryPoint

# LIST OF REGIONS
# US = 1
# CA = 2
# UK = 3
# DE = 4
# ES = 5
# IT = 6


REGION_TO_BE_MIMIC = 1
REGION_TO_BE_ADDED = 2

# LIST OF TERMINALS
# Verifone = 1
# Tetra/Ingenico = 2
# Pax = 3
# Mobile = 4
TERMINAL_TO_BE_MIMIC = 3


def main():
    entry_point = EntryPoint(
        TERMINAL_TO_BE_MIMIC, REGION_TO_BE_MIMIC, REGION_TO_BE_ADDED
    )
    entry_point.run_update()


if __name__ == "__main__":
    main()
