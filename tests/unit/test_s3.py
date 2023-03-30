import pytest

import awsmate.s3 as s3

from unittest.mock import patch

from awsmate.lambdafunction import AwsEventSpecificationError


def test_LambdaNotificationEvent_init_initializesInternalEventObject():
    event = {}

    test = s3.LambdaNotificationEvent(event)

    assert test._event is event


def LambdaNotificationEvent__records_structure_returnsTheProperStructure():
    event = {
        "Records": [
            {
                "anything": {}
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    assert test._records_structure() == event['Records']


def LambdaNotificationEvent__records_structure_raisesIfEventHasNoRecordKey():
    event = {}    

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseCannotReachError', side_effect=s3.LambdaEvent._raiseCannotReachError) as mcre:
            test._records_structure()

    mcre.assert_called_once_with("'Records'")


def test_LambdaNotificationEvent__records_structure_raisesIfRecordsIsEmpty():
    event = {
        "Records": []
    }

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseEventStructureError', side_effect=s3.LambdaEvent._raiseEventStructureError) as mcre:
            test._records_structure()

    mcre.assert_called_once_with("'Records' is empty")     


def test_LambdaNotificationEvent_records_structure_raisesIfRecordsContainsMoreThanOneElement():
    event = {
        "Records": [
            {},
            {}
        ]
    }

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseEventStructureError', side_effect=s3.LambdaEvent._raiseEventStructureError) as mcre:
            test._records_structure()

    mcre.assert_called_once_with("event contains 2 Records where 1 is expected")       


def test_LambdaNotificationEvent__s3_structure_returnsTheProperStructure():
    event = {
        "Records": [
            {
                "s3": {
                    "anything": {}
                }
            }
        ]
    }

    test = s3.LambdaNotificationEvent(event)

    assert test._s3_structure() == test._records_structure()['s3']
    
    
def LambdaNotificationEvent__s3_structure_raisesIfEventHasNoS3UnderRecords():
    event = {
        "Records": [
            {}
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseCannotReachError', side_effect=s3.LambdaEvent._raiseCannotReachError) as mcre:
            test._s3_structure()

    mcre.assert_called_once_with("'s3'")


def test_LambdaNotificationEvent__s3_structure_reliesOn_records_structure():
    event = {
        "Records": [
            {
                "s3": {}
            }
        ]
    }

    test = s3.LambdaNotificationEvent(event)

    with patch.object(s3.LambdaNotificationEvent, '_s3_structure') as ms3n:
        test._s3_structure()

    ms3n.assert_called_once_with()


def test_LambdaNotificationEvent__object_structure_returnsTheProperStructure():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "anything": {}
                    }
                }
            }
            ]
    }

    test = s3.LambdaNotificationEvent(event)

    assert test._object_structure() == test._s3_structure()['object']


def test_LambdaNotificationEvent__object_structure_raisesIfEventDoesNotHaveAnObjectUnderS3():
    event = {
        "Records": [
            {
                "s3": {}
            }
        ]
    }

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseCannotReachError', side_effect=s3.LambdaEvent._raiseCannotReachError) as mcre:
            test._object_structure()

    mcre.assert_called_once_with("'object'")    
    
    
def test_LambdaNotificationEvent__object_structure_reliesOn_s3_structure():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {}
                }
            }
        ]
    }

    test = s3.LambdaNotificationEvent(event)

    with patch.object(s3.LambdaNotificationEvent, '_s3_structure') as ms3n:
        test._object_structure()

    ms3n.assert_called_once_with()
    

def test_LambdaNotificationEvent__bucket_structure_returnsTheProperStructure():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "anything": {}
                    }
                }
            }
            ]
    }

    test = s3.LambdaNotificationEvent(event)

    assert test._bucket_structure() == test._s3_structure()['bucket']
    
    
def test_LambdaNotificationEvent__bucket_structure_raisesIfEventDoesNotHaveABucketUnderS3():
    event = {
        "Records": [
            {
                "s3": {}
            }
        ]
    }

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseCannotReachError', side_effect=s3.LambdaEvent._raiseCannotReachError) as mcre:
            test._bucket_structure()

    mcre.assert_called_once_with("'bucket'")  


def test_LambdaNotificationEvent__bucket_structure_reliesOn_s3_structure():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {}
                }
            }
        ]
    }

    test = s3.LambdaNotificationEvent(event)

    with patch.object(s3.LambdaNotificationEvent, '_s3_structure') as ms3n:
        test._bucket_structure()

    ms3n.assert_called_once_with()
    

