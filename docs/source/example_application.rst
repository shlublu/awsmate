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
    *   Define the environment variables ``AWS_ACCESS_KEY_ID``, ``AWS_SECRET_ACCESS_KEY``, (...) with the parameters corresponding to your AWS IAM credentials 
    *   Export them all using the shell ``export`` command
    *   Please see the `AWS documentation of these environment variables <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html>`_  for further details

Depending on your AWS IAM setup, you may have to use the AWS CLI to execute commands such as ``aws sts assume-role`` or ``aws sso login`` on top of the above.

.. _Deployment:

Deployment
~~~~~~~~~~

From the ``example`` directory seen above:

* run ``./deploy.sh``: this will deploy all AWS resources described in the ``tf/`` directory. This may take some time, and this produces a pretty verbose log.
* then take note of the final log message ``endpoint_url = "https://<deployment id>.execute-api.<region>.amazonaws.com/v0"``: this is the URL of the newly deployed example API.

The :ref:`section "Application users's guide" <UsersGuide>` below explains how to use this example application.

**Caveat**: 

Should you redeploy the example application after having modified the API Gateway routes or parameters defined in ``tf/03-apigateway.tf`` to experiment on your own, the 
API Gateway resources will be modified ib AWS but the API will not be actually redeployed. You will need to redeploy it using the AWS console or the AWS CLI 
before continuing to use the example application, otherwise unexpected behaviour may occur such as unexpected messages ``{"message":"Missing Authentication Token"}`` when
querying the example API. 

You can also undeploy the application (see :ref:`section "Undeployment" <Undeployment>`) below before deploying it again. This would work but this would change the ``endpoint_url``. 

.. _Undeployment:

Undeployment
~~~~~~~~~~~~

From the ``example`` directory above, run:

* ``./undeploy.sh``: this will destroy all AWS resources created by ``./deploy.sh``. This may take some time.

.. _UsersGuide:

Application users's guide
-------------------------

This example application demonstrates the various modules of the ``awsmate`` library:

API Gateway features: :doc:`apigateway<apigateway>` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Relevant source files

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


