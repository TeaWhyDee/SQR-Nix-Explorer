from locust import HttpUser, task, between

username = "perftester"
password = "S0M3pwd"


class User(HttpUser):
    wait_time = between(0.05, 0.1)

    def on_start(self):
        self.client.post("/auth/register", json={"username": username, "password": password})
        request = self.client.post("/auth/token",
                                   data={
                                       "username": username,
                                       "password": password,
                                   },
                                   headers={"Content-Type": "application/x-www-form-urlencoded"})
        self.client.headers = {"Authorization": "Bearer " + request.json()["access_token"]}

    @task
    def default_route(self):
        self.client.post("/store",
                         params={"store_name": "teststore"})
        self.client.delete("/store",
                           params={"store_name": "teststore"})
