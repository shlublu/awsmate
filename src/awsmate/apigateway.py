import typing

from awsmate.lambdafunction import LambdaEvent, AwsEventSpecificationError


class MalformedPayloadError(RuntimeError):
    """
    Error raised in case of malformed input payload.

    """

    def __init__(self, msg):
        super().__init__(msg)
        

class LambdaProxyEvent(LambdaEvent):
    """
    Mapping of the input event received by an AWS Lambda function triggered by an AWS Api Gateway during a client API call.

    ...

    Methods
    -------
    http_headers()
        Returns all HTTP headers of the API call.
    header_sorted_preferences(header)
        Returns all values assigned to the given header, sorted by decreasing preferences.
    http_method()
        Returns the HTTP method of the API call.
    call_path()
        Returns the path of the API call, broken down into elements.
    query_string_parameters()
        Returns all URL parameters of the API call.
    call_string()
        Convenience method that returns the HTTP method of the call followed by the path and the URL parameters of the call.
    payload()
        Returns the data sent as the body of the API call.

    Examples
    --------
    def lambda_handler(rawEvent, context):
        import awsmate.apigateway as ag
        event = ag.LambdaProxyEvent(rawEvent)    

    """

    def __init__(self, eventObject: dict):
        """
        Parameters
        ----------
        eventObject : dict
            The parameter ``event`` received by the AWS Lambda function handler.
        """
        
        super().__init__(eventObject)


    def http_headers(self) -> typing.Dict[str, str]:
        """
        Returns all HTTP headers of the API call.

        Values of these headers are returned unparsed, as submitted.

        Returns
        -------
        dict
            Keys are header names as ``str``, values are corresponding raw values as ``str``.
            
        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``headers`` key is present in the event data.
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
        An empty ``tuple'' is returned if the given header is not found among those submitted by the caller.

        Returns
        -------
        tuple
            Header values as ``str``, in decreasing preference order.
            
        Examples
        --------
        Header ``Encoding: gzip;q=0.2,deflate,identity;q=0.9`` leads to ``('deflate', 'identity', 'gzip')``
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
            HTTP method of the API call, as transmitted by the API Gateway.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``httpMethod`` key is present in the event data.            
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
        API call ``GET /projects/foobar/modules`` leads to ``('projects', 'foobar', 'modules')``                  
        """
        
        try: 
            path = self._event["path"].split('/')
            path = path[1 if not len(path[0]) else 0 : -1 if len(path[-1]) == 0 else len(path)]

        except KeyError as err:
            raise AwsEventSpecificationError("Event structure is not as expected: cannot reach " + str(err) + ".")

        return tuple(path)


    def query_string_parameters(self) -> typing.Dict[str, str]:
        """
        Returns all URL parameters of the API call.

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
        ``GET /projects/foobar/modules?order=alphabetical&released=true``                
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
            HTTP method of the API call, as transmitted by the API Gateway.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``body`` key is present in the event data.    
        MalformedPayloadError
            If the data is not valid JSON.        
        """
        import json

        try:
            ret = json.loads(self._event['body'])
    
        except KeyError as err:
            raise AwsEventSpecificationError("Event structure is not as expected: cannot reach " + str(err) + ".")
    
        except (TypeError, json.JSONDecodeError) as err:
            raise MalformedPayloadError("Payload is malformed. JSON cannot be decoded: " + str(err) + ".")

        return ret



class HttpClientError(RuntimeError):
    def __init__(self, status: int, msg: str):
        import re

        from awsmate.logger import logger

        super().__init__(msg)

        self._status = status
        matched = re.match(r".*'.*\.(.*)'.*", str(self.__class__))

        logger.error(f'{"" if matched is None else matched.group(1)}: {str(status)} - {str(msg)}')


    @property
    def status(self):
        return self._status


class HttpBadRequestError(HttpClientError):
    def __init__(self, msg: str):
        super().__init__(400, msg)


class HttpUnauthorizedError(HttpClientError):
    def __init__(self, msg: str):
        super().__init__(403, msg)


class HttpNotFoundError(HttpClientError):
    def __init__(self, msg: str):
        super().__init__(404, msg)


class HttpNotAcceptableError(HttpClientError):
    def __init__(self, msg: str):
        super().__init__(406, msg)
        

class HttpConflictError(HttpClientError):
    def __init__(self, msg: str):
        super().__init__(409, msg)    


def json_transformer(payload: dict) -> typing.Tuple[str, str]:
    import json
       
    return json.dumps(payload, indent = 2), 'application/json; charset=utf-8'


def simple_message(message: str) -> typing.Dict[str, str]:
    return {
         "Message": message
    }


def determine_content_type(event: LambdaProxyEvent, *, customTransformers: typing.Optional[dict] = None) -> str:
    acceptedMimeTypes = event.header_sorted_preferences('Accept')

    if len(acceptedMimeTypes) == 0:
        acceptedMimeTypes = ( '*/*', None )

    contentType = None

    if customTransformers is None:
        customTransformers = {}
        
    for pref in acceptedMimeTypes:
        if pref in _basic_transformers or pref in customTransformers:
            contentType = pref
            break

    if contentType is None:
        availableFormats = ', '.join(
            ( k for k in sorted(set(list(_basic_transformers.keys()) + list(customTransformers.keys()))) if not k.endswith('*') )
        )

        raise HttpNotAcceptableError(
            f"None of the formats specified in the Accept header are available. Available formats are: {availableFormats}."
        )

    return contentType


def is_binary(contentType: str) -> bool:
    splitted = contentType.split('/')

    if len(splitted) == 1:
        splitted.append('*')

    mainType = splitted[0]
    subType = splitted[1].split(';')[0]

    return (
        mainType not in ('text', 'application') or (mainType == 'application' and subType not in ('json', 'xml'))
    )


_basic_transformers = {
    '*/*': json_transformer,
    'application/*': json_transformer,
    'application/json': json_transformer
}


def build_http_response(
        status: int, payload: typing.Union[dict, str], *, 
        event: typing.Optional[LambdaProxyEvent] = None, 
        customTransformers: typing.Optional[typing.Dict[str, typing.Callable[[dict], typing.Tuple[str, str]]]] = None,
        extraHeaders: typing.Optional[typing.Dict[str, str]] = None
    ) -> dict:
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

        if customTransformers is not None:
            contentTypeTransformers = {
                **contentTypeTransformers,
                **customTransformers
            }

        try:
            selectedMimeType = determine_content_type(event, customTransformers = customTransformers)
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
            **(extraHeaders if extraHeaders else {})
        }
    }

    if useGzip:
        ret['headers']['Content-Encoding'] = 'gzip'

    return ret


def build_http_server_error_response(message: typing.Optional[str] = None) -> None:
    return build_http_response(500, message if message else "Sorry, an error occured. Please contact the API administrator to have this sorted out.")


def build_http_client_error_response(error: HttpClientError) -> None:
    return build_http_response(error.status, str(error))

