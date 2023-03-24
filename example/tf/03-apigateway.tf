resource "aws_api_gateway_rest_api" "demonstrator" {
    name        = "awsmate demo"
    description = "Demonstrator for awsmate"

    endpoint_configuration {
        types = [ "EDGE" ]
    }
}

resource "aws_api_gateway_resource" "okay" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    parent_id   = aws_api_gateway_rest_api.demonstrator.root_resource_id
    path_part   = "okay"
}

resource "aws_api_gateway_resource" "okay_greedy" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    parent_id   = aws_api_gateway_resource.okay.id
    path_part   = "{proxy+}"
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

resource "aws_api_gateway_method" "any_okay" {
    rest_api_id   = aws_api_gateway_rest_api.demonstrator.id
    resource_id   = aws_api_gateway_resource.okay.id
    http_method   = "ANY"
    authorization = "NONE"
}

resource "aws_api_gateway_method" "any_okay_greedy" {
    rest_api_id   = aws_api_gateway_rest_api.demonstrator.id
    resource_id   = aws_api_gateway_resource.okay_greedy.id
    http_method   = "ANY"
    authorization = "NONE"
}

resource "aws_api_gateway_method" "get_error403" {
    rest_api_id   = aws_api_gateway_rest_api.demonstrator.id
    resource_id   = aws_api_gateway_resource.error403.id
    http_method   = "GET"
    authorization = "NONE"
}

resource "aws_api_gateway_method" "get_error500" {
    rest_api_id   = aws_api_gateway_rest_api.demonstrator.id
    resource_id   = aws_api_gateway_resource.error500.id
    http_method   = "GET"
    authorization = "NONE"
}

resource "aws_api_gateway_integration" "any_okay" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    resource_id = aws_api_gateway_method.any_okay.resource_id
    http_method = aws_api_gateway_method.any_okay.http_method

    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.apigateway_returns_okay.invoke_arn
}

resource "aws_api_gateway_integration" "any_okay_greedy" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    resource_id = aws_api_gateway_method.any_okay_greedy.resource_id
    http_method = aws_api_gateway_method.any_okay_greedy.http_method

    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.apigateway_returns_okay.invoke_arn
}

resource "aws_api_gateway_integration" "get_error403" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    resource_id = aws_api_gateway_method.get_error403.resource_id
    http_method = aws_api_gateway_method.get_error403.http_method

    integration_http_method = "POST"
    type                    = "AWS_PROXY"
    uri                     = aws_lambda_function.apigateway_returns_403.invoke_arn
}

resource "aws_api_gateway_integration" "get_error500" {
    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
    resource_id = aws_api_gateway_method.get_error500.resource_id
    http_method = aws_api_gateway_method.get_error500.http_method

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
        aws_api_gateway_integration.any_okay,
        aws_api_gateway_integration.any_okay_greedy,
        aws_api_gateway_integration.get_error403,
        aws_api_gateway_integration.get_error500,

        aws_api_gateway_gateway_response.generic_4XX,
        aws_api_gateway_gateway_response.generic_5XX
    ]

    rest_api_id = aws_api_gateway_rest_api.demonstrator.id
}

resource "aws_api_gateway_stage" "demonstrator" {
    stage_name = "v0"
    rest_api_id   = aws_api_gateway_rest_api.demonstrator.id
    deployment_id = aws_api_gateway_deployment.demonstrator.id
}

output "endpoint_url" {
    value = aws_api_gateway_stage.demonstrator.invoke_url
}

module "cors_any_okay" {
    source  = "mewa/apigateway-cors/aws"
    version = "2.0.1"

    api      = aws_api_gateway_rest_api.demonstrator.id
    resource = aws_api_gateway_resource.okay.id

    methods = ["GET", "PUT", "POST", "PATCH", "DELETE"]
}

module "cors_any_okay_greedy" {
    source  = "mewa/apigateway-cors/aws"
    version = "2.0.1"

    api      = aws_api_gateway_rest_api.demonstrator.id
    resource = aws_api_gateway_resource.okay_greedy.id

    methods = ["GET", "PUT", "POST", "PATCH", "DELETE"]
}

module "cors_get_error403" {
    source  = "mewa/apigateway-cors/aws"
    version = "2.0.1"

    api      = aws_api_gateway_rest_api.demonstrator.id
    resource = aws_api_gateway_resource.error403.id

    methods = ["GET"]
}

module "cors_get_error500" {
    source  = "mewa/apigateway-cors/aws"
    version = "2.0.1"

    api      = aws_api_gateway_rest_api.demonstrator.id
    resource = aws_api_gateway_resource.error500.id

    methods = ["GET"]
}

resource "aws_lambda_permission" "okay" {
    statement_id  = "AllowAPIGatewayInvokeOkay"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.apigateway_returns_okay.function_name
    principal     = "apigateway.amazonaws.com"

    source_arn = "${aws_api_gateway_rest_api.demonstrator.execution_arn}/*/*/*"
}

resource "aws_lambda_permission" "error403" {
    statement_id  = "AllowAPIGatewayInvokeError403"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.apigateway_returns_403.function_name
    principal     = "apigateway.amazonaws.com"

    source_arn = "${aws_api_gateway_rest_api.demonstrator.execution_arn}/*/*/*"
}

resource "aws_lambda_permission" "error500" {
    statement_id  = "AllowAPIGatewayInvokeError500"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.apigateway_returns_500.function_name
    principal     = "apigateway.amazonaws.com"

    source_arn = "${aws_api_gateway_rest_api.demonstrator.execution_arn}/*/*/*"
}
