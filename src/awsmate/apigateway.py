import base64
import gzip
import ipaddress
import json
import re
import typing

from http import HTTPStatus

from awsmate.logger import logger, log_internal_error
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
            Explanatory message.
        """
        
        super().__init__(msg)
        

class LambdaProxyEvent(LambdaEvent):
    """
    Mapping of the input event received by an AWS Lambda function triggered by AWS API Gateway and integrated 
    in `AWS_PROXY <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-set-up-simple-proxy.html>`_ mode.
    """

    def __init__(self, event_object: dict) -> None:
        """
        Parameters
        ----------
        event_object : dict
            The parameter ``event`` received by the AWS Lambda function handler.

        Raises
        ------
        TypeError
            If ``event_object`` is not a ``dict``.  
                    
        Examples
        --------
        >>> def lambda_handler(raw_event, context):
        >>>     from awsmate.apigateway import LambdaProxyEvent
        >>>     event = LambdaProxyEvent(raw_event)                
        """
        
        super().__init__(event_object)


    def source_ip(self) -> typing.Union[ipaddress.IPv4Address, ipaddress.IPv6Address]:
        """
        Returns the source IP address of the API call.

        Returns
        -------
        ipaddress.IPv4Address or ipaddress.IPv6Address
            The IP address the API call comes from.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``requestContext.identity.sourceIp`` key is present in the event data or if the IP address is invalid.            

        Examples
        --------
        >>> event.source_ip()
        IPv4Address('93.184.216.34')
        """

        try: 
            sourceIp = ipaddress.ip_address(self._event["requestContext"]["identity"]["sourceIp"])

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        except ValueError as err:
            raise AwsEventSpecificationError(f'Invalid IP address: {err}')

        return sourceIp      
        
    
    def http_headers(self) -> typing.Dict[str, str]:
        """
        Returns all HTTP headers of the API call.

        Header names are always returned in lower case. Values of these headers are returned unparsed, as submitted.

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
            LambdaEvent._raiseCannotReachError(str(err))

        return {} if headers is None else { k.lower(): v for k, v in headers.items() }


    def http_method(self) -> str:
        """
        Returns the HTTP method of the API call.

        The method verb is always returned in upper case. GET, PUT, POST, PATCH, DELETE are expected, but no verification is performed.

        Returns
        -------
        str
            HTTP method of the API call.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``requestContext.httpMethod`` key is present in the event data.            

        Examples
        --------
        >>> event.http_method()
        'GET'
        """

        try: 
            method = self._event["requestContext"]["httpMethod"]

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return method.upper()
    

    def http_protocol(self) -> str:
        """
        Returns the HTTP protocol of the API call.

        The protocol is always returned in upper case.

        Returns
        -------
        str
            HTTP protocol of the API call.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``requestContext.protocol`` key is present in the event data.            

        Examples
        --------
        >>> event.http_protocol()
        'HTTP/1.1'
        """

        try: 
            protocol = self._event["requestContext"]["protocol"]

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return protocol.upper()    
    

    def http_user_agent(self) -> str:
        """
        Returns the HTTP user-agent of the API call.

        The user-agent is returned as transmitted by AWS API Gateway.

        Returns
        -------
        str
            HTTP user-agent of the API call.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``requestContext.identity.userAgent`` key is present in the event data.            

        Examples
        --------
        >>> event.http_user_agent()
        'curl/7.83.1'
        """

        try: 
            userAgent = self._event["requestContext"]["identity"]["userAgent"]

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return userAgent        
    

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


    def query_domain_name(self) -> str:
        """
        Returns the domain name of the API call.

        The domain name is always returned in lower case.

        Returns
        -------
        str
            Domain name of the API call.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``requestContext.domainName`` key is present in the event data.            

        Examples
        --------
        >>> event.query_domain_name()
        'example.com'
        """

        try: 
            domainName = self._event["requestContext"]["domainName"]

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

        return domainName.lower()   
        
        
    def query_path(self) -> typing.Tuple[str, ...]:
        """
        Returns the path of the API call, broken down into elements.

        Returns
        -------
        tuple
            Path elements as ``str``.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``requestContext.path`` key is present in the event data.      

        Examples
        --------
        Given the API call ``GET /projects/foobar/modules``
         
        >>> event.query_path()
        ('projects', 'foobar', 'modules')              
        """
        
        try: 
            path = self._event["requestContext"]["path"].split('/')
            path = path[1 if not len(path[0]) else 0 : -1 if len(path[-1]) == 0 else len(path)]

        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))

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
            LambdaEvent._raiseCannotReachError(str(err))

        return params or {}


    def query_string(self) -> str:
        """
        Convenience function that returns the HTTP method of the call followed by the URL of the call.

        Returns
        -------
        str
            The query string of the API call, including URL parameters if any.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If at least one of the ``httpMethod``, ``query_domain``, ``query_path`` or ``query_string_parameters`` keys is not present in the event data.     

        Examples
        --------
        Given the API call ``curl -X GET 'https://api.example.com/billing/reports?from_date=2020-01-01&to_date=2023-03-01'``

        >>> event.query_string()
        'GET https://api.example.com/billing/reports?from_date=2020-01-01&to_date=2023-03-01'                  
        """
        
        paramsString = '&'.join(f'{key}={value}' for key, value in self.query_string_parameters().items())

        return f'{self.http_method()} https://{self.query_domain_name()}/{"/".join(self.query_path())}{"?" if len(paramsString) else ""}{paramsString}'


    def query_payload(self) -> typing.Dict[str, typing.Any]:
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
        >>> event.query_payload()
        {'some_key': 5, 'some_other_key': [1, 2, 3, 4, 5]}            
        """

        try:
            body = self._event['body']
            ret = None if body is None else json.loads(body)
    
        except KeyError as err:
            LambdaEvent._raiseCannotReachError(str(err))
    
        except (TypeError, json.JSONDecodeError) as err:
            raise MalformedPayloadError(f"Payload is malformed. JSON cannot be decoded: {str(err)}.")

        return ret
    

    def authorizer_claims(self) -> typing.Optional[typing.Dict[str, typing.Any]]:
        """
        Returns the authenticated user details or ``None`` if this is an anonymous API call.

        Returns
        -------
        dict
            User details or ``None`` if this call is anonymous.

        Raises
        ------
        awsmate.lambdafunction.AwsEventSpecificationError
            If no ``requestContext`` key is present in the event data, or if claims is not ``None`` and not a ``dict``.  

        Examples
        --------
        >>> event.authorizer_claims()
        {'cognito:username': '192837645', 'email': 'jane@example.com', 'given_name': 'Jane', 'family_name': 'Doe'}
        """

        try:
            claims = self._event['requestContext']['authorizer']['claims']
    
        except KeyError as err:
            if str(err) == "'requestContext'":
                LambdaEvent._raiseCannotReachError(str(err))
            else:
                claims = None

        if claims and not isinstance(claims, dict):
            raise AwsEventSpecificationError(f"Claims should be a dict, not a {type(claims)}.")

        return claims
    

class HttpError(RuntimeError):
    """
    HTTP error response: status code and message.

    Examples
    --------
    >>> raise HttpError(404, 'Not Found')    
    """

    def __init__(self, status: int, msg: str) -> None:
        """
        Parameters
        ----------
        status : int
            The HTTP response status code. This value is taken as-is, there is no validation routine.
        msg : str
            The explanatory message.
        """

        super().__init__(msg)

        self._status = status


    @property
    def status(self) -> int:
        """
        int : HTTP response status code. 

        Examples
        --------
        Given ``e = HttpError(403, 'Forbidden')``

        >>> e.status
        403
        """
        
        return self._status


class HttpClientError(HttpError):
    """
    Client HTTP error response.

    Examples
    --------
    >>> raise HttpClientError(404, 'Not Found')    
    """
    pass


class HttpServerError(HttpError):
    """
    Server-side HTTP error response.

    Examples
    --------
    >>> raise HttpServerError(503, 'Service Unavailable')    
    """
    pass


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
        >>> raise HttpBadRequestError()  
        """
        
        httpStatus = HTTPStatus.BAD_REQUEST
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)


