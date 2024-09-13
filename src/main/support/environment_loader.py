import os

from dotenv import load_dotenv


class EnvironmentLoader:
    """
    Class to load and manage environment variables from .env file.
    """

    REQUIRED_ENV_VARS = [
        "TESTRAIL_BASE_URL",
        "TESTRAIL_USERNAME",
        "TESTRAIL_API_KEY",
        "TESTRAIL_PROJECT_ID",
    ]

    def __init__(self):
        load_dotenv()  # Load environment variables from .env file
        self._env_vars = {
            "base_url": os.getenv("TESTRAIL_BASE_URL"),
            "username": os.getenv("TESTRAIL_USERNAME"),
            "api_key": os.getenv("TESTRAIL_API_KEY"),
            "project_id": os.getenv("TESTRAIL_PROJECT_ID"),
        }
        self.validate_env_vars()

    def validate_env_vars(self):
        """
        Validates that all required environment variables are loaded.
        """
        missing_vars = [var for var in self.REQUIRED_ENV_VARS if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

    @property
    def base_url(self):
        """Returns the TestRail base URL."""
        return self._env_vars["base_url"]

    @property
    def project_id(self):
        """Returns the TestRail project ID."""
        return self._env_vars["project_id"]

    def get_auth(self):
        """
        Returns authentication tuple for TestRail API.

        :return: A tuple containing the username and API key.
        """
        return self._env_vars["username"], self._env_vars["api_key"]

    def get_env_variable(self, var_name):
        """
        Returns the value of the requested environment variable.

        :param var_name: The name of the environment variable.
        :return: The value of the environment variable or None if not found.
        """
        return os.getenv(var_name)
