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

From the ``example`` directory above:

* ``./deploy.sh``

This wil deploy all AWS resources described in the ``tf/`` directory.

**Caveat**: Should you redeploy the example application after having modified the API Gateway routes or parameters defined in ``tf/03-apigateway.tf``, the 
API Gateway will be modified but not redeployed in AWS. You will need to redeploy it using the AWS console or the AWS CLI before continuing to use the example
application, otherwise unexpected behaviour may occur. You can also undeploy the application (see next section) before deplying it again, but this would
change the example API URL. 

Undeployment
~~~~~~~~~~~~

From the ``example`` directory above:

* ``./undeploy.sh``

This will destroy all AWS resources created by ``./deploy.sh``.


Application users's guide
-------------------------

* API Gateway
* S3 Notifications
