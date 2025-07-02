# Automated Document Uploader (Python GUI with VBA Launcher)

This project showcases a comprehensive desktop application designed for automating document uploads to a web-based system. It combines a Python GUI for user interaction, a Python backend for web automation (using Playwright), and a VBA macro in a Microsoft Office file (e.g., Excel) to launch the Python script seamlessly. This version has been meticulously sanitized for public demonstration on GitHub, ensuring no sensitive company data, internal URLs, or specific credentials are exposed.

## 🚀 Features

This application demonstrates a versatile skillset, including:

* **User-Friendly GUI:** A CustomTkinter-based graphical interface for configuring upload settings, selecting files/folders, and monitoring process logs.
* **Web Automation (Simulated):** Python logic utilizing a conceptual Playwright framework to interact with web forms, simulating login, file uploads, and metadata entry. (Note: All web interactions are simulated for security and demonstration purposes).
* **VBA Integration:** A VBA macro embedded in a Microsoft Office file (e.g., Excel) provides a convenient way to launch the Python backend, acting as a "launch button" within a familiar application environment.
* **Automated File Processing:** Reads document mappings from an Excel/CSV file to intelligently name and categorize uploads.
* **Robust File Management:** Automatically moves processed documents to designated "success" or "failure" folders.
* **Progress & Logging:** Provides real-time activity logging within the GUI and generates detailed log files for post-processing review.
* **Configurable Settings:** Allows users to define source/destination folders, authentication details (for demo), and document-specific metadata via the GUI.
* **Graceful Abort:** Capability to stop the automation process mid-run from the GUI.
* **Desktop Application Deployment:** Illustrates a complete package for deployment as a desktop application, including batch file launcher, VBA integration, and shortcut/icon considerations.

## 💻 Technologies Used

* **Python 3.x:** Core application logic.
    * **`CustomTkinter`:** For building the modern-looking graphical user interface.
    * **`Playwright` (Conceptual):** Framework demonstrating browser automation capabilities. (Actual web interactions are simulated).
    * **`pandas`:** For reading and processing Excel/CSV mapping files.
    * **Standard Libraries:** `os`, `threading`, `csv`, `pathlib`, `time`, `logging`, `getpass`.
* **VBA (Visual Basic for Applications):** Used within a Microsoft Office application (e.g., Excel) to launch the Python script via a batch file.
* **Batch Script (`.bat`):** A simple Windows batch script to execute the Python application.

## 🔒 Important Note on Security & Data Sanitization

This project, in its original form, handled sensitive company data, interacted with internal web applications, and contained proprietary configurations. **For public demonstration on GitHub, all sensitive information has been rigorously sanitized:**

* **API Endpoints & URLs:** All specific company-internal web URLs (login pages, upload forms) have been replaced with generic `https://example.com` placeholders.
* **Authentication & Web Interaction:** All browser automation logic (`playwright` interactions like `goto`, `fill`, `click`) targeting sensitive URLs has been **commented out and replaced with simulations** (e.g., `time.sleep` and `logging.info`). This ensures the code can be run safely without attempting to connect to private infrastructure. The login is simulated with generic "demo" credentials.
* **Internal Identifiers:** Hardcoded customer IDs, internal system names, proprietary field mappings, and document type codes have been generalized or replaced with descriptive placeholders (e.g., `EQUIPMENT_ID_API_FIELD`, `DOC_TYPE_APPROVAL`).
* **File Paths:** Hardcoded absolute file paths have been replaced with relative paths or generic default locations, and the GUI now prompts for all necessary directories.
* **VBA Code:** The VBA module has been stripped of any actual sensitive paths or direct database/API calls, providing a conceptual launcher.
* **Shortcuts & Icons:** `.lnk` shortcut files are NOT included due to their machine-specific nature. Instructions are provided for creating them. Generic icons should be used if included.

This thorough sanitization allows the project to be shared publicly, demonstrating your technical capabilities while adhering to strict security and confidentiality practices.

<img src="https://github.com/27jarrett/Clean_Project_Files/blob/main/DIT/assets/Screenshot.png">

## ▶️ How to Run Locally

To get this application running on your local machine:

1.  **Clone the repository** (once uploaded to GitHub):
    ```bash
    git clone [https://github.com/YourUsername/document-automation-tool.git](https://github.com/YourUsername/document-automation-tool.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd document-automation-tool
    ```
