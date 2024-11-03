from locust import HttpUser, task


class LoadTest(HttpUser):

    @task
    def visit_home_page(self):
        with self.client.get("/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code {response.status_code}")
