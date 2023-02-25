import pytest

import awsmate.lambdafunction as lf


def test_LambdaEvent_init_initializesInternalEventObject():
    event = {}

    test = lf.LambdaEvent(event)

    assert test._event is event


def test_LambdaEvent_init_raisesIfEventObjectIsNotADict():
    event = "not a dict"

    with pytest.raises(TypeError) as exceptionInfo:
        lf.LambdaEvent(event) # type: ignore

    assert exceptionInfo.value.args[0] == f"eventObject should be a dict. Here: {str(type(event))}."
