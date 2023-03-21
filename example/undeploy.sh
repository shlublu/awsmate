#!/bin/sh

. check_terraform.sh

cd tf

../${BUILD_DIR}/${TERRAFORM_EXECUTABLE} init
../${BUILD_DIR}/${TERRAFORM_EXECUTABLE} destroy -auto-approve -var-file="../variables.tfvars"

cd ..
