# Resource monitoring

## Installation
### 1. Pre-requisites
- Create Grafana cloud account
- Add API key
- Edit prometheus.yml 

### 2. Run
```shell
docker-compose up -d
```

### 3. Add a dashboard to your Grafana cloud
- Raspberry Pi Linux host metrics
- VPS Linux host metrics

### 4. Add more nodes for monitoring
- Run metrics exporter on a new node using docker-compose.node.yml
- Configure UFW: `sudo ufw allow 9100 comment "Node exporter"`
- Edit `prometheus.yml`:
```shell
  - job_name: "node"
    static_configs:
    # add new target here (e.g. raspberry)
    - targets: ["vps:9100", "raspberry:9100"]
```
- Restart prometheus

## Do not forget to configure alerts
- No data received for a long time
- Raspberry Pi CPU temperature
- Disk space is running out

## Sources
- https://grafana.com/docs/grafana-cloud/quickstart/docker-compose-linux/
- https://grafana.com/grafana/dashboards/893
- https://russianblogs.com/article/54981368691/
- https://habr.com/ru/post/659813/
