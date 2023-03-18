apigateway
==========

Lambda event
------------

.. autoclass:: awsmate.apigateway.LambdaProxyEvent

Lambda event related errors
---------------------------

.. autoexception:: awsmate.apigateway.MalformedPayloadError

HTTP responses builders
-----------------------

.. autofunction:: awsmate.apigateway.build_http_response
.. autofunction:: awsmate.apigateway.build_http_server_error_response
.. autofunction:: awsmate.apigateway.build_http_client_error_response

Common HTTP client errors
-------------------------

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
