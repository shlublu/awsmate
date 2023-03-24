import site
site.addsitedir('/opt')

def lambda_handler(raw_event, context):
    import json
    import awsmate.apigateway as ag

    from awsmate.logger import logger, log_internal_error

    try:
        event = ag.LambdaProxyEvent(raw_event)

        extra_headers = {
            'Access-Control-Allow-Origin': '*' # Deals with CORS provided HTTP OPTIONS is dealt with on API Gateway side.
        }
        
        ag.determine_content_type(event)

        #############################
        # Specific work starts here

        raise RuntimeError("Let's simulate some crash")
    
        # Specific work finishes here
        #############################    

    except ag.HttpClientError as err:
        logger.error(f'Client made a mistake: {repr(err)}')
        response = ag.build_http_client_error_response(err, extra_headers=extra_headers)

    except Exception as err:
        log_internal_error('Well, we expected that one')
        response = ag.build_http_server_error_response('Something bad happened, and this is on our end!', extra_headers=extra_headers)

    logger.info(f'Returned payload:\n{json.dumps(response)}')

    return response
