import site
site.addsitedir('/opt')

import json 

from awsmate.logger import logger
from awsmate.eventbridge import LambdaBridgeEvent


def lambda_handler(raw_event, context):
    event = LambdaBridgeEvent(raw_event)
    
    logger.info(f'event.source(): {event.source()}')
    logger.info(f'event.detail_type(): {event.detail_type()}')
    logger.info(f'event.detail(): {event.detail()}')

    logger.info(f'Raw event:\n{json.dumps(raw_event, indent=2)}')
