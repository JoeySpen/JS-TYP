from ReporterDiscord import ReporterDiscord
from EmailReporter import EmailReporter
import threading

# Reporter = None


# def makeBot():
#     Reporter = ReporterDiscord("192.168.0.27", "8001")
#     print("Ok")


# t = threading.Thread(target=makeBot)
# #t.daemon = True
# t.start()

# while(True):
#     x = 1+1

repoter = EmailReporter()

