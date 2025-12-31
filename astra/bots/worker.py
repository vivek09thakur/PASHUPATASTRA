from instagrapi import Client
from time import sleep
from random import randint

class Worker:
    def __init__(self, username, password, session_file):
        self.username = username
        self.password = password
        self.session_file = session_file
        self.client = Client()
        self._login()

    def _login(self):
        try:
            self.client.load_settings(self.session_file)
            self.client.login_by_sessionid(self.client.sessionid)
        except Exception:
            self.client.login(self.username, self.password)
            self.client.dump_settings(self.session_file)

    def like_and_save_by_hashtag(self, hashtag, limit=15, min_delay=20, max_delay=50):
        media_list = self.client.hashtag_medias_top(hashtag, amount=limit)
        for media in media_list:
            try:
                self.client.media_like(media.id)
                self.client.media_save(media.id)
                sleep(randint(min_delay, max_delay))
            except Exception:
                sleep(randint(60, 120))
