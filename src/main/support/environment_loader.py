import os

from dotenv import load_dotenv


class EnvironmentLoader:
    """
    Class to load environment variables from .env file.
    """

    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self.base_url = os.getenv("TESTRAIL_BASE_URL")
        self.username = os.getenv("TESTRAIL_USERNAME")
        self.api_key = os.getenv("TESTRAIL_API_KEY")
        self.project_id = os.getenv("TESTRAIL_PROJECT_ID")

    def get_auth(self):
        """Returns authentication tuple for TestRail API."""
        return self.username, self.api_key

    def get_env_variable(self, var_name):
        """
        Returns the value of the requested environment variable.

        :param var_name: The name of the environment variable.
        :return: The value of the environment variable or None if not found.
        """
        return os.getenv(var_name)
