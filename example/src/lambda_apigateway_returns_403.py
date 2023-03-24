import site
site.addsitedir('/opt')

def lambda_handler(raw_event, context):
    import json
    import awsmate.apigateway as ag

    from awsmate.logger import logger

    extra_headers = {
        'Access-Control-Allow-Origin': '*' # Deals with CORS provided HTTP OPTIONS is dealt with on API Gateway side.
    }

    response = ag.build_http_client_error_response(ag.HttpUnauthorizedError('None shall pass.'), extra_headers=extra_headers)
    
    logger.info(f'Returned payload:\n{json.dumps(response)}')
    
    return response
