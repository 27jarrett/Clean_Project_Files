import os
import time
import csv
import pandas as pd
from pathlib import Path
import shutil
# Playwright is included for demonstrating browser automation capability.
# In a sanitized version, actual browser interactions with sensitive internal systems are simulated.
from playwright.sync_api import sync_playwright

# --- Configuration for Demo (DO NOT USE REAL URLs/SELECTORS FOR PUBLIC REPO) ---
# These URLs and selectors are placeholders. In a real-world application,
# these would point to your actual web application and its elements.
# For public demonstration, we simulate these interactions.
GENERIC_LOGIN_URL = "https://your-automated-system.example.com/login"
GENERIC_UPLOAD_URL = "https://your-automated-system.example.com/upload-documents"

# Generic selectors (replace with actual selectors if running against a test environment)
USERNAME_INPUT_SELECTOR = 'input[name="username"]' # Generalized from 'loginName'
PASSWORD_INPUT_SELECTOR = 'input[name="password"]' # Generalized
LOGIN_BUTTON_SELECTOR = 'button[type="submit"]'
UPLOAD_FILE_INPUT_SELECTOR = 'input[type="file"]' # More generic selector for file input
SUBMIT_FORM_BUTTON_SELECTOR = 'button:has-text("Submit Document")' # Generalized from 'Save & New'

# Patterns to block resources for faster simulated page loads
RESOURCE_BLOCK_PATTERNS = [
    "**/*.css", "**/*.png", "**/*.jpg", "**/*.jpeg", "**/*.gif",
    "**/*.svg", "**/*.woff", "**/*.woff2", "**/*.ttf", "**/*.eot", "**/*.ico",
]
# --- End Configuration ---