def test_LambdaNotificationEvent_object_key_returnsTheExpectedKey():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": "stuff"
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    assert test.object_key() == "stuff" 


def test_LambdaNotificationEvent_object_key_raisesIfEventDoesNotHaveAKeyUnderObject():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {}
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseCannotReachError', side_effect=s3.LambdaEvent._raiseCannotReachError) as mcre:
            test.object_key()

    mcre.assert_called_once_with("'key'")


def test_LambdaNotificationEvent_object_key_reliesOn_object_structure():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "key": "stuff"
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with patch.object(s3.LambdaNotificationEvent, '_object_structure') as ms3n:
        test.object_key()

    ms3n.assert_called_once_with()


def test_LambdaNotificationEvent_object_size_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "size": 123456
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    assert test.object_size() == 123456


def test_LambdaNotificationEvent_object_size_returnsNoneIfEventDoesNotHaveASizeUnderObject():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {}
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    assert test.object_size() is None


def test_LambdaNotificationEvent_object_size_reliesOn_object_structure():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "size": 123456
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with patch.object(s3.LambdaNotificationEvent, '_object_structure') as ms3n:
        test.object_size()

    ms3n.assert_called_once_with()


def test_LambdaNotificationEvent_object_etag_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "eTag": "8b38dac3b5c48c44704ec934eabae5a2"
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    assert test.object_etag() == "8b38dac3b5c48c44704ec934eabae5a2"


def test_LambdaNotificationEvent_object_etag_returnsNoneIfEventDoesNotHaveAnEtagUnderObject():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {}
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    assert test.object_etag() is None


def test_LambdaNotificationEvent_object_etag_reliesOn_object_structure():
    event = {
        "Records": [
            {
                "s3": {
                    "object": {
                        "eTag": "8b38dac3b5c48c44704ec934eabae5a2"
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with patch.object(s3.LambdaNotificationEvent, '_object_structure') as ms3n:
        test.object_etag()

    ms3n.assert_called_once_with()


def test_LambdaNotificationEvent_bucket_name_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "my-example-bucket"
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    assert test.bucket_name() == "my-example-bucket"


def test_LambdaNotificationEvent_bucket_name_raisesIfEventDoesNotHaveANameUnderBucket():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {}
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseCannotReachError', side_effect=s3.LambdaEvent._raiseCannotReachError) as mcre:
            test.bucket_name()

    mcre.assert_called_once_with("'name'")


def test_LambdaNotificationEvent_bucket_name_reliesOn_bucket_structure():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": "my-example-bucket"
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with patch.object(s3.LambdaNotificationEvent, '_bucket_structure') as ms3n:
        test.bucket_name()

    ms3n.assert_called_once_with()


def test_LambdaNotificationEvent_bucket_arn_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "arn": "arn:aws:s3:::my-example-s3-bucket"
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    assert test.bucket_arn() == "arn:aws:s3:::my-example-s3-bucket"


def test_LambdaNotificationEvent_bucket_arn_raisesIfEventDoesNotHaveAnArnUnderBucket():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {}
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseCannotReachError', side_effect=s3.LambdaEvent._raiseCannotReachError) as mcre:
            test.bucket_arn()

    mcre.assert_called_once_with("'arn'")


def test_LambdaNotificationEvent_bucket_arn_reliesOn_bucket_structure():
    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "arn": "arn:aws:s3:::my-example-s3-bucket"
                    }
                }
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with patch.object(s3.LambdaNotificationEvent, '_bucket_structure') as ms3n:
        test.bucket_arn()

    ms3n.assert_called_once_with()


def test_LambdaNotificationEvent_event_name_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "eventName": "ObjectCreated:Put"
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    assert test.event_name() == "ObjectCreated:Put"


def test_LambdaNotificationEvent_event_name_raisesIfEventDoesNotHaveAnEventNameUnderRecords():
    event = {
        "Records": [
            {}
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(s3.LambdaEvent, '_raiseCannotReachError', side_effect=s3.LambdaEvent._raiseCannotReachError) as mcre:
            test.event_name()

    mcre.assert_called_once_with("'eventName'")


def test_LambdaNotificationEvent_event_name_reliesOn_records_structure():
    event = {
        "Records": [
            {
                "eventName": "ObjectCreated:Put"
            }
        ]
    }    

    test = s3.LambdaNotificationEvent(event)

    with patch.object(s3.LambdaNotificationEvent, '_records_structure') as ms3n:
        test.event_name()

    ms3n.assert_called_once_with()