* Use

    The ``<endpoint_url>`` placeholder below need replacing by the actual value returned by ``./deploy.sh``, as seen in :ref:`section "Deployment" <Deployment>` above.

    * Route "okay": ``lambda_apigateway_returns_okay.py``
        * Command-line with ``curl`` 
            * ``curl -X https://<endpoint_url>/okay/<any path>?<any url parameter>=<any value> --data '<any JSON payload>' --header '<any name>: <any value>'`` 
            * Example: ``curl -X POST https://<endpoint_url>/okay/lets/go?someParam=someValue --data '{ "someKey": 42 }' --header 'X-example: 42'``
            * Returns 200 with a JSON payload that contains the result of all methods of ``awsmate.apigateway.LambdaProxyEvent`` plus the raw event received from AWS API Gateway.
            * Demonstrates
                * the use of all methods of ``awsmate.apigateway.LambdaProxyEvent``,
                * the use of the HTTP response builder ``awsmate.apigateway.build_http_response()``
            * Tip: play with the ``Accept`` and ``Accept-Encoding`` headers, play with the routes, play with the URL parameters
        * With a web browser
            * ``https://<endpoint_url>/okay/<any path>?<any url parameter>=<any value>``
            * Example: ``https://<endpoint_url>/okay/lets/go?someParam=someValue``
            * Returns an HTML page that is an HTML transformation of the JSON payload described in the command-line example just above.
            * Demonstrates 
                * the same of the above, plus
                * the use of the ``custom_transformers`` (here: HTML transformation of the API response) described in :doc:`the apigateway module documentation <apigateway>`,
                * the use of ``extra_headers`` (here: to handle CORS) with ``awsmate.apigateway.build_http_response()``,
                * the ``gzip`` built-in functionality of ``awsmate.apigateway.build_http_response()`` based on the ``Accept-Encoding`` header (unless your browser does not accept gzip!),
                * the handling of preferences submitted through ``Accept*`` headers in `weighted quality value syntax <https://developer.mozilla.org/en-US/docs/Web/HTTP/Content_negotiation>`_.
            * Tip: think of how you could localize the returned content depending on the ``Accept-Language`` header submitted by the browser
    * Route "forbidden": ``lambda_apigateway_returns_403.py``
        * Command-line with ``curl`` 
            * ``curl -X GET https://<endpoint_url>/forbidden' --header '<any name>: <any value>'`` 
            * Example: ``curl -X GET https://<endpoint_url>/forbidden``
            * Returns 403 with a JSON payload that explains access is forbidden
            * Demonstrates
                * the use of the HTTP response builder ``awsmate.apigateway.build_http_client_error_response()``
        * With a web browser
            * ``https://<endpoint_url>/forbidden``
            * Example: ``https://<endpoint_url>/forbidden``
            * Returns an HTML page that is an HTML transformation of the JSON payload described in the command-line example just above.
            * Demonstrates 
                * the same of the above plus the same extras seen with the "okay" route above
    * Route "crash": ``lambda_apigateway_returns_500.py``
        * Command-line with ``curl`` 
            * ``curl -X GET https://<endpoint_url>/crash' --header '<any name>: <any value>'`` 
            * Example: ``curl -X GET https://<endpoint_url>/crash``
            * Returns 500 with a JSON payload that explains an internal error occurred
            * Logs a complete stack trace in AWS Cloudwatch. See :ref:`section "Logger features" <LoggerFeatures>` below for further details.
            * Demonstrates
                * the use of the HTTP response builder ``awsmate.apigateway.build_http_server_error_response()`` 
                * how not to reveal the cause of the crash to the end user (which would be a security breach) while logging it for debugging purposes
        * With a web browser
            * ``https://<endpoint_url>/crash``
            * Example: ``https://<endpoint_url>/crash``
            * Returns an HTML page that is an HTML transformation of the JSON payload described in the command-line example just above.
            * Demonstrates 
                * the same of the above plus the same extras seen with the "okay" route above                


Lambda Function features: :doc:`lambdafunction <lambdafunction>` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*Nothing for now*

S3 features: :doc:`s3 <s3>` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Relevant source files

::

    awsmate
        |___example
                |
                |___src
                     |
                     |___lambda_s3_notification.py


* Use
    * Step by step instructions
        * Go to the S3 service page
        * Open the page of the S3 bucket ``awsmate-drop-files-here-<your AWS account number>``
        * Upload a file into this bucket
        * Go to the Cloudwatch service page
        * Follow the "Logs/Log group" link of the left navigation panel
        * Search for the ``/aws/lambda/s3_notification`` log group and open it
        * Open the most recent log stream
        * This show a log that contains the result of all methods of ``awsmate.s3.LambdaNotificationEvent`` plus the raw event received from the AWS S3 service.
    * This demonstrates
        * the use of all methods of ``awsmate.s3.LambdaNotificationEvent``
    * Tip: try to delete a file from the S3 bucket and see the corresponding log, try to drop or delete several files in a single action


.. _LoggerFeatures:

Logger features: :doc:`logger <logger>` module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Relevant source files

All files are relevant but we recommand the following one:

::

    awsmate
        |___example
                |
                |___src
                     |
                     |___lambda_apigateway_returns_500.py 


* Use
    * Step by step instructions
        * Open the URL ``https://<endpoint_url>/crash`` with your web browser
        * Go to the Cloudwatch service page
        * Follow the "Logs/Log group" link of the left navigation panel
        * Search for the ``/aws/lambda/apigateway_returns_500`` log group and open it
        * Open the most recent log stream
        * This shows a log containing a critical error message followed by a stack trace showing the details of this crash simulation, and then an informational message showing the returned payload
    * This demonstrates
        * the use of the ``log_internal_error`` function of ``awsmate.logger``
        * the use of the ``logger`` object of ``awsmate.logger``, which is a `standard Python logger <https://docs.python.org/3/library/logging.html>`_
