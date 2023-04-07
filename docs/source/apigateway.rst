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

HTTP errors
-----------

.. autoexception:: awsmate.apigateway.HttpError
.. autoexception:: awsmate.apigateway.HttpClientError
.. autoexception:: awsmate.apigateway.HttpServerError
.. autoexception:: awsmate.apigateway.HttpBadRequestError
.. autoexception:: awsmate.apigateway.HttpUnauthorizedError
.. autoexception:: awsmate.apigateway.HttpPaymentRequiredError
.. autoexception:: awsmate.apigateway.HttpForbiddenError
.. autoexception:: awsmate.apigateway.HttpNotFoundError
.. autoexception:: awsmate.apigateway.HttpMethodNotAllowedError
.. autoexception:: awsmate.apigateway.HttpNotAcceptableError
.. autoexception:: awsmate.apigateway.HttpProxyAuthenticationRequiredError
.. autoexception:: awsmate.apigateway.HttpRequestTimeoutError
.. autoexception:: awsmate.apigateway.HttpConflictError
.. autoexception:: awsmate.apigateway.HttpGoneError
.. autoexception:: awsmate.apigateway.HttpLengthRequiredError
.. autoexception:: awsmate.apigateway.HttpPreconditionFailedError
.. autoexception:: awsmate.apigateway.HttpRequestEntityTooLargeError
.. autoexception:: awsmate.apigateway.HttpRequestUriTooLongError
.. autoexception:: awsmate.apigateway.HttpUnsupportedMediaTypeError
.. autoexception:: awsmate.apigateway.HttpRequestRangeNotSatisfiableError  
.. autoexception:: awsmate.apigateway.HttpExpectationFailedError  
.. autoexception:: awsmate.apigateway.HttpMisdirectedRequestError  
.. autoexception:: awsmate.apigateway.HttpUnprocessableEntityError  
.. autoexception:: awsmate.apigateway.HttpLockedError  
.. autoexception:: awsmate.apigateway.HttpFailedDependencyError  
.. autoexception:: awsmate.apigateway.HttpUpgradeRequiredError  
.. autoexception:: awsmate.apigateway.HttpPreconditionRequiredError  
.. autoexception:: awsmate.apigateway.HttpTooManyRequestsError   
.. autoexception:: awsmate.apigateway.HttpRequestHeaderFieldsTooLargeError     
.. autoexception:: awsmate.apigateway.HttpInternalServerError  
.. autoexception:: awsmate.apigateway.HttpNotImplementedError     
.. autoexception:: awsmate.apigateway.HttpBadGatewayError  
.. autoexception:: awsmate.apigateway.HttpRServiceUnavailableError  
.. autoexception:: awsmate.apigateway.HttpGatewayTimeoutError  
.. autoexception:: awsmate.apigateway.HttpVersionNotSupportedError  
.. autoexception:: awsmate.apigateway.HttpVarianteAlsoNegociatesError  
.. autoexception:: awsmate.apigateway.HttpInsufficientStorageError
.. autoexception:: awsmate.apigateway.HttpLoopDetectedError
.. autoexception:: awsmate.apigateway.HttpNotEXtendedError
.. autoexception:: awsmate.apigateway.HttpNetworkAuthenticationRequiredError  

 
Helper functions
----------------

.. autofunction:: awsmate.apigateway.simple_message
.. autofunction:: awsmate.apigateway.determine_content_type
.. autofunction:: awsmate.apigateway.is_binary
.. autofunction:: awsmate.apigateway.json_transformer   
