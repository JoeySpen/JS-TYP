import smtplib, ssl
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

port = 465
email = "JSTYP21@gmail.com"
password = "Turing41"
subject = "PiVision Security Alert"
footer = "This message was sent by your PiVision device."

# Convert image CV2 -> jpg bytes
img = cv2.imread('image/1.png')
encodedImage = cv2.imencode(".jpg", img)[1].tobytes()

# Mime settings, create message
msg = MIMEMultipart()
msg["From"] = email
msg["To"] = "dragonslash42@gmail.com"
msg["Subject"] = subject
msg.attach(MIMEText('<b>Below is an image from your device</b><br><img src="cid:image1"><br>' + footer, 'html'))

# Add image to message
image = MIMEImage(encodedImage)
image.add_header('Content-ID', '<image1>')
msg.attach(image)

# Create SSL context
sslContext = ssl.create_default_context()

# Login to gmail
server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=sslContext)
server.login(email, password)

# Send message
text = msg.as_string()
server.sendmail(email, "dragonslash42@gmail.com",
                text)
