import sys

import requests

from src.main.support.environment_loader import EnvironmentLoader
from src.main.support.test_case_updater import TestCaseUpdater
from src.main.support.testrail_api import TestRailAPI

# Configuration Constants
FIELD_NAME = "custom_region_country"
REGION_TO_BE_MIMIC = 3
REGION_TO_BE_ADDED = 4


def initialize_testrail_api():
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


def main():
    """
    Main function to handle the logic for updating TestRail test cases.
    """
    # Initialize TestRail API
    testrail_api, project_id = initialize_testrail_api()

    # Initialize TestCaseUpdater
    test_case_updater = TestCaseUpdater(
        testrail_api,
        project_id,
        REGION_TO_BE_MIMIC,
        REGION_TO_BE_ADDED,
    )

    # Update test cases for all suites
    try:
        test_case_updater.update_test_cases_for_all_suites(FIELD_NAME)
        print("Test cases updated successfully.")
        sys.exit(0)
    except requests.exceptions.RequestException as e:
        print(f"Failed to update test cases due to network error: {e}")
    except ValueError as e:
        print(f"Value error while updating test cases: {e}")
    except KeyError as e:
        print(f"Unexpected data format encountered: {e}")

    print(f"An unexpected error occurred while updating test cases: {e}")


if __name__ == "__main__":
    main()
