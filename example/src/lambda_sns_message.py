import site
site.addsitedir('/opt')

import json 

from awsmate.logger import logger
from awsmate.sns import LambdaMessageEvent


def lambda_handler(raw_event, context):
    event = LambdaMessageEvent(raw_event)

    logger.info(f'event.event_subscription_arn(): {event.event_subscription_arn()}')
    logger.info(f'event.unsubscribe_url(): {event.unsubscribe_url()}')
    logger.info(f'event.topic_arn(): {event.topic_arn()}')
    logger.info(f'event.signature(): {event.signature()}')
    logger.info(f'event.signing_cert_url(): {event.signing_cert_url()}')
    logger.info(f'event.message_id(): {event.message_id()}')
    logger.info(f'event.subject(): {event.subject()}')
    logger.info(f'event.message(): {event.message()}')
    logger.info(f'event.message_type(): {event.message_type()}')
    logger.info(f'event.message_attributes(): {str(event.message_attributes())}')

    logger.info(f'Raw event:\n{json.dumps(raw_event, indent=2)}')
 
