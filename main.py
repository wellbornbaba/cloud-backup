import os
import threading
from dotenv import load_dotenv
import dropbox
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from github import Github
from onedrivesdk import AuthProvider, Client
import ftplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class MultiUploader:
    def __init__(self, file_path, file_name="", emaillist=[]):
        load_dotenv()  # Load environment variables from .env file

        if not file_name:
            file_name = os.path.splitext(os.path.basename(file_path))[0]

        self.file_path = file_path
        self.file_name = file_name
        self.dropbox_token = os.getenv("DROPBOX_TOKEN")
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("REPO_NAME")
        self.onedrive_client_id = os.getenv("ONEDRIVE_CLIENT_ID")
        self.onedrive_client_secret = os.getenv("ONEDRIVE_CLIENT_SECRET")
        self.onedrive_refresh_token = os.getenv("ONEDRIVE_REFRESH_TOKEN")
        self.ftp_host = os.getenv("FTP_HOST")
        self.ftp_username = os.getenv("FTP_USERNAME")
        self.ftp_password = os.getenv("FTP_PASSWORD")
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_port = os.getenv("SMTP_PORT")
        self.smtp_protocol = os.getenv("SMTP_PROTOCOL").lower()
        self.emaillist = emaillist
        # set which upload should be use ALL is for all
        self.uploadwith = []  # list name e.g gdrive,github if empty use all

        self.upload_complete = {
            "gdrive": False,
            "dropbox": False,
            "github": False,
            "onedrive": False,
            "ftp": False,
            "smtp": False,
        }  # Flags to track upload completion

    # Function to upload file to Google Drive
    def upload_to_google_drive(self):
        keyname = "gdrive"
        if keyname in self.uploadwith or not self.uploadwith:
            gauth = GoogleAuth()
            gauth.ServiceAuth()  # Use service account credentials
            drive = GoogleDrive(gauth)

            with drive.CreateFile({"title": self.file_name}) as file:
                file.SetContentFile(self.file_path)
                file.Upload()

            self.upload_complete[keyname] = True

    # Function to upload file to Dropbox
    def upload_to_dropbox(self):
        keyname = "dropbox"
        if keyname in self.uploadwith or not self.uploadwith:
            dbx = dropbox.Dropbox(self.dropbox_token)

            with open(self.file_path, "rb") as f:
                dbx.files_upload(f.read(), "/" + self.file_name)
            self.upload_complete[keyname] = True

    # Function to upload file to GitHub
    def upload_to_github(self):
        keyname = "github"
        if keyname in self.uploadwith or not self.uploadwith:
            g = Github(self.github_token)
            repo = g.get_user().get_repo(self.repo_name)

            with open(self.file_path, "rb") as f:
                content = f.read()
                repo.create_file(self.file_name, "Uploaded via Python", content)
            self.upload_complete[keyname] = True

    # Function to upload file to OneDrive
    def upload_to_onedrive(self):
        keyname = "onedrive"
        if keyname in self.uploadwith or not self.uploadwith:
            auth_provider = AuthProvider(
                client_id=self.onedrive_client_id,
                client_secret=self.onedrive_client_secret,
            )
            client = Client(auth_provider)
            client.auth_provider.authenticate(self.onedrive_refresh_token)

            client.item(drive="me", id="root").children[self.file_name].upload(
                self.file_path
            )
            self.upload_complete[keyname] = True

    # Function to upload file via FTP
    def upload_via_ftp(self):
        keyname = "ftp"
        if keyname in self.uploadwith or not self.uploadwith:
            with ftplib.FTP(self.ftp_host) as ftp:
                ftp.login(self.ftp_username, self.ftp_password)
                with open(self.file_path, "rb") as f:
                    ftp.storbinary("STOR " + self.file_name, f)
            self.upload_complete[keyname] = True

    # Function to send file via SMTP
    def send_via_smtp(self):
        keyname = "smtp"
        if keyname in self.uploadwith or not self.uploadwith:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_username
            msg["To"] = ", ".join(self.emaillist)
            msg["Subject"] = "File Upload"

            with open(self.file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", f"attachment; filename= {self.file_name}"
                )
                msg.attach(part)

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_protocol == "tls":
                    server.starttls()  # Upgrade to a secure connection using STARTTLS
                elif self.smtp_protocol == "ssl":
                    server = smtplib.SMTP_SSL(
                        self.smtp_host, self.smtp_port
                    )  # Use SSL directly
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.smtp_username, self.emaillist, msg.as_string())

            self.upload_complete[keyname] = True

    # Function to start upload threads
    def start_upload(self):
        threads = [
            threading.Thread(target=self.upload_to_google_drive),
            threading.Thread(target=self.upload_to_dropbox),
            threading.Thread(target=self.upload_to_github),
            threading.Thread(target=self.upload_to_onedrive),
            threading.Thread(target=self.upload_via_ftp),
            threading.Thread(target=self.send_via_smtp),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        # Check if all uploads are complete
        for key, value in self.upload_complete.items():
            if value:
                print(f"{key.capitalize()} uploaded successfully.")
            else:
                print(f"{key.capitalize()} upload failed.")


if __name__ == "__main__":
    file_path = "path_to_your_file"
    file_name = "example.txt"
    emaillist = ["recipient1@example.com", "recipient2@example.com"]
    uploader = MultiUploader(file_path, file_name, emaillist)
    uploader.uploadwith = ["gdrive", "dropbox", "github"]  # Use Google Drive, Dropbox, and empty for all
    uploader.start_upload()
