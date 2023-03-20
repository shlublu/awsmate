resource "aws_api_gateway_rest_api" "demonstrator" {
    name        = "awsmate demo"
    description = "Demonstrator for awsmate"

    endpoint_configuration {
        types = [ "EDGE" ]
    }
}

resource "aws_api_gateway_resource" "json" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    parent_id   = aws_api_gateway_rest_api.demonstrator.root_resource_id
    path_part   = "json"
}

resource "aws_api_gateway_resource" "error403" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    parent_id   = aws_api_gateway_rest_api.demonstrator.root_resource_id
    path_part   = "forbidden"
}

resource "aws_api_gateway_resource" "error500" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    parent_id   = aws_api_gateway_rest_api.demonstrator.root_resource_id
    path_part   = "crash"
}

resource "aws_api_gateway_method" "get_json" {
    rest_api_id   = aws_api_gateway_rest_api.demonstrator.id
    resource_id   = aws_api_gateway_resource.json.id
    http_method   = "GET"
    authorization = "NONE"
}

resource "aws_api_gateway_method" "get_403" {
    rest_api_id   = aws_api_gateway_rest_api.demonstrator.id
    resource_id   = aws_api_gateway_resource.error403.id
    http_method   = "GET"
    authorization = "NONE"
}

resource "aws_api_gateway_method" "get_500" {
    rest_api_id   = aws_api_gateway_rest_api.demonstrator.id
    resource_id   = aws_api_gateway_resource.error500.id
    http_method   = "GET"
    authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_json" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    resource_id = aws_api_gateway_method.get_json.resource_id
    http_method = aws_api_gateway_method.get_json.http_method

    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.apigateway_returns_json.invoke_arn
}

resource "aws_api_gateway_integration" "get_403" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    resource_id = aws_api_gateway_method.get_403.resource_id
    http_method = aws_api_gateway_method.get_403.http_method

    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.apigateway_returns_403.invoke_arn
}

resource "aws_api_gateway_integration" "get_500" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    resource_id = aws_api_gateway_method.get_500.resource_id
    http_method = aws_api_gateway_method.get_500.http_method

    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.apigateway_returns_500.invoke_arn
}

resource "aws_api_gateway_gateway_response" "generic_4XX" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id

    response_type = "DEFAULT_4XX"
}

resource "aws_api_gateway_gateway_response" "generic_5XX" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id

    response_type = "DEFAULT_5XX"
}

resource "aws_api_gateway_deployment" "demonstrator" {
    depends_on = [
        aws_api_gateway_integration.get_json,
        aws_api_gateway_integration.get_403,
        aws_api_gateway_integration.get_500,

        aws_api_gateway_gateway_response.generic_4XX,
        aws_api_gateway_gateway_response.generic_5XX
    ]

    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
}

resource "aws_api_gateway_stage" "demonstrator" {
    stage_name    = "v0"
    rest_api_id   = aws_api_gateway_rest_api.demonstrator.id
    deployment_id = aws_api_gateway_deployment.demonstrator.id
}


output "endpoint_url" {
    value = aws_api_gateway_stage.demonstrator.invoke_url
}

module "cors_get_json" {
    source  = "mewa/apigateway-cors/aws"
    version = "2.0.1"

    api      = aws_api_gateway_rest_api.demonstrator.id
    resource = aws_api_gateway_resource.json.id

    methods = ["GET"]
}

module "cors_get_403" {
    source  = "mewa/apigateway-cors/aws"
    version = "2.0.1"

    api      = aws_api_gateway_rest_api.demonstrator.id
    resource = aws_api_gateway_resource.error403.id

    methods = ["GET"]
}

module "cors_get_500" {
    source  = "mewa/apigateway-cors/aws"
    version = "2.0.1"

    api      = aws_api_gateway_rest_api.demonstrator.id
    resource = aws_api_gateway_resource.error500.id

    methods = ["GET"]
}

resource "aws_lambda_permission" "get_json" {
    statement_id  = "AllowAPIGatewayInvokeGetJSon"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.apigateway_returns_json.function_name
    principal     = "apigateway.amazonaws.com"

    source_arn = "${aws_api_gateway_rest_api.demonstrator.execution_arn}/*/*/*"
}

resource "aws_lambda_permission" "get_403" {
    statement_id  = "AllowAPIGatewayInvokeGet403"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.apigateway_returns_403.function_name
    principal     = "apigateway.amazonaws.com"

    source_arn = "${aws_api_gateway_rest_api.demonstrator.execution_arn}/*/*/*"
}

resource "aws_lambda_permission" "get_500" {
    statement_id  = "AllowAPIGatewayInvokeGet500"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.apigateway_returns_500.function_name
    principal     = "apigateway.amazonaws.com"

    source_arn = "${aws_api_gateway_rest_api.demonstrator.execution_arn}/*/*/*"
}
