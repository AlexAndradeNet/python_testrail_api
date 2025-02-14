import sys

import requests

from main.support.environment_loader import EnvironmentLoader
from main.support.testrail_api import TestRailAPI


class TestCaseUpdater:
    """
    Class to process and update test cases.
    """

    def __init__(
        self,
        terminal_to_be_mimic,
        region_to_be_mimic,
        region_to_be_added,
    ):
        self.testrail_api, self.project_id = (
            self.initialize_testrail_api()
        )  # Store these as instance variables
        self.terminal_to_be_mimic = terminal_to_be_mimic
        self.region_to_be_mimic = region_to_be_mimic
        self.region_to_be_added = region_to_be_added

    def initialize_testrail_api(self):
        """
        Initializes the TestRail API using environment variables.

        :return: Initialized TestRailAPI object and project ID.
        """
        try:
            # Load environment variables
            env_loader = EnvironmentLoader()
            auth = env_loader.get_auth()

            # Initialize TestRail API class
            testrail_api = TestRailAPI(env_loader.base_url, auth)
            return testrail_api, env_loader.project_id

        except requests.exceptions.RequestException as e:
            print(f"Failed to connect to TestRail API: {e}")
            sys.exit(1)
        except EnvironmentError as e:
            print(f"Environment error: {e}")
            sys.exit(1)
        except KeyError as e:
            print(f"Missing required configuration: {e}")
            sys.exit(1)

    def update_test_cases_for_all_suites(self):
        """
        Update test cases for all suites in the project.
        """
        field_name_prefix = "custom_"
        terminal_field_name = field_name_prefix + "terminalmultiple"
        region_field_name = field_name_prefix + "region_country"

        suites = self.testrail_api.get_suites(self.project_id)
        if not suites:
            print("No suites found or failed to fetch suites.")
            return

        for suite in suites:
            suite_id = suite.get("id")
            if not suite_id:
                print(f"Invalid suite data: {suite}")
                continue

            print(f"Processing suite ID: {suite_id}")
            test_cases = self.testrail_api.get_test_cases(self.project_id, suite_id)
            if not test_cases:
                print(
                    f"No test cases found or failed to fetch for suite ID: {suite_id}"
                )
                continue

            for case in test_cases:
                self.process_test_case(case, terminal_field_name, region_field_name)

    def process_test_case(self, case, terminal_field_name, region_field_name):
        """
        Process and update a single test case based on region conditions.

        :param case: The test case to process.
        :param region_field_name: The field to update in the test case.
        """
        if not isinstance(case, dict):  # Validate the case structure
            print(f"Unexpected case format: {case}")
            return

        case_id = case.get("id")
        if not case_id:
            print(f"Invalid test case data: {case}")
            return

        current_region_value = case.get(region_field_name, [])

        if not isinstance(current_region_value, list):
            print(
                f"Invalid format for field '{region_field_name}' "
                f"in test case {case_id}: {current_region_value}"
            )
            return

        current_terminal_value = None
        if self.terminal_to_be_mimic is not None:
            current_terminal_value = case.get(terminal_field_name, [])

            if not isinstance(current_terminal_value, list):
                print(
                    f"Invalid format for field '{terminal_field_name}' "
                    f"in test case {case_id}: {current_terminal_value}"
                )
                return

        # Check if the target region is present and the new region is not
        # already added
        if self.should_update_case(current_terminal_value, current_region_value):
            self.update_case(case_id, region_field_name, current_region_value)
        else:
            self.log_no_update_needed(
                case_id, current_terminal_value, current_region_value
            )

    def should_update_case(self, current_terminal_value, current_region_value):
        """
        Determine whether the test case should be updated.

        :param current_terminal_value: The current value of the terminal to be checked.
        :param current_region_value: The current value of the region to be checked.
        :return: True if the test case should be updated; False otherwise.
        """
        if self.terminal_to_be_mimic is not None:
            return (
                self.terminal_to_be_mimic in current_terminal_value
                and self.region_to_be_mimic in current_region_value
                and self.region_to_be_added not in current_region_value
            )

        if self.terminal_to_be_mimic is None:
            return (
                self.region_to_be_mimic in current_region_value
                and self.region_to_be_added not in current_region_value
            )

        return False

    def update_case(self, case_id, field_name, current_field_value):
        """
        Update the test case with the new region value.

        :param case_id: The ID of the test case.
        :param field_name: The field to update.
        :param current_field_value: The current value of the field.
        """
        new_region_list = current_field_value + [self.region_to_be_added]
        try:
            self.testrail_api.update_test_case(case_id, field_name, new_region_list)
            print(f"Test case {case_id} updated successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to update test case {case_id}: {e}")

    def log_no_update_needed(
        self, case_id, current_terminal_value, current_region_value
    ):
        """
        Log that no update is needed for the test case.

        :param case_id: The ID of the test case.
        :param current_region_value: The current value of the field.
        """
        if (
            self.terminal_to_be_mimic is not None
            and self.terminal_to_be_mimic not in current_terminal_value
        ):
            print(
                f"Test case {case_id} does not need an update; it does not "
                f"contain terminal to be mimic."
            )
            return

        if self.region_to_be_mimic not in current_region_value:
            print(
                f"Test case {case_id} does not need an update; it does not "
                f"contain region to be mimic."
            )
            return

        print(
            f"Test case {case_id} does not need an update or already "
            f"contains region {self.region_to_be_added}."
        )
