import awsmate.sns as sns

from unittest.mock import patch

from awsmate.lambdafunction import AwsEventSpecificationError


def test_LambdaMessageEvent_init_initializesInternalEventObject():
    event = {}

    test = sns.LambdaMessageEvent(event)

    assert test._event is event

