from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    def on_start(self):
        response = self.client.post("/users/login",json={
            "username": "string",
            "password": "string"}
            )
        access_token = response.json()["access_token"]
        self.client.headers = {
            "Authorization": f"Bearer {access_token}"
        }

    @task
    def expenses_get_all(self):
        self.client.get("/expenses/get-all")

    @task
    def not_found(self):
        self.client.get("/not-found")

