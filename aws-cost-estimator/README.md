# AWS Cost Estimator 💰

A Python Flask web application to estimate monthly AWS infrastructure costs.
Built as part of #100DaysOfDevOps challenge.

## Tech Stack
- Python 3.11
- Flask 3.0
- Docker

## Supported AWS Services
- EC2 (12 instance types)
- RDS (6 instance classes)
- S3 (3 storage classes)
- ELB / ALB / NLB
- EBS (4 volume types)
- NAT Gateway
- CloudFront
- Lambda
- EKS

## Run Locally

### Without Docker
```bash
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000

### With Docker
```bash
# Build the image
docker build -t aws-cost-estimator .

# Run the container
docker run -d -p 5000:5000 --name aws-cost-estimator aws-cost-estimator

# Open in browser
http://localhost:5000
```

### Docker Commands
```bash
# View running containers
docker ps

# View logs
docker logs aws-cost-estimator

# Stop container
docker stop aws-cost-estimator

# Remove container
docker rm aws-cost-estimator
```
