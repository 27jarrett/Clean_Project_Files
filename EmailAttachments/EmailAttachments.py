import os
import win32com.client
from datetime import datetime
import uuid
import time
import threading
import logging
import traceback
from pathlib import Path # Added for Path.home()

# --- Configuration Section (TO BE CUSTOMIZED BY USER) ---
# It's highly recommended to use environment variables or a configuration file
# for paths and folder names in a real-world application.

# Set base folder where attachments will be saved and logs stored.
# This default path is generic and points to the current user's Documents folder.
# IMPORTANT: Customize this path to your desired location before running!
# Example: save_folder = r"C:\Your\Preferred\Attachment\Save\Location"
save_folder = os.path.join(Path.home(), "Documents", "Automated_Attachments")

# Outlook folder names to monitor.
# Customize these to match the actual folder names in your Outlook client.
# Example: "MyProjectAttachments", "ProcessedItems"
OUTLOOK_SOURCE_FOLDER_NAME = "Automated Attachments - Source" # Generalized from "Organized"
OUTLOOK_SUB_FOLDER_NAME = "Processed Documents" # Generalized from "PM_Data"
OUTLOOK_PROCESSED_FOLDER_NAME = "Processed - Scraper Output" # Generalized from "Processed"
# --- End Configuration Section ---


# Create necessary sub-folders within the save_folder
duplicate_folder = os.path.join(save_folder, "Duplicates") # Renamed for clarity
log_folder = os.path.join(save_folder, "Logs") # Renamed for clarity

# Ensure all necessary directories exist
os.makedirs(save_folder, exist_ok=True)
os.makedirs(duplicate_folder, exist_ok=True)
os.makedirs(log_folder, exist_ok=True)

# Configure logging
log_filename = os.path.join(log_folder, f"attachment_scraper_log_{datetime.now().strftime('%Y-%m-%d')}.txt") # Generic log name
logging.basicConfig(
    filename=log_filename,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Attachment Scraper Script started.")

# Initialize Outlook Application
try:
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6) # 6 corresponds to olFolderInbox
except Exception as e:
    logging.critical(f"Failed to initialize Outlook: {e}. Ensure Outlook is running.")
    print(f"ERROR: Failed to initialize Outlook: {e}. Ensure Outlook is running.")
    exit() # Exit if Outlook cannot be initialized

def get_outlook_folder(root_folder, folder_name):
    """Helper function to safely get an Outlook folder by name."""
    for folder in root_folder.Folders:
        if folder.Name == folder_name:
            return folder
    return None

