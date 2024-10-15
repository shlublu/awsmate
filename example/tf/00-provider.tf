terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
            version = ">= 5.71.0"
        }
        archive = {
            source = "hashicorp/archive"
            version = ">= 2.6.0"           
        }
    }
    
    required_version = ">= 1.9.0"
}

provider "aws" {
}
