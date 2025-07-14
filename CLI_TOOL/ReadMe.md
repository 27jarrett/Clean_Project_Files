# CLI Tool for Generic Record Management

This project presents a Command-Line Interface (CLI) tool designed for managing records via an external API. Originally developed for internal use to automate bulk updates of device information, this version has been thoroughly sanitized for public release. It demonstrates key aspects of Python programming for API interaction, data processing, and CLI application development.

## 🚀 Features

This CLI tool showcases capabilities in:

* **Asynchronous HTTP Requests:** Utilizes `aiohttp` for efficient, non-blocking network operations when interacting with an API.
* **Excel Integration:** Reads and processes data from Excel files (`.xlsx`) using `pandas` for bulk operations.
* **Data Mapping & Transformation:** Maps human-readable field names to generic API-specific field names.
* **CLI User Interaction:** Guides the user through prompts for credentials, field selection, and file paths.
* **Template Generation:** Creates a standardized Excel template for input data, improving user experience and data consistency.
* **Progress Tracking:** Integrates `tqdm` for visual progress bars during long-running tasks.
* **Robust Logging:** Provides clear feedback and logs API call outcomes, even in simulated environments.
* **Dry Run Mode:** Allows users to simulate updates without making actual changes to the backend, crucial for testing and safety.
* **Error Handling:** Includes mechanisms to gracefully handle file I/O errors, invalid inputs, and simulated API failures.

## 💻 Technologies Used

* **Python 3.x:** The core programming language.
* **`asyncio`:** For asynchronous programming, enabling efficient I/O operations.
* **`aiohttp`:** An asynchronous HTTP client/server framework for making API requests.
* **`pandas`:** A powerful data analysis and manipulation library, used here for Excel file processing.
* **`tqdm`:** For displaying smart progress bars.
* **`getpass`:** For securely prompting sensitive information like passwords.
* **`logging`:** Python's standard logging library for structured output.

## 🔒 Important Note on Security & Data Sanitization

This project includes functionalities that, in a live production environment, would interact with sensitive APIs and company data. **For public demonstration on GitHub, all actual API endpoints and authentication mechanisms have been replaced with placeholders and simulated logic.**

* **API Endpoints:** Real API URLs (e.g., those from a specific fleet management system) have been replaced with generic placeholders like `https://api.example.com`.
* **Authentication:** The authentication process is **simulated**. No real credentials are used or exposed. In a production application, credentials would be managed through secure means (e.g., environment variables, a secure vault, or OAuth tokens), not hardcoded or passed directly as shown in the original implementation concept. The `login` function now returns a mock session ID.
* **API Calls:** All `aiohttp` requests to external APIs have been replaced with `asyncio.sleep` calls and simulated success/error responses. This ensures the script can be run locally without attempting to connect to private infrastructure.
* **Sensitive Data:** All company-specific identifiers (e.g., customer IDs, internal object names) and references to specific systems (e.g., "DMSi") have been generalized or removed to protect proprietary information. The `FIELD_MAP` now uses generic API field names as values.

This approach demonstrates the functionality and logic of the CLI tool while adhering to best practices for sharing code publicly.

## ▶️ How to Run Locally

To run this project locally and explore its features:

1.  **Clone the repository** (once you upload it to GitHub):
    ```bash
    git clone [https://github.com/27jarrett/cli-record-manager.git](https://github.com/YourUsername/cli-record-manager.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd cli-record-manager
    ```
3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
    (You'll need to create a `requirements.txt` file in the project root with the following content):
    ```
    aiohttp
    pandas
    tqdm
    openpyxl # pandas requires this for .xlsx files
    ```
4.  **Run the script:**
    ```bash
    python fms_api_cli_tool.py
    ```
    The script will then guide you through the process via command-line prompts. You can use any non-empty string for username, password, and customer ID for the simulated login.

## 💡 Potential Enhancements

* **Configuration File:** Implement reading API URLs and other settings from a configuration file (e.g., `config.ini`, `.env`) instead of hardcoding, making the tool more flexible.
* **Command-Line Arguments:** Utilize a library like `argparse` to handle command-line arguments (e.g., for `--dry-run`, `--file-path`), providing more advanced CLI usage.
* **Modularization:** Further break down the `main` function and other large functions into smaller, more focused modules or classes.
* **Comprehensive Testing:** Add unit tests for individual functions and integration tests for the overall flow.
* **Mocking Framework:** Use a dedicated Python mocking library (e.g., `unittest.mock`) for more sophisticated simulation of API responses during testing.
