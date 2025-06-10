from locust import FastHttpUser, task, between, events
import random
import logging
import grpc
import string
import time
from concurrent import futures

import sys

sys.path.append("/mnt/locust")
import hello_pb2
import hello_pb2_grpc

logging.basicConfig(level=logging.INFO)

class ProductTestUser(FastHttpUser):
    wait_time = between(1, 3)  # Simulate think time between requests

    def on_start(self):
        # Initialize gRPC channel and stub here once per user instance
        self.grpc_channel = grpc.insecure_channel("localhost:8081")
        self.grpc_stub = hello_pb2_grpc.HelloGrpcStub(self.grpc_channel)

    def on_stop(self):
        self.grpc_channel.close()

    @task
    def hello_grpc(self):
        name = random.choice(["Alice", "Bob", "Charlie"])
        request = hello_pb2.HelloRequest(name=name)
        start_time = time.time()
        try:
            response = self.grpc_stub.SayHello(request)
            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="gRPC",
                name="SayHello",
                response_time=total_time,
                response_length=0,
                exception=None
            )
            logging.info(f"gRPC test -> [SayHello] -> Success -> {response.message}")
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name="SayHello",
                response_time=total_time,
                response_length=0,
                exception=e
            )
            logging.error(f"gRPC test -> [SayHello] -> Failed: {e}")

    @task
    def grpc_insert_product(self):
        request = hello_pb2.ProductRequest(
            name="Product_" + ''.join(random.choices(string.ascii_letters, k=5)),
            price=str(round(random.uniform(10.0, 100.0), 2)),
            quantity=random.randint(1, 50)
        )
        start_time = time.time()
        try:
            response = self.grpc_stub.InsertProduct(request)
            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="gRPC",
                name="InsertProduct",
                response_time=total_time,
                response_length=0,
                exception=None
            )
            logging.info(f"gRPC test -> [InsertProduct] -> Success -> Name: {response.name}, Price: {response.price}, Qty: {response.quantity}")
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name="InsertProduct",
                response_time=total_time,
                response_length=0,
                exception=e
            )
            logging.error(f"gRPC tst -> [InsertProduct] -> Failed: {e}")

    @task
    def grpc_get_product_by_id(self):
        product_id = random.randint(1, 30)
        request = hello_pb2.ProductIdRequest(id=product_id)
        start_time = time.time()
        try:
            response = self.grpc_stub.GetProductById(request)
            total_time = int((time.time() - start_time) * 1000)

            events.request.fire(
                request_type="gRPC",
                name="GetProductById",
                response_time=total_time,
                response_length=0,
                exception=None
            )

            if response:
                logging.info(f"gRPC test -> [GetProductById] -> Success -> Name: {response.name}, price: {response.price}, quantity: {response.quantity}")
        except grpc.RpcError as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request.fire(
                request_type="gRPC",
                name="GetProductById",
                response_time=total_time,
                response_length=0,
                exception=e
            )
            logging.error(f"gRPC test -> [GetProductById] -> Failed: {e}")