import requests


class TestRailAPI:
    """
    Class to interact with TestRail API.
    """

    def __init__(self, base_url, auth):
        self.base_url = base_url
        self.auth = auth

    def fetch_and_parse_response(self, url):
        """
        Fetches data from the given URL and parses the JSON response.

        :param url: The URL to fetch data from.
        :return: The parsed JSON response or an empty list if an error occurs.
        """
        try:
            response = requests.get(url, auth=self.auth, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            print("Response content (first 100 characters):", response.text[:100])
        return []

    def get_suites(self, project_id):
        """
        Get all test suites for a project in TestRail.

        :param project_id: The ID of the project.
        :return: A list of suites.
        """
        get_suites_url = f"{self.base_url}/index.php?/api/v2/get_suites/{project_id}"
        return self.fetch_and_parse_response(get_suites_url)

    def get_test_cases(self, project_id, suite_id):
        """
        Get existing test cases from TestRail with pagination.

        :param project_id: The ID of the project.
        :param suite_id: The ID of the test suite.
        :return: A list of test cases.
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

            response_data = self.fetch_and_parse_response(get_cases_url)

            if not response_data or "cases" not in response_data:
                print(f"Unexpected response format: {response_data}")
                break

            cases_list = response_data.get("cases", [])
            cases.extend(cases_list)

            if len(cases_list) < limit:
                break  # No more cases to fetch

            offset += limit

        return cases

    def update_test_case(self, case_id, field_name, new_value_list):
        """
        Update the test case with the new value.

        :param case_id: The ID of the test case.
        :param field_name: The field to update.
        :param new_value_list: The new value to set.
        :return: None
        """
        update_case_url = f"{self.base_url}/index.php?/api/v2/update_case/{case_id}"
        update_data = {field_name: new_value_list}
        try:
            response = requests.post(
                update_case_url, json=update_data, auth=self.auth, timeout=10
            )
            response.raise_for_status()
            print(
                f"Test case {case_id} updated successfully with {field_name}: {new_value_list}"
            )
        except requests.exceptions.RequestException as e:
            print(f"Failed to update test case {case_id}: {e}")
