import smtplib, ssl
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
#from email.MIMEimage import MIMEImage
import email.mime
import base64

port = 465
email = "JSTYP21@gmail.com"
password = "Turing41"
subject = "Subject: PiVision Security Alert \n\n"
footer = "\n\nThis message was sent by your PiVision device."
img = cv2.imread('image/4n.png')
encodedImage = cv2.imencode(".jpg", img)[1].tobytes()
# jpg_as_text = base64.b64encode(encodedImage)




msg = MIMEMultipart()
msg['From'] = email
msg['To'] = "dragonslash42@gmail.com"
msg['Subject'] = "PiVision"
msg.attach(MIMEText('<b>Below is an image from your device</b><br><img src="cid:image1"><br>Sent from your PiVision device.', 'html'))


fp = open('image/1.png', 'rb')
img2 = fp.read()

# print(encodedImage)


image = MIMEImage(encodedImage)
image.add_header('Content-ID', '<image1>')
msg.attach(image)

# Create SSL context
context = ssl.create_default_context()

server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
server.login(email, password)

text = msg.as_string()

server.sendmail(email, "dragonslash42@gmail.com",
                text)
