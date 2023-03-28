Example application
===================

An example application is provided with this library to show how to implement its features.

Prerequisites
-------------

To deploy and run this application, you will need:

* an AWS account with valid credentials to create, modify and destroy AWS resources
* a Linux shell able to use ``curl`` and ``unzip``. This can either be a native one or a Cygwin or equivalent should you be using Windows.

Example files location
----------------------

::

    awsmate
        |___example
                |
                |___deploy.sh
                |
                |___undeploy.sh
                |
                |___ ...
                |
                |___src/ (Python sources of this example application)                    
                |
                |___tf/ (Terraform sources of this example application)


Instructions for deployment
---------------------------

Credentials
~~~~~~~~~~~ 

* Using configuration and credentials files:
    *   Define a default profile in ``~/.aws/``, or use the AWS CLI ``aws configure`` command
    *   Please see the `AWS documentation <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html>`_  for further details
* Using environment variables: 
    *   Define the environment variables ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY`` with the parameters corresponding to your AWS IAM access key 
    *   Export them both using the shell ``export`` command

Deployment
~~~~~~~~~~

From the ``example`` directory above, run:

* ``./deploy.sh``: this will deploy all AWS resources described in the ``tf/`` directory. This may take a few minutes.
* then take note of the final message ``endpoint_url = "https://XXXXXXX.execute-api.eu-west-1.amazonaws.com/v0"``: this is the URL of the newly deployed example API.

The section "Application users's guide" below explains how to use this example application.

**Caveat**: 

Should you redeploy the example application after having modified the API Gateway routes or parameters defined in ``tf/03-apigateway.tf``, the 
API Gateway resources will be modified but the API will not redeployed in AWS. You will need to redeploy it using the AWS console or the AWS CLI 
before continuing to use the example application, otherwise unexpected behaviour may occur such as unexpected ``{"message":"Missing Authentication Token"}``
messages when querying the example API. 

You can also undeploy the application (see next section) before deploying it again. This would workflows
but this would change the example API URL. 

Undeployment
~~~~~~~~~~~~

From the ``example`` directory above, run:

* ``./undeploy.sh``: this will destroy all AWS resources created by ``./deploy.sh``. This may take a few minutes.

Application users's guide
-------------------------

TODO:

This example application demonstrates the various modules of the ``awsmate`` library:

*  :doc:`apigateway <apigateway>` module: API Gateway features
* Lambda Function features
* Logger features
* S3 features
