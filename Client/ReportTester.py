from ReporterDiscord import ReporterDiscord
from EmailReporter import EmailReporter
from TwitterReporter import TwitterReporter
import threading
import cv2

# Reporter = None


# def makeBot():
#     Reporter = ReporterDiscord("192.168.0.27", "8001")
#     print("Ok")


# t = threading.Thread(target=makeBot)
# #t.daemon = True
# t.start()

# while(True):
#     x = 1+1

img = cv2.imread('image/3.png')

reporter = TwitterReporter()

reporter.send(img, "OK")

