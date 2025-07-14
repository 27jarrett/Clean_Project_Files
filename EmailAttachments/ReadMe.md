# Outlook Attachment Scraper

This project presents a Python script designed to automate the process of extracting PDF attachments from specific Outlook folders and saving them to a designated local directory. It's built to help organize incoming documents, handle duplicates, and log its activities. This version has been sanitized for public demonstration to ensure no sensitive paths or internal company names are exposed.

## 🚀 Features

This script demonstrates proficiency in:

* **Outlook Automation:** Interacts with the local Microsoft Outlook client (via `win32com.client`) to access mailboxes and folders.
* **Targeted Attachment Extraction:** Scans a configurable source Outlook folder and its sub-folders for new emails containing PDF attachments.
* **File Management:** Saves extracted PDF attachments to a specified local directory.
* **Duplicate Handling:** Manages duplicate file names by saving them to a separate "Duplicates" folder, ensuring no original files are overwritten.
* **Unique Naming Convention:** Appends timestamps and unique IDs to saved filenames to prevent conflicts and provide traceability.
* **Email Management:** Moves processed emails to a dedicated Outlook folder, keeping your inbox organized.
* **Robust Logging:** Utilizes Python's `logging` module to record script activities, warnings, and errors.
* **User-Controlled Termination:** Includes a multi-platform (Windows-specific for `msvcrt`) input monitor for gracefully stopping the script from the command line.
* **Error Handling:** Implements `try-except` blocks for resilient operation against common issues like Outlook not running or file saving errors.

## 💻 Technologies Used

* **Python 3.x:** The core programming language.
* **`pywin32` (`win32com.client`):** Python for Windows extensions, enabling COM automation with Microsoft Outlook.
* **Standard Python Libraries:** `os`, `datetime`, `uuid`, `time`, `threading`, `logging`, `traceback`, `pathlib`.

## 🔒 Important Note on Security & Data Sanitization

This script, in its original form, would have contained hardcoded paths and specific Outlook folder names relevant to an internal company environment. **For public demonstration on GitHub, these sensitive details have been generalized and made configurable.**

* **File Paths:** All hardcoded local file paths (e.g., `C:\Users\Jastanley\...`) have been replaced with generic, relative paths (e.g., pointing to `Documents` folder in the user's home directory). Users are explicitly instructed to configure these paths.
* **Outlook Folder Names:** Specific Outlook folder names (e.g., "Organized", "PM_Data") have been replaced with generic placeholders (`OUTLOOK_SOURCE_FOLDER_NAME`, etc.) and moved to a prominent "Configuration Section" at the top of the script, guiding users to customize them.
* **No Sensitive Data Processing:** The script only handles file system operations and Outlook interactions; it does not process or store any sensitive content from the email body or attachments themselves beyond saving the files.

This approach demonstrates the functionality and logic of the attachment scraper while adhering to best practices for sharing code publicly.

## ▶️ How to Run Locally

To run this project locally and explore its features:

1.  **Clone the repository** (once you upload it to GitHub):
    ```bash
    git clone [https://github.com/YourUsername/outlook-attachment-scraper.git](https://github.com/YourUsername/outlook-attachment-scraper.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd outlook-attachment-scraper
    ```
3.  **Install the `pywin32` package:**
    This package is essential for interacting with Outlook on Windows.
    ```bash
    pip install pywin32
    ```
    *Note: `pywin32` is Windows-specific. This script will not run on macOS or Linux.*
4.  **Configure the script:**
    Open `Attachement_Scraper.py` in a text editor and **customize the `save_folder` and `OUTLOOK_..._FOLDER_NAME` variables** in the "Configuration Section" at the top to match your desired local save location and your Outlook folder structure.
5.  **Ensure Outlook is running:** The script needs an active Outlook application instance to function.
6.  **Run the script:**
    ```bash
    python Attachement_Scraper.py
    ```
    The script will run continuously, checking for new attachments. You can type `exit` and press Enter in the console to stop it.

## 💡 Potential Enhancements

* **Configuration File:** Implement a more robust configuration management using a `.ini` file or environment variables, instead of requiring direct code edits for setup.
* **Cross-Platform Compatibility:** Explore alternative libraries or approaches for email processing if cross-platform support (e.g., IMAP for webmail) is desired.
* **Attachment Type Filtering:** Allow users to specify a list of desired attachment file types (e.g., `.docx`, `.xlsx`) in addition to PDF.
* **Email Content Analysis:** Add features to analyze email subjects or bodies for keywords before processing attachments.
* **GUI:** Develop a simple graphical user interface (GUI) using libraries like `Tkinter` or `PyQt` for easier interaction.
* **Scheduling:** Integrate with Windows Task Scheduler or Python's `APScheduler` for automated, timed execution.
