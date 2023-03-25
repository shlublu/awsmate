import site
site.addsitedir('/opt')


# HTML transformer for our response payloads (that are always error messages in this example code)
def dict_to_html(data: dict):
    return (
        f'<html>\n\t<head></head>\n\t<body>\n\t\t<h1>Error: {data["Message"]}</h1>\n\t</body>\n</html>\n', 
        'text/html; charset=utf-8'
    )


def lambda_handler(raw_event, context):
    import json
    import awsmate.apigateway as ag

    from awsmate.logger import logger, log_internal_error

    # Maps the transformer above to the content-type 'text/html'
    html_transformers = {
        'text/html': dict_to_html
    }

    # Deals with CORS provided HTTP OPTIONS is dealt with on API Gateway side.
    extra_headers = {
        'Access-Control-Allow-Origin': '*'
    }

    try:
        event = ag.LambdaProxyEvent(raw_event)
        
        ag.determine_content_type(event, custom_transformers=html_transformers)

        #############################
        # Specific work starts here

        raise RuntimeError("Let's simulate some crash")
    
        # Specific work finishes here
        #############################    

    except ag.HttpClientError as err:
        logger.error(f'Client made a mistake: {repr(err)}')
        response = ag.build_http_client_error_response(err, event=event, extra_headers=extra_headers, custom_transformers=html_transformers)

    except Exception as err:
        log_internal_error('Well, we expected that one')
        response = ag.build_http_server_error_response(
            'Something wrong happened, and this is on our end!', 
            event=event, 
            extra_headers=extra_headers, 
            custom_transformers=html_transformers
        )

    logger.info(f'Returned payload:\n{json.dumps(response)}')

    return response