class HttpUnauthorizedError(HttpClientError):
    """
    Error that represents a HTTP response status 401 "Unauthorized".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpUnauthorizedError()  
        """
        
        httpStatus = HTTPStatus.UNAUTHORIZED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)


class HttpPaymentRequiredError(HttpClientError):
    """
    Error that represents a HTTP response status 402 "Payment required".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpPaymentRequiredError()       
        """
        
        httpStatus = HTTPStatus.PAYMENT_REQUIRED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)        


class HttpForbiddenError(HttpClientError):
    """
    Error that represents a HTTP response status 403 "Forbidden".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpForbiddenError()             
        """
        
        httpStatus = HTTPStatus.FORBIDDEN
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)         


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
        >>> raise HttpNotFoundError()             
        """
        
        httpStatus = HTTPStatus.NOT_FOUND
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpMethodNotAllowedError(HttpClientError):
    """
    Error that represents a HTTP response status 405 "Method not allowed".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpMethodNotAllowedError()                
        """
        
        httpStatus = HTTPStatus.METHOD_NOT_ALLOWED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)          


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
        >>> raise HttpNotAcceptableError()            
        """
        
        httpStatus = HTTPStatus.NOT_ACCEPTABLE
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  
        

class HttpProxyAuthenticationRequiredError(HttpClientError):
    """
    Error that represents a HTTP response status 407 "Proxy authentication required".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpProxyAuthenticationRequiredError()                
        """
        
        httpStatus = HTTPStatus.PROXY_AUTHENTICATION_REQUIRED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpRequestTimeoutError(HttpClientError):
    """
    Error that represents a HTTP response status 408 "Request timeout".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpRequestTimeoutError()            
        """
        
        httpStatus = HTTPStatus.REQUEST_TIMEOUT
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)          
        
        
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
        >>> raise HttpConflictError()                          
        """
        
        httpStatus = HTTPStatus.CONFLICT
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)    


class HttpGoneError(HttpClientError):
    """
    Error that represents a HTTP response status 410 "Gone".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpGoneError()                          
        """
        
        httpStatus = HTTPStatus.GONE
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)            


class HttpLengthRequiredError(HttpClientError):
    """
    Error that represents a HTTP response status 411 "Length required".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpLengthRequiredError()                     
        """
        
        httpStatus = HTTPStatus.LENGTH_REQUIRED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)   


class HttpPreconditionFailedError(HttpClientError):
    """
    Error that represents a HTTP response status 412 "Precondition failed".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpPreconditionFailedError()                           
        """
        
        httpStatus = HTTPStatus.PRECONDITION_FAILED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           


class HttpRequestEntityTooLargeError(HttpClientError):
    """
    Error that represents a HTTP response status 413 "Request entity too large".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpRequestEntityTooLargeError()                          
        """
        
        httpStatus = HTTPStatus.REQUEST_ENTITY_TOO_LARGE
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpRequestUriTooLongError(HttpClientError):
    """
    Error that represents a HTTP response status 414 "Request URI too long".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpRequestUriTooLongError()                       
        """
        
        httpStatus = HTTPStatus.REQUEST_URI_TOO_LONG
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpUnsupportedMediaTypeError(HttpClientError):
    """
    Error that represents a HTTP response status 415 "Unsupported media type".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpUnsupportedMediaTypeError()                        
        """
        
        httpStatus = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpRequestRangeNotSatisfiableError(HttpClientError):
    """
    Error that represents a HTTP response status 416 "Request range not satisfiable".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpRequestRangeNotSatisfiableError()                          
        """
        
        httpStatus = HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpExpectationFailedError(HttpClientError):
    """
    Error that represents a HTTP response status 417 "Expectation failed".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpExpectationFailedError()                         
        """
        
        httpStatus = HTTPStatus.EXPECTATION_FAILED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpMisdirectedRequestError(HttpClientError):
    """
    Error that represents a HTTP response status 421 "Misdirected request".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpMisdirectedRequestError()                        
        """
        
        httpStatus = HTTPStatus.MISDIRECTED_REQUEST
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpUnprocessableEntityError(HttpClientError):
    """
    Error that represents a HTTP response status 422 "Unprocessable entity".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpUnprocessableEntityError()                         
        """
        
        httpStatus = HTTPStatus.UNPROCESSABLE_ENTITY
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpLockedError(HttpClientError):
    """
    Error that represents a HTTP response status 423 "Locked".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpLockedError()                        
        """
        
        httpStatus = HTTPStatus.LOCKED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpFailedDependencyError(HttpClientError):
    """
    Error that represents a HTTP response status 424 "Failed dependency".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpFailedDependencyError()                          
        """
        
        httpStatus = HTTPStatus.FAILED_DEPENDENCY
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpUpgradeRequiredError(HttpClientError):
    """
    Error that represents a HTTP response status 426 "Upgrade required".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpUpgradeRequiredError()                          
        """
        
        httpStatus = HTTPStatus.UPGRADE_REQUIRED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpPreconditionRequiredError(HttpClientError):
    """
    Error that represents a HTTP response status 428 "Precondition required".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpPreconditionRequiredError()                     
        """
        
        httpStatus = HTTPStatus.PRECONDITION_REQUIRED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpTooManyRequestsError(HttpClientError):
    """
    Error that represents a HTTP response status 429 "Too many requests".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpTooManyRequestsError()                        
        """
        
        httpStatus = HTTPStatus.TOO_MANY_REQUESTS
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           
        

class HttpRequestHeaderFieldsTooLargeError(HttpClientError):
    """
    Error that represents a HTTP response status 431 "Request header fields too large".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpRequestHeaderFieldsTooLargeError()               
        """
        
        httpStatus = HTTPStatus.REQUEST_HEADER_FIELDS_TOO_LARGE
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)           


class HttpInternalServerError(HttpServerError):
    """
    Error that represents a HTTP response status 500 "Internal server error".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpInternalServerError()               
        """
        
        httpStatus = HTTPStatus.INTERNAL_SERVER_ERROR
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)       


class HttpNotImplementedError(HttpServerError):
    """
    Error that represents a HTTP response status 501 "Not implemented".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpNotImplementedError()               
        """
        
        httpStatus = HTTPStatus.NOT_IMPLEMENTED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpBadGatewayError(HttpServerError):
    """
    Error that represents a HTTP response status 502 "Bad gateway".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpBadGatewayError()               
        """
        
        httpStatus = HTTPStatus.BAD_GATEWAY
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpRServiceUnavailableError(HttpServerError):
    """
    Error that represents a HTTP response status 503 "Service unavailable".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpRServiceUnavailableError()               
        """
        
        httpStatus = HTTPStatus.SERVICE_UNAVAILABLE
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpGatewayTimeoutError(HttpServerError):
    """
    Error that represents a HTTP response status 504 "GatewayTimeout".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpGatewayTimeoutError()               
        """
        
        httpStatus = HTTPStatus.GATEWAY_TIMEOUT
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpVersionNotSupportedError(HttpServerError):
    """
    Error that represents a HTTP response status 505 "HTTP version not supported".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpVersionNotSupportedError()               
        """
        
        httpStatus = HTTPStatus.HTTP_VERSION_NOT_SUPPORTED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpVarianteAlsoNegociatesError(HttpServerError):
    """
    Error that represents a HTTP response status 506 "Variant also negociates".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpVarianteAlsoNegociatesError()               
        """
        
        httpStatus = HTTPStatus.VARIANT_ALSO_NEGOTIATES
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpInsufficientStorageError(HttpServerError):
    """
    Error that represents a HTTP response status 507 "Insufficient storage".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpInsufficientStorageError()               
        """
        
        httpStatus = HTTPStatus.INSUFFICIENT_STORAGE
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpLoopDetectedError(HttpServerError):
    """
    Error that represents a HTTP response status 508 "Loop detected"".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpLoopDetectedError()               
        """
        
        httpStatus = HTTPStatus.LOOP_DETECTED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpNotExtendedError(HttpServerError):
    """
    Error that represents a HTTP response status 510 "Not extended".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpNotExtendedError()               
        """
        
        httpStatus = HTTPStatus.NOT_EXTENDED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)  


class HttpNetworkAuthenticationRequiredError(HttpServerError):
    """
    Error that represents a HTTP response status 511 "Network authentication required".
    """
    
    def __init__(self, msg: typing.Optional[str] = None):
        """
        Parameters
        ----------
        msg : str
            Explanatory message. A default message is used if omitted.

        Examples
        --------
        >>> raise HttpNetworkAuthenticationRequiredError()               
        """
        
        httpStatus = HTTPStatus.NETWORK_AUTHENTICATION_REQUIRED
        super().__init__(httpStatus.value, msg if msg else httpStatus.phrase)         
        

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
    ``*/*``, ``application/*`` and ``application/json``. Any other ``Accept`` value leads to a :exc:`HttpNotAcceptableError` unless
    ``custom_transformers`` map this ``Accept`` value to an appropriate transformer.

    Preferences are handled by :func:`LambdaProxyEvent.header_sorted_preferences`. Should no ``Accept`` header be given, ``*/*`` is assumed.

    Parameters
    ----------
    event : LambdaProxyEvent
        The API call event.    
    custom_transformers : dict
        Optional mapping of ``Content-Type`` to transformer functions returning (the content as ``Content-Type``, the ``Content-Type`` with encoding as ``str``).

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
    It is a good idea to call this function at the very beginning of your Lambda handler. This way you can make sure that
    the accepted ``Content-Type`` matches what your API is capable of returning, and return an :exc:`~HttpNotAcceptableError` 
    response without doing any unnecessary processing otherwise.

    The example below only accepts ``*/*``, ``application/*`` and ``application/json``, all mapped to ``application/json`` by default. 

    >>> def lambda_handler(raw_event, context):
    >>>     import awsmate.apigateway as amag
    >>>
    >>>     event = amag.LambdaProxyEvent(raw_event) 
    >>>
    >>>     try:
    >>>         amag.determine_content_type(event)
    >>>
    >>>         # Everything you need to do
    >>>
    >>>         return amag.build_http_response(200, "OK", event=event)
    >>>
    >>>     except amag.HttpClientError as err:
    >>>         return amag.build_http_client_error_response(err, event=event) # We will end up here should HttpNotAcceptableError be raised by determine_content_type()
    >>>     except Exception:
    >>>         return amag.build_http_server_error_response(amag.HttpInternalServerError(), event=event)
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
    Transformer used by :func:`build_http_response` to build ``application/json`` responses.

    There is no need to this function directly normally, although it may not cause any harm.    

    Parameters
    ----------
    payload : dict
        The payload to convert to ``application/json``.    

    Returns
    -------
    tuple
        The ``application/json`` payload as a ``str``, the ``Content-Type`` with its encoding specifier.      
        
    Examples
    --------
    >>> json_transformer({'TopThreeBibs': (751,25,372)})
    ('{\\n  "TopThreeBibs": [\\n    751,\\n    25,\\n    372\\n  ]\\n}', 'application/json; charset=utf-8')
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
    Builds the HTTP response the Lambda handler has to return to API Gateway.

    Should the ``Accept`` header of the API call lead to a :exc:`HttpNotAcceptableError`, an error message is returned instead
    of the passed payload and the status code is set accordingly. 
    
    This function handles the ``Accept-Encoding: gzip`` header of the API call for you. It also sets the base-64 flag of the response to ``True`` if
    the returned ``Content-Type`` is binary.

    Parameters
    ----------
    status : int
        The HTTP status code.  
    payload : dict or str
        The payload that constitutes the body of the response. Should it be a ``str``, it will first be transformed by :func:`simple_message`.
    event : LambdaProxyEvent
        Optional wrapper of the event the Lambda handler receives from the API Gateway.
    custom_transformers : dict
        Optional mapping of ``Content-Type`` to transformer functions returning (the content as ``Content-Type``, the ``Content-Type`` with encoding as ``str``).
    extra_headers : dict
        Optional extra headers to return. For example : ``{ 'Access-Control-Allow-Origin': '*' }`` to handle CORS.   

    Returns
    -------
    dict
        The HTTP response to return to API Gateway.     
      
    Examples
    --------
    >>> payload = { 
    >>>     'someKey': 'someVal' 
    >>> }
    >>>
    >>> event = None # Use defaults: no specific headers ('Accept: */*' assumed), no body, no URL parameters
    >>>
    >>> custom_transformers = None # 'application/json' transformer is built-in and is bound to 'Accept: */*'. We don't need anything else here.
    >>>
    >>> extra_headers = {
    >>>     'Access-Control-Allow-Origin': '*' # Deals with CORS provided HTTP OPTIONS is dealt with on API Gateway side.
    >>> }
    >>>
    >>> build_http_response(200, payload, event=event, custom_transformers=custom_transformers, extra_headers=extra_headers)
    {'isBase64Encoded': False, 'statusCode': 200, 'body': '{\\n  "someKey": "someVal"\\n}', 'headers': {'Content-Type': 'application/json; charset=utf-8', 'Access-Control-Allow-Origin': '*'}}

    See Also
    --------
    determine_content_type : more details on the use of the optional parameter ``custom_transformers``.
    """

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


