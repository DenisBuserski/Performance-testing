# Instructions for testing Locust

Used project - https://github.com/DenisBuserski/quarkus-grpc-demo

<br>

## Test REST

```bash
docker run --rm --network host -v $(pwd):/mnt/locust -w /mnt/locust locustio/locust -f locustfile.py --host=http://localhost:8082
```

```bash
docker run --rm --network host \
  -v $(pwd):/mnt/locust \
  -w /mnt/locust \
  locustio/locust \
  -f locustfile.py \
  --host=http://localhost:8082 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 2m \
  --headless
```

| Command                        | Explanation                                                                                                           |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| `docker run`                   | Start new Docker container                                                                                            |
| `--rm`                         | Automatically removes the container after it exits                                                                    |
| `--network host`               | - The container shares the host machine’s network stack<br>- Inside the container, `localhost` is your actual machine |
| `-v ${pwd}:/mnt/locust`        | Mounts the current directory(Where you run the command) into the container at "/mnt/locust"                           |
| `locustio/locust`              | The Docker image                                                                                                      |
| `-f locustfile.py`             | The test script                                                                                                       |
| `--host=http://localhost:8082` | Set the target host URL where Locust will load 8082 is where the application is running                               |
| `--users 100`                  | Simulate 100 concurrent virtual users                                                                                 |
| `--spawn-rate 10`              | Start 10 users per second (ramp-up in 10s)                                                                            |
| `--run-time 2m `               | Run the test for 2 minutes                                                                                            |
| `--headless`                   | Skip the Web UI and run automatically                                                                                 |
| `--csv results/load_test`      | Save results to CSV                                                                                                   |

<br>

## Test gRPC

Create a [Dockerfile]()

```bash
docker build -t locust-grpc .
```

```bash
docker run --rm --network host locust-grpc -f /mnt/locust/locustfile-grpc.py --host=http://localhost:8081
```