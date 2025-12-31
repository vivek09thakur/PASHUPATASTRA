from astra.bots.worker import Worker

worker = Worker("marshal_jon333","dollar@1357","session.json")
worker.like_and_save_by_hashtag("hinduism", limit=10, min_delay=5, max_delay=10)