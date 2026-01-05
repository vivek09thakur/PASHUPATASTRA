import os
from instagrapi import Client

class LoginManager:
    def __init__(self, credentials):
        self.credentials = credentials
        self.clients = {}

    def login_all(self):
        for username, password, session_file in self.credentials:
            client = Client()

            if os.path.exists(session_file):
                client.load_settings(session_file)
                try:
                    client.get_timeline_feed()
                    self.clients[username] = client
                    continue
                except Exception:
                    pass

            client.login(username, password)
            client.dump_settings(session_file)
            self.clients[username] = client

        return self.clients
