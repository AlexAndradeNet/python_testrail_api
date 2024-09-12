import os

import requests
from dotenv import load_dotenv


def load_environment_variables():
    """
    Load environment variables
    """
    region_to_be_mimic = 3
    region_to_be_added = 4

    # Load environment variables from .env file.
    load_dotenv()

    # TestRail credentials and API endpoint from .env
    base_url = os.getenv("TESTRAIL_BASE_URL")
    username = os.getenv("TESTRAIL_USERNAME")
    api_key = os.getenv("TESTRAIL_API_KEY")

    # Define the project ID from .env
    project_id = os.getenv("TESTRAIL_PROJECT_ID")

    return (
        base_url,
        username,
        api_key,
        project_id,
        region_to_be_mimic,
        region_to_be_added,
    )


def get_suites(base_url, project_id, auth):
    """
    Get all test suites for a project in TestRail.
    """
    get_suites_url = f"{base_url}/index.php?/api/v2/get_suites/{project_id}"
    response = requests.get(get_suites_url, auth=auth, timeout=10)
    response.raise_for_status()  # Raise an error if the request fails

    # Parse the JSON response
    try:
        suites = response.json()
    except ValueError as e:
        print(f"Failed to parse JSON response for suites: {e}")
        print("Response content (first 100 characters):", response.text[:100])
        return []

    return suites


def get_test_cases(base_url, project_id, suite_id, auth):
    """
    Get existing test cases from TestRail with pagination.
    """
    cases = []
    limit = 250  # TestRail's maximum limit per request
    offset = 0

    while True:
        get_cases_url = (
            f"{base_url}/index.php?/api/v2/get_cases/{project_id}"
            f"&suite_id={suite_id}"
            f"&limit={limit}"
            f"&offset={offset}"
        )
        response = requests.get(get_cases_url, auth=auth, timeout=10)
        response.raise_for_status()  # Raise an error if the request fails

        # Check and print the response to debug
        try:
            response_data = response.json()  # Parse JSON response
        except ValueError as e:
            print(f"Failed to parse JSON response: {e}")
            # Print only the first 100 characters of the response text
            print("Response content (first 100 characters):", response.text[:100])
            return []  # Return an empty list if parsing fails

        # Check if 'cases' key is present in the response
        if "cases" not in response_data:
            print(f"Unexpected response format: {response_data}")
            return []  # Return an empty list if 'cases' is not found

        # Append the retrieved cases to the list
        cases.extend(response_data["cases"])

        # Check if there are more cases to fetch
        if len(response_data["cases"]) < limit:
            break  # No more cases to fetch

        # Increase the offset for the next batch
        offset += limit

    return cases


def update_test_case(update_case_url, case_id, new_region_list, auth):
    """
    Update the test case with the new "Region" value.
    """
    update_data = {
        "custom_region_country": new_region_list
        # Replace 'custom_region_country' with the actual field name in TestRail
    }
    update_response = requests.post(
        f"{update_case_url}{case_id}", json=update_data, auth=auth, timeout=10
    )
    update_response.raise_for_status()  # Raise an error if the update fails
    print(f"Test case {case_id} updated successfully with region: {new_region_list}")


def process_test_cases(
    test_cases, region_to_be_mimic, region_to_be_added, update_case_url, auth
):
    """
    Process and update test cases based on region conditions.
    """
    for case in test_cases:
        if not isinstance(case, dict):  # Check if each case is a dictionary
            print(f"Unexpected case format: {case}")
            continue

        case_id = case["id"]
        current_regions = case.get(
            "custom_region_country", []
        )  # Replace 'custom_region_country' with the actual field name in TestRail

        # Ensure 'current_regions' is a list
        if not isinstance(current_regions, list):
            print(
                f"Invalid format for regions in test case {case_id}: {current_regions}"
            )
            continue

        # Check if region '3' is present and '4' is not already present
        if (
            region_to_be_mimic in current_regions
            and region_to_be_added not in current_regions
        ):
            # Add region '4' to the current regions
            new_region_list = current_regions + [region_to_be_added]

            # Update the test case with the new "Region" value
            try:
                update_test_case(update_case_url, case_id, new_region_list, auth)
            except requests.exceptions.RequestException as e:
                print(f"Failed to update test case {case_id}: {e}")
        else:
            if region_to_be_mimic not in current_regions:
                print(
                    f"Test case {case_id} does not need an update; it does not "
                    + "contain region to be mimic."
                )
            else:
                print(
                    f"Test case {case_id} does not need an update or already "
                    + f"contains region {region_to_be_added}."
                )


def main():
    """
    Main function to handle the logic for updating TestRail test cases.
    """
    # Load environment variables
    (
        base_url,
        username,
        api_key,
        project_id,
        region_to_be_mimic,
        region_to_be_added,
    ) = load_environment_variables()

    # Define TestRail API authentication
    auth = (username, api_key)

    # Get all test suites for the project
    try:
        suites = get_suites(base_url, project_id, auth)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch test suites: {e}")
        return

    # Iterate over each suite and update test cases
    update_case_url = f"{base_url}/index.php?/api/v2/update_case/"
    for suite in suites:
        suite_id = suite["id"]
        print(f"Processing suite ID: {suite_id}")

        # Get test cases for each suite with pagination
        try:
            test_cases = get_test_cases(base_url, project_id, suite_id, auth)
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch test cases for suite {suite_id}: {e}")
            continue

        # Process and update test cases
        process_test_cases(
            test_cases, region_to_be_mimic, region_to_be_added, update_case_url, auth
        )


if __name__ == "__main__":
    main()
