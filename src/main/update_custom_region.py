import os

import requests
from dotenv import load_dotenv


def load_environment_variables():
    region_to_be_mimic = 3
    region_to_be_added = 4

    # Load environment variables from .env file.

    load_dotenv()
    # TestRail credentials and API endpoint from .env
    base_url = os.getenv("TESTRAIL_BASE_URL")
    username = os.getenv("TESTRAIL_USERNAME")
    api_key = os.getenv("TESTRAIL_API_KEY")

    # Define the project and test suite IDs from .env
    project_id = os.getenv("TESTRAIL_PROJECT_ID")
    suite_id = os.getenv("TESTRAIL_SUITE_ID")

    return (
        base_url,
        username,
        api_key,
        project_id,
        suite_id,
        region_to_be_mimic,
        region_to_be_added,
    )


def get_test_cases(base_url, project_id, suite_id, auth):
    """
    Get existing test cases from TestRail.
    """
    get_cases_url = (
        f"{base_url}/index.php?/api/v2/get_cases/{project_id}&suite_id={suite_id}"
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

    return response_data["cases"]  # Extract the list of test cases


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
        suite_id,
        region_to_be_mimic,
        region_to_be_added,
    ) = load_environment_variables()

    # Define TestRail API authentication
    auth = (username, api_key)

    # Get test cases
    try:
        test_cases = get_test_cases(base_url, project_id, suite_id, auth)
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch test cases: {e}")
        return

    # Update test cases
    update_case_url = f"{base_url}/index.php?/api/v2/update_case/"

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
                    f"Test case {case_id} does not need an update it not "
                    + "contains region to be mimic."
                )
            else:
                print(
                    f"Test case {case_id} does not need an update or already "
                    + "contains region {region_to_be_added}."
                )


if __name__ == "__main__":
    main()
