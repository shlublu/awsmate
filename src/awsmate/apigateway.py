import typing

from awsmate.errors import AwsEventSpecificationError
from awsmate.lambdafunction import LambdaEvent


class MalformedPayloadError(RuntimeError):
    def __init__(self, msg):
        super().__init__(msg)
        

class LambdaProxyEvent(LambdaEvent):
    def __init__(self, eventObject: dict):
        super().__init__(eventObject)


    def http_headers(self) -> typing.Dict[str, str]:
        try: 
            headers = self._event["headers"]

        except KeyError as err:
            raise AwsEventSpecificationError("Event structure is not as expected: cannot reach " + str(err) + ".")

        return {} if headers is None else { k.lower(): v for k, v in headers.items() }


    def header_sorted_preferences(self, header: str) -> typing.Tuple[str, ...]:
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
        try: 
            method = self._event["httpMethod"]

        except KeyError as err:
            raise AwsEventSpecificationError("Event structure is not as expected: cannot reach " + str(err) + ".")

        return str(method).upper()

    
    def call_path(self) -> typing.Tuple[str, ...]:
        try: 
            path = self._event["path"].split('/')
            path = path[1 if not len(path[0]) else 0 : -1 if len(path[-1]) == 0 else len(path)]

        except KeyError as err:
            raise AwsEventSpecificationError("Event structure is not as expected: cannot reach " + str(err) + ".")

        return tuple(path)


    def query_string_parameters(self) -> typing.Dict[str, str]:
        try:
            params = self._event["queryStringParameters"]

        except KeyError as err:
            raise AwsEventSpecificationError("Event structure is not as expected: cannot reach " + str(err) + ".")

        return params or {}


    def call_string(self) -> str:
        paramsString = '&'.join(f'{key}={value}' for key, value in self.query_string_parameters().items())

        return f'{self.http_method()} /{"/".join(self.call_path())}{"?" if len(paramsString) else ""}{paramsString}'


    def payload(self) -> typing.Dict[str, typing.Any]:
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

