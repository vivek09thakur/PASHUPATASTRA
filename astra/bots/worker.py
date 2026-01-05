from time import sleep
from random import randint

class Worker:
    def __init__(self, client):
        self.client = client

    def like_and_save_by_hashtag(self, hashtag, limit=10, min_delay=5, max_delay=10):
        medias = self.client.hashtag_medias_top(hashtag, amount=limit)
        for media in medias:
            try:
                self.client.media_like(media.id)
                self.client.media_save(media.id)
                sleep(randint(min_delay, max_delay))
            except Exception:
                sleep(randint(60, 120))
