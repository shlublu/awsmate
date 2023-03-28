import pytest

import json
import random

import awsmate.apigateway as ag

from unittest.mock import patch
from awsmate.lambdafunction import AwsEventSpecificationError


def test_LambdaProxyEvent_init_initializesInternalEventObject():
    event = {}

    test = ag.LambdaProxyEvent(event)

    assert test._event is event


def test_LambdaProxyEvent_http_headers_returnsAllHeadersWithKeysInLowerCase():
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
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.http_headers()

    mcre.assert_called_once_with("'headers'")


def test_LambdaProxyEvent_http_method_returnsTheHttpMethodOfTheCallInUpperCase():
    event = {
        'requestContext' : { 
            'httpMethod': 'PoSt'
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert  test.http_method() == 'POST'


def test_LambdaProxyEvent_http_method_raisesIfMethodFieldIsMissing():
    event = {
        'requestContext' : {}
    }

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.http_method()

    mcre.assert_called_once_with("'httpMethod'")


def test_LambdaProxyEvent_http_method_raisesIfRequestContextFieldIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.http_method()

    mcre.assert_called_once_with("'requestContext'")


def test_LambdaProxyEvent_http_protocol_returnsTheHttpProtocolOfTheCallInUpperCase():
    event = {
        'requestContext' : { 
            'protocol': 'HtTp/1.1'
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert  test.http_protocol() == 'HTTP/1.1'


def test_LambdaProxyEvent_http_protocol_raisesIfProtocolFieldIsMissing():
    event = {
        'requestContext' : {}
    }

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.http_protocol()

    mcre.assert_called_once_with("'protocol'")


def test_LambdaProxyEvent_http_protocol_raisesIfRequestContextFieldIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.http_protocol()

    mcre.assert_called_once_with("'requestContext'")


def test_LambdaProxyEvent_http_user_agent_returnsTheHttpUserAgentOfTheCall():
    event = {
        'requestContext' : { 
            'identity': {
                'userAgent': 'agent/1.0'
            }
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert  test.http_user_agent() == 'agent/1.0'


def test_LambdaProxyEvent_http_user_agent_raisesIfUserAGentFieldIsMissing():
    event = {
        'requestContext' : {
            'identity': {}
        }
    }

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.http_user_agent()

    mcre.assert_called_once_with("'userAgent'")


def test_LambdaProxyEvent_http_user_agent_raisesIfIdentityFieldIsMissing():
    event = {
        'requestContext' : {}
    }

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.http_user_agent()

    mcre.assert_called_once_with("'identity'")
    
    
def test_LambdaProxyEvent_http_user_agent_raisesIfRequestContextFieldIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.http_user_agent()

    mcre.assert_called_once_with("'requestContext'")


def test_LambdaProxyEvent_header_sorted_preferences_returnsNonWeightedPreferencesAsPassed():
    event = { 
        "headers": { 'Accept-Encoding': 'gzip,deflate,other' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('accept-encoding') == ('gzip', 'deflate', 'other')
    

def test_LambdaProxyEvent_header_sorted_preferences_consideresNoWeightMeansOne():
    event = { 
        "headers": { 'Accept-Encoding': 'gzip;q=0.4,deflate,other;q=0.6' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('accept-encoding') == ('deflate', 'other', 'gzip')

    
def test_LambdaProxyEvent_header_sorted_preferences_returnsPreferencesAccordingToWeightsGivenSorted():
    event = { 
        "headers": { 'Accept-Encoding': 'gzip,deflate;q=0.8,other;q=0.1' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('accept-encoding') == ('gzip', 'deflate', 'other')


def test_LambdaProxyEvent_header_sorted_preferences_returnsPreferencesAccordingToWeightsGivenUnsorted():
    event = { 
        "headers": { 'Accept-Encoding': 'gzip;q=0.2,deflate,other;q=0.9' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('accept-encoding') == ('deflate', 'other', 'gzip')


def test_LambdaProxyEvent_header_sorted_preferences_considersBadlyFormattedWeightMeansHalf():
    event = { 
        "headers": { 'Accept-Encoding': 'gzip;q=0.4,deflate;q=0.6,other;garbage' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('accept-encoding') == ('deflate', 'other', 'gzip')


def test_LambdaProxyEvent_header_sorted_preferences_silentelyIgnoresEmptyPreference():
    event = { 
        "headers": { 'Accept-Encoding': 'gzip;q=0.4,,;q=1,;garbage,deflate;q=0.6,other' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('accept-encoding') == ('other', 'deflate', 'gzip')


def test_LambdaProxyEvent_header_sorted_preferences_silentelyIgnoreSpaces():
    event = { 
        "headers": { 'Accept-Encoding': 'gzip ; q = 0.6,deflate;q=0.4,other' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('accept-encoding') == ('other', 'gzip', 'deflate')  


def test_LambdaProxyEvent_header_sorted_preferences_returnsNoPreferenceIfQueriedHeaderHasNotBeenPassed():
    event = { 
        "headers": { 'Accept-Encoding': 'gzip;q=0.2,deflate,other' }
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
        "headers": { 'Accept-Encoding': 'gzip;q=0.3,deflate;q=0.2,other' }
    }
    
    test = ag.LambdaProxyEvent(event)

    assert test.header_sorted_preferences('aCcEpT-eNcOdInG') == ('other', 'gzip', 'deflate')  


def test_LambdaProxyEvent_query_domain_name_returnsTheDomainNameOfTheCallInLowerCase():
    event = {
        'requestContext': {
            'domainName': 'eXaMpLe.CoM'
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert  test.query_domain_name() == 'example.com'


def test_LambdaProxyEvent_query_domain_name_raisesIfDomainNameFieldIsMissing():
    event = {
        'requestContext' : {}
    }

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.query_domain_name()

    mcre.assert_called_once_with("'domainName'")


def test_LambdaProxyEvent_query_domain_name_raisesIfRequestContextFieldIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.query_domain_name()

    mcre.assert_called_once_with("'requestContext'")


def test_LambdaProxyEvent_query_path_returnsPathElementsIgnoringTrailingSeparator():
    randPathA = f'{random.randint(1000, 9999)}FirstElement' 
    randPathB = f'{random.randint(1000, 9999)}SecondElement' 
    randPathC = f'{random.randint(1000, 9999)}ThirdElement' 

    event = {
        'requestContext' : {
            'path': f'/{randPathA}/{randPathB}/{randPathC}/'
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert test.query_path() == ( randPathA, randPathB, randPathC )


def test_LambdaProxyEvent_query_path_livesWellWithNoTrailingSeparator():
    randPathA = f'{random.randint(1000, 9999)}FirstElement' 
    randPathB = f'{random.randint(1000, 9999)}SecondElement' 
    randPathC = f'{random.randint(1000, 9999)}ThirdElement' 

    event = {
        'requestContext' : {
            'path': f'/{randPathA}/{randPathB}/{randPathC}'
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert test.query_path() == ( randPathA, randPathB, randPathC )


def test_LambdaProxyEvent_query_path_assumesLeadingSeparator():
    randPathA = f'{random.randint(1000, 9999)}FirstElement' 
    randPathB = f'{random.randint(1000, 9999)}SecondElement' 
    randPathC = f'{random.randint(1000, 9999)}ThirdElement' 

    event = {
        'requestContext' : {
            'path': f'{randPathA}/{randPathB}/{randPathC}/'
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert test.query_path() == ( randPathA, randPathB, randPathC )


def test_LambdaProxyEvent_query_path_assumesLeadingSeparatorEvenIfNoTrailingSeparator():
    randPathA = f'{random.randint(1000, 9999)}FirstElement' 
    randPathB = f'{random.randint(1000, 9999)}SecondElement' 
    randPathC = f'{random.randint(1000, 9999)}ThirdElement' 

    event = {
        'requestContext' : {
            'path': f'{randPathA}/{randPathB}/{randPathC}'
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert test.query_path() == ( randPathA, randPathB, randPathC )


def test_LambdaProxyEvent_query_path_livesWithASingleElement():
    event = {
        'requestContext' : {        
            'path': f'{random.randint(1000, 9999)}Element'
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert test.query_path() == ( event['requestContext']['path'], )


def test_LambdaProxyEvent_query_path_raisesIfPathFieldIsMissing():
    event = {
        'requestContext' : {}
    }

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.query_path()

    mcre.assert_called_once_with("'path'")


def test_LambdaProxyEvent_query_path_raisesIfRequestContextFieldIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.query_path()

    mcre.assert_called_once_with("'requestContext'")


def test_LambdaProxyEvent_query_string_parameters_returnsAllQueryStringParametersAsTheyAre():
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
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.query_string_parameters()

    mcre.assert_called_once_with("'queryStringParameters'")


def test_LambdaProxyEvent_query_string_returnsTheWholeString():
    randMethod = str(random.randint(1000, 9999))

    randPathA = str(random.randint(1000, 9999)) 
    randPathB = str(random.randint(1000, 9999)) 
    randPathC = str(random.randint(1000, 9999)) 

    randParamsA = str(random.randint(1000, 9999)) 
    randParamsB = str(random.randint(1000, 9999))  
    randParamsC = str(random.randint(1000, 9999))  

    path = f'/{randPathA}/{randPathB}/{randPathC}/'

    params = {
        'a': randParamsA,
        'b': randParamsB,
        'c': randParamsC
    }

    event = {
        'requestContext': {
            'httpMethod': randMethod,
            'path': path,
            'domainName': 'example.com'
        },
        'queryStringParameters': params
    }

    test = ag.LambdaProxyEvent(event)
    expected = f'{randMethod} https://example.com{path[0:-1]}?a={randParamsA}&b={randParamsB}&c={randParamsC}'

    assert test.query_string() == expected


def test_LambdaProxyEvent_query_string_livesWellWithNoQueryParameters():
    randMethod = str(random.randint(1000, 9999))

    randPathA = str(random.randint(1000, 9999)) 
    randPathB = str(random.randint(1000, 9999)) 
    randPathC = str(random.randint(1000, 9999)) 

    path = f'/{randPathA}/{randPathB }/{randPathC}/'

    event = {
        'requestContext': {
            'httpMethod': randMethod,
            'path': path,
            'domainName': 'example.com'
        },
        'queryStringParameters': None
    }

    test = ag.LambdaProxyEvent(event)
    expected = f'{randMethod} https://example.com{path[0:-1]}'

    assert test.query_string() == expected


def test_LambdaProxyEvent_query_string_reliesOnEventMethods():
    from unittest.mock import patch

    event = {
        'requestContext': {
            'httpMethod': 'GET',
            'path': '/a/b/c/',
            'domainName': 'example.com'
        },
        'queryStringParameters': {
            'a': 'paramA',
            'b': 'paramB',
            'c': 'paramC'
        }
    }

    with patch.object(ag.LambdaProxyEvent, 'http_method', return_value=None) as acm:
        with patch.object(ag.LambdaProxyEvent, 'query_path', return_value = ()) as acp:
            with patch.object(ag.LambdaProxyEvent, 'query_string_parameters', return_value = {}) as acqp:
                ag.LambdaProxyEvent(event).query_string()

    acm.assert_called_once()
    acp.assert_called_once()
    acqp.assert_called_once()


def test_LambdaProxyEvent_query_payload_returnsThePayloadAsItIs():
    randInt = random.randint(1000, 100000)

    event = {
        "body": "{ \"key\": " + repr(randInt) + " }"
    }

    test = ag.LambdaProxyEvent(event)

    assert test.query_payload() == { 'key': randInt }


def test_LambdaProxyEvent_query_payload_returnsNoneIfBodyIsNull():
    event = {
        "body": None
    }

    test = ag.LambdaProxyEvent(event)

    assert test.query_payload() is None   


def test_LambdaProxyEvent_query_payload_raisesIfBodyIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.query_payload()

    mcre.assert_called_once_with("'body'")


def test_LambdaProxyEvent_query_payload_raisesIfJsonIsIncorrect():
    randInt = random.randint(1000, 100000)

    event = {
        "body": " \"key\": " + repr(randInt) + " }"
    }

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(ag.MalformedPayloadError) as exceptionInfo:
        test.query_payload()

    assert exceptionInfo.value.args[0] == f"Payload is malformed. JSON cannot be decoded: Extra data: line 1 column 7 (char 6)."



def test_LambdaProxyEvent_authorizer_claims_returnsTheClaimsIfAny():
    claims = {
        'cognito:username': '192837645', 
        'email': 'jane@example.com', 
        'given_name': 'Jane', 
        'family_name': 'Doe'
    }
    
    event = {
        'requestContext': {
            'authorizer': {
                'claims': claims
            }
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert  test.authorizer_claims() == claims


def test_LambdaProxyEvent_authorizer_claims_returnsTheClaimsEvenIfNone():
    event = {
        'requestContext': {
            'authorizer': {
                'claims': None
            }
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert  test.authorizer_claims() is None    


def test_LambdaProxyEvent_authorizer_claims_returnsNoneIfNoClaims():
    event = {
        'requestContext': {
            'authorizer': {}
        }
    }

    test = ag.LambdaProxyEvent(event)

    assert  test.authorizer_claims() is None


def test_LambdaProxyEvent_authorizer_claims_returnsNoneIfNoAuthorizer():
    event = {
        'requestContext': {}
    }

    test = ag.LambdaProxyEvent(event)

    assert  test.authorizer_claims() is None


def test_LambdaProxyEvent_authorizer_claims_raisesIfRequestContextFieldIsMissing():
    event = {}

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(ag.LambdaEvent, '_raiseCannotReachError', side_effect=ag.LambdaEvent._raiseCannotReachError) as mcre:
            test.authorizer_claims()

    mcre.assert_called_once_with("'requestContext'")


def test_LambdaProxyEvent_authorizer_claims_raisesIfClaimsIsNotADict():
    claims = ['192837645', 'jane@example.com', 'Jane', 'Doe']
    
    event = {
        'requestContext': {
            'authorizer': {
                'claims': claims
            }
        }
    }

    test = ag.LambdaProxyEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.authorizer_claims()

    assert exceptionInfo.value.args[0] == "Claims should be a dict, not a <class 'list'>."  
    
    
def test_HttpClientError_init_initializesStatusProperly(caplog):
    status = random.randint(200, 599)
    message = f'{random.randint(1000, 9999)} some text'

    test = ag.HttpClientError(status, message)

    assert test.status == status


def test_HttpClientError_init_initializesMessageProperly(caplog):
    status = random.randint(200, 599)
    message = f'{random.randint(1000, 9999)} some text'

    test = ag.HttpClientError(status, message)

    assert str(test) == message


def test_HttpClientError_init_logsProperly(caplog):
    import re

    status = random.randint(200, 599)
    message = f'{random.randint(1000, 9999)} some text'

    ag.HttpClientError(status, message)

    assert re.match(f'ERROR    root:apigateway.py:[0-9]{{3}} HttpClientError: {str(status)} - {message}\n', caplog.text)


def test_simple_message_returnsProperPayload():
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

    selected = ag.determine_content_type(event, custom_transformers = { 'something/weird': lambda x : x})

    assert selected == 'something/weird'      


def test_determine_content_type_stillAcceptsJsonWithCustomTypes():
    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': 'application/json'
            }
        }
    )

    selected = ag.determine_content_type(event, custom_transformers = { 'something/weird': lambda x : x})

    assert selected == 'application/json'        


def test_determine_content_type_handlesPreferencesProperly():
    event = ag.LambdaProxyEvent(
        {
            'headers': {
                'Accept': 'application/json;q=0.5,something/weird;q=0.6,something/wonderful;q=1'
            }
        }
    )

    selected = ag.determine_content_type(event, custom_transformers = { 'something/weird': lambda x : x, 'other/stuff': lambda x : x})

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
    mimeType = f'application/{random.randint(1000, 9999)}'

    assert ag.is_binary(mimeType) is True


def test_is_binary_returnsTrueForApplication():
    mimeType = 'application'

    assert ag.is_binary(mimeType) is True    


def test_is_binary_returnsTrueForAnyAny():
    mimeType = f'{random.randint(1000, 9999)}/{random.randint(1000, 9999)}'

    assert ag.is_binary(mimeType) is True   


def test_is_binary_returnsTrueForAny():
    mimeType = f'{random.randint(1000, 9999)}'

    assert ag.is_binary(mimeType) is True  


def test_json_transformer_returnsProperContent():
    payload = {
        'a': random.randint(0, 9999),
        'b': f'{random.randint(0, 9999)}'
    }

    content, _ = ag.json_transformer(payload)

    assert json.loads(content) == payload


def test_json_transformer_returnsProperContentType():
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

    response = ag.build_http_response(status, payload, event=event, custom_transformers={ 'text/*': lambda x : (x, 'text/strange') })

    assert response == expectedResponse


def test_build_http_response_allowsReturningExtraHeaders():
    status = random.randint(200, 599)
    
    payload = {
        "val": random.randint(0, 1000),
        "msg": f"MSG{str(random.randint(0, 1000))}"
    }

    extra_headers = {
        f'{random.randint(0, 1000)}' : f'{random.randint(0, 1000)}',
        f'{random.randint(0, 1000)}' : f'{random.randint(0, 1000)}'
    }

    expectedResponse = {
        'isBase64Encoded': False,
        'statusCode': status,
        'body': json.dumps(payload, indent = 2),
        'headers': {     
            'Content-Type': 'application/json; charset=utf-8',
            **extra_headers
        }
    }

    response = ag.build_http_response(status, payload, extra_headers = extra_headers)

    assert response == expectedResponse    


def test_build_http_server_error_response_passeAllParameters():
    message = 'some msg'
    event = ag.LambdaProxyEvent({})
    transformers = { 'text/*': lambda x : (x, 'text/strange') }
    extra_headers={ 'someKey': 'someValue' }

    with patch('awsmate.apigateway.build_http_response') as mbhser:
        ag.build_http_server_error_response(message, event=event, custom_transformers=transformers, extra_headers=extra_headers)

    mbhser.assert_called_once_with(
        500, 
        message, 
        event=event,
        custom_transformers=transformers,
        extra_headers=extra_headers
        )
    

def test_build_http_server_error_response_usesDefaultMessageIfUnspecified():
    with patch('awsmate.apigateway.build_http_response') as mbhser:
        ag.build_http_server_error_response()

    mbhser.assert_called_once_with(
        500, 
        "Sorry, an error occured. Please contact the API administrator to have this sorted out.", 
        )


def test_build_http_client_error_response_passeAllParameters():
    exception = ag.HttpBadRequestError("some message")
    event = ag.LambdaProxyEvent({})
    transformers = { 'text/*': lambda x : (x, 'text/strange') }
    extra_headers={ 'someKey': 'someValue' }

    with patch('awsmate.apigateway.build_http_response') as mbhser:
        ag.build_http_client_error_response(exception, event=event, custom_transformers=transformers, extra_headers=extra_headers)

    mbhser.assert_called_once_with(
        exception.status, 
        str(exception), 
        event=event,
        custom_transformers=transformers,
        extra_headers=extra_headers
        )
