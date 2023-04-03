import pytest

import awsmate.eventbridge as eb

from unittest.mock import patch

from awsmate.lambdafunction import AwsEventSpecificationError


def test_LambdaBridgeEvent_init_initializesInternalEventObject():
    event = {}

    test = eb.LambdaBridgeEvent(event)

    assert test._event is event


def test_LambdaBridgeEvent_detail_type_returnsTheExpectedDetails():
    event = {
        'detail-type': 'Some readable explanations'
    }    

    test = eb.LambdaBridgeEvent(event)

    assert test.detail_type() == 'Some readable explanations'


def test_LambdaBridgeEvent_detail_type_raisesIfEventDoesNotHaveADetailType():
    event = {}    

    test = eb.LambdaBridgeEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(eb.LambdaEvent, '_raiseCannotReachError', side_effect=eb.LambdaEvent._raiseCannotReachError) as mcre:
            test.detail_type()

    mcre.assert_called_once_with("'detail-type'")


def test_LambdaBridgeEvent_source_returnsTheExpectedServiceName():
    event = {
        'source': 'aws.scheduler'
    }    

    test = eb.LambdaBridgeEvent(event)

    assert test.source() == 'aws.scheduler'


def test_LambdaBridgeEvent_source_raisesIfEventDoesNotHaveASource():
    event = {}    

    test = eb.LambdaBridgeEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(eb.LambdaEvent, '_raiseCannotReachError', side_effect=eb.LambdaEvent._raiseCannotReachError) as mcre:
            test.source()

    mcre.assert_called_once_with("'source'")
    

def test_LambdaBridgeEvent_detail_returnsTheExpectedServiceName():
    event = {
        'detail': { 'someKey': 'someValue' }
    }    

    test = eb.LambdaBridgeEvent(event)

    assert test.detail() == { 'someKey': 'someValue' }


def test_LambdaBridgeEvent_detail_LivesWellWithEmptyDetail():
    event = {
        'detail': {}
    }    

    test = eb.LambdaBridgeEvent(event)

    assert test.detail() == {}    


def test_LambdaBridgeEvent_source_raisesIfEventDoesNotHaveASDetail():
    event = {}    

    test = eb.LambdaBridgeEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(eb.LambdaEvent, '_raiseCannotReachError', side_effect=eb.LambdaEvent._raiseCannotReachError) as mcre:
            test.detail()

    mcre.assert_called_once_with("'detail'")


def test_LambdaBridgeEvent_source_raisesIfDetailsIsNotADict():
    event = {
        'detail': 'something that is not a dict'
    }    

    test = eb.LambdaBridgeEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(eb.LambdaEvent, '_raiseEventStructureError', side_effect=eb.LambdaEvent._raiseEventStructureError) as mese:
            test.detail()

    mese.assert_called_once_with("Detail should be a dict, not a <class 'str'>.") 
