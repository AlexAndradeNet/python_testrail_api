from src.main.support.environment_loader import EnvironmentLoader
from src.main.support.test_case_updater import TestCaseUpdater
from src.main.support.testrail_api import TestRailAPI


def main():
    """
    Main function to handle the logic for updating TestRail test cases.
    """
    region_to_be_mimic = 3
    region_to_be_added = 4
    # Load environment variables
    env_loader = EnvironmentLoader()
    auth = env_loader.get_auth()

    # Initialize TestRail API and TestCaseUpdater classes
    testrail_api = TestRailAPI(env_loader.base_url, auth)
    test_case_updater = TestCaseUpdater(
        testrail_api,
        env_loader.project_id,
        region_to_be_mimic,
        region_to_be_added,
    )

    # Update test cases for all suites
    test_case_updater.update_test_cases_for_all_suites()


if __name__ == "__main__":
    main()
