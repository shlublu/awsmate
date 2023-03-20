#!/bin/sh

cd tf

terraform init
terraform apply -auto-approve -var-file="../variables.tfvars"

cd ..
