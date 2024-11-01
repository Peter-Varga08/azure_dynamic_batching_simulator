import random

from locust import HttpUser, between, task

texts = [
    "The sun is always shining in California",
    "1+1=2",
]


class WebsiteUser(HttpUser):
    wait_time = between(2, 3)

    @task
    def score(self):
        self.client.post("/score", json={"text": random.choice(texts)})


# Run application with `locust -f locustfile.py`
