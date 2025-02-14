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


def main():
    entry_point = EntryPoint(None, REGION_TO_BE_MIMIC, REGION_TO_BE_ADDED)
    entry_point.run_update()


if __name__ == "__main__":
    main()
