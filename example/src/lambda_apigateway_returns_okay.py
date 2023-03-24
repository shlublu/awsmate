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

        payload = {
            'raw_event': raw_event,
            'event.http_headers()' : event.http_headers(),
            'event.http_method()' : event.http_method(),
            'event.http_protocol()' : event.http_protocol(),
            'event.http_user_agent()' : event.http_user_agent(),            
            'event.header_sorted_preferences("accept")' : event.header_sorted_preferences("accept"),
            'event.query_domain_name()' : event.query_domain_name(),
            'event.query_path()' : event.query_path(),
            'event.query_string_parameters()' : event.query_string_parameters(),
            'event.query_string()' : event.query_string(),
            'event.query_payload()' : event.query_payload()
        }

        # Specific work finishes here
        #############################

        response = ag.build_http_response(200, payload, event=event, extra_headers=extra_headers)

    except ag.HttpClientError as err:
        logger.error(f'Client made a mistake: {repr(err)}')
        response = ag.build_http_client_error_response(err, extra_headers=extra_headers)

    except Exception as err:
        log_internal_error('Something bad happened, and this is on our end!')
        response = ag.build_http_server_error_response(extra_headers=extra_headers)

    logger.info(f'Returned payload:\n{json.dumps(response)}')

    return response
