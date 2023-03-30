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
    *   Please see the `AWS documentation of these configuration files <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html>`_  for further details
* Using environment variables: 
    *   Define the environment variables ``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, ``AWS_ROLE_ARN`` (...) with the parameters corresponding to your AWS IAM access key 
    *   Export them all using the shell ``export`` command
    *   Please see the `AWS documentation of these environment variables <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html>`_  for further details

.. _Deployment:

Deployment
~~~~~~~~~~

From the ``example`` directory above, run:

* ``./deploy.sh``: this will deploy all AWS resources described in the ``tf/`` directory. This may take a few minutes.
* then take note of the final message ``endpoint_url = "https://<deployment id>.execute-api.<region>.amazonaws.com/v0"``: this is the URL of the newly deployed example API.

The :ref:`section "Application users's guide" <UsersGuide>` below explains how to use this example application.

**Caveat**: 

Should you redeploy the example application after having modified the API Gateway routes or parameters defined in ``tf/03-apigateway.tf``, the 
API Gateway resources will be modified but the API will not redeployed in AWS. You will need to redeploy it using the AWS console or the AWS CLI 
before continuing to use the example application, otherwise unexpected behaviour may occur such as unexpected ``{"message":"Missing Authentication Token"}``
messages when querying the example API. 

You can also undeploy the application (see :ref:`section "Undeployment" <Undeployment>`) below before deploying it again. This would work but this would change the example API URL. 

.. _Undeployment:

Undeployment
~~~~~~~~~~~~

From the ``example`` directory above, run:

* ``./undeploy.sh``: this will destroy all AWS resources created by ``./deploy.sh``. This may take a few minutes.

.. _UsersGuide:

Application users's guide
-------------------------

This example application demonstrates the various modules of the ``awsmate`` library:

API Gateway features: :doc:`apigateway<apigateway>` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Relevant source files:

::

    awsmate
        |___example
                |
                |___src
                     |
                     |___lambda_apigateway_returns_okay.py
                     |
                     |___lambda_apigateway_returns_403.py
                     |
                     |___lambda_apigateway_returns_500.py


* Use (``<deployment id>`` and ``<region>`` below need replacing by actual values returned by ``./deploy.sh``, as seen in :ref:`section "Deployment" <Deployment>` above):
    * Route "okay"
        * Command-line with ``curl`` 
            * ``curl -X <any HTTP verb> https://<deployment id>.execute-api.<region>.amazonaws.com/v0/okay/<any path>?<any url parameter>=<any value>&<etc>=<etc> --data '<any JSON payload>' --header '<any name>: <any value>'`` 
            * Example: ``curl -X POST https://<deployment id>.execute-api.<region>.amazonaws.com/v0/okay/lets/go?someParam=someValue --data '{ "someKey": 42 }' --header 'X-example: 42'``
            * Returns 200 with a JSON payload that contains the result of all methods of ``awsmate.apigateway.LambdaProxyEvent`` plus the raw event received from AWS API Gateway.
            * Demonstrates
                * the use of all methods of ``awsmate.apigateway.LambdaProxyEvent``,
                * the use of the HTTP response builder ``awsmate.apigateway.build_http_response()``
        * With a web browser
            * ``https://<deployment id>.execute-api.<region>.amazonaws.com/v0/okay/<any path>?<any url parameter>=<any value>&<etc>=<etc>``
            * Example: ``https://<deployment id>.execute-api.<region>.amazonaws.com/v0/okay/lets/go?someParam=someValue``
            * Returns an HTML page that is an HTML transformation of the JSON payload described in the command-line example just above.
            * Demonstrates 
                * the same of the above, plus
                * the use of the ``custom_transformers`` (here: HTML transformation of the API response) described in :doc:`the apigateway module documentation <apigateway>`,
                * the use of ``extra_headers`` (here: to handle CORS) with ``awsmate.apigateway.build_http_response()``,
                * the ``gzip`` built-in functionality of ``awsmate.apigateway.build_http_response()`` based on the ``Accept-Encoding`` header (unless your browser does not accept gzip!),
                * the handling of preferences submitted through ``Accept<*>`` headers in `weighted quality value syntax<https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation>`.
    * Route "forbidden"
        * Command-line with ``curl`` 
            * ``curl -X GET https://<deployment id>.execute-api.<region>.amazonaws.com/v0/forbidden' --header '<any name>: <any value>'`` 
            * Example: ``curl -X GET https://<deployment id>.execute-api.<region>.amazonaws.com/v0/forbidden``
            * Returns 403 with a JSON payload that explains access is forbidden
            * Demonstrates
                * the use of the HTTP response builder ``awsmate.apigateway.build_http_client_error_response()``
        * With a web browser
            * ``https://<deployment id>.execute-api.<region>.amazonaws.com/v0/forbidden``
            * Example: ``https://<deployment id>.execute-api.<region>.amazonaws.com/v0/forbidden``
            * Returns an HTML page that is an HTML transformation of the JSON payload described in the command-line example just above.
            * Demonstrates 
                * the same of the above plus the same extras seen with the "okay" route above
    * Route "crash"
        * Command-line with ``curl`` 
            * ``curl -X GET https://<deployment id>.execute-api.<region>.amazonaws.com/v0/crash' --header '<any name>: <any value>'`` 
            * Example: ``curl -X GET https://<deployment id>.execute-api.<region>.amazonaws.com/v0/crash``
            * Returns 500 with a JSON payload that explains an internal error occurred
            * Demonstrates
                * the use of the HTTP response builder ``awsmate.apigateway.build_http_server_error_response()``
        * With a web browser
            * ``https://<deployment id>.execute-api.<region>.amazonaws.com/v0/crash``
            * Example: ``https://<deployment id>.execute-api.<region>.amazonaws.com/v0/crash``
            * Returns an HTML page that is an HTML transformation of the JSON payload described in the command-line example just above.
            * Demonstrates 
                * the same of the above plus the same extras seen with the "okay" route above                


Lambda Function features: :doc:`lambdafunction <lambdafunction>` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Nothing for now*

S3 features: :doc:`s3 <s3>` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Relevant source files:

::

    awsmate
        |___example
                |
                |___src
                     |
                     |___lambda_s3_notification.py


* Use: TODO

Logger features: :doc:`logger <logger>` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Relevant source files:

All files are relevant but we recommand the following one:

::

    awsmate
        |___example
                |
                |___src
                     |
                     |___lambda_apigateway_returns_500.py 


* Use: TODO -- think of suggesting Cloudwatch