def build_http_server_error_response(
        error: HttpServerError, *,
        client_message: typing.Optional[str] = None,
        log: bool = True,
        **kwargs: typing.Any
    ) -> dict:
    """
    Convenience function that builds an HTTP error 5XX response to be returned to API Gateway by the Lambda handler.

    Unless specified otherwise, calling this function logs a stack trace of the error showing the status and the actual error message. 
    This message is replaced by a client-oriented message in the HTTP response.

    Parameters
    ----------
    error : HttpServerError
        Object representing the error. 
    client_message : str
        Optional client-oriented message. An english canned message is used if omitted.
    log : bool
        Optional flag that defines whether a stack trace should be logged. ``True`` if omitted.
    **kwarg : any
        Optional arguments to pass to :func:`build_http_response`

    Returns
    -------
    dict
        The HTTP error 5XX response to return to API Gateway.        
      
    Examples
    --------
    >>> build_http_server_error_response(HttpInsufficientStorageError(), client_message='Sorry, we have an issue.')
    {'isBase64Encoded': False, 'statusCode': 507, 'body': '{\\n  "Message": "Sorry, we have an issue."\\n}', 'headers': {'Content-Type': 'application/json; charset=utf-8'}}

    Notes
    -----
    This function simply calls 
    
    >>> build_http_response(error.status, client_message, **kwargs)
        
    It is a good idea to make your Lambda handler to catch all unexpected errors to return a clean user-oriented error message should anything go wrong.

    >>> def lambda_handler(raw_event, context):
    >>>     import awsmate.apigateway as amag
    >>>
    >>>     event = amag.LambdaProxyEvent(raw_event) 
    >>>
    >>>     try:
    >>>         # Everything you need to do
    >>>
    >>>         return amag.build_http_response(200, "OK", event=event)
    >>>
    >>>     except amag.HttpClientError as err:
    >>>         return amag.build_http_client_error_response(err, event=event) 
    >>>     except Exception:
    >>>         # We will end up here should any unexpected error occur
    >>>         return amag.build_http_server_error_response(amag.HttpInternalServerError(), event=event) 
    """
    
    if log:
        log_internal_error(f'{error.status} - {error}')

    return build_http_response(
        error.status, 
        client_message if client_message else 'Sorry, an error occured. Please contact the API administrator to have this sorted out.',
        **kwargs
    )


