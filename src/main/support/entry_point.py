import sys

import requests

from main.support.test_case_updater import TestCaseUpdater


class EntryPoint:

    def __init__(self, terminal_to_be_mimic, region_to_be_mimic, region_to_be_added):
        """
        Main function to handle the logic for updating TestRail test cases.
        """
        # Initialize TestRail API
        self.terminal_to_be_mimic = terminal_to_be_mimic
        self.region_to_be_mimic = region_to_be_mimic
        self.region_to_be_added = region_to_be_added

        self.test_case_updater = TestCaseUpdater(
            self.terminal_to_be_mimic,
            self.region_to_be_mimic,
            self.region_to_be_added,
        )

    def run_update(self):  # New public method
        try:
            self.test_case_updater.update_test_cases_for_all_suites()
            print("Test cases updated successfully.")
            sys.exit(0)
        except requests.exceptions.RequestException as e:
            print(f"Failed to update test cases due to network error: {e}")
        except ValueError as e:
            print(f"Value error while updating test cases: {e}")
        except KeyError as e:
            print(f"Unexpected data format encountered: {e}")

        print(f"An unexpected error occurred while updating test cases: {e}")
