import json
import typing

from awsmate.lambdafunction import LambdaEvent, AwsEventSpecificationError


class MalformedPayloadError(RuntimeError):
    """
    Error raised by :class:`~LambdaProxyEvent` in case of malformed input payload.
    """

    def __init__(self, msg: str):
        """
        Parameters
        ----------
        msg : str
            The explanatory message.
        """
        
        super().__init__(msg)
        

class LambdaProxyEvent(LambdaEvent):
    """
    Mapping of the input event received by an AWS Lambda function triggered by an AWS Api Gateway during a client API call.
    """

    def __init__(self, eventObject: dict):
        """
        Parameters
        ----------
        eventObject : dict
            The parameter ``event`` received by the AWS Lambda function handler.

        Examples
        --------
        >>> def lambda_handler(rawEvent, context):
        >>>     from awsmate.apigateway import LambdaProxyEvent
        >>>     event = LambdaProxyEvent(rawEvent)                
        """
        
        super().__init__(eventObject)


    def http_headers(self) -> typing.Dict[str, str]:
        """
        Returns all HTTP headers of the API call.

        Values of these headers are returned unparsed, as submitted.

        Returns
        -------
        dict
            Keys: header names as ``str``. Values: corresponding raw values as ``str``.
            
        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``headers`` key is present in the event data.

        Examples
        --------
        >>> event.http_headers()
        {'accept': 'application/json', 'accept-encoding': 'gzip,identity'}                
        """
        
        try: 
            headers = self._event["headers"]

        except KeyError as err:
            raise AwsEventSpecificationError("Event structure is not as expected: cannot reach " + str(err) + ".")

        return {} if headers is None else { k.lower(): v for k, v in headers.items() }


    def header_sorted_preferences(self, header: str) -> typing.Tuple[str, ...]:
        """
        Returns all values assigned to the given header, sorted by decreasing preferences.

        Preferences are determined according to the weighted quality value syntax.
        An empty ``tuple`` is returned if the given header is not found among those submitted by the caller.

        Returns
        -------
        tuple
            Header values as ``str``, in decreasing preference order.
            
        Examples
        --------
        Given the header ``Accept-Encoding: gzip;q=0.2,deflate,identity;q=0.9``: 

        >>> event.header_sorted_preferences('Accept-Encoding')
        ('deflate', 'identity', 'gzip')
        """
        
        headers = self.http_headers()
        preferences = {}
        header = header.lower()

        if header in headers:
            for p in headers[header].split(','):
                prefDesc = p.replace(' ', '').split(';')

                if len(prefDesc[0]):
                    try:
                        qValue = 1.0 if len(prefDesc) == 1 else float(prefDesc[1].split('q=')[1])
                    except:
                        qValue = 0.5

                    preferences[prefDesc[0]] = qValue

        return tuple(sorted(preferences.keys(), key = lambda k: preferences[k], reverse = True))


    def http_method(self) -> str:
        """
        Returns the HTTP method of the API call.

        The method verb is returned as transmitted by AWS API Gateway. GET, PUT, POST, PATCH, DELETE are expected, but no verification is performed.

        Returns
        -------
        str
            HTTP method of the API call.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``httpMethod`` key is present in the event data.            

        Examples
        --------
        >>> event.http_method()
        'GET'
        """

        try: 
            method = self._event["httpMethod"]

        except KeyError as err:
            raise AwsEventSpecificationError("Event structure is not as expected: cannot reach " + str(err) + ".")

        return str(method).upper()

    
    def call_path(self) -> typing.Tuple[str, ...]:
        """
        Returns the path of the API call, broken down into elements.

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
        Given the API call ``GET /projects/foobar/modules``
         
        >>> event.call_path()
        ('projects', 'foobar', 'modules')              
        """
        
        try: 
            path = self._event["path"].split('/')
            path = path[1 if not len(path[0]) else 0 : -1 if len(path[-1]) == 0 else len(path)]

        except KeyError as err:
            raise AwsEventSpecificationError(f"Event structure is not as expected: cannot reach {str(err)}.")

        return tuple(path)


    def query_string_parameters(self) -> typing.Dict[str, str]:
        """
        Returns all URL parameters of the API call.

        Values of these parameters are returned as transmitted by AWS API Gateway.
        An empty ``dict`` is returned if no parameters were submitted by the caller.

        Returns
        -------
        dict
            Keys: parameter names as ``str``. Values: corresponding raw values as ``str``.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``queryStringParameters`` key is present in the event data. No parameters is supposed to be represented as ``'queryStringParameters': None``.       

        Examples
        --------
        Given the API call ``GET '/reports?from_date=2020-01-01&to_date=2023-03-01'``

        >>> event.query_string_parameters()
        {'from_date': '2020-01-01', 'to_date': '2023-03-01'}     
        """
        
        try:
            params = self._event["queryStringParameters"]

        except KeyError as err:
            raise AwsEventSpecificationError("Event structure is not as expected: cannot reach " + str(err) + ".")

        return params or {}


    def call_string(self) -> str:
        """
        Convenience method that returns the HTTP method of the call followed by the path and the URL parameters of the call.

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
        Given the API call ``curl -X GET 'https://api.example.com/billing/reports?from_date=2020-01-01&to_date=2023-03-01'``

        >>> event.call_string()
        'GET /billing/reports?from_date=2020-01-01&to_date=2023-03-01'                  
        """
        
        paramsString = '&'.join(f'{key}={value}' for key, value in self.query_string_parameters().items())

        return f'{self.http_method()} /{"/".join(self.call_path())}{"?" if len(paramsString) else ""}{paramsString}'


    def payload(self) -> typing.Dict[str, typing.Any]:
        """
        Returns the data sent as the body of the API call.

        Data is expected to be valid JSON.

        Returns
        -------
        dict
            Data sent as the body of the API call loaded as a ``dict``, ``None`` if body is null.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``body`` key is present in the event data.    
        MalformedPayloadError
            If the submitted data is not valid JSON.        

        Examples
        --------
        >>> event.payload()
        {'some_key': 5, 'some_other_key': [1, 2, 3, 4, 5]}            
        """

        try:
            body = self._event['body']
            ret = None if body is None else json.loads(body)
    
        except KeyError as err:
            raise AwsEventSpecificationError(f"Event structure is not as expected: cannot reach {str(err)}.")
    
        except (TypeError, json.JSONDecodeError) as err:
            raise MalformedPayloadError(f"Payload is malformed. JSON cannot be decoded: {str(err)}.")

        return ret


