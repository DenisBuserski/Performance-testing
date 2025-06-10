# Use the official Locust image as base
FROM locustio/locust:latest

# Install gRPC and related tools
RUN pip install grpcio grpcio-tools

# Set work directory
WORKDIR /mnt/locust

# Copy everything into the container
COPY . .

# Compile the proto file into Python gRPC client stubs
RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hello.proto