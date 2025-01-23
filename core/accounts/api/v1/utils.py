import threading

class EmailThread(threading.Thread):
    # overriding constructor
    def __init__(self, email_obj):
        # calling parent class constructor
        threading.Thread.__init__(self)
        self.email_obj = email_obj
        
    # define your own run method
    def run(self):
        self.email_obj.send()