def build_http_client_error_response(
        error: HttpClientError, *,
        log: bool = True,
        **kwargs: typing.Any
    ) -> dict:
    """
    Convenience function that builds an HTTP error 4XX response to be returned to API Gateway by the Lambda handler.

    Unless specified otherwise, calling this function logs an error showing the status and message. 

    Parameters
    ----------
    error : HttpClientError
        Object representing the error. 
    log : bool
        Optional flag that defines whether a stack trace should be logged. ``True`` if omitted.
    **kwarg : any
        Optional arguments to pass to :func:`build_http_response`

    Returns
    -------
    dict
        The HTTP error 4XX response to return to API Gateway.      

    Examples
    --------
    >>> build_http_client_error_response(HttpNotFoundError())
    {'isBase64Encoded': False, 'statusCode': 404, 'body': '{\\n  "Message": "Not Found"\\n}', 'headers': {'Content-Type': 'application/json; charset=utf-8'}}
    
    Notes
    -----
    This function simply calls 
    
    >>> build_http_response(error.status, str(error), **kwargs)

    It is a good idea to make your Lambda handler to catch all HttpClientError to return a clean error message should there be any problem with the request.

    >>> def lambda_handler(raw_event, context):
    >>>     import awsmate.apigateway as amag
    >>>
    >>>     event = amag.LambdaProxyEvent(raw_event) 
    >>>
    >>>     try:
    >>>         # Everything you need to do
    >>>
    >>>         return amag.build_http_response(200, "OK", event=event)
    >>>
    >>>     except amag.HttpClientError as err:
    >>>         return amag.build_http_client_error_response(err, event=event) # We will end up here should anything be wrong in the client's request
    >>>     except Exception:
    >>>         return amag.build_http_server_error_response(amag.HttpInternalServerError(), event=event) 
    """

    if log:
        logger.error(f'{error.status} - {error}')

    return build_http_response(
        error.status, 
        str(error),
        **kwargs
    )
