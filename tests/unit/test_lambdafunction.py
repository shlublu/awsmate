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

    assert exceptionInfo.value.args[0] == f"eventObject should be a dict. Here: {str(type(event))}."
