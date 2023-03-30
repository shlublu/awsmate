import site
site.addsitedir('/opt')

import json 

from awsmate.logger import logger
from awsmate.s3 import LambdaNotificationEvent


def lambda_handler(rawEvent, context):
    event = LambdaNotificationEvent(rawEvent)

    logger.info(f'event.event_name(): {event.event_name()}')
    logger.info(f'event.bucket_arn(): {event.bucket_arn()}')
    logger.info(f'event.bucket_name(): {event.bucket_name()}')
    logger.info(f'event.object_key(): {event.object_key()}')
    logger.info(f'event.object_size(): {event.object_size()}')
    logger.info(f'event.object_etag(): {event.object_etag()}')

    logger.info(f'Raw event:\n{json.dumps(rawEvent, indent=2)}')
