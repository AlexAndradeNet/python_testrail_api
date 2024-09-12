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
        """
        suites = self.testrail_api.get_suites(self.project_id)

        for suite in suites:
            suite_id = suite["id"]
            print(f"Processing suite ID: {suite_id}")

            test_cases = self.testrail_api.get_test_cases(self.project_id, suite_id)

            for case in test_cases:
                self.process_test_case(case, field_name)

    def process_test_case(self, case, field_name):
        """
        Process and update a single test case based on region conditions.
        """
        if not isinstance(case, dict):  # Check if each case is a dictionary
            print(f"Unexpected case format: {case}")
            return

        case_id = case["id"]
        current_field_value = case.get(field_name, [])

        if not isinstance(current_field_value, list):
            print(
                f"Invalid format for regions in test case {case_id}: {current_field_value}"
            )
            return

        # Check if region '3' is present and '4' is not already present
        if (
            self.region_to_be_mimic in current_field_value
            and self.region_to_be_added not in current_field_value
        ):
            new_region_list = current_field_value + [self.region_to_be_added]
            try:
                self.testrail_api.update_test_case(case_id, field_name, new_region_list)
            except requests.exceptions.RequestException as e:
                print(f"Failed to update test case {case_id}: {e}")
        else:
            if self.region_to_be_mimic not in current_field_value:
                print(
                    f"Test case {case_id} does not need an update; "
                    + "it does not contain region to be mimic."
                )
            else:
                print(
                    f"Test case {case_id} does not need an update or already "
                    f"contains region {self.region_to_be_added}."
                )
