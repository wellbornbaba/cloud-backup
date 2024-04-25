# README.md

# MultiUploader

MultiUploader is a Python tool that allows you to simultaneously upload files to multiple cloud storage services and send them via email. This tool is designed to streamline the process of sharing files across different platforms.

## Features

- Upload files to Google Drive, Dropbox, GitHub, OneDrive, and FTP servers simultaneously.
- Send files via email using SMTP.
- Easy-to-use command-line interface.
- Customizable upload options and configurations.

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/wellbornbaba/cloud-backup.git

   ```

2. Navigate to the project directory:

   ```bash
   cd cloud-backup

   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

   ```

## Configuration

1. Create a .env file in the root directory of the project:

   ````plaintext
   DROPBOX_TOKEN=YOUR_DROPBOX_ACCESS_TOKEN
   GITHUB_TOKEN=YOUR_GITHUB_ACCESS_TOKEN
   REPO_NAME=repository_name
   ONEDRIVE_CLIENT_ID=YOUR_ONEDRIVE_CLIENT_ID
   ONEDRIVE_CLIENT_SECRET=YOUR_ONEDRIVE_CLIENT_SECRET
   ONEDRIVE_REFRESH_TOKEN=YOUR_ONEDRIVE_REFRESH_TOKEN
   FTP_HOST=YOUR_FTP_HOST
   FTP_USERNAME=YOUR_FTP_USERNAME
   FTP_PASSWORD=YOUR_FTP_PASSWORD
   SMTP_HOST=YOUR_SMTP_HOST
   SMTP_USERNAME=YOUR_SMTP_USERNAME
   SMTP_PASSWORD=YOUR_SMTP_PASSWORD
   SMTP_PORT=YOUR_SMTP_PORT
   SMTP_PROTOCOL=YOUR_SMTP_PROTOCOL  # "tls" or "ssl"

update this setting
   ```python
   # main.py

   import os
   from MultiUploader import MultiUploader

   def main():
      file_path = os.getenv("FILE_PATH")
      file_name = os.getenv("FILE_NAME")
      emaillist = []  # Your email list
      uploader = MultiUploader(file_path, file_name, emaillist)
      uploader.start_upload()

   if __name__ == "__main__":
      main()
   

Replace placeholders with your actual credentials and configuration options.

2. Customize the uploadwith attribute in main.py to specify which upload services to use. For example:

   ```python
   uploader.uploadwith = ["gdrive", "dropbox", "github"]  # Use Google Drive, Dropbox, and GitHub
   ```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
-python-dotenv
-pydrive
-dropbox
-PyGithub
-onedrivesdk
-ftplib
-smtplib


## Usage

Run the main.py script to start the upload process:

   ```python
   python main.py




```
