# Python + TestRail API

This project provides a solution for adding a new country or region to a custom
field in TestRail without overwriting existing values. The TestRail web UI
typically requires users to overwrite the entire value of a field when making
updates, which complicates the process of adding a new region without affecting
the current ones.

### Example:

| Original Test Case | Desired Update | Update with Web UI |
|--------------------|----------------|--------------------|
| US, CA, UK         | US, CA, UK, DE | US, CA, UK, DE     |
| US, UK             | US, UK, DE     | US, CA, UK, DE     |

By using this Python-based solution with the TestRail API, you can easily append
new regions to existing values without overwriting them.

---

## ✨ Features

- **Preserve Existing Data**: Append new regions or countries to a custom field
  without losing the current data.
- **Automated Updates**: Automate updates to test cases using the TestRail API,
  avoiding the need for manual UI updates.
- **Python Integration**: Built with Python, leveraging its simplicity and power
  to interact with the TestRail API.

---

## 🧰 Tech Stack

- **Python 3**: The core programming language used for scripting and interacting
  with the TestRail API.
- **[Poetry](https://python-poetry.org)**: A dependency management and packaging
  tool for Python, providing isolated environments for running the project.

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7 or higher
- [Poetry](https://python-poetry.org/) for dependency management

### Installation

To set up the project, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/testrail-api-python.git
   cd testrail-api-python
   ```

2. Install the dependencies and activate the environment:

   ```bash
   poetry install
   poetry shell
   ```

3. Run the post-install script to complete the setup:

   ```bash
   poetry run post-install
   ```

For more detailed instructions, refer to
the [Installation Guide](docs/INSTALLATION.md).

### Running the Script

To update the region for test cases in TestRail, use the following command:

```bash
poetry run update-region
```

Ensure you have set up your environment and configured your `.env` file with the
necessary TestRail credentials.

### Development

To contribute to the project, please refer to
the [Contribution Guidelines](docs/CONTRIBUTE-python.md) for detailed
development guidelines, best practices, and coding standards.

---

## 🔧 Troubleshooting

Below are some common issues you might encounter and how to resolve them:

- **Installation Issues**: Ensure that all dependencies are installed correctly.
  Refer to the [Installation Guide](docs/INSTALLATION.md) for help.
- **Python Interpreter Issues**: Make sure your IDE is configured to use the
  Python interpreter from the Poetry environment.
- **Virtual Environment Issues**: If you accidentally create a virtual
  environment outside of Poetry, delete it and follow the installation steps
  again.
- **Environment Variable Issues**: Ensure your `.env` file is correctly set up
  with the necessary TestRail credentials and settings.

For more troubleshooting tips, visit
our [Troubleshooting Guide](docs/TROUBLESHOOTING.md).

---

## ✏️ Contributing

We welcome and appreciate contributions! Please see
our [Contribution Guidelines](docs/CONTRIBUTE-python.md) for detailed
instructions on how to contribute to this project.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file
for more details.

---

## 💬 Contact

If you have any questions or feedback, please open an issue or contact us
directly via email at support@example.com.

---

Following these guidelines will help you get started quickly and contribute
efficiently to the project. Happy coding!