class DocumentUploader: # Generalized class name from CRMUploader
    """
    A class to demonstrate automated document uploading to a web system
    using Playwright. Interactions with external systems are simulated for security.
    """
    def __init__(self, username, password, excel_path, upload_folder, uploaded_folder, failed_folder, field_to_fill_api_name, document_type_api_code, logger=print, abort_flag=None):
        self.username = username
        self.password = password
        self.excel_path = excel_path
        self.upload_folder = upload_folder
        self.uploaded_folder = uploaded_folder
        self.failed_folder = failed_folder
        # Renamed for clarity that these are generalized API names/codes for the demo
        self.field_to_fill_api_name = field_to_fill_api_name
        self.document_type_api_code = document_type_api_code
        self.abort_flag = abort_flag # Used for external abortion (e.g., from GUI)

        # Log file path within the uploaded_folder for consistency
        self.log_file_path = os.path.join(uploaded_folder, "automated_upload_log.txt") # Generic log name
        self.log_entries = []
        self.logger = logger # Custom logger function (e.g., GUI log, or default print)

        # Ensure output folders exist
        os.makedirs(self.uploaded_folder, exist_ok=True)
        os.makedirs(self.failed_folder, exist_ok=True)

    def log(self, message):
        """Appends a timestamped message to the internal log and calls the logger."""
        timestamped = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] - {message}"
        self.log_entries.append(timestamped)
        self.logger(timestamped)

    def export_log(self, as_csv=False):
        """Exports log entries to a file (text or CSV)."""
        try:
            if as_csv:
                csv_path = os.path.splitext(self.log_file_path)[0] + ".csv"
                with open(csv_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Timestamp_Message"]) # Header for CSV
                    for entry in self.log_entries:
                        writer.writerow([entry])
                self.log(f"📄 Log exported to {csv_path}")
            else:
                with open(self.log_file_path, 'w', encoding='utf-8') as f:
                    for entry in self.log_entries:
                        f.write(entry + "\n")
                self.log(f"📄 Log exported to {self.log_file_path}")
        except Exception as e:
            self.log(f"❌ Error exporting log: {e}")

    def disable_resources(self, page):
        """
        Disables loading of certain static resources to speed up page loads.
        This is useful for automation where rendering is not the primary goal.
        """
        try:
            for pattern in RESOURCE_BLOCK_PATTERNS:
                page.route(pattern, lambda route: route.abort())
            self.log("✅ Resource blocking configured for faster simulation.")
        except Exception as e:
            self.log(f"⚠️ Warning: Could not set up resource blocking (may not be critical for simulation): {e}")

    def login(self, page):
        """
        Simulates the login process to the web system.
        In a real application, this would interact with a live login page.
        For this public demo, it's a conceptual representation.
        """
        self.log("🔐 Simulating login process...")
        # Simulate navigating to the login page (no actual network request made here)
        self.log(f"  Attempting to access: {GENERIC_LOGIN_URL}")
        time.sleep(2) # Simulate network delay for page load

        if self.username == "demo" and self.password == "password":
            self.log("✅ Simulated login successful with demo credentials.")
            return True
        else:
            self.log("❌ Simulated login failed. Use 'demo' / 'password' for demo.")
            return False
        # The following original Playwright code is commented out as it interacts with a live system:
        # try:
        #     page.goto(GENERIC_LOGIN_URL, timeout=30000)
        #     page.wait_for_selector(USERNAME_INPUT_SELECTOR, timeout=15000)
        #     page.fill(USERNAME_INPUT_SELECTOR, self.username)
        #     page.fill(PASSWORD_INPUT_SELECTOR, self.password)
        #     page.click(LOGIN_BUTTON_SELECTOR)
        #     page.wait_for_load_state("networkidle", timeout=30000)
        #     if page.locator(USERNAME_INPUT_SELECTOR).count() > 0: # Check if still on login page
        #         self.log("❌ Login failed. Check credentials.")
        #         return False
        #     self.log("✅ Login successful.")
        #     return True
        # except Exception as e:
        #     self.log(f"❌ Login error (simulated): {e}")
        #     return False

    def rename_and_move(self, file, success):
        """Moves processed files to either the 'uploaded' or 'failed' folder."""
        try:
            source = os.path.join(self.upload_folder, file)
            if not os.path.exists(source):
                self.log(f"⚠️ Warning: Source file not found: {source}. Skipping move.")
                return

            ext = Path(file).suffix
            # Use a generic name for the destination file
            dest_name_status = 'uploaded' if success else 'failed'
            dest_name = f"{Path(file).stem}_{dest_name_status}{ext}"
            dest_folder = self.uploaded_folder if success else self.failed_folder

            os.makedirs(dest_folder, exist_ok=True) # Ensure destination folder exists

            dest_path = os.path.join(dest_folder, dest_name)

            # Handle duplicate filenames in destination folder
            counter = 1
            original_dest_path = dest_path # Store original proposed path
            while os.path.exists(dest_path):
                name_part = Path(original_dest_path).stem
                ext_part = Path(original_dest_path).suffix
                # Append counter before the final status suffix to maintain clarity
                dest_path = os.path.join(dest_folder, f"{name_part}_{counter}_{dest_name_status}{ext_part}")
                counter += 1

            shutil.move(source, dest_path)
            self.log(f"📁 Moved '{os.path.basename(file)}' to: '{os.path.basename(dest_path)}'")

        except Exception as e:
            self.log(f"❌ Error moving file '{file}': {e}")

    def load_mapping_data(self):
        """
        Loads and validates the Excel/CSV mapping file.
        Expects 'Title' (original filename stem) and 'FinalName' (target system identifier).
        """
        try:
            ext = Path(self.excel_path).suffix.lower()
            self.log(f"📄 Reading mapping file: {os.path.basename(self.excel_path)} (format: {ext})")

            if ext == ".csv":
                df = pd.read_csv(self.excel_path)
            elif ext in [".xls", ".xlsx"]:
                df = pd.read_excel(self.excel_path, engine="openpyxl")
            else:
                raise ValueError(f"Unsupported file format for mapping: {ext}. Please use .csv, .xls, or .xlsx.")

            # Validate required columns
            required_columns = ['Title', 'FinalName']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns in mapping file: {missing_columns}. Expected 'Title' and 'FinalName'.")

            # Clean whitespace from columns
            df['Title'] = df['Title'].astype(str).str.strip()
            df['FinalName'] = df['FinalName'].astype(str).str.strip()

            # Remove rows where either 'Title' or 'FinalName' is empty
            df = df.dropna(subset=['Title', 'FinalName'])
            df = df[df['Title'] != '']
            df = df[df['FinalName'] != '']

            self.log(f"✅ Loaded {len(df)} valid mappings from file.")
            return df

        except FileNotFoundError:
            self.log(f"❌ Mapping file not found at: {self.excel_path}")
            raise
        except pd.errors.EmptyDataError:
            self.log(f"❌ Mapping file at '{self.excel_path}' is empty or has no valid data.")
            raise
        except Exception as e:
            self.log(f"❌ Failed to read mapping file: {e}")
            raise

    def get_files_to_upload(self):
        """Retrieves a list of supported files from the designated upload folder."""
        try:
            if not os.path.exists(self.upload_folder):
                raise FileNotFoundError(f"Upload folder not found: {self.upload_folder}")

            # Define supported file extensions for documents
            supported_extensions = (
                ".pdf", ".docx", ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp", ".jfif", ".svg", ".txt", ".csv", ".xls", ".xlsx"
            )
            files = [f for f in os.listdir(self.upload_folder)
                     if f.lower().endswith(supported_extensions) and os.path.isfile(os.path.join(self.upload_folder, f))]

            if not files:
                self.log(f"⚠️ No supported files found in upload folder: {self.upload_folder}. Supported types: {', '.join(supported_extensions)}")
                raise ValueError("No supported files found in upload folder.")

            self.log(f"📁 Found {len(files)} files to process in '{self.upload_folder}'.")
            return files

        except Exception as e:
            self.log(f"❌ Error scanning upload folder: {e}")
            raise

    def upload_files(self, page):
        """
        Main function to orchestrate the simulated upload of multiple documents.
        This function iterates through files, calls upload_single (simulated),
        and moves files to appropriate success/failure folders.
        """
        try:
            self.log("📤 Beginning simulated document upload process...")
            # Simulate navigating to the upload page
            self.log(f"  Simulating navigation to upload page: {GENERIC_UPLOAD_URL}")
            time.sleep(2) # Simulate page load time

            df = self.load_mapping_data() # Load mappings
            files = self.get_files_to_upload() # Get files to upload

            uploaded_count = 0
            failed_count = 0

            for i, file in enumerate(files, 1):
                if self.abort_flag and self.abort_flag.is_set():
                    self.log("⏹️ Upload aborted by user.")
                    break

                self.log(f"\n📁 Processing file {i}/{len(files)}: '{file}'")
                # Call the simulated single file upload
                success = self.upload_single(page, file, df)

                if self.abort_flag and self.abort_flag.is_set():
                    self.log("⏹️ Upload aborted by user.")
                    break

                if success:
                    uploaded_count += 1
                else:
                    failed_count += 1

                self.rename_and_move(file, success)

            self.log(f"\n📊 Upload Summary:")
            self.log(f"✅ Successfully processed (simulated): {uploaded_count}")
            self.log(f"❌ Failed to process (simulated): {failed_count}")
            self.log(f"📁 Total files attempted: {uploaded_count + failed_count}")

        except Exception as e:
            self.log(f"❌ Critical error during simulated upload process: {e}")

    def upload_single(self, page, file, df):
        """
        Simulates the upload of a single file and filling of form fields.
        No actual Playwright interactions for file upload or form submission occur here.
        """
        if self.abort_flag and self.abort_flag.is_set():
            self.log("⏹️ Upload aborted before processing file.")
            return False

        try:
            file_path = os.path.join(self.upload_folder, file)
            title = Path(file).stem

            # Find matching record in mapping data
            match = df[df['Title'].str.lower() == title.lower()]
            if match.empty:
                self.log(f"❌ No mapping found for original filename '{title}' in the provided Excel/CSV file.")
                return False

            final_name = str(match.iloc[0]['FinalName']).strip()
            if not final_name:
                self.log(f"❌ 'FinalName' is empty for '{title}' in mapping file.")
                return False

            self.log(f"📋 Mapping found: Original '{title}' → Target System Identifier '{final_name}'")

            # --- Simulate web interaction ---
            # Simulate navigating to upload page and waiting for elements
            self.log(f"  Simulating file selection and upload for '{file_path}'...")
            time.sleep(1) # Simulate file selection time

            self.log(f"  Simulating setting document type to code: '{self.document_type_api_code}'")
            # Original code would have used: page.evaluate(f'rbf_setPicklistCode("SRS_Document_Type", "{self.document_type_api_code}")')
            time.sleep(0.5) # Simulate JS execution time

            self.log(f"  Simulating setting field '{self.field_to_fill_api_name}' to value: '{final_name}'")
            # Original code would have used: page.evaluate(f'rbf_setFieldValue("{self.field_to_fill_api_name}", "{final_name}")')
            time.sleep(0.5) # Simulate JS execution time

            self.log("  Simulating form submission...")
            time.sleep(2) # Simulate submission and page load

            # Simulate a successful upload for demonstration purposes
            self.log(f"✅ Successfully simulated upload for: '{file}'.")
            return True

        except Exception as e:
            self.log(f"❌ Simulated upload failed for '{file}': {e}")
            return False

    def run(self):
        """
        Main execution method for the document uploader automation.
        Launches a headless browser (conceptually) and orchestrates login and upload.
        """
        try:
            self.log("🚀 Starting document upload automation (simulated interactions)...")

            # Basic validation of required paths
            if not all([self.username, self.password, self.excel_path,
                       self.upload_folder, self.uploaded_folder, self.failed_folder,
                       self.field_to_fill_api_name, self.document_type_api_code]):
                raise ValueError("Missing required configuration parameters. Please check all paths and API mappings.")

            # Playwright context is conceptually set up, but actual browser interactions are skipped for sensitive URLs.
            # This block primarily demonstrates the *structure* of using Playwright.
            with sync_playwright() as p:
                # Playwright launch is still here to demonstrate the *capability* of browser automation,
                # but the actual browser interactions for sensitive URLs are mocked/simulated within methods.
                browser = p.chromium.launch(
                    headless=True, # Recommended for automation
                    args=[
                        '--no-sandbox', # Recommended for CI/CD environments
                        '--disable-dev-shm-usage',
                        '--disable-web-security', # Be cautious with this in real scenarios
                        '--disable-features=VizDisplayCompositor'
                    ]
                )

                context = browser.new_context(
                    viewport={'width': 1280, 'height': 720}, # Standard viewport for consistency
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36' # Common user agent
                )

                page = context.new_page()

                try:
                    self.disable_resources(page) # Still useful for conceptual speed up

                    if self.login(page): # Calls the simulated login
                        self.upload_files(page) # Calls the simulated upload
                    else:
                        self.log("❌ Exiting due to simulated login failure.")

                except Exception as e:
                    self.log(f"❌ An unexpected error occurred during browser automation (simulated): {e}")

                finally:
                    # Ensure the browser is closed in a real scenario
                    self.log("Browser context closed (simulated).")
                    browser.close()

        except Exception as e:
            self.log(f"❌ A critical error occurred during the overall process: {e}")

        finally:
            self.log("🏁 Process completed. Log exported.")
            self.export_log(as_csv=True)
