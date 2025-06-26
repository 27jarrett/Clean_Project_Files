import asyncio
import aiohttp
import pandas as pd
from tqdm.asyncio import tqdm
import logging
from getpass import getpass
import os
import csv
from pathlib import Path
from datetime import datetime
import time # Added for simulation delays

# Configure logging for better output during simulation
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Mapping of human-readable field names to generic API integration names.
# These are kept for demonstration, but the actual 'values'
# represent a generic API's expected field names.
FIELD_MAP = {
    "Accessory Last Annual PM": "accessory_last_annual_pm_api_field",
    "Accessory Next Annual PM": "accessory_next_annual_pm_api_field",
    "Accessory Last PM": "accessory_last_pm_api_field",
    "Accessory Next PM": "accessory_next_pm_api_field",
    "Chassis Last Annual PM": "chassis_last_annual_pm_api_field",
    "Chassis Next Annual PM Due Date": "chassis_next_annual_pm_due_date_api_field",
    "Chassis Last PM": "chassis_last_pm_api_field",
    "Chassis Next PM Due Date": "chassis_next_pm_due_date_api_field",
    "Color": "color_api_field",
    "Engine Displacement": "engine_displacement_api_field",
    "Engine Family Name": "engine_family_name_api_field",
    "Engine Make": "engine_make_api_field",
    "Engine Model": "engine_model_api_field",
    "Engine Notification Value": "engine_notification_value_api_field",
    "Engine Serial #": "engine_serial_num_api_field",
    "Engine Year": "engine_year_api_field",
    "GeoTab ID": "geotab_id_api_field",
    "Camera IMEI": "camera_imei_api_field",
    "Geotab Serial Number": "geotab_serial_number_api_field",
    "GVW": "gvw_api_field",
    "License Exp": "license_exp_api_field",
    "License Expiration": "license_expiration_api_field",
    "License Plate": "license_plate_api_field",
    "License State": "license_state_api_field",
    "License Type": "license_type_api_field",
    "Title": "title_api_field",
    "Toll Tag #": "toll_tag_num_api_field",
    "Toll Tag Effective Date": "toll_tag_effective_date_api_field",
    "Toll Tag Expiration": "toll_tag_expiration_api_field",
}

def prompt_credentials():
    """Prompts for generic API credentials."""
    logging.info("🔐 Enter your API credentials (for demonstration purposes):")
    login_name = input("Username: ").strip()
    password = getpass("Password: ").strip()
    # For a public repo, you might even hardcode 'demo_id' here or make it optional.
    customer_id = input("Customer ID (e.g., 'DEMO_CUST_ID'): ").strip()
    return login_name, password, customer_id


def prompt_field_selection():
    """Allows user to select fields for update from a predefined map."""
    logging.info("\n📝 Select fields to update (comma-separated numbers):")
    for i, field in enumerate(FIELD_MAP.keys(), 1):
        print(f"{i}. {field}")
    selection = input("Enter numbers (e.g. 1,3,5): ").strip()
    try:
        selected = [list(FIELD_MAP.keys())[int(i) - 1] for i in selection.split(",") if i.strip().isdigit()]
        if not selected: # Handle empty selection
            raise ValueError("No valid fields selected.")
        return selected
    except (IndexError, ValueError) as e:
        logging.error(f"⚠️ Invalid selection: {e}. Please enter comma-separated numbers corresponding to the list.")
        return prompt_field_selection() # Recursively ask again


def sanitize_path(path: str) -> str:
    """Cleans up input path string."""
    return path.strip().strip('"').strip("'").strip()


def prompt_excel_path():
    """Prompts user for the path to the Excel file."""
    return sanitize_path(input('\n📄 Enter path to Excel file: '))


def prompt_generate_template(selected_fields):
    """Asks user if they want to generate an Excel template."""
    answer = input("\n📁 Generate Excel template with required columns? (y/n): ").strip().lower()
    return answer == "y"

def get_default_template_path():
    """Returns a default path for saving the Excel template in the user's Downloads folder."""
    downloads = Path.home() / "Downloads"
    downloads.mkdir(exist_ok=True)  # ensure it exists
    return str(downloads / "DEMO_UPDATE_TEMPLATE.xlsx") # Renamed template file for generalization


def create_excel_template(path, selected_fields, overwrite=False):
    """Creates an Excel template with specified headers."""
    # The 'equipment_id' is a placeholder for the unique identifier used in updates.
    # It can be generalized to 'record_id' or 'unique_identifier' as needed.
    headers = ['equipment_id'] + selected_fields
    df = pd.DataFrame(columns=headers)

    if Path(path).exists() and not overwrite:
        logging.warning(f"⚠️ File already exists: {path}")
        confirm = input("Overwrite? (y/n): ").strip().lower()
        if confirm != 'y':
            logging.info("🚫 Skipping template creation.")
            return

    try:
        df.to_excel(path, index=False)
        logging.info(f"✅ Template saved to: {path}")
    except Exception as e:
        logging.error(f"❌ Failed to save Excel template: {e}")


# --- API Interaction Functions (SIMULATED) ---

# Generalized API endpoints - Replace with your actual (mock) API if demonstrating live calls.
# These are placeholders and will not make real network requests in this sanitized version.
GENERIC_LOGIN_API_URL = "https://api.example.com/auth/login" # Generic login endpoint
GENERIC_UPDATE_API_URL = "https://api.example.com/records/update" # Generic update endpoint

