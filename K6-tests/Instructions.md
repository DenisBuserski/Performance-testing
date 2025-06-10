# Instructions for testing K6

Used project - https://github.com/DenisBuserski/quarkus-grpc-demo

Run:
```bash
docker run --rm -i -v $(pwd):/scripts -v $(pwd):/proto -w /scripts --network=host grafana/k6 run test-k6.js
```

| Command              | Explanation                                                                                                           |
|----------------------|-----------------------------------------------------------------------------------------------------------------------|
| `docker run`         | Start new Docker container                                                                                            |
| `--rm`               | Automatically removes the container after it exits                                                                    |
| `-i`                 | Interactive mode                                                                                                      |
| `-v $(pwd):/scripts` | Mounts the current directory(Where you run the command) into the container at "/scripts"                              |
| `-v $(pwd):/proto`   | Mounts the proto files directory from the host into the container at "/proto"                                         |
| `-w /scripts`        | Set the working directory inside the container to "/scripts"                                                          |
| `--network host`     | - The container shares the host machine’s network stack<br>- Inside the container, `localhost` is your actual machine |
| `grafana/k6`         | The Docker image                                                                                                      |
| `run test-k6.js`     | Run the script                                                                                                        |

<br>

```
running (10.0s), 100/100 VUs, 731 complete and 0 interrupted iterations
default   [ 100% ] 100 VUs  10.0s/10s
```
The test ran for 10 seconds
100 Virtual Users (VUs) were active the entire time
They completed 731 iterations(Loops of the script)
None of them were interrupted

<br>

```
checks_total.......................: 3324    303.22325/s
checks_succeeded...................: 100.00% 3324 out of 3324
checks_failed......................: 0.00%   0 out of 3324
```
Total of 3324 checks/assertions were executed

<br>

```
HTTP
http_req_duration.......................................................: avg=84.57ms min=307.34µs med=3.63ms  max=1.43s    p(90)=77.8ms   p(95)=1.11s   
  { expected_response:true }............................................: avg=84.57ms min=307.34µs med=3.63ms  max=1.43s    p(90)=77.8ms   p(95)=1.11s   
http_req_failed.........................................................: 0.00%  0 out of 1662
http_reqs...............................................................: 1662   151.611625/s
```

```
EXECUTION
iteration_duration......................................................: avg=1.26s   min=1s       med=1.03s   max=2.79s    p(90)=2.57s    p(95)=2.76s   
iterations..............................................................: 831    75.805812/s
vus.....................................................................: 100    min=100       max=100
vus_max.................................................................: 100    min=100       max=100
```

```
NETWORK
data_received...........................................................: 433 kB 40 kB/s
data_sent...............................................................: 454 kB 41 kB/s
```

```
GRPC
grpc_req_duration.......................................................: avg=38.73ms min=950.19µs med=13.16ms max=391.66ms p(90)=104.83ms p(95)=163.42ms
```