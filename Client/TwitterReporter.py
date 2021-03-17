import tweepy
import cv2

class TwitterReporter:
    def __init__(self):
        auth = tweepy.OAuthHandler("IqdO8jY9WmhxrnQqF68w02lHh", "JsUNLHDgHgNw6qc7BgrwViYtLbNWbB9TYIorxNNNVaBcEjY0bh")
        auth.set_access_token("1358527695290793984-4APu9YLN2UuY1nx12tlpLd6kpPsRVL", "Ns62URxKb1XK9212J5pyQwkvWt1WLEhrjndtq6nt0qGkE")

        # Create API object
        self.api = tweepy.API(auth)


    def send(self, inputImage, recipient):
        cv2.imwrite('report.jpg', inputImage)
        self.api.update_with_media(filename="report.jpg", status="PiVision reporting update!")
