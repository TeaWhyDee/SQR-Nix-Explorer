import os
import random

from locust import HttpUser, task, between

username = ""  # os.environ['PERFTEST_USERNAME']
password = ""  # os.environ['PERFTEST_PASSWORD']


class User(HttpUser):
    wait_time = between(0.1, 0.1)

    def on_start(self):
        request = self.client.post("/auth/token",
                                   data={
                                       "username": username,
                                       "password": password,
                                   },
                                   headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.client.headers = {"Authorization": "Bearer " + request.json()["access_token"]}

    @task
    def default_route(self):
        print(self.client.post("/store",
                         params={"store_name": "test_store"}).headers)
        print(self.client.delete("/store",
                           params={"store_name": "test_store"}).headers)
