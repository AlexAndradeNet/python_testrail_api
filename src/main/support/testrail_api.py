import requests


class TestRailAPI:
    """
    Class to interact with TestRail API.
    """

    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    def get_suites(self, project_id):
        """
        Get all test suites for a project in TestRail.
        """
        get_suites_url = f"{self.base_url}/index.php?/api/v2/get_suites/{project_id}"
        response = requests.get(get_suites_url, auth=self.auth, timeout=10)
        response.raise_for_status()

        try:
            suites = response.json()
        except ValueError as e:
            print(f"Failed to parse JSON response for suites: {e}")
            print("Response content (first 100 characters):", response.text[:100])
            return []

        return suites

    def get_test_cases(self, project_id, suite_id):
        """
        Get existing test cases from TestRail with pagination.
        """
        cases = []
        limit = 250  # TestRail's maximum limit per request
        offset = 0

        while True:
            get_cases_url = (
                f"{self.base_url}/index.php?/api/v2/get_cases/{project_id}"
                f"&suite_id={suite_id}"
                f"&limit={limit}"
                f"&offset={offset}"
            )
            response = requests.get(get_cases_url, auth=self.auth, timeout=10)
            response.raise_for_status()

            try:
                response_data = response.json()
            except ValueError as e:
                print(f"Failed to parse JSON response: {e}")
                print("Response content (first 100 characters):", response.text[:100])
                return []

            if "cases" not in response_data:
                print(f"Unexpected response format: {response_data}")
                return []

            cases.extend(response_data["cases"])

            if len(response_data["cases"]) < limit:
                break  # No more cases to fetch

            offset += limit

        return cases

    def update_test_case(self, case_id, new_region_list):
        """
        Update the test case with the new "Region" value.
        """
        update_case_url = f"{self.base_url}/index.php?/api/v2/update_case/{case_id}"
        update_data = {
            "custom_region_country": new_region_list
            # Replace with the actual field name in TestRail
        }
        response = requests.post(
            update_case_url, json=update_data, auth=self.auth, timeout=10
        )
        response.raise_for_status()
        print(
            f"Test case {case_id} updated successfully with region: {new_region_list}"
        )