class HttpClientError(RuntimeError):
    """
    Error that represents a HTTP response status code that comes with a message.
    """

    def __init__(self, status: int, msg: str) -> None:
        """
        Parameters
        ----------
        status : int
            The HTTP response status code. This value is taken as-is, there is no validation routine.
        msg : str
            The explanatory message.

        Examples
        --------
        >>> from awsmate.apigateway import HttpClientError
        >>> raise HttpClientError(404, 'Not sure where it is!')
        HttpClientError: 404 - Not sure where it is!
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        awsmate.apigateway.HttpClientError: Not sure where it is!
        """
        
        import re

        from awsmate.logger import logger

        super().__init__(msg)

        self._status = status
        matched = re.match(r".*'.*\.(.*)'.*", str(self.__class__))

        logger.error(f'{"" if matched is None else matched.group(1)}: {str(status)} - {str(msg)}')


    @property
    def status(self) -> int:
        """
        Returns the HTTP response status code. 

        Returns
        -------
        int
            The HTTP response status code. 

        Examples
        --------
        Given ``e = HttpClientError(403, 'Forbidden')``

        >>> e.status
        403
        """
        
        return self._status


class HttpBadRequestError(HttpClientError):
    """
    Error that represents a HTTP response status 400 "Bad request".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpBadRequestError('This is a very very bad request')
        """
        
        super().__init__(400, msg if msg else 'Bad request')


class HttpUnauthorizedError(HttpClientError):
    """
    Error that represents a HTTP response status 403 "Unauthorized".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpUnauthorizedError('None shall pass')            
        """
        
        super().__init__(403, msg if msg else 'Unauthorized')


class HttpNotFoundError(HttpClientError):
    """
    Error that represents a HTTP response status 404 "Not found".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpUnauthorizedError('This stuff is nowhere to be found')                
        """
        
        super().__init__(404, msg if msg else 'Not found')


class HttpNotAcceptableError(HttpClientError):
    """
    Error that represents a HTTP response status 406 "Not acceptable".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpNotAcceptableError('No I won`t respond in audio/mp3')              
        """
        
        super().__init__(406, msg if msg else 'Not acceptable')
        

class HttpConflictError(HttpClientError):
    """
    Error that represents a HTTP response status 409 "Conflict".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpConflictError('Not the best idea ever')                          
        """
        
        super().__init__(409, msg if msg else 'Conflict')    


def simple_message(message: str) -> typing.Dict[str, str]:
    """
    Turns a ``str`` into a ``dict`` payload having "Message" as a key and the passed string as a value.

    :func:`build_http_response` uses this function to build response payloads from strings. 

    There is no need to call :func:`simple_message` directly normally, although it may not cause any harm.

    Parameters
    ----------
    message : str
        The string to turn into a message payload.    

    Returns
    -------
    dict
        Payload built from the message string.     

    Examples
    --------
    >>> simple_message("This is fine!")
    {'Message': 'This is fine!'}
    """

    return {
         "Message": message
    }


