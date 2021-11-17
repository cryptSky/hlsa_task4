### Setup

1. Install docker
2. Install siege

## Steps to run

1. `docker-compose up --build` 
2. When all services are up -- upload default configs (grafana dashboard, datasource and init data) by running `./run.sh`
3. run siege test: `siege -d1  -c50  -t100s http://localhost:3000`

### Results

You can check the implementation of probabilistic cache flushing [here](server/rest/user.py)

`siege -d1  -c25  -t30s http://localhost:3000`
```console
Transactions:                   6050 hits
Availability:                 100.00 %
Elapsed time:                  29.75 secs
Data transferred:            9490.21 MB
Response time:                  0.04 secs
Transaction rate:             203.36 trans/sec
Throughput:                   319.00 MB/sec
Concurrency:                    8.46
Successful transactions:        6061
Failed transactions:               0
Longest transaction:            0.52
Shortest transaction:           0.00
```

`siege -d1  -c50  -t30s http://localhost:3000`

```console
Transactions:                   8027 hits
Availability:                 100.00 %
Elapsed time:                  29.30 secs
Data transferred:           12566.61 MB
Response time:                  0.10 secs
Transaction rate:             273.96 trans/sec
Throughput:                   428.89 MB/sec
Concurrency:                   26.31
Successful transactions:        8040
Failed transactions:               0
Longest transaction:            0.97
Shortest transaction:           0.00
```

`siege -d1  -c50  -t60s http://localhost:3000`

```console
Transactions:                  16328 hits
Availability:                 100.00 %
Elapsed time:                  59.05 secs
Data transferred:           25517.79 MB
Response time:                  0.09 secs
Transaction rate:             276.51 trans/sec
Throughput:                   432.14 MB/sec
Concurrency:                   26.12
Successful transactions:       16336
Failed transactions:               0
Longest transaction:            1.09
Shortest transaction:           0.00
```

`siege -d1  -c50  -t100s http://localhost:3000`

```console
Transactions:                  28036 hits
Availability:                 100.00 %
Elapsed time:                  99.81 secs
Data transferred:           43786.39 MB
Response time:                  0.09 secs
Transaction rate:             280.89 trans/sec
Throughput:                   438.70 MB/sec
Concurrency:                   25.47
Successful transactions:       28042
Failed transactions:               0
Longest transaction:            1.17
Shortest transaction:           0.00
```


![siege](screenshot/siege.png)

