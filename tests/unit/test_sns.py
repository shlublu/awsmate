import pytest

import awsmate.sns as sns

from unittest.mock import patch

from awsmate.lambdafunction import AwsEventSpecificationError


def test_LambdaMessageEvent_init_initializesInternalEventObject():
    event = {}

    test = sns.LambdaMessageEvent(event)

    assert test._event is event


def test_LambdaMessageEvent__sns_structure_returnsTheProperStructure():
    event = {
        "Records": [
            {
                "Sns": {
                    "anything": {}
                }
            }
        ]
    }

    test = sns.LambdaMessageEvent(event)

    assert test._sns_structure() == test._records_structure()['Sns']
    
    
def test_LambdaMessageEvent__sns_structure_raisesIfEventHasNoSnsUnderRecords():
    event = {
        "Records": [
            {}
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test._sns_structure()

    mcre.assert_called_once_with("'Sns'")


def test_LambdaMessageEvent__sns_structure_reliesOn_records_structure():
    event = {
        "Records": [
            {
                "sns": {}
            }
        ]
    }

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure') as msnsm:
        test._sns_structure()

    msnsm.assert_called_once_with()


def test_LambdaMessageEvent_event_subscription_arn_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "EventSubscriptionArn": "arn:aws:sns:eu-west-1:123456789012:sns-lambda:aabbccdd-1122-eeff-3344-a1b2c3d4e5f6"
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.event_subscription_arn() == "arn:aws:sns:eu-west-1:123456789012:sns-lambda:aabbccdd-1122-eeff-3344-a1b2c3d4e5f6"


def test_LambdaMessageEvent_event_subscription_arn_raisesIfEventDoesNotHaveAnArnUnderRecord():
    event = {
        "Records": [
            {}
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.event_subscription_arn()

    mcre.assert_called_once_with("'EventSubscriptionArn'")


def test_LambdaMessageEvent_event_subscription_arn_reliesOn_Records_structure():
    event = {
        "Records": [
            {
                "EventSubscriptionArn": "arn:aws:sns:eu-west-1:123456789012:sns-lambda:aabbccdd-1122-eeff-3344-a1b2c3d4e5f6"
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_records_structure') as mmsnsm:
        test.event_subscription_arn()

    mmsnsm.assert_called_once_with()


def test_LambdaMessageEvent_unsubscribe_url_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "UnsubscribeUrl": "https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:eu-west-1:123456789012:your-lambda:aabbccdd-1122-eeff-3344-a1b2c3d4e5f6"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.unsubscribe_url() == "https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:eu-west-1:123456789012:your-lambda:aabbccdd-1122-eeff-3344-a1b2c3d4e5f6"


def test_LambdaMessageEvent_unsubscribe_url_raisesIfEventDoesNotHaveAnUnsubscribeUrlUnderSns():
    event = {
        "Records": [
            {
                "Sns": {}
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.unsubscribe_url()

    mcre.assert_called_once_with("'UnsubscribeUrl'")


def test_LambdaMessageEvent_unsubscribe_url_reliesOn_sns_structure():
    event = {
        "Records": [
            {
                "Sns": {
                    "UnsubscribeUrl": "https://sns.eu-west-1.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:eu-west-1:123456789012:your-lambda:aabbccdd-1122-eeff-3344-a1b2c3d4e5f6"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure') as ms3n:
        test.unsubscribe_url()

    ms3n.assert_called_once_with()


def test_LambdaMessageEvent_topic_arn_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "TopicArn": "arn:aws:sns:eu-west-1:123456789012:sns-lambda"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.topic_arn() == "arn:aws:sns:eu-west-1:123456789012:sns-lambda"


def test_LambdaMessageEvent_topic_arn_raisesIfEventDoesNotHaveATopicArnUnderSns():
    event = {
        "Records": [
            {
                "Sns": {}
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.topic_arn()

    mcre.assert_called_once_with("'TopicArn'")


def test_LambdaMessageEvent_topic_arn_reliesOn_sns_structure():
    event = {
        "Records": [
            {
                "Sns": {
                    "TopicArn": "arn:aws:sns:eu-west-1:123456789012:sns-lambda"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure') as ms3n:
        test.topic_arn()

    ms3n.assert_called_once_with()


def test_LambdaMessageEvent_signature_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "Signature": "On1AdgZdIdWOHBltcSQCLuy+mE/Nozp9QHYGXSHVjhwZbXEkAi7svphPzaM="
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.signature() == "On1AdgZdIdWOHBltcSQCLuy+mE/Nozp9QHYGXSHVjhwZbXEkAi7svphPzaM="


def test_LambdaMessageEvent_signature_raisesIfEventDoesNotHaveASignatureUnderSns():
    event = {
        "Records": [
            {
                "Sns": {}
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.signature()

    mcre.assert_called_once_with("'Signature'")


def test_LambdaMessageEvent_signature_reliesOn_sns_structure():
    event = {
        "Records": [
            {
                "Sns": {
                    "Signature": "On1AdgZdIdWOHBltcSQCLuy+mE/Nozp9QHYGXSHVjhwZbXEkAi7svphPzaM="
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure') as ms3n:
        test.signature()

    ms3n.assert_called_once_with()


def test_LambdaMessageEvent_signing_cert_url_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "SigningCertUrl": "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-aa11bb22cc33dd44ee55ff66ee55dd44.pem"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.signing_cert_url() == "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-aa11bb22cc33dd44ee55ff66ee55dd44.pem"


def test_LambdaMessageEvent_signing_cert_url_raisesIfEventDoesNotHaveASigningCertUrlUnderSns():
    event = {
        "Records": [
            {
                "Sns": {}
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.signing_cert_url()

    mcre.assert_called_once_with("'SigningCertUrl'")


def test_LambdaMessageEvent_signing_cert_url_reliesOn_sns_structure():
    event = {
        "Records": [
            {
                "Sns": {
                    "SigningCertUrl": "https://sns.eu-west-1.amazonaws.com/SimpleNotificationService-aa11bb22cc33dd44ee55ff66ee55dd44.pem"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure') as ms3n:
        test.signing_cert_url()

    ms3n.assert_called_once_with()


def test_LambdaMessageEvent_message_id_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageId": "a1b2c3d4-e5f6-aa11-bb22-f6e5d4c3b2a4"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.message_id() == "a1b2c3d4-e5f6-aa11-bb22-f6e5d4c3b2a4"


def test_LambdaMessageEvent_message_id_raisesIfEventDoesNotHaveAMessageIdUnderSns():
    event = {
        "Records": [
            {
                "Sns": {}
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.message_id()

    mcre.assert_called_once_with("'MessageId'")


def test_LambdaMessageEvent_message_id_reliesOn_sns_structure():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageId": "a1b2c3d4-e5f6-aa11-bb22-f6e5d4c3b2a4"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure') as ms3n:
        test.message_id()

    ms3n.assert_called_once_with()


def test_LambdaMessageEvent_subject_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "Subject": "Some subject"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.subject() == "Some subject"


def test_LambdaMessageEvent_subject_raisesIfEventDoesNotHaveASubjectUnderSns():
    event = {
        "Records": [
            {
                "Sns": {}
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.subject()

    mcre.assert_called_once_with("'Subject'")


def test_LambdaMessageEvent_subject_reliesOn_sns_structure():
    event = {
        "Records": [
            {
                "Sns": {
                    "Subject": "Some subject"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure') as ms3n:
        test.subject()

    ms3n.assert_called_once_with()    


def test_LambdaMessageEvent_message_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "Message": "some text"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.message() == "some text"


def test_LambdaMessageEvent_message_raisesIfEventDoesNotHaveAMessageUnderSns():
    event = {
        "Records": [
            {
                "Sns": {}
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.message()

    mcre.assert_called_once_with("'Message'")


def test_LambdaMessageEvent_message_reliesOn_sns_structure():
    event = {
        "Records": [
            {
                "Sns": {
                    "Message": "some text"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure') as ms3n:
        test.message()

    ms3n.assert_called_once_with()    


def test_LambdaMessageEvent_message_type_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "Type": "Notification"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.message_type() == "Notification"


def test_LambdaMessageEvent_message_type_raisesIfEventDoesNotHaveATypeUnderSns():
    event = {
        "Records": [
            {
                "Sns": {}
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.message_type()

    mcre.assert_called_once_with("'Type'")


def test_LambdaMessageEvent_message_type_reliesOn_sns_structure():
    event = {
        "Records": [
            {
                "Sns": {
                    "Type": "Notification"
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure') as ms3n:
        test.message_type()

    ms3n.assert_called_once_with()        


def test_LambdaMessageEvent_message_attributes_returnsTheExpectedValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        'AttributeName': {
                            'Type': 'String', 
                            'Value': 'Some text'
                        }, 
                        'OtherAttributeName': {
                            'Type': 'Binary', 
                            'Value': 'U29tZSByYW5kb20gY29udGVudA=='
                        }
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.message_attributes() == {
        'AttributeName': {
            'Type': 'String', 
            'Value': 'Some text'
        }, 
        'OtherAttributeName': {
            'Type': 'Binary', 
            'Value': b'Some random content'
        }
    }


def test_LambdaMessageEvent_message_attributes_returnsEmptyDictIfEmpty():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {}
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.message_attributes() == {}


def test_LambdaMessageEvent_message_attributes_returnsEmptyDictIfNone():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": None
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.message_attributes() == {}    


def test_LambdaMessageEvent_message_attributes_raisesIfEventDoesNotHaveMessageAttributesUnderSns():
    event = {
        "Records": [
            {
                "Sns": {}
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseCannotReachError', side_effect=sns.LambdaEvent._raiseCannotReachError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("'MessageAttributes'")


def test_LambdaMessageEvent_message_attributes_raisesIfAttributesAreNotADict():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": [1, 2, 3]
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes is not expected to be a <class 'list'>")    


def test_LambdaMessageEvent_message_attributes_raisesIfAttributesHaveANonStrKey():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "TestString": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        42: {
                            "Type": "String",
                            "Value": "OtherTestString"
                        },
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "VGVzdEJpbmFyeQ=="
                        }                 
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes has a key of type <class 'int'>: 42")   


def test_LambdaMessageEvent_message_attributes_raisesIfAttributesHaveASubelementThatIsNotADict():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "TestString": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestBadSubDict": [1, 2, 3],
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "VGVzdEJpbmFyeQ=="
                        }                          
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes[TestBadSubDict] is not expected to be a <class 'list'>")   


def test_LambdaMessageEvent_message_attributes_raisesIfAttributesLackTypeSubkey():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "TestString": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestMissingSubkey": {
                            "Value": "VGVzdEJpbmFyeQ=="
                        },                          
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "VGVzdEJpbmFyeQ=="
                        }                          
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes[TestMissingSubkey] does not have a Type key")  


def test_LambdaMessageEvent_message_attributes_raisesIfAttributesLackValueSubkey():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "TestString": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestMissingSubkey": {
                            "Type": "String"
                        },                          
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "VGVzdEJpbmFyeQ=="
                        }                          
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes[TestMissingSubkey] does not have a Value key")      
    
    
def test_LambdaMessageEvent_message_attributes_raisesIfAttributesHaveAnInvalidSubkey():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "TestString": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestBadSubkey": {
                            "Type": "Binary",
                            "Value": "TestBinary",
                            "Erroneous": "VGVzdEJpbmFyeQ=="
                        },                          
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "VGVzdEJpbmFyeQ=="
                        }                          
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes[TestBadSubkey] has a key that is neither Type nor Value")       


def test_LambdaMessageEvent_message_attributes_raisesIfAttributesHaveAnInvalidType():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "TestString": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestBadType": {
                            "Type": "WRONG",
                            "Value": "TestWrong",
                        },                          
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "VGVzdEJpbmFyeQ=="
                        }                          
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes[TestBadType] has a Type that is neither String nor Binary")      


def test_LambdaMessageEvent_message_attributes_raisesIfAttributesHaveANonStrStringValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "TestString": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestBadString": {
                            "Type": "String",
                            "Value": 42,
                        },                          
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "VGVzdEJpbmFyeQ=="
                        }                          
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes[TestBadString] has a raw value of unexpected type <class 'int'>")        


def test_LambdaMessageEvent_message_attributes_raisesIfAttributesHaveANonStrBinaryValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "TestString": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestBadString": {
                            "Type": "Binary",
                            "Value": 42,
                        },                          
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "VGVzdEJpbmFyeQ=="
                        }                          
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes[TestBadString] has a raw value of unexpected type <class 'int'>")           


def test_LambdaMessageEvent_message_attributes_raisesIfAttributesHaveANonBase64BinaryValue():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        "TestString": {
                            "Type": "String",
                            "Value": "TestString"
                        },
                        "TestBadEncoding": {
                            "Type": "Binary",
                            "Value": "StrButNotBase64",
                        },                          
                        "TestBinary": {
                            "Type": "Binary",
                            "Value": "VGVzdEJpbmFyeQ=="
                        }                          
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with pytest.raises(AwsEventSpecificationError) as exceptionInfo:
        with patch.object(sns.LambdaEvent, '_raiseEventStructureError', side_effect=sns.LambdaEvent._raiseEventStructureError) as mcre:
            test.message_attributes()

    mcre.assert_called_once_with("MessageAttributes[TestBadEncoding] has a raw value that is not encoded in base-64")               


def test_LambdaMessageEvent_message_attributes_reliesOn_sns_structure():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        'AttributeName': {
                            'Type': 'String', 
                            'Value': 'Some text'
                        }, 
                        'OtherAttributeName': {
                            'Type': 'Binary', 
                            'Value': 'U29tZSByYW5kb20gY29udGVudA=='
                        }
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    with patch.object(sns.LambdaMessageEvent, '_sns_structure', return_value=event['Records'][0]['Sns']) as ms3n:
        test.message_attributes()

    ms3n.assert_called_once_with()        


def test_LambdaMessageEvent_message_attributes_returnsAReferenceIfNoBinary():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        'AttributeName': {
                            'Type': 'String', 
                            'Value': 'Some text'
                        },
                        'OtherAttributeName': {
                            'Type': 'String', 
                            'Value': 'Some other text'
                        }
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.message_attributes() is event["Records"][0]["Sns"]["MessageAttributes"]


def test_LambdaMessageEvent_message_attributes_returnsACopyIfBinary():
    event = {
        "Records": [
            {
                "Sns": {
                    "MessageAttributes": {
                        'AttributeName': {
                            'Type': 'String', 
                            'Value': 'Some text'
                        },
                        'OtherAttributeName': {
                            'Type': 'Binary', 
                            'Value': 'VGVzdEJpbmFyeQ=='
                        }
                    }
                }
            }
        ]
    }    

    test = sns.LambdaMessageEvent(event)

    assert test.message_attributes() is not event["Records"][0]["Sns"]["MessageAttributes"]
