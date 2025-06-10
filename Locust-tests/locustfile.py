from locust import FastHttpUser, task, between
import random
import logging

logging.basicConfig(level=logging.INFO)

class ProductTestUser(FastHttpUser):
    wait_time = between(1, 3)  # Simulate think time between requests

    @task
    def hello(self):
        response = self.client.get("/hello")
        if response.status_code == 200:
            logging.info(f"REST call to [/hello] -> Status:{response.status_code}")
        else:
            logging.error(f"REST call to [/hello] FAILED -> Status:{response.status_code}")

    @task
    def get_product_by_id(self):
        product_id = random.randint(1, 30)
        with self.client.get(f"/product/get/{product_id}", name="/product/get/:id", catch_response=True) as response:
            if response.status_code != 200:
                logging.error(f"ERROR: Failed to fetch product with id:{product_id} -> Status:{response.status_code}")
            else:
                logging.info(f"REST call to [/product/get/{product_id}] successful")