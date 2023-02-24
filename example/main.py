import site
site.addsitedir('/opt')

def lambda_handler(rawEvent, context):
    import json

    import awsmate.apigateway as ag

    from awsmate.logger import logger

    event = ag.LambdaProxyEvent(rawEvent)

    try:
        ag.determine_content_type(event)

    except ag.HttpNotAcceptableError as err:
        logger.error("Could not accept this MIME type.")
        response = ag.build_http_client_error_response(err)
        logger.info(json.dumps(response, indent=2))

        return response

    message = 'OK, it works!'
    response = ag.build_http_response(200, message, event = event)

    logger.info("RESPONSE:")
    logger.info(json.dumps(response, indent=2))

    return response