async def login(username, password, customer_id):
    """
    Simulates a login API call.
    In a real scenario, this would authenticate against a real service
    and return a session ID or token.
    """
    logging.info(f"Simulating login for user: {username} with customer ID: {customer_id}...")
    # Simulate network delay
    await asyncio.sleep(1)

    # For demonstration, let's say any non-empty username/password is "successful"
    if username and password and customer_id:
        # Simulate a session ID or token
        simulated_session_id = f"mock_session_id_{hash(username + password + customer_id)}"
        logging.info("✅ Login simulated successfully.")
        return simulated_session_id
    else:
        raise Exception("Simulated login failed: Please provide username, password, and customer ID.")

def read_excel(file_path, selected_fields):
    """Reads data from an Excel file for updates."""
    try:
        df = pd.read_excel(file_path)
        df.columns = [str(col).strip() for col in df.columns] # Normalize headers

        # Ensure a generic identifier column is present (e.g., 'equipment_id')
        expected_cols = ['equipment_id'] + selected_fields
        missing = [col for col in expected_cols if col not in df.columns]
        if missing:
            raise ValueError(f"❌ Missing required columns in Excel: {missing}. Expected: {expected_cols}")

        logging.info(f"✅ Found {len(df)} records in Excel")

        updates = {}
        for _, row in df.iterrows():
            equipment_id = row['equipment_id'] # Using 'equipment_id' as generic record identifier
            # Use FIELD_MAP to convert human-readable names to simulated API field names
            update_fields = {FIELD_MAP[f]: row[f] for f in selected_fields if pd.notna(row[f])}
            if update_fields:
                updates[equipment_id] = update_fields

        return updates
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ Error: Excel file not found at '{file_path}'")
    except pd.errors.EmptyDataError:
        raise ValueError(f"❌ Error: Excel file at '{file_path}' is empty or has no valid data.")
    except Exception as e:
        raise Exception(f"❌ Failed to read Excel file: {e}")


async def update_record(session, base_url, session_id, record_id, fields, log_writer, dry_run=False):
    """
    Simulates sending an update request for a single record to the API.
    In a real scenario, this would make an actual API call.
    """
    # Parameters are generalized.
    params = {
        "sessionId": session_id,
        "record_type": "GenericRecordType", # Generalized from an internal object name
        "id": record_id,
        "useIds": "false" # Retained original API parameter for consistency in demo
    }
    params.update({k: str(v) for k, v in fields.items()})

    if dry_run:
        status_message = f"✅ Dry run - simulated no update sent for record ID: {record_id}"
        logging.info(status_message)
        log_writer.writerow([record_id, "DRY_RUN", "Success", status_message])
        return

    logging.info(f"Simulating update for record ID: {record_id} with fields: {fields}")
    await asyncio.sleep(0.1) # Simulate a small network delay

    # Simulate success or failure (e.g., 90% success rate)
    if time.time() % 10 < 9: # Simple way to get some variability
        simulated_status_code = 200
        simulated_response_text = "Simulated: Record updated successfully."
        result = "Success"
    else:
        simulated_status_code = 500
        simulated_response_text = "Simulated: Internal server error during update."
        result = "Failed"

    log_writer.writerow([record_id, simulated_status_code, result, simulated_response_text])


async def send_updates(updates, session_id, dry_run=False):
    """Initiates the process of sending bulk updates to the API."""
    log_file = "simulated_update_log.csv" # Renamed log file for generalization
    try:
        with open(log_file, "w", newline="", encoding='utf-8') as f: # Added encoding for robustness
            writer = csv.writer(f)
            # Standardized log headers
            writer.writerow(["record_id", "response_code", "status", "details"])
            async with aiohttp.ClientSession() as session:
                for record_id, fields in tqdm(updates.items(), desc="🚚 Sending simulated updates"):
                    await update_record(session, GENERIC_UPDATE_API_URL, session_id, record_id, fields, writer, dry_run=dry_run)

        logging.info(f"🧾 Simulated update log saved to: {log_file}")
    except Exception as e:
        logging.error(f"❌ Failed to write log file or send updates: {e}")


async def main():
    """Main function to run the CLI tool."""
    # Replaced hardcoded 'cust_id' with user input
    login_name, password, cust_id = prompt_credentials()

    selected_fields = prompt_field_selection()

    # Prompt for generating template
    if prompt_generate_template(selected_fields):
        template_path = get_default_template_path()
        overwrite = input("⚠️ Overwrite if file exists? (y/n): ").lower() == "y"
        create_excel_template(template_path, selected_fields, overwrite=overwrite)
        # You might choose to exit here if template generation is the primary task
        # return

    dry_run = input("🔎 Dry run (no updates sent)? (y/n): ").lower() == "y"

    session_id = None
    try:
        # Calls the simulated login function
        session_id = await login(login_name, password, cust_id)
        logging.info("✅ Logged in successfully (Simulated).")
    except Exception as e:
        logging.error(f"❌ Login failed: {e}")
        return # Exit if login fails

    file_path = prompt_excel_path()

    updates = {}
    try:
        updates = read_excel(file_path, selected_fields)
        if not updates:
            logging.warning("⚠️ No updates to process. Check your Excel data.")
            return
        logging.info(f"📦 Prepared {len(updates)} records for simulated update.")
    except FileNotFoundError as e:
        logging.error(f"{e}")
        return
    except ValueError as e:
        logging.error(f"{e}")
        return
    except Exception as e:
        logging.error(f"❌ An unexpected error occurred while reading Excel: {e}")
        return

    # Sends updates using the simulated update functions
    await send_updates(updates, session_id, dry_run=dry_run)
    logging.info("Operation complete.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("\n👋 Operation cancelled by user.")
    except Exception as e:
        logging.critical(f"An unhandled error occurred: {e}")