3.  **Install Python Dependencies:**
    It's highly recommended to use a Python virtual environment.
    ```bash
    python -m venv venv
    .\venv\Scripts\activate   # On Windows
    # source venv/bin/activate  # On macOS/Linux
    pip install -r requirements.txt
    ```
    Create a `requirements.txt` file in your project root with the following content:
    ```
    customtkinter
    pandas
    openpyxl # Required by pandas for .xlsx files
    playwright # Although interactions are simulated, the library is still imported
    ```
    *Note: `playwright` also requires browser binaries. You might need to run `playwright install` in your activated virtual environment if you wish to run `playwright` for other purposes, but for this simulated demo, it's not strictly necessary.*
4.  **Configure Local Folders & Mapping:**
    * Create empty folders on your local machine that will serve as:
        * Your "Documents to Upload" folder (where you'll place sample files like `SampleDocumentTitle.pdf`).
        * Your "Successfully Uploaded" folder.
        * Your "Failed Uploads" folder.
    * Run `python main.py`, and when the GUI appears, select these folders for the respective inputs.
    * **Export a CSV Mapping Template:** Use the "Export CSV Mapping Template" button in the GUI to create an example `document_mapping_template.csv`. Populate this CSV with sample filenames (under the 'Title' column, e.g., `SampleDocumentTitle`) and corresponding `FinalName` identifiers (e.g., `DEV-001`). Place this updated CSV file in a chosen location and select it in the GUI as "Excel Mapping File".

5.  **Run the GUI Application:**
    ```bash
    python main.py
    ```
    The GUI will launch. Fill in "demo" for username and "password" for password, select your configured paths and dropdown options, then click "Start Simulated Upload". Observe the log output.

### 🧩 Optional: Launching via Batch File (`run_uploader.bat`)

For a more "desktop application" feel, you can launch the GUI using the provided batch script:

1.  Place the `run_uploader.bat` file in the same directory as `main.py`.
2.  Open `run_uploader.bat` in a text editor to verify the `python main.py` command is correct and adjust the virtual environment activation if necessary (lines are commented).
3.  Double-click `run_uploader.bat` to run the application.

### 📄 Optional: Launching via VBA Macro (`LaunchScript.bas`)

If you wish to demonstrate the VBA integration:

1.  Open a new or existing Microsoft Excel workbook (or other Office application).
2.  Press `Alt + F11` to open the VBA editor.
3.  In the Project Explorer (left pane), right-click on your workbook project (e.g., `VBAProject (YourWorkbookName.xlsm)`), then choose `Insert > Module`.
4.  Open the newly created module (e.g., `Module1`) and paste the content of `LaunchScript.bas` (the sanitized VBA code) into it.
5.  You can then create a button in your Excel sheet and assign the `RunPythonUploader` macro to it, or run it directly from `Developer > Macros`.

### 🖼️ Optional: Desktop Shortcut & Icon

* **Desktop Shortcut:** Right-click on your desktop, select `New > Shortcut`. For the "Type the location of the item:", browse to your `run_uploader.bat` file (or `main.py` if running directly). Give it a name like "Document Uploader".
* **Icon:** You can associate a generic `.ico` file (e.g., one you create or find that is publicly licensed) with your shortcut for a custom look. Do not use proprietary company icons.

## 💡 Potential Enhancements

* **Full Mock Backend:** Implement a local mock API server (e.g., using Flask or FastAPI) to handle the simulated web requests more realistically, rather than just using `time.sleep` in the `uploader.py`.
* **Advanced UI/UX:** Enhance the CustomTkinter GUI with more sophisticated layouts, progress indicators, and user feedback mechanisms.
* **Configuration File:** Implement a structured configuration file (e.g., `config.ini`, YAML, or JSON) for all paths, API endpoints, and other settings, removing the need to hardcode them even for local testing.
* **Cross-Platform Playwright:** Configure Playwright to support different browsers (Chromium, Firefox, WebKit).
* **Error Reporting:** Implement a more robust error reporting mechanism (e.g., logging to a file with rotation, sending error notifications).
* **Automated Testing:** Develop unit tests for Python modules and integration tests for the full workflow.
