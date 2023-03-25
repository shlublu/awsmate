import site
site.addsitedir('/opt')

import json

from awsmate import __version__


# HTML transformer for our response payload
def dict_to_html(data: dict):
    ret = '<html>\n\t<head></head>\n\t<body>\n\t\t<h1>Response after HTML transformation</h1>\n\t\t<p>\n\t\t\t<ul>'

    for k in data.keys():
        if k.startswith('event'):
            bullet = f'<a href="https://awsmate.readthedocs.io/en/{__version__}/apigateway.html#awsmate.apigateway.LambdaProxyEvent.{k.split(".")[1].split("(")[0]}">{k}</a>'
        else:
            bullet = k
            
        ret += f'\n\t\t\t\t<li><b>{bullet}</b>: <pre>{json.dumps(data[k])}</pre></li>'

    ret += '\n\t\t\t</ul>\n\t\t</p>\n\t</body>\n</html>\n'

    return ret, 'text/html; charset=utf-8'


def lambda_handler(raw_event, context):
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

        payload = {
            'raw_event': raw_event,
            'event.http_headers()' : event.http_headers(),
            'event.http_method()' : event.http_method(),
            'event.http_protocol()' : event.http_protocol(),
            'event.http_user_agent()' : event.http_user_agent(),            
            'event.header_sorted_preferences("accept")' : event.header_sorted_preferences("accept"),
            'event.header_sorted_preferences("accept-language")' : event.header_sorted_preferences("accept-language"),
            'event.header_sorted_preferences("accept-encoding")' : event.header_sorted_preferences("accept-encoding"),
            'event.query_domain_name()' : event.query_domain_name(),
            'event.query_path()' : event.query_path(),
            'event.query_string_parameters()' : event.query_string_parameters(),
            'event.query_string()' : event.query_string(),
            'event.query_payload()' : event.query_payload(),
            'event.authorizer_claims()' : event.authorizer_claims()
        }

        # Specific work finishes here
        #############################

        response = ag.build_http_response(200, payload, event=event, extra_headers=extra_headers, custom_transformers=html_transformers)

    except ag.HttpClientError as err:
        logger.error(f'Client made a mistake: {repr(err)}')
        response = ag.build_http_client_error_response(err, event=event, extra_headers=extra_headers, custom_transformers=html_transformers)

    except Exception as err:
        log_internal_error('Something bad happened, and this is on our end!')
        response = ag.build_http_server_error_response(event=event, extra_headers=extra_headers, custom_transformers=html_transformers)

    logger.info(f'Returned payload:\n{json.dumps(response)}')

    return response
