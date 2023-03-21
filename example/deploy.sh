#!/bin/sh

. check_terraform

cd tf

../${BUILD_DIR}/${TERRAFORM_EXECUTABLE} init
../${BUILD_DIR}/${TERRAFORM_EXECUTABLE} apply -auto-approve -var-file="../variables.tfvars"

cd ..
