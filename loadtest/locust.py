import time
from locust import HttpUser, task

class QuickstartUser(HttpUser):

    def on_start(self):
        self.client.post(
            "/users", 
            headers={"Content-Type": "application/json"},
            json={"email": "test@gmail.com",
            "password": "password"})
    

    @task
    def hello_world(self):
        self.client.get(
            "/token", 
            headers={"Content-Type": "application/json"},
            json={"username": "test@gmail.com",
            "password": "password"})
