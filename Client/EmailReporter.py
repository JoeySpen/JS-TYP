import smtplib
import ssl
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


class EmailReporter:
    def __init__(self):

        self.port = 465
        self.email = "JSTYP21@gmail.com"
        self.password = "Turing41"
        self.subject = "PiVision Security Alert"
        self.footer = "This message was sent by your PiVision device."

        # Mime settings, create message
        self.msg = MIMEMultipart()
        self.msg["From"] = self.email
        self.msg["To"] = "dragonslash42@gmail.com"
        self.msg["Subject"] = self.subject
        self.msg.attach(MIMEText('<b>Here if your PiVision report! </b><br><img src="cid:image1"><br>' + self.footer, 'html'))

        # Create SSL context
        self.sslContext = ssl.create_default_context()

        # Login to gmail
        self.server = smtplib.SMTP_SSL("smtp.gmail.com",
                                       self.port, context=self.sslContext)
        self.server.login(self.email, self.password)

    def send(self, inputImage, recipient):
        # Convert and add image
        # self.img = cv2.imread('image/1.png') # Load test image
        encodedImage = cv2.imencode(".jpg", inputImage)[1].tobytes()
        image = MIMEImage(encodedImage)
        image.add_header('Content-ID', '<image1>')
        self.msg.attach(image)

        # Send message
        text = self.msg.as_string()
        self.server.sendmail(self.email, recipient, text)
