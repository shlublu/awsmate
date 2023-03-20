#!/bin/sh

cd tf

terraform destroy -auto-approve -var-file="../variables.tfvars"

cd ..
