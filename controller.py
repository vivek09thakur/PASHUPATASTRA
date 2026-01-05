import threading
from astra.bots.login_manager import LoginManager
from astra.bots.worker import Worker

class BotController:
    def __init__(self, credentials):
        self.credentials = credentials
        self.threads = []

    def run_worker(self, client):
        worker = Worker(client)
        worker.like_and_save_by_hashtag("hinduism")

    def start(self):
        manager = LoginManager(self.credentials)
        clients = manager.login_all()

        for client in clients.values():
            t = threading.Thread(target=self.run_worker, args=(client,))
            self.threads.append(t)
            t.start()

    def wait(self):
        for t in self.threads:
            t.join()
        print("All bots have finished.")

if __name__ == "__main__":
    credentials = [
        ("account1", "password1", "session1.json"),
        ("account2", "password2", "session2.json"),
    ]

    controller = BotController(credentials)
    controller.start()
    controller.wait()