def determine_content_type(event: LambdaProxyEvent, *, custom_transformers: typing.Optional[typing.Dict[str, typing.Callable[[dict], typing.Tuple[str, str]]]] = None) -> str:
    """
    Determines the ``Content-Type`` of the response to be sent based on the ``Accept`` header of the request.

    ``application/json`` is the only ``Content-Type`` transformer available by default. It is mapped to the ``Accept`` values
    ``*/*``, ``application/*`` and ``application/json``. Any other ``Accept`` value leads to a :class:`HttpNotAcceptableError` unless
    ``custom_transformers`` map this ``Accept`` value to an appropriate transformer.

    Preferences are handled by :func:`LambdaProxyEvent.header_sorted_preferences`. Should no ``Accept`` header be given, ``*/*`` is assumed.

    Parameters
    ----------
    event : LambdaProxyEvent
        The API call event.    
    custom_transformers : dict
        Optional mapping of ``Content-Type``: ``dict`` to (content as ``Content-Type``, ``Content-Type`` with encoding as ``str``) transformer functions.

    Returns
    -------
    str
        The ``Content-Type`` of the response.     

    Raises
    ------
    HttpNotAcceptableError
        If no transformer meets the criteria of the ``Accept`` header.
            
    Examples
    --------
    Given an API call that was made with a ``Accept: */*`` header, with no custom format handled by the application:

    >>> determine_content_type(event)
    'application/json'

    Given an API call that was made with a ``Accept: text/csv`` header, with an application handling ``text/csv`` and 
    ``application/xml`` on top of the default ``application/json``:

    >>> def csv_transformer(payload: dict) -> typing.Tuple[str, str]:
    >>>     # ... code that converts the json payload to csv and stores it into a variable called csvContent ...
    >>>     return csvContent, 'text/csv; charset=utf-8'
    >>>    
    >>> def xml_transformer(payload: dict) -> typing.Tuple[str, str]:
    >>>     # ... code that converts the json payload to xml and stores it into a variable called xmlContent ...
    >>>     return xmlContent, 'application/xml; charset=utf-8'
    >>> 
    >>> custom_transformers = {
    >>>     'text/csv': csv_transformer,
    >>>     'application/xml': xml_transformer
    >>> }
    >>>
    >>> determine_content_type(event, custom_transformers=custom_transformers)
    'text/csv'

    Notes
    -----
    It is a good idea to call this function at the very beginning of your Lambda handler. That way, you can make sure that
    the accepted ``Content-Type`` matches what your API is capable of returning, and return an :class:`~HttpNotAcceptableError` 
    response without doing any unnecessary processing otherwise.
    """

    acceptedMimeTypes = event.header_sorted_preferences('Accept')

    if len(acceptedMimeTypes) == 0:
        acceptedMimeTypes = ( '*/*', None )

    contentType = None

    if custom_transformers is None:
        custom_transformers = {}
        
    for pref in acceptedMimeTypes:
        if pref in _basic_transformers or pref in custom_transformers:
            contentType = pref
            break

    if contentType is None:
        availableFormats = ', '.join(
            ( k for k in sorted(set(list(_basic_transformers.keys()) + list(custom_transformers.keys()))) if not k.endswith('*') )
        )

        raise HttpNotAcceptableError(
            f"None of the formats specified in the Accept header are available. Available formats are: {availableFormats}."
        )

    return contentType


def is_binary(content_type: str) -> bool:
    """
    Determines whether the given ``Content-Type`` is binary. 

    :func:`build_http_response` uses this function to determine if the API Gateway requires a ``base64`` encoding prior returning the content. 
    All types but ``text/*``, ``application/xml`` and ``application/json`` are considered binary. 

    There is no need to call :func:`is_binary` directly normally, although it may not cause any harm.    

    Parameters
    ----------
    content_type : str
        The ``Content-Type`` to assess.    

    Returns
    -------
    bool
        Whether the ``Content-Type`` is binary.     
        
    Examples
    --------
    >>> is_binary('image/jpeg')
    True
    """
     
    splitted = content_type.split('/')

    if len(splitted) == 1:
        splitted.append('*')

    mainType = splitted[0]
    subType = splitted[1].split(';')[0]

    return (
        mainType not in ('text', 'application') or (mainType == 'application' and subType not in ('json', 'xml'))
    )


