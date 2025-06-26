import customtkinter as ctk
from tkinter import filedialog
from threading import Thread # For running the upload in a separate thread
import csv
# Import the generalized DocumentUploader class
from uploader import DocumentUploader # Renamed import

ctk.set_appearance_mode("dark")  # Options: "dark", "light"
ctk.set_default_color_theme("blue")  # Options: "blue", "dark-blue", "green"

class DocumentUploaderGUI(ctk.CTk): # Generalized class name from CRMUploaderGUI
    """
    A CustomTkinter GUI application for demonstrating automated document uploading.
    Provides user interface for inputting credentials, selecting folders,
    and configuring upload settings.
    """
    def __init__(self):
        super().__init__()

        self.title("📤 Document Automation Tool") # Generalized title
        self.geometry("720x800")
        self.resizable(False, False)
        self.abort_flag = False # Flag to signal abortion from GUI

        self.paths = {} # Dictionary to store paths selected by the user

        # Field and document type mappings (values are generalized for public demo)
        # These demonstrate the *concept* of mapping user-friendly names
        # to internal system/API identifiers.
        self.field_mapping = {
            "Please Select": "",
            "Equipment Identifier": "EQUIPMENT_ID_API_FIELD", # Generalized
            "Purchase Request ID": "PURCHASE_REQ_ID_API_FIELD", # Generalized
            "Request Details ID": "REQ_DETAILS_ID_API_FIELD", # Generalized
            "Order Number": "ORDER_NUM_API_FIELD" # Generalized
        }

        self.doc_types = {
            "Please Select": "",
            "Approval Document": "DOC_TYPE_APPROVAL", # Generalized
            "Bill Of Lading": "DOC_TYPE_BOL", # Generalized
            "Campaign Document": "DOC_TYPE_CAMPAIGN", # Generalized
            "Capex Approval": "DOC_TYPE_CAPEX_APPROVAL", # Generalized
            "Insurance Policy": "DOC_TYPE_INSURANCE", # Generalized
            "Lease Agreement": "DOC_TYPE_LEASE_AGREEMENT", # Generalized
            "Maintenance Record": "DOC_TYPE_MAINTENANCE", # Generalized
            "Permit Document": "DOC_TYPE_PERMIT", # Generalized
            "PM Invoice": "DOC_TYPE_PM_INVOICE", # Generalized
            "Recall Notice": "DOC_TYPE_RECALL", # Generalized
            "Registration Document": "DOC_TYPE_REGISTRATION", # Generalized
            "Rental Agreement": "DOC_TYPE_RENTAL_AGREEMENT", # Generalized
            "Repair Estimate": "DOC_TYPE_REPAIR_ESTIMATE", # Generalized
            "Repair Invoice": "DOC_TYPE_REPAIR_INVOICE", # Generalized
            "Sales Document": "DOC_TYPE_SALES", # Generalized
            "Title Document": "DOC_TYPE_TITLE", # Generalized
            "Warranty Document": "DOC_TYPE_WARRANTY" # Generalized
        }

        # String variables to hold selected dropdown values
        self.selected_field = ctk.StringVar(value=list(self.field_mapping.keys())[0])
        self.selected_doc_type = ctk.StringVar(value=list(self.doc_types.keys())[0])

        self.build_gui()

    def build_gui(self):
        """Constructs the GUI layout with various frames and widgets."""
        # --- User Credentials Frame ---
        credentials_frame = ctk.CTkFrame(self, corner_radius=8)
        credentials_frame.pack(fill="x", padx=15, pady=(15, 10))

        ctk.CTkLabel(credentials_frame, text="User Credentials (For Demo)", font=ctk.CTkFont(size=16, weight="bold"))\
            .grid(row=0, column=0, columnspan=1, pady=(5, 15))
        
        # Note for demo purposes that credentials are not real
        ctk.CTkLabel(credentials_frame, text="Use 'demo' / 'password' for simulated login.", font=ctk.CTkFont(size=12, slant="italic"))\
            .grid(row=0, column=2, columnspan=1, pady=(5, 15))


        self.username_var = ctk.StringVar(value="demo") # Set default for demo
        self.password_var = ctk.StringVar(value="password") # Set default for demo

        self.add_labeled_entry(credentials_frame, "Username:", self.username_var, row=1)
        self.add_labeled_entry(credentials_frame, "Password:", self.password_var, row=2, show="*")

        # --- Path Configuration Frame ---
        path_frame = ctk.CTkFrame(self, corner_radius=8)
        path_frame.pack(fill="x", padx=15, pady=(5, 10))

        ctk.CTkLabel(path_frame, text="File Path Configuration", font=ctk.CTkFont(size=16, weight="bold"))\
            .grid(row=0, column=0, columnspan=1, pady=(5, 15))

        self.add_path_selector(path_frame, "Excel Mapping File", 1, filedialog.askopenfilename, "Select the Excel/CSV file with Title and FinalName mappings.")
        self.add_path_selector(path_frame, "Documents to Upload Folder", 2, filedialog.askdirectory, "Select the folder containing documents to be uploaded.")
        self.add_path_selector(path_frame, "Successfully Uploaded Folder", 3, filedialog.askdirectory, "Select where to move documents after successful (simulated) upload.")
        self.add_path_selector(path_frame, "Failed Uploads Folder", 4, filedialog.askdirectory, "Select where to move documents after failed (simulated) upload.")

        # --- Upload Settings Frame ---
        dropdown_frame = ctk.CTkFrame(self, corner_radius=8)
        dropdown_frame.pack(fill="x", padx=15, pady=(5, 10))

        ctk.CTkLabel(dropdown_frame, text="Document Metadata Settings", font=ctk.CTkFont(size=16, weight="bold"))\
            .grid(row=0, column=0, columnspan=1, pady=(5, 15))

        self.add_dropdown(dropdown_frame, "Field to Map:", self.selected_field, list(self.field_mapping.keys()), 1, "This maps to a field in the target system (e.g., Equipment ID).")
        self.add_dropdown(dropdown_frame, "Document Type:", self.selected_doc_type, list(self.doc_types.keys()), 2, "This maps to a document type code in the target system.")

        # --- Buttons Frame ---
        button_frame = ctk.CTkFrame(self, corner_radius=8)
        button_frame.pack(fill="x", padx=15, pady=10)

        export_btn = ctk.CTkButton(button_frame, text="Export CSV Mapping Template", command=self.export_csv_template) # Renamed button
        export_btn.pack(side="left", padx=(0, 10), expand=True)

        start_btn = ctk.CTkButton(button_frame, text="Start Simulated Upload", command=self.start_upload_thread, # Renamed button
                                  fg_color="#28a745", hover_color="#218838")
        start_btn.pack(side="left", expand=True)

        abort_btn = ctk.CTkButton(button_frame, text="Abort & Exit", command=self.abort_and_exit,
                          fg_color="#dc3545", hover_color="#c82333")
        abort_btn.pack(side="left", padx=(10, 0), expand=True)

        # --- Log Frame ---
        log_frame = ctk.CTkFrame(self, corner_radius=8)
        log_frame.pack(fill="both", expand=True, padx=15, pady=(10, 15))

        ctk.CTkLabel(log_frame, text="Upload Activity Log", font=ctk.CTkFont(size=16, weight="bold"))\
            .pack(pady=(5, 10))

        self.log_box = ctk.CTkTextbox(log_frame, wrap="word")
        self.log_box.pack(fill="both", expand=True)

        self.log("GUI Initialized. Please configure paths and settings.")
        self.log("Note: All web interactions are simulated for demonstration purposes.")


    def add_labeled_entry(self, parent, label_text, variable, row, show=None):
        """Helper to add a label and entry widget."""
        label = ctk.CTkLabel(parent, text=label_text, width=120, anchor="w")
        label.grid(row=row, column=0, padx=5, pady=8, sticky="w") # Added sticky

        entry = ctk.CTkEntry(parent, textvariable=variable, show=show, width=400)
        entry.grid(row=row, column=1, padx=5, pady=8, sticky="ew") # Changed sticky to ew for expand

    def add_path_selector(self, parent, label, row, dialog_func, tooltip_text=""):
        """Helper to add a label, read-only entry for path, and a browse button."""
        label_widget = ctk.CTkLabel(parent, text=label, width=120, anchor="w")
        label_widget.grid(row=row, column=0, padx=5, pady=8, sticky="w")

        path_var = ctk.StringVar()
        self.paths[label] = path_var

        entry = ctk.CTkEntry(parent, textvariable=path_var, width=400, state="readonly")
        entry.grid(row=row, column=1, padx=5, pady=8, sticky="ew")

        def select_path():
            path = dialog_func(title=f"Select {label}")
            if path:
                path_var.set(path)
                self.log(f"{label} selected: {path}")

        browse_btn = ctk.CTkButton(parent, text="Browse", width=80, command=select_path)
        browse_btn.grid(row=row, column=2, padx=5, pady=8, sticky="e") # Changed sticky for alignment

    def add_dropdown(self, parent, label, variable, options, row, tooltip_text=""):
        """Helper to add a label and a dropdown (option menu) widget."""
        label_widget = ctk.CTkLabel(parent, text=label, width=120, anchor="w")
        label_widget.grid(row=row, column=0, padx=5, pady=8, sticky="w")

        dropdown = ctk.CTkOptionMenu(parent, variable=variable, values=options, width=400)
        dropdown.grid(row=row, column=1, padx=5, pady=8, sticky="ew")

    def export_csv_template(self):
        """Prompts user to save a CSV template for document mapping."""
        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile="document_mapping_template.csv" # Generic template name
        )
        if save_path:
            try:
                with open(save_path, "w", newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Title", "FinalName"])
                    writer.writerow(["SampleDocumentTitle", "SampleFinalIdentifier"]) # Generic sample data
                self.log(f"✅ CSV template exported to: {save_path}")
            except Exception as e:
                self.log(f"❌ Error exporting CSV template: {e}")

    def log(self, message):
        """Adds a message to the GUI's log box."""
        self.log_box.configure(state="normal")
        self.log_box.insert(ctk.END, message + "\n")
        self.log_box.see(ctk.END) # Scroll to end
        self.log_box.configure(state="disabled")

    def start_upload_thread(self):
        """Starts the upload process in a separate thread to keep GUI responsive."""
        # Ensure the abort flag is reset for a new upload attempt
        self.abort_flag = False
        # Use a threading.Event object for a more robust abort signal between threads
        self._abort_event = Threading.Event() # Create an Event object
        thread = Thread(target=self.run_upload, args=(self._abort_event,), daemon=True) # Pass event to thread
        thread.start()
        self.log("Initiating upload process in background...")

    def abort_and_exit(self):
        """Sets the abort flag and schedules GUI destruction."""
        self.log("🛑 User requested to abort upload and exit.")
        self._abort_event.set() # Signal the thread to abort
        # Give a moment for the thread to potentially react before destroying GUI
        self.after(500, self.destroy) # Reduced delay for faster exit

    def run_upload(self, abort_event):
        """
        The main upload logic executed in a separate thread.
        Instantiates DocumentUploader and runs the automation.
        """
        try:
            # Retrieve values from GUI elements
            username = self.username_var.get()
            password = self.password_var.get()
            excel_path = self.paths["Excel Mapping File"].get() # Renamed key
            upload_folder = self.paths["Documents to Upload Folder"].get() # Renamed key
            uploaded_folder = self.paths["Successfully Uploaded Folder"].get() # Renamed key
            failed_folder = self.paths["Failed Uploads Folder"].get() # Renamed key

            # Get the actual API mapping value based on selected display text
            selected_field_api_name = self.field_mapping[self.selected_field.get()]
            document_type_api_code = self.doc_types[self.selected_doc_type.get()]

            # Basic validation that paths are selected
            if not all([username, password, excel_path, upload_folder, uploaded_folder, failed_folder,
                        selected_field_api_name, document_type_api_code]):
                self.log("❌ Error: All fields (credentials, paths, and settings) must be selected/filled.")
                return

            uploader = DocumentUploader( # Use generalized class
                username=username,
                password=password,
                excel_path=excel_path,
                upload_folder=upload_folder,
                uploaded_folder=uploaded_folder,
                failed_folder=failed_folder,
                field_to_fill_api_name=selected_field_api_name, # Renamed parameter
                document_type_api_code=document_type_api_code, # Renamed parameter
                logger=self.log, # Pass the GUI's log method
                abort_flag=abort_event # Pass the Event object
            )
            uploader.run() # Execute the uploader logic

        except Exception as e:
            self.log(f"❌ An error occurred during the upload process: {e}")
        finally:
            self.log("Upload process thread finished.")

