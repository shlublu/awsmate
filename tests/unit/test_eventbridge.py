import pytest

import awsmate.eventbridge as eb

from unittest.mock import patch

from awsmate.lambdafunction import AwsEventSpecificationError


def test_LambdaBridgePutEvent_init_initializesInternalEventObject():
    event = {}

    test = eb.LambdaBridgePutEvent(event)

    assert test._event is event


def test_LambdaBridgePutEvent_detail_type_returnsTheExpectedDetailsType():
    event = {
        'detail-type': 'Some readable explanations'
    }    

    test = eb.LambdaBridgePutEvent(event)

    assert test.detail_type() == 'Some readable explanations'


def test_LambdaBridgePutEvent_detail_type_raisesIfEventDoesNotHaveADetailType():
    event = {}    

    test = eb.LambdaBridgePutEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(eb.LambdaEvent, '_raiseCannotReachError', side_effect=eb.LambdaEvent._raiseCannotReachError) as mcre:
            test.detail_type()

    mcre.assert_called_once_with("'detail-type'")


def test_LambdaBridgePutEvent_source_returnsTheExpectedServiceName():
    event = {
        'source': 'aws.scheduler'
    }    

    test = eb.LambdaBridgePutEvent(event)

    assert test.source() == 'aws.scheduler'


def test_LambdaBridgePutEvent_source_raisesIfEventDoesNotHaveASource():
    event = {}    

    test = eb.LambdaBridgePutEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(eb.LambdaEvent, '_raiseCannotReachError', side_effect=eb.LambdaEvent._raiseCannotReachError) as mcre:
            test.source()

    mcre.assert_called_once_with("'source'")
    

def test_LambdaBridgePutEvent_detail_returnsTheExpectedDetail():
    event = {
        'detail': '{ "someKey": "someValue" }'
    }    

    test = eb.LambdaBridgePutEvent(event)

    assert test.detail() == { 'someKey': 'someValue' }


def test_LambdaBridgePutEvent_detail_LivesWellWithEmptyDetail():
    event = {
        'detail': '{}'
    }    

    test = eb.LambdaBridgePutEvent(event)

    assert test.detail() == {}    


def test_LambdaBridgePutEvent_source_raisesIfEventDoesNotHaveASDetail():
    event = {}    

    test = eb.LambdaBridgePutEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(eb.LambdaEvent, '_raiseCannotReachError', side_effect=eb.LambdaEvent._raiseCannotReachError) as mcre:
            test.detail()

    mcre.assert_called_once_with("'detail'")


def test_LambdaBridgePutEvent_source_raisesIfDetailsIsNotValidJSON():
    event = {
        'detail': {}
    }    

    test = eb.LambdaBridgePutEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(eb.LambdaEvent, '_raiseEventStructureError', side_effect=eb.LambdaEvent._raiseEventStructureError) as mese:
            test.detail()

    mese.assert_called_once_with('Detail JSON cannot be decoded: the JSON object must be str, bytes or bytearray, not dict.') 
    
