import requests


class TestCaseUpdater:
    """
    Class to process and update test cases.
    """

    def __init__(
        self, testrail_api, project_id, region_to_be_mimic, region_to_be_added
    ):
        self.testrail_api = testrail_api
        self.project_id = project_id
        self.region_to_be_mimic = region_to_be_mimic
        self.region_to_be_added = region_to_be_added

    def update_test_cases_for_all_suites(self, field_name):
        """
        Update test cases for all suites in the project.

        :param field_name: The field to update in each test case.
        """
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
                self.process_test_case(case, field_name)

    def process_test_case(self, case, field_name):
        """
        Process and update a single test case based on region conditions.

        :param case: The test case to process.
        :param field_name: The field to update in the test case.
        """
        if not isinstance(case, dict):  # Validate the case structure
            print(f"Unexpected case format: {case}")
            return

        case_id = case.get("id")
        if not case_id:
            print(f"Invalid test case data: {case}")
            return

        current_field_value = case.get(field_name, [])

        if not isinstance(current_field_value, list):
            print(
                f"Invalid format for field '{field_name}' "
                f"in test case {case_id}: {current_field_value}"
            )
            return

        # Check if the target region is present and the new region is not
        # already added
        if self.should_update_case(current_field_value):
            self.update_case(case_id, field_name, current_field_value)
        else:
            self.log_no_update_needed(case_id, current_field_value)

    def should_update_case(self, current_field_value):
        """
        Determine whether the test case should be updated.

        :param current_field_value: The current value of the field to be checked.
        :return: True if the test case should be updated; False otherwise.
        """
        return (
            self.region_to_be_mimic in current_field_value
            and self.region_to_be_added not in current_field_value
        )

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

    def log_no_update_needed(self, case_id, current_field_value):
        """
        Log that no update is needed for the test case.

        :param case_id: The ID of the test case.
        :param current_field_value: The current value of the field.
        """
        if self.region_to_be_mimic not in current_field_value:
            print(
                f"Test case {case_id} does not need an update; it does not "
                f"contain region to be mimic."
            )
        else:
            print(
                f"Test case {case_id} does not need an update or already "
                f"contains region {self.region_to_be_added}."
            )
