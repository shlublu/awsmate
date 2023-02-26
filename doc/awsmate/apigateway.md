Module awsmate.apigateway
=========================

Functions
---------

    
`build_http_client_error_response(error: awsmate.apigateway.HttpClientError) ‑> None`
:   

    
`build_http_response(status: int, payload: Union[dict, str], *, event: Optional[awsmate.apigateway.LambdaProxyEvent] = None, customTransformers: Optional[Dict[str, Callable[[dict], Tuple[str, str]]]] = None, extraHeaders: Optional[Dict[str, str]] = None) ‑> dict`
:   

    
`build_http_server_error_response(message: Optional[str] = None) ‑> None`
:   

    
`determine_content_type(event: awsmate.apigateway.LambdaProxyEvent, *, customTransformers: Optional[dict] = None) ‑> str`
:   

    
`is_binary(contentType: str) ‑> bool`
:   

    
`json_transformer(payload: dict) ‑> Tuple[str, str]`
:   

    
`simple_message(message: str) ‑> Dict[str, str]`
:   

Classes
-------

`HttpBadRequestError(msg: str)`
:   Unspecified run-time error.

    ### Ancestors (in MRO)

    * awsmate.apigateway.HttpClientError
    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException

`HttpClientError(status: int, msg: str)`
:   Unspecified run-time error.

    ### Ancestors (in MRO)

    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException

    ### Descendants

    * awsmate.apigateway.HttpBadRequestError
    * awsmate.apigateway.HttpConflictError
    * awsmate.apigateway.HttpNotAcceptableError
    * awsmate.apigateway.HttpNotFoundError
    * awsmate.apigateway.HttpUnauthorizedError

    ### Instance variables

    `status`
    :

`HttpConflictError(msg: str)`
:   Unspecified run-time error.

    ### Ancestors (in MRO)

    * awsmate.apigateway.HttpClientError
    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException

`HttpNotAcceptableError(msg: str)`
:   Unspecified run-time error.

    ### Ancestors (in MRO)

    * awsmate.apigateway.HttpClientError
    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException

`HttpNotFoundError(msg: str)`
:   Unspecified run-time error.

    ### Ancestors (in MRO)

    * awsmate.apigateway.HttpClientError
    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException

`HttpUnauthorizedError(msg: str)`
:   Unspecified run-time error.

    ### Ancestors (in MRO)

    * awsmate.apigateway.HttpClientError
    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException

`LambdaProxyEvent(eventObject: dict)`
:   Mapping of the input event received by an AWS Lambda function triggered by an AWS Api Gateway during a client API call.
    
    Examples
    --------
    >>> def lambda_handler(rawEvent, context):
    >>>     import awsmate.apigateway as ag
    >>>     event = ag.LambdaProxyEvent(rawEvent)    
    
    Parameters
    ----------
    eventObject : dict
        The parameter ``event`` received by the AWS Lambda function handler.

    ### Ancestors (in MRO)

    * awsmate.lambdafunction.LambdaEvent

    ### Methods

    `call_path(self) ‑> Tuple[str, ...]`
    :   Returns the path of the API call, broken down into elements.
        
        Returns
        -------
        tuple
            Path elements as ``str``.
        
        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``path`` key is present in the event data.      
        
        Examples
        --------
        API call ``GET /projects/foobar/modules`` leads to ``('projects', 'foobar', 'modules')``

    `call_string(self) ‑> str`
    :   Convenience method that returns the HTTP method of the call followed by the path and the URL parameters of the call.
        
        Returns
        -------
        str
            The complete call string of the API call, including URL parameters if any.
        
        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If at least one of the ``httpMethod``, ``path`` or ``query_string_parameters`` keys is not present in the event data.     
        
        Examples
        --------
        ``GET /projects/foobar/modules?order=alphabetical&released=true``

    `header_sorted_preferences(self, header: str) ‑> Tuple[str, ...]`
    :   Returns all values assigned to the given header, sorted by decreasing preferences.
        
        Preferences are determined according to the weighted quality value syntax.
        An empty ``tuple'' is returned if the given header is not found among those submitted by the caller.
        
        Returns
        -------
        tuple
            Header values as ``str``, in decreasing preference order.
            
        Examples
        --------
        Header ``Encoding: gzip;q=0.2,deflate,identity;q=0.9`` leads to ``('deflate', 'identity', 'gzip')``

    `http_headers(self) ‑> Dict[str, str]`
    :   Returns all HTTP headers of the API call.
        
        Values of these headers are returned unparsed, as submitted.
        
        Returns
        -------
        dict
            Keys are header names as ``str``, values are corresponding raw values as ``str``.
            
        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``headers`` key is present in the event data.

    `http_method(self) ‑> str`
    :   Returns the HTTP method of the API call.
        
        The method verb is returned as transmitted by AWS API Gateway. GET, PUT, POST, PATCH, DELETE are expected, but no verification is performed.
        
        Returns
        -------
        str
            HTTP method of the API call, as transmitted by the API Gateway.
        
        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``httpMethod`` key is present in the event data.

    `payload(self) ‑> Dict[str, Any]`
    :   Returns the data sent as the body of the API call.
        
        Data is expected to be valid JSON.
        
        Returns
        -------
        dict
            HTTP method of the API call, as transmitted by the API Gateway.
        
        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``body`` key is present in the event data.    
        MalformedPayloadError
            If the data is not valid JSON.

    `query_string_parameters(self) ‑> Dict[str, str]`
    :   Returns all URL parameters of the API call.
        
        Values of these parameters are returned as transmitted by AWS API Gateway.
        An empty ``dict'' is returned if no parameters were submitted by the caller.
        
        Returns
        -------
        dict
            Keys are parameter names as ``str``, values are corresponding raw values as ``str``.
        
        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``queryStringParameters`` key is present in the event data. No parameters is supposed to be represented as ``'queryStringParameters': None``.

`MalformedPayloadError(msg)`
:   Error raised in case of malformed input payload.

    ### Ancestors (in MRO)

    * builtins.RuntimeError
    * builtins.Exception
    * builtins.BaseException