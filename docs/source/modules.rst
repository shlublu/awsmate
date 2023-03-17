apigateway
==========

.. currentmodule:: awsmate.apigateway

LambdaProxyEvent
----------------

.. autoclass:: LambdaProxyEvent
.. autoexception:: MalformedPayloadError

HTTP responses
--------------

.. autofunction:: build_http_response
.. autofunction:: build_http_server_error_response
.. autofunction:: build_http_client_error_response

.. autoexception:: HttpClientError
.. autoexception:: HttpBadRequestError
.. autoexception:: HttpUnauthorizedError
.. autoexception:: HttpNotFoundError
.. autoexception:: HttpNotAcceptableError
.. autoexception:: HttpConflictError

Helper functions
----------------

.. autofunction:: simple_message
.. autofunction:: determine_content_type
.. autofunction:: is_binary
.. autofunction:: json_transformer   

lambdafunction
==============

.. currentmodule:: awsmate.lambdafunction

LambdaProxyEvent
----------------

.. autoclass:: LambdaEvent
.. autoexception:: AwsEventSpecificationError

s3
===

.. currentmodule:: awsmate.s3

LambdaNotificationEvent   
-----------------------

.. autoclass:: LambdaNotificationEvent

Logger
======

.. currentmodule:: awsmate.logger

logger
------

.. autodata:: logger
   :no-value:

log_internal_error
------------------

.. autofunction:: log_internal_error   
