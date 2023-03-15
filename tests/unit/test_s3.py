import pytest

import awsmate.s3 as s3

from awsmate.lambdafunction import AwsEventSpecificationError


def test_LambdaNotificationEvent_KEY_RECORDS_correspondsToAwsSpecifications():
    assert isinstance(s3.LambdaNotificationEvent.KEY_RECORDS, str)
    assert s3.LambdaNotificationEvent.KEY_RECORDS == "Records"

    
def test_LambdaNotificationEvent_KEY_S3_correspondsToAwsSpecifications():
    assert isinstance(s3.LambdaNotificationEvent.KEY_S3, str)
    assert s3.LambdaNotificationEvent.KEY_S3 == "s3"


def test_LambdaNotificationEvent_init_initializesInternalEventObject():
    event = {}

    test = s3.LambdaNotificationEvent(event)

    assert test._event is event


def test_LambdaNotificationEvent_object_key_returnsTheProperValue():
    import random

    randString = repr(random.randint(1000, 100000))

    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": randString
                        }
                }
            }
            ]
    }

    test = s3.LambdaNotificationEvent(event)

    assert test.object_key() == randString


def test_LambdaNotificationEvent_object_key_raisesIfKeyDoesNotHaveARecordElement():
    event = {
        "randomStuff": "stuff"
    }

    test = s3.LambdaNotificationEvent(event)
    
    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.object_key()

    assert exceptionInfo.value.args[0] == "Event structure is not as expected: cannot reach 'Records'."


def test_LambdaNotificationEvent_object_key_raisesIfKeyDoesNotHaveAS3ElementUnderRecords():
    event = {
        "Records": [
            {
                "randomStuff": {
                    "object": {
                        "key": "stuff"
                        }
                }
            }
        ]
    }

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.object_key()

    assert exceptionInfo.value.args[0] == "Event structure is not as expected: cannot reach 's3'."


def test_LambdaNotificationEvent_object_key_raisesIfKeyDoesNotHaveAnObjectElementUnderS3():
    event = {
        "Records": [
            {
                "s3": {
                    "randomStuff": {
                        "key": "stuff"
                        }
                }
            }
            ]
    }

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.object_key()

    assert exceptionInfo.value.args[0] == "Event structure is not as expected: cannot reach 'object'."


def test_LambdaNotificationEvent_object_key_raisesIfKeyDoesNotHaveAKeyElementUnderObject():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "randomStuff": "stuff"
                        }
                }
            }
            ]
    }

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.object_key()

    assert exceptionInfo.value.args[0] == "Event structure is not as expected: cannot reach 'key'."


def test_LambdaNotificationEvent_object_key_raisesIfRecordsIsEmpty():
    event = {
        "Records": []
    }

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.object_key()

    assert exceptionInfo.value.args[0] == "Event structure is not as expected: no Records object is present in 's3'."


def test_LambdaNotificationEvent_object_key_raisesIfRecordsContainsMoreThanOneElement():
    import random

    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": repr(random.randint(1000, 100000))
                        }
                }
            },
            {
                "s3": {
                    "object": {
                        "key": repr(random.randint(1000, 100000))
                        }
                }
            }
        ]
    }

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        test.object_key()

    assert exceptionInfo.value.args[0] == "Event contains 2 Records where 1 is expected."
