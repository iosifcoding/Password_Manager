Of course! Here is the complete README.md file for your Secure Password Manager project, translated into English.

🔑 Secure Password Manager (CLI)

This project is a simple, secure Command Line Interface (CLI) Password Manager written in Python. It utilizes Fernet—a robust symmetric encryption scheme—to ensure the safety and integrity of stored user credentials.


✨ Features

	•	Strong Encryption: Implements the Fernet specification (based on AES-128) for encrypting all sensitive passwords.
	•	Automatic Key Management: Automatically generates and loads the critical encryption key (secret.key) upon startup.
	•	Secure Input: Uses the built-in getpass function to mask passwords during input in the Terminal.
	•	Data Storage: Stores credentials (service name, username, and the encrypted password) in a structured CSV file (credentials.dat).


🛠️ Technology Stack

	•	Language: Python 3.x
	•	Core Libraries:
	◦	cryptography (for Fernet encryption)
	◦	os
	◦	getpass


⚙️ Setup and Execution

Follow these steps to set up and run the application. Using a Virtual Environment (Venv) is highly recommended.

1. Create and Activate Virtual Environment

Open your Terminal and run the following commands:
Bash

# Navigate to the project folder
cd Password_Manager

# Create the Virtual Environment
python3 -m venv .venv

# Activate the Venv (macOS/Linux)
source .venv/bin/activate

# Activate the Venv (Windows - Command Prompt)
# .venv\Scripts\activate

2. Install Dependencies

Ensure the Venv is active ((.venv) should appear in the command line) and install the necessary cryptography library.
Bash

pip install cryptography

3. Run the Application

Execute the main script:
Bash

python main.py
Upon first execution, the application will automatically generate and save the secret.key file.


📖 Usage

The application operates through a simple menu displayed in the Terminal:
Option
Description
1
Save new account: Prompts for Service Name, Username, and Password (the password is encrypted and saved).
2
Retrieve account: Prompts for Service Name, finds the entry, and decrypts the password for display.
3
Exit: Terminates the application.


⚠️ Security Notes

	•	Key Security is Paramount: The secret.key file is critical. Its loss means all stored passwords are lost irrevocably.
	•	Enhancement: For increased security, a future improvement would be to implement a Master Password to encrypt the secret.key itself.