def process_attachments():
    """
    Processes emails in a specified Outlook folder, saves PDF attachments,
    and moves processed emails to a 'Processed' folder.
    """
    # Locate the source folder within Inbox
    source_folder = get_outlook_folder(inbox, OUTLOOK_SOURCE_FOLDER_NAME)
    if not source_folder:
        logging.warning(f"Source folder '{OUTLOOK_SOURCE_FOLDER_NAME}' not found in Inbox. Skipping processing.")
        return

    # Locate the sub-folder within the source folder
    sub_folder_to_process = get_outlook_folder(source_folder, OUTLOOK_SUB_FOLDER_NAME)
    if not sub_folder_to_process:
        logging.warning(f"Sub-folder '{OUTLOOK_SUB_FOLDER_NAME}' not found within '{OUTLOOK_SOURCE_FOLDER_NAME}'. Skipping processing.")
        return

    # Locate or create the processed emails folder in Inbox
    processed_emails_folder = get_outlook_folder(inbox, OUTLOOK_PROCESSED_FOLDER_NAME)
    if not processed_emails_folder:
        try:
            processed_emails_folder = inbox.Folders.Add(OUTLOOK_PROCESSED_FOLDER_NAME)
            logging.info(f"Created Outlook folder: '{OUTLOOK_PROCESSED_FOLDER_NAME}'.")
        except Exception as e:
            logging.error(f"Failed to create Outlook processed folder: {e}")
            return # Cannot proceed if processed folder can't be set up

    items_to_process = list(sub_folder_to_process.Items)
    processed_count = 0

    for item in items_to_process:
        # MailItem class (43) and check for attachments
        if item.Class == 43 and item.Attachments.Count > 0:
            attachments_saved_for_this_item = False

            for attachment in item.Attachments:
                # Check if it's a regular file attachment (Type 1) and a PDF
                if attachment.Type == 1 and attachment.FileName.lower().endswith(".pdf"):
                    original_attachment_filename = attachment.FileName
                    potential_save_path = os.path.join(save_folder, original_attachment_filename)

                    # Create a unique file name for saving
                    unique_id = uuid.uuid4().hex[:8]
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_name, file_extension = os.path.splitext(original_attachment_filename)
                    new_attachment_filename = f"{file_name}_{timestamp}_{unique_id}{file_extension}"
                    final_save_path = os.path.join(save_folder, new_attachment_filename)

                    try:
                        if os.path.exists(potential_save_path):
                            # Handle duplicate file name in the main save folder by moving to 'Duplicates'
                            duplicate_save_path = os.path.join(duplicate_folder, new_attachment_filename)
                            attachment.SaveAsFile(duplicate_save_path)
                            logging.info(f"Duplicate file saved to duplicates folder: {duplicate_save_path}")
                        else:
                            # Save the attachment to the main save folder
                            attachment.SaveAsFile(final_save_path)
                            logging.info(f"Attachment processed and saved: {final_save_path}")
                            attachments_saved_for_this_item = True
                    except Exception as e:
                        logging.error(f"Error saving attachment '{original_attachment_filename}': {e}")

            if attachments_saved_for_this_item:
                try:
                    item.Move(processed_emails_folder)
                    processed_count += 1
                except Exception as e:
                    logging.error(f"Error moving email '{item.Subject}' to processed folder: {e}")

    logging.info(f"Checked and processed {processed_count} emails in '{OUTLOOK_SUB_FOLDER_NAME}'.")


# Flag to stop the loop
stop_flag = False

def monitor_input():
    """Monitors for user input to stop the script. This function is Windows-specific."""
    global stop_flag
    print("Type 'exit' and press Enter to stop the script:")
    buffer = ""
    try:
        # msvcrt is a Windows-specific module for direct console I/O
        import msvcrt
        while not stop_flag:
            if msvcrt.kbhit(): # Checks if a keyboard hit is waiting
                char = msvcrt.getwche() # Gets a wide character console input
                if char in ('\r', '\n'): # Enter key pressed
                    if buffer.strip().lower() == "exit":
                        print("\nExiting script due to user command...")
                        stop_flag = True
                    buffer = "" # Reset buffer after Enter
                else:
                    buffer += char
            time.sleep(0.1) # Small delay to prevent busy-waiting
    except ImportError:
        logging.warning("msvcrt module not found. Input monitoring will not work on non-Windows systems.")
        print("Input monitoring is disabled (msvcrt module not found). To stop, you may need to close the console.")
        # On non-Windows, without msvcrt, this thread will just run and do nothing.
        # The main loop's sleep will be the only delay.
        while not stop_flag: # Keep thread alive for stop_flag to work if set externally (e.g. from a debugger)
            time.sleep(1)


# Start input monitor thread as a daemon so it exits with main program
input_thread = threading.Thread(target=monitor_input, daemon=True)
input_thread.start()

# Main script loop
logging.info("Starting main processing loop. Will check for emails periodically.")
while not stop_flag:
    try:
        process_attachments()
    except Exception as e:
        logging.error(f"An unexpected error occurred during attachment processing: {str(e)}")
        logging.error(traceback.format_exc()) # Log full traceback for debugging

    # Sleep in intervals to allow the stop_flag to be checked more frequently
    # and to reduce the delay if the user types 'exit'.
    for _ in range(60): # Loop for 60 iterations * 10 seconds = 600 seconds (10 minutes)
        if stop_flag:
            break # Exit loop immediately if stop_flag is set
        time.sleep(10) # Wait for 10 seconds

logging.info("Attachment Scraper Script has stopped.")
print("Script has stopped.")