# Data Ingest Platform

> For deployment steps follow `Deployment.md`and for details about the project raed `Report.md`

> Below is the project delivery directory structure. 

```
.
├── LICENSE
├── README.md
├── code
│   ├── README.md
│   └── mysimbdp
│       ├── app
│       │   ├── consumer.py
│       │   ├── producer.py
│       │   └── requirements.txt
│       ├── docker-compose.yaml
│       ├── mongo
│       │   ├── config.init.js
│       │   ├── enable-shard.js
│       │   ├── router.init.js
│       │   ├── shardrs.init.js
│       │   └── user.init.js
│       ├── mongo-up.sh
│       ├── server-1.properties
│       ├── server.properties
│       └── zoo-up.sh
├── data
│   └── reviews.csv
├── logs
│   ├── consumer_log_20240215_183129.txt
│   ├── consumer_log_20240216_033458.txt
│   ├── consumer_log_20240216_044626.txt
│   ├── kafka_metrics_log_1.txt
│   ├── kafka_metrics_log_4.txt
│   ├── kafka_metrics_log_5.txt
│   ├── mongo_log_20240215_183128.txt
│   ├── mongo_log_20240216_033458.txt
│   ├── mongo_log_20240216_044626.txt
│   ├── producer_log_20240215_164911.txt
│   ├── producer_log_20240216_033357.txt
│   └── producer_log_20240216_035543.txt
└── reports
    ├── Deployment.md
    ├── Report.md
    └── resources
        ├── data-dictionary.png
        ├── json-schema.png
        ├── kf-console.png
        ├── lineage-data.png
        ├── mongo-compass.png
        ├── mysimbdp.png
        ├── service-info-schema.png
        ├── test1-broker.png
        ├── test2-broker.png
        ├── test3-broker.png
        └── zk-console.png
```
> 