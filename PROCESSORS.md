## Connecting to running processors
```
ssh ubuntu@ec2-34-222-61-229.us-west-2.compute.amazonaws.com -i ~/.ssh/hsg-tungite-labs.pem 
```

## Stop all processors on remote
```
sudo systemctl stop runner_1
sudo systemctl stop runner_2
sudo systemctl stop runner_3
sudo systemctl stop runner_4
```
Note: It takes up to 90 seconds for each runner to come online.


## Running the remote manually.

```
cd canopy-processor-aws/
/home/ubuntu/.pyenv/versions/env/bin/python runner.py
```