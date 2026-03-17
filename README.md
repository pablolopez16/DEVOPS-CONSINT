# DevOps Technical Assessment README.md

## Start LocalStack and the Application

First, pull the application image from Docker Hub:

```bash
docker pull pablolopez161616/s3-app:latest
```

Then start both LocalStack and the API:

```bash
docker-compose up 
```


## Terraform apply

There are 2 options:

- Add a new step in the GitHub Actions workflow after Terraform Plan that runs terraform apply -auto-approve automatically. 
- Run it manually from the terraform folder by executing the following commands in order:

```bash
cd terraform
terraform init
terraform validate
terraform plan
terraform apply (typing yes when prompted)
´´´

## Run application
Once LocalStack is running and Terraform has been applied, the API is available at `http://localhost:8000`.

To list the objects inside the S3 bucket:

```bash
curl http://localhost:8000/terraform/s3/bucket/objects
```


To upload a JSON file to the S3 bucket:

```bash
curl -X POST http://localhost:8000/terraform/s3/bucket/objects \
     -H "Content-Type: application/json" \
     -d '{"filename": "constella.json", "user": "pablo"}'
```

## Destroy the infrastructure

2 options:

- Add a new step in the GitHub Actions workflow that runs docker-compose down and terraform destroy -auto-approve automatically after the previous steps.
- Run it manually from the terminal by executing the following commands in order:

```bash
docker-compose down
cd terraform
terraform destroy
```