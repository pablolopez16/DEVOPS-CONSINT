# DevOps Technical Assessment README.md

## Start Localstack

docker-compose up localstack

## Terraform apply

2 options:

- Add a new step in the GitHub Actions workflow after Terraform Plan that runs terraform apply -auto-approve automatically. 
- Run it manually from the terraform folder by executing the following commands in order:
cd terraform
terraform init
terraform validate
terraform plan
terraform apply (typing yes when prompted)

## Run application


## Destroy the infraestructure

2 options:

- Add a new step in the GitHub Actions workflow that runs docker-compose down and terraform destroy -auto-approve automatically after the previous steps.
- Run it manually from the terminal by executing the following commands in order:

docker-compose down
cd terraform
terraform destroy