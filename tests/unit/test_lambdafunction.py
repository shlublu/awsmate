import pytest

import awsmate.lambdafunction as lf

from unittest.mock import patch


def test_LambdaEvent__raiseEventStructureError_raisesAsExpected(caplog):
    with pytest.raises(lf.AwsEventSpecificationError) as exdesc:
        lf.LambdaEvent._raiseEventStructureError('some message')

    assert exdesc.value.args[0] == "Event structure is not as expected: some message."    


def test_LambdaEvent__raiseCannotReachError_raisesAsExpected(caplog):
    with pytest.raises(lf.AwsEventSpecificationError) as exdesc:
        lf.LambdaEvent._raiseCannotReachError('some field')

    assert exdesc.value.args[0] == 'Event structure is not as expected: cannot reach "some field".'    


def test_LambdaEvent__raiseCannotReachError_reliesOn_raiseEventStructureError(caplog):
    with patch.object(lf.LambdaEvent, '_raiseEventStructureError') as mrese:
        lf.LambdaEvent._raiseCannotReachError('some field')

    mrese.assert_called_once_with('cannot reach "some field"')


def test_LambdaEvent_init_initializesInternalEventObject():
    event = {}

    test = lf.LambdaEvent(event)

    assert test._event is event


def test_LambdaEvent_init_raisesIfEventObjectIsNotADict():
    event = "not a dict"

    with pytest.raises(TypeError) as exceptionInfo:
        lf.LambdaEvent(event) # type: ignore

    assert exceptionInfo.value.args[0] == f"event_object should be a dict. Here: {str(type(event))}."


def test_LambdaEvent__records_structure_returnsTheProperStructure():
    event = {
        "Records": [
            {
                "anything": {}
            }
        ]
    }    

    test = lf.LambdaEvent(event)

    assert test._records_structure() == event['Records'][0]


def test_LambdaEvent__records_structure_raisesIfEventHasNoRecordKey():
    event = {}    

    test = lf.LambdaEvent(event)

    with pytest.raises(lf.AwsEventSpecificationError) as exceptionInfo:
        with patch.object(lf.LambdaEvent, '_raiseCannotReachError', side_effect=lf.LambdaEvent._raiseCannotReachError) as mcre:
            test._records_structure()

    mcre.assert_called_once_with("'Records'")


def test_LambdaEvent__records_structure_raisesIfRecordsIsEmpty():
    event = {
        "Records": []
    }

    test = lf.LambdaEvent(event)

    with pytest.raises(lf.AwsEventSpecificationError) as exceptionInfo:
        with patch.object(lf.LambdaEvent, '_raiseEventStructureError', side_effect=lf.LambdaEvent._raiseEventStructureError) as mcre:
            test._records_structure()

    mcre.assert_called_once_with("'Records' is empty")     


def test_LambdaEvent_records_structure_raisesIfRecordsContainsMoreThanOneElement():
    event = {
        "Records": [
            {},
            {}
        ]
    }

    test = lf.LambdaEvent(event)

    with pytest.raises(lf.AwsEventSpecificationError) as exceptionInfo:
        with patch.object(lf.LambdaEvent, '_raiseEventStructureError', side_effect=lf.LambdaEvent._raiseEventStructureError) as mcre:
            test._records_structure()

    mcre.assert_called_once_with("event contains 2 Records where 1 is expected")       