def json_transformer(payload: dict) -> typing.Tuple[str, str]:
    """
    Determines whether the given ``Content-Type`` is binary. 

    :func:`build_http_response` uses this function to determine if the API Gateway requires a ``base64`` encoding prior returning the content. 
    All types but ``text/*``, ``application/xml`` and ``application/json`` are considered binary. 

    There is no need to call :func:`is_binary` directly normally, although it may not cause any harm.    

    Parameters
    ----------
    content_type : str
        The ``Content-Type`` to assess.    

    Returns
    -------
    bool
        Whether the ``Content-Type`` is binary.     
        
    Examples
    --------
    >>> is_binary('image/jpeg')
    True
    """
    
    return json.dumps(payload, indent = 2), 'application/json; charset=utf-8'


_basic_transformers = {
    '*/*': json_transformer,
    'application/*': json_transformer,
    'application/json': json_transformer
}


def build_http_response(
        status: int, 
        payload: typing.Union[dict, str], *, 
        event: typing.Optional[LambdaProxyEvent] = None, 
        custom_transformers: typing.Optional[typing.Dict[str, typing.Callable[[dict], typing.Tuple[str, str]]]] = None,
        extra_headers: typing.Optional[typing.Dict[str, str]] = None
    ) -> dict:
    """
    Determines whether the given ``Content-Type`` is binary. 

    :func:`build_http_response` uses this function to determine if the API Gateway requires a ``base64`` encoding prior returning the content. 
    All types but ``text/*``, ``application/xml`` and ``application/json`` are considered binary. 

    There is no need to call :func:`is_binary` directly normally, although it may not cause any harm.    

    Parameters
    ----------
    content_type : str
        The ``Content-Type`` to assess.    

    Returns
    -------
    bool
        Whether the ``Content-Type`` is binary.     
        
    Examples
    --------
    >>> is_binary('image/jpeg')
    True
    """

    import base64
    import gzip

    if isinstance(payload, str):
        payload = simple_message(payload)

    useGzip = False
    contentTypeTransformers = _basic_transformers

    if event:
        for pref in event.header_sorted_preferences('Accept-Encoding'):
            if pref == 'gzip':
                useGzip = True
                break
            elif pref == 'identity':
                break

        if custom_transformers is not None:
            contentTypeTransformers = {
                **contentTypeTransformers,
                **custom_transformers
            }

        try:
            selectedMimeType = determine_content_type(event, custom_transformers = custom_transformers)
            stringifiedPayload, contentType = contentTypeTransformers[selectedMimeType](payload)

        except HttpNotAcceptableError as err:
            status = err.status
            useGzip = False

            stringifiedPayload, contentType = contentTypeTransformers['*/*'](
                simple_message(str(err))
            )

    else:
        stringifiedPayload, contentType = contentTypeTransformers['*/*'](payload)

    ret = {
        'isBase64Encoded': useGzip or is_binary(contentType),
        'statusCode': status,
        'body': stringifiedPayload if not useGzip else base64.b64encode(gzip.compress(stringifiedPayload.encode('utf-8'))).decode('utf-8'),
        'headers': {     
            'Content-Type': contentType,
            **(extra_headers if extra_headers else {})
        }
    }

    if useGzip:
        ret['headers']['Content-Encoding'] = 'gzip'

    return ret


def build_http_server_error_response(message: typing.Optional[str] = None, extra_headers: typing.Optional[typing.Dict[str, str]] = None) -> dict:
    """
    Determines whether the given ``Content-Type`` is binary. 

    :func:`build_http_response` uses this function to determine if the API Gateway requires a ``base64`` encoding prior returning the content. 
    All types but ``text/*``, ``application/xml`` and ``application/json`` are considered binary. 

    There is no need to call :func:`is_binary` directly normally, although it may not cause any harm.    

    Parameters
    ----------
    content_type : str
        The ``Content-Type`` to assess.    

    Returns
    -------
    bool
        Whether the ``Content-Type`` is binary.     
        
    Examples
    --------
    >>> is_binary('image/jpeg')
    True
    """
    
    return build_http_response(
        500, 
        message if message else "Sorry, an error occured. Please contact the API administrator to have this sorted out.",
        extra_headers=extra_headers
    )


def build_http_client_error_response(error: HttpClientError, extra_headers: typing.Optional[typing.Dict[str, str]] = None) -> dict:
    """
    Determines whether the given ``Content-Type`` is binary. 

    :func:`build_http_response` uses this function to determine if the API Gateway requires a ``base64`` encoding prior returning the content. 
    All types but ``text/*``, ``application/xml`` and ``application/json`` are considered binary. 

    There is no need to call :func:`is_binary` directly normally, although it may not cause any harm.    

    Parameters
    ----------
    content_type : str
        The ``Content-Type`` to assess.    

    Returns
    -------
    bool
        Whether the ``Content-Type`` is binary.     
        
    Examples
    --------
    >>> is_binary('image/jpeg')
    True
    """

    return build_http_response(
        error.status, 
        str(error),
        extra_headers=extra_headers
    )
