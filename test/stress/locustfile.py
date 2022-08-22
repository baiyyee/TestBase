from locust import FastHttpUser, task


class QuickstartUser(FastHttpUser):
    
    @task
    def hello_world(self):
        self.client.get("/")