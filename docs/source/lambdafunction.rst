apigateway
==========

LambdaProxyEvent
----------------

.. autoclass:: awsmate.apigateway.LambdaProxyEvent
.. autoexception:: awsmate.apigateway.MalformedPayloadError

HTTP responses
--------------

.. autofunction:: awsmate.apigateway.build_http_response
.. autofunction:: awsmate.apigateway.build_http_server_error_response
.. autofunction:: awsmate.apigateway.build_http_client_error_response

.. autoexception:: awsmate.apigateway.HttpClientError
.. autoexception:: awsmate.apigateway.HttpBadRequestError
.. autoexception:: awsmate.apigateway.HttpUnauthorizedError
.. autoexception:: awsmate.apigateway.HttpNotFoundError
.. autoexception:: awsmate.apigateway.HttpNotAcceptableError
.. autoexception:: awsmate.apigateway.HttpConflictError

Helper functions
----------------

.. autofunction:: awsmate.apigateway.simple_message
.. autofunction:: awsmate.apigateway.determine_content_type
.. autofunction:: awsmate.apigateway.is_binary
.. autofunction:: awsmate.apigateway.json_transformer   

lambdafunction
==============

LambdaEvent
----------------

.. autoclass:: awsmate.lambdafunction.LambdaEvent
.. autoexception:: awsmate.lambdafunction.AwsEventSpecificationError

s3
===

LambdaNotificationEvent   
-----------------------

.. autoclass:: awsmate.s3.LambdaNotificationEvent

logger
======

logger
------

.. autodata:: awsmate.logger.logger
   :no-value:

log_internal_error
------------------

.. autofunction:: awsmate.logger.log_internal_error   
