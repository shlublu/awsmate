import pytest

import awsmate.apigateway as ag

from awsmate.lambdafunction import AwsEventSpecificationError


def test_LambdaProxyEvent_init_initializesInternalEventObject():
    event = {}

    test = ag.LambdaProxyEvent(event)

    assert test._event is event


def test_LambdaProxyEvent_http_headers_returnsAllHeadersWithKeysInLowerCase():
    import random

    randStringA = str(random.randint(1000, 9999))
    randStringB = str(random.randint(1000, 9999))

    event = {
        'headers': { "A-a": randStringA, "b-B": randStringB }
    }

    test = ag.LambdaProxyEvent(event)

    assert test.http_headers() == { "a-a": randStringA, "b-b": randStringB }


def test_LambdaProxyEvent_http_headers_returnsAnEmptyDictIfNoHeadersArePassed():
    event = {
        'headers': None
    }

    test = ag.LambdaProxyEvent(event)

    assert test.http_headers() == {}


def test_LambdaProxyEvent_http_headers_raisesIfNoHeaderElementIsPresent():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.http_headers()

    assert exceptionInfo.value.args[0] == "Event structure is not as expected: cannot reach 'headers'."


def test_LambdaProxyEvent_header_sorted_preferences_returnsNonWeightedPreferencesAsPassed():
    event = { 
        "headers": { 'Encoding': 'gzip,deflate,other' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('encoding') == ('gzip', 'deflate', 'other')
    

def test_LambdaProxyEvent_header_sorted_preferences_consideresNoWeightMeansOne():
    event = { 
        "headers": { 'Encoding': 'gzip;q=0.4,deflate,other;q=0.6' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('encoding') == ('deflate', 'other', 'gzip')

    
def test_LambdaProxyEvent_header_sorted_preferences_returnsPreferencesAccordingToWeightsGivenSorted():
    event = { 
        "headers": { 'Encoding': 'gzip,deflate;q=0.8,other;q=0.1' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('encoding') == ('gzip', 'deflate', 'other')


def test_LambdaProxyEvent_header_sorted_preferences_returnsPreferencesAccordingToWeightsGivenUnsorted():
    event = { 
        "headers": { 'Encoding': 'gzip;q=0.2,deflate,other;q=0.9' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('encoding') == ('deflate', 'other', 'gzip')


def test_LambdaProxyEvent_header_sorted_preferences_considersBadlyFormattedWeightMeansHalf():
    event = { 
        "headers": { 'Encoding': 'gzip;q=0.4,deflate;q=0.6,other;garbage' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('encoding') == ('deflate', 'other', 'gzip')


def test_LambdaProxyEvent_header_sorted_preferences_silentelyIgnoresEmptyPreference():
    event = { 
        "headers": { 'Encoding': 'gzip;q=0.4,,;q=1,;garbage,deflate;q=0.6,other' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('encoding') == ('other', 'deflate', 'gzip')


def test_LambdaProxyEvent_header_sorted_preferences_silentelyIgnoreSpaces():
    event = { 
        "headers": { 'Encoding': 'gzip ; q = 0.6,deflate;q=0.4,other' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('encoding') == ('other', 'gzip', 'deflate')  


def test_LambdaProxyEvent_header_sorted_preferences_returnsNoPreferenceIfQueriedHeaderHasNotBeenPassed():
    event = { 
        "headers": { 'Encoding': 'gzip;q=0.2,deflate,other' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('NonPassedHeader') == ()


def test_LambdaProxyEvent_header_sorted_preferences_livesWellWithNoHeaders():
    event = { 
        "headers": {}
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('NonPassedHeader') == ()


def test_LambdaProxyEvent_header_sorted_preferences_isCaseUnsensitive():
    event = { 
        "headers": { 'Encoding': 'gzip;q=0.3,deflate;q=0.2,other' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('eNcOdInG') == ('other', 'gzip', 'deflate')  

     
def test_LambdaProxyEvent_http_method_returnsTheHttpMethodOfTheCallInUpperCase():
    event = {
        'httpMethod': 'PoSt'
    }

    test = ag.LambdaProxyEvent(event)

    assert  test.http_method() == 'POST'


def test_LambdaProxyEvent_http_method_raisesIfMethodFieldIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.http_method()

    assert exceptionInfo.value.args[0] == "Event structure is not as expected: cannot reach 'httpMethod'."


def test_LambdaProxyEvent_call_path_returnsPathElementsIgnoringTrailingSeparator():
    import random

    randPathA = f'{random.randint(1000, 9999)}FirstElement' 
    randPathB = f'{random.randint(1000, 9999)}SecondElement' 
    randPathC = f'{random.randint(1000, 9999)}ThirdElement' 

    event = {
        'path': f'/{randPathA}/{randPathB}/{randPathC}/'
    }

    test = ag.LambdaProxyEvent(event)

    assert test.call_path() == ( randPathA, randPathB, randPathC )


def test_LambdaProxyEvent_call_path_livesWellWithNoTrailingSeparator():
    import random

    randPathA = f'{random.randint(1000, 9999)}FirstElement' 
    randPathB = f'{random.randint(1000, 9999)}SecondElement' 
    randPathC = f'{random.randint(1000, 9999)}ThirdElement' 

    event = {
        'path': f'/{randPathA}/{randPathB}/{randPathC}'
    }

    test = ag.LambdaProxyEvent(event)

    assert test.call_path() == ( randPathA, randPathB, randPathC )


def test_LambdaProxyEvent_call_path_assumesLeadingSeparator():
    import random

    randPathA = f'{random.randint(1000, 9999)}FirstElement' 
    randPathB = f'{random.randint(1000, 9999)}SecondElement' 
    randPathC = f'{random.randint(1000, 9999)}ThirdElement' 

    event = {
        'path': f'{randPathA}/{randPathB}/{randPathC}/'
    }

    test = ag.LambdaProxyEvent(event)

    assert test.call_path() == ( randPathA, randPathB, randPathC )


def test_LambdaProxyEvent_call_path_assumesLeadingSeparatorEvenIfNoTrailingSeparator():
    import random

    randPathA = f'{random.randint(1000, 9999)}FirstElement' 
    randPathB = f'{random.randint(1000, 9999)}SecondElement' 
    randPathC = f'{random.randint(1000, 9999)}ThirdElement' 

    event = {
        'path': f'{randPathA}/{randPathB}/{randPathC}'
    }

    test = ag.LambdaProxyEvent(event)

    assert test.call_path() == ( randPathA, randPathB, randPathC )



def test_LambdaProxyEvent_call_path_raisesIfPathFieldIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.call_path()

    assert exceptionInfo.value.args[0] == "Event structure is not as expected: cannot reach 'path'."


def test_LambdaProxyEvent_query_string_parameters_returnsAllQueryStringParametersAsTheyAre():
    import random

    randParamsA = f'{random.randint(1000, 9999)} (Some Random Value)'
    randParamsB = f'{random.randint(1000, 9999)} (Some Other Random Value)'

    event = {
        'queryStringParameters': {
            'someQueryParameter': randParamsA,
            'someOtherQueryParameter': randParamsB
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert test.query_string_parameters() == event['queryStringParameters']


def test_LambdaProxyEvent_query_string_parameters_returnsAnEmptyDictIfNoQueryStringParametersArePassed():
    event = {
        'queryStringParameters': None
    }

    test = ag.LambdaProxyEvent(event)

    assert test.query_string_parameters() == {}


def test_LambdaProxyEvent_query_string_parameters_raisesIfParametersFieldIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.query_string_parameters()

    assert exceptionInfo.value.args[0] == "Event structure is not as expected: cannot reach 'queryStringParameters'."


def test_LambdaProxyEvent_call_string_returnsTheWholeString():
    import random

    randMethod = str(random.randint(1000, 9999))

    randPathA = str(random.randint(1000, 9999)) 
    randPathB = str(random.randint(1000, 9999)) 
    randPathC = str(random.randint(1000, 9999)) 

    randParamsA = str(random.randint(1000, 9999)) 
    randParamsB = str(random.randint(1000, 9999))  
    randParamsC = str(random.randint(1000, 9999))  

    path = f'/{randPathA}/{randPathB }/{randPathC}/'

    params = {
        'a': randParamsA,
        'b': randParamsB,
        'c': randParamsC
    }

    event = {
        'httpMethod': randMethod,
        'path': path,
        'queryStringParameters': params
    }

    test = ag.LambdaProxyEvent(event)
    expected = f'{randMethod} {path[0:-1]}?a={randParamsA}&b={randParamsB}&c={randParamsC}'

    assert test.call_string() == expected


def test_LambdaProxyEvent_call_string_livesWellWithNoQueryParameters():
    import random

    randMethod = str(random.randint(1000, 9999))

    randPathA = str(random.randint(1000, 9999)) 
    randPathB = str(random.randint(1000, 9999)) 
    randPathC = str(random.randint(1000, 9999)) 

    path = f'/{randPathA}/{randPathB }/{randPathC}/'

    event = {
        'httpMethod': randMethod,
        'path': path,
        'queryStringParameters': None
    }

    test = ag.LambdaProxyEvent(event)
    expected = f'{randMethod} {path[0:-1]}'

    assert test.call_string() == expected


def test_LambdaProxyEvent_call_string_reliesOnEventMethods():
    from unittest.mock import patch

    event = {
        'httpMethod': 'GET',
        'path': '/a/b/c/',
        'queryStringParameters': {
            'a': 'paramA',
            'b': 'paramB',
            'c': 'paramC'
        }
    }

    with patch.object(ag.LambdaProxyEvent, 'http_method', return_value=None) as acm:
        with patch.object(ag.LambdaProxyEvent, 'call_path', return_value = ()) as acp:
            with patch.object(ag.LambdaProxyEvent, 'query_string_parameters', return_value = {}) as acqp:
                ag.LambdaProxyEvent(event).call_string()

    acm.assert_called_once()
    acp.assert_called_once()
    acqp.assert_called_once()


def test_LambdaProxyEvent_payload_returnsThePayloadAsItIs():
    import random

    randInt = random.randint(1000, 100000)

    event = {
        "body": "{ \"key\": " + repr(randInt) + " }"
    }

    test = ag.LambdaProxyEvent(event)

    assert test.payload() == { 'key': randInt }


def test_LambdaProxyEvent_payload_raisesIfBodyIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.payload()

    assert exceptionInfo.value.args[0] == f"Event structure is not as expected: cannot reach 'body'."


def test_LambdaProxyEvent_payload_raisesIfJsonIsIncorrect():
    import random

    randInt = random.randint(1000, 100000)

    event = {
        "body": " \"key\": " + repr(randInt) + " }"
    }

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(ag.MalformedPayloadError) as exceptionInfo:
        test.payload()

    assert exceptionInfo.value.args[0] == f"Payload is malformed. JSON cannot be decoded: Extra data: line 1 column 7 (char 6)."

    
def test_HttpClientError_init_initializesStatusProperly(caplog):
    import random

    status = random.randint(200, 599)
    message = f'{random.randint(1000, 9999)} some text'

    test = ag.HttpClientError(status, message)

    assert test.status == status


def test_HttpClientError_init_initializesMessageProperly(caplog):
    import random

    status = random.randint(200, 599)
    message = f'{random.randint(1000, 9999)} some text'

    test = ag.HttpClientError(status, message)

    assert str(test) == message


def test_HttpClientError_init_logsProperly(caplog):
    import random

    status = random.randint(200, 599)
    message = f'{random.randint(1000, 9999)} some text'

    ag.HttpClientError(status, message)

    assert caplog.text == f'ERROR    root:apigateway.py:270 HttpClientError: {str(status)} - {message}\n'


def test_simple_message_returnsProperPayload():
    import random

    message = f'{random.randint(0, 9999)} with some blablah'

    payload = ag.simple_message(message)

    assert payload == { "Message": message }


def test_determine_content_type_acceptsAnyAnyByDefault():
    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': '*/*'
            }
        }
    )

    selected = ag.determine_content_type(event)

    assert selected == '*/*'


def test_determine_content_type_acceptsApplicationAnyByDefault():
    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': 'application/*'
            }
        }
    )

    selected = ag.determine_content_type(event)

    assert selected == 'application/*'


def test_determine_content_type_acceptsApplicationJSonByDefault():
    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': 'application/json'
            }
        }
    )

    selected = ag.determine_content_type(event)

    assert selected == 'application/json'    


def test_determine_content_type_acceptsCustomTypes():
    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': 'something/weird'
            }
        }
    )

    selected = ag.determine_content_type(event, customTransformers = { 'something/weird': lambda x : x})

    assert selected == 'something/weird'      


def test_determine_content_type_stillAcceptsJsonWithCustomTypes():
    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': 'application/json'
            }
        }
    )

    selected = ag.determine_content_type(event, customTransformers = { 'something/weird': lambda x : x})

    assert selected == 'application/json'        


def test_determine_content_type_handlesPreferencesProperly():
    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': 'application/json;q=0.5,something/weird;q=0.6,something/wonderful;q=1'
            }
        }
    )

    selected = ag.determine_content_type(event, customTransformers = { 'something/weird': lambda x : x, 'other/stuff': lambda x : x})

    assert selected == 'something/weird'     


def test_determine_content_type_fallsBackToAnyAnyIfNoAcceptHeader():
    event = ag.LambdaProxyEvent(
        {
            'headers': {}
        }
    )

    selected = ag.determine_content_type(event)

    assert selected == '*/*'        


def test_determine_content_type_raisesWithRandomType():
    import random

    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': f'{random.randint(1000, 9999)}/{random.randint(1000, 9999)}'
            }
        }
    )

    with pytest.raises(ag.HttpNotAcceptableError) as exceptionInfo:
        ag.determine_content_type(event)

    assert exceptionInfo.value.args[0] == "None of the formats specified in the Accept header are available. Available formats are: application/json."  


def test_is_binary_returnsFalseForTextAny():
    import random
    
    mimeType = f'text/{random.randint(1000, 9999)}'

    assert ag.is_binary(mimeType) is False


def test_is_binary_returnsFalseForText():
    mimeType = 'text'

    assert ag.is_binary(mimeType) is False

    
def test_is_binary_returnsFalseForApplicationJson():
    mimeType = 'application/json'

    assert ag.is_binary(mimeType) is False    


def test_is_binary_returnsFalseForApplicationXml():
    mimeType = 'application/xml'

    assert ag.is_binary(mimeType) is False    


def test_is_binary_returnsTrueForApplicationAny():
    import random
    
    mimeType = f'application/{random.randint(1000, 9999)}'

    assert ag.is_binary(mimeType) is True


def test_is_binary_returnsTrueForApplication():
    mimeType = 'application'

    assert ag.is_binary(mimeType) is True    


def test_is_binary_returnsTrueForAnyAny():
    import random

    mimeType = f'{random.randint(1000, 9999)}/{random.randint(1000, 9999)}'

    assert ag.is_binary(mimeType) is True   


def test_is_binary_returnsTrueForAny():
    import random

    mimeType = f'{random.randint(1000, 9999)}'

    assert ag.is_binary(mimeType) is True  


def test_json_transformer_returnsProperContent():
    import json 
    import random

    payload = {
        'a': random.randint(0, 9999),
        'b': f'{random.randint(0, 9999)}'
    }

    content, _ = ag.json_transformer(payload)

    assert json.loads(content) == payload


def test_json_transformer_returnsProperContentType():
    import random

    payload = {
        'a': random.randint(0, 9999),
        'b': f'{random.randint(0, 9999)}'
    }

    _, contentType = ag.json_transformer(payload)

    assert contentType == 'application/json; charset=utf-8'    


def test__basic_transformers_areAllJson():
    assert ag._basic_transformers == {
        '*/*': ag.json_transformer,
        'application/*': ag.json_transformer,
        'application/json': ag.json_transformer
    }


def test_build_http_response_returnsPrettyJsonPayloadByDefault():
    import json
    import random

    status = random.randint(200, 599)
    
    payload = {
        "val": random.randint(0, 1000),
        "msg": f"MSG{str(random.randint(0, 1000))}"
    }

    expectedResponse = {
        'isBase64Encoded': False,
        'statusCode': status,
        'body': json.dumps(payload, indent = 2),
        'headers': {     
            'Content-Type': 'application/json; charset=utf-8'
        }
    }

    response = ag.build_http_response(status, payload)

    assert response == expectedResponse


def test_build_http_response_turnsStringPayloadsIntoSimpleMessages():
    import json
    import random

    status = random.randint(200, 599)
    
    message = f"MSG{str(random.randint(0, 1000))}"

    expectedResponse = {
        'isBase64Encoded': False,
        'statusCode': status,
        'body': json.dumps(ag.simple_message(message), indent = 2),
        'headers': {     
            'Content-Type': 'application/json; charset=utf-8'
        }
    }

    response = ag.build_http_response(status, message)

    assert response == expectedResponse    


def test_build_http_response_returnsZippedPayloadIfDesired():
    import base64
    import gzip
    import json
    import random

    status = random.randint(200, 599)
    
    payload = {
        "val": random.randint(0, 1000),
        "msg": f"MSG{str(random.randint(0, 1000))}"
    }

    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept-Encoding': 'gzip,identity'
            }
        }
    )    

    expectedResponse = {
        'isBase64Encoded': True,
        'statusCode': status,
        'body': base64.b64encode(gzip.compress(json.dumps(payload, indent = 2).encode('utf-8'))).decode('utf-8'),
        'headers': {     
            'Content-Type': 'application/json; charset=utf-8',
            'Content-Encoding': 'gzip'
        }
    }

    response = ag.build_http_response(status, payload, event = event) 

    assert response == expectedResponse


def test_build_http_response_returnsMimeTypeAccordingToCustomPreferences():
    import random

    status = random.randint(200, 599)
    
    payload = {
        "val": random.randint(0, 1000),
        "msg": f"MSG{str(random.randint(0, 1000))}"
    }

    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': '*/*;q=0.2,text/*'
            }
        }
    )   

    expectedResponse = {
        'isBase64Encoded': False,
        'statusCode': status,
        'body': payload,
        'headers': {     
            'Content-Type': 'text/strange'
        }
    }

    response = ag.build_http_response(status, payload, event = event, customTransformers = { 'text/*': lambda x : (x, 'text/strange') })

    assert response == expectedResponse


def test_build_http_response_allowsReturningExtraHeaders():
    import json
    import random

    status = random.randint(200, 599)
    
    payload = {
        "val": random.randint(0, 1000),
        "msg": f"MSG{str(random.randint(0, 1000))}"
    }

    extraHeaders = {
        f'{random.randint(0, 1000)}' : f'{random.randint(0, 1000)}',
        f'{random.randint(0, 1000)}' : f'{random.randint(0, 1000)}'
    }

    expectedResponse = {
        'isBase64Encoded': False,
        'statusCode': status,
        'body': json.dumps(payload, indent = 2),
        'headers': {     
            'Content-Type': 'application/json; charset=utf-8',
            **extraHeaders
        }
    }

    response = ag.build_http_response(status, payload, extraHeaders = extraHeaders)

    assert response == expectedResponse    


def test_build_http_server_error_response_returnsOopsMessage():
    import json

    expectedResponse = {
        'isBase64Encoded': False,
        'statusCode': 500,
        'body': json.dumps(
                { "Message": "Sorry, an error occured. Please contact the API administrator to have this sorted out." }, 
                indent = 2
            ),
        'headers': {     
            'Content-Type': 'application/json; charset=utf-8',
        }
    }

    response = ag.build_http_server_error_response()

    assert response == expectedResponse


def test_build_http_server_error_response_returnsCustomMessageIfSpecified():
    import json

    expectedResponse = {
        'isBase64Encoded': False,
        'statusCode': 500,
        'body': json.dumps(
                { "Message": "Some custom message" }, 
                indent = 2
            ),
        'headers': {     
            'Content-Type': 'application/json; charset=utf-8',
        }
    }

    response = ag.build_http_server_error_response('Some custom message')

    assert response == expectedResponse


def test_build_http_client_error_response_returnsWhatTheExceptionCarries():
    import json 

    ex = ag.HttpBadRequestError("some message")

    expectedResponse = {
        'isBase64Encoded': False,
        'statusCode': ex.status,
        'body': json.dumps(
                { "Message": str(ex) }, 
                indent = 2
            ),
        'headers': {     
            'Content-Type': 'application/json; charset=utf-8',
        }
    }    

    response = ag.build_http_client_error_response(ex)

    assert response == expectedResponse

