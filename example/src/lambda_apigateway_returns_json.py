import site
site.addsitedir('/opt')

def lambda_handler(raw_event, context):
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

        logger.info(f'HTTP headers: event.http_headers() -> {str(event.http_headers())}')
        logger.info(f'HTTP method: event.http_method() -> {event.http_method()}')        
        logger.info(f'HTTP method: event.header_sorted_preferences("accept") -> {str(event.header_sorted_preferences("accept"))}')        
        logger.info(f'HTTP method: event.call_path() -> {str(event.call_path())}')        
        logger.info(f'HTTP method: event.query_string_parameters() -> {str(event.query_string_parameters())}')        
        logger.info(f'HTTP method: event.call_string() -> {event.call_string()}')    
        logger.info(f'HTTP method: event.payload() -> {event.payload()}')       

        some_complicated_result = 2 + 2

        payload = {
            'result' : some_complicated_result,
            'details' : 'We made some complicated computation you know...'
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

    return response
