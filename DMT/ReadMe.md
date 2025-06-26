# Device Management Tool

This project showcases a client-side web application developed to streamline various device management operations. Originally designed for internal company use, this version has been carefully sanitized for public demonstration purposes to protect sensitive company data and credentials.

## 🚀 Features

This tool provides a user-friendly interface for common device administration tasks, demonstrating proficiency in:

* **Authentication Flow:** A simulated login process to manage API access.
* **Device IMEI/Name Mapping:** Dynamically add and update device information (IMEI and custom names).
* **Factory Reset Command:** Simulate sending a factory reset command to a specific device via its IMEI.
* **Random String Generation:** Generate various types of random strings (alphanumeric, numeric, hex, with special characters) for testing or data generation.
* **QR Code Generation:** Generate QR codes based on device IDs or other unique identifiers, useful for physical asset tracking or quick lookups.
* **Bulk Operations (CSV Import):** Simulate the import of device data from a CSV file, showcasing handling of structured data.
* **Responsive Design:** Adapts to different screen sizes for usability on various devices.
* **Dark Mode Toggle:** User-friendly interface enhancement.

## 💻 Technologies Used

* **HTML5:** Structure of the web application.
* **CSS3:** Styling and responsive design (using MUI CSS framework for basic components).
* **JavaScript (ES6+):** Core logic for interacting with the UI, handling user input, and simulating API calls.
* **QRCode.js:** A client-side library for generating QR codes.

## 🔒 Important Note on Security & Data Sanitization

This project includes functionalities that, in a live production environment, would interact with sensitive APIs and data. **For public demonstration on GitHub, all actual API endpoints and credential handling have been replaced with placeholders and simulated logic.**

* **API Endpoints:** Real API URLs (e.g., `https://api-prod.surfsight.net`) have been replaced with generic placeholders like `https://api.example.com`.
* **Authentication:** The authentication process is **simulated**. No real credentials are used or exposed. In a production application, robust and secure authentication methods (like OAuth, JWT, or API keys stored in secure environment variables) would be implemented server-side, not directly in client-side JavaScript.
* **API Calls:** All `fetch` requests to external APIs have been commented out and replaced with `console.log` statements and simulated success/error responses. This ensures the application can be run locally without attempting to connect to private infrastructure.
* **Sensitive Data:** All company-specific names, IDs, and internal URLs have been generalized or removed to protect proprietary information.

This approach demonstrates the functionality and logic of the application while adhering to best practices for sharing code publicly.

## ▶️ How to Run Locally

To run this project locally and explore its features:

1.  **Clone the repository** (once you upload it to GitHub):
    ```bash
    git clone [https://github.com/YourUsername/device-management-tool.git](https://github.com/YourUsername/device-management-tool.git)
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd device-management-tool
    ```
3.  **Open the `index.html` file:** Simply open the `index.html` file directly in your web browser. There's no server-side setup required as it's a client-side application.

## 💡 Potential Enhancements

* Integrate with a mock API server (e.g., using Node.js with Express or JSON Server) to provide a more realistic API interaction experience without exposing real data.
* Implement a proper state management solution for larger applications.
* Expand error handling and user feedback.
* Add unit and integration tests.
* Refactor the JavaScript into modules for better organization.

---

Feel free to customize this README further to highlight specific aspects of your contributions or any additional features you want to emphasize!