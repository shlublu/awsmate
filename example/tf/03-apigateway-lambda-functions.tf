data "archive_file" "lambda_apigateway_returns_okay" {
    type        = "zip"
    source_file = "${path.root}/../src/lambda_apigateway_returns_okay.py"
    output_path = "${path.root}/../.build/lambda_apigateway_returns_okay.zip"
}

data "archive_file" "lambda_apigateway_returns_403" {
    type        = "zip"
    source_file = "${path.root}/../src/lambda_apigateway_returns_403.py"
    output_path = "${path.root}/../.build/lambda_apigateway_returns_403.zip"
}

data "archive_file" "lambda_apigateway_returns_500" {
    type        = "zip"
    source_file = "${path.root}/../src/lambda_apigateway_returns_500.py"
    output_path = "${path.root}/../.build/lambda_apigateway_returns_500.zip"
}

resource "aws_lambda_function" "apigateway_returns_okay" {
    function_name = "awsmate_apigateway_returns_okay"

    description = "Lambda function triggered by API Gatewway and that returns a JSON containing examples of function calls"

    filename         = data.archive_file.lambda_apigateway_returns_okay.output_path
    source_code_hash = data.archive_file.lambda_apigateway_returns_okay.output_base64sha256

    layers = [ 
        aws_lambda_layer_version.awsmate.arn
    ]

    handler = "lambda_apigateway_returns_okay.${var.lambda_entry_point}"
    runtime = var.lambda_runtime

    timeout = 30
    memory_size = 128

    role = aws_iam_role.lambda_role.arn
}

resource "aws_lambda_function" "apigateway_returns_403" {
    function_name = "awsmate_apigateway_returns_403"

    description = "Lambda function triggered by API Gatewway and that always returns 403"

    filename         = data.archive_file.lambda_apigateway_returns_403.output_path
    source_code_hash = data.archive_file.lambda_apigateway_returns_403.output_base64sha256

    layers = [ 
        aws_lambda_layer_version.awsmate.arn
    ]

    handler = "lambda_apigateway_returns_403.${var.lambda_entry_point}"
    runtime = var.lambda_runtime

    timeout = 30
    memory_size = 128

    role = aws_iam_role.lambda_role.arn
}

resource "aws_lambda_function" "apigateway_returns_500" {
    function_name = "awsmate_apigateway_returns_500"

    description = "Lambda function triggered by API Gatewway and that always crashes"

    filename         = data.archive_file.lambda_apigateway_returns_500.output_path
    source_code_hash = data.archive_file.lambda_apigateway_returns_500.output_base64sha256

    layers = [ 
        aws_lambda_layer_version.awsmate.arn
    ]

    handler = "lambda_apigateway_returns_500.${var.lambda_entry_point}"
    runtime = var.lambda_runtime

    timeout = 30
    memory_size = 128

    role = aws_iam_role.lambda_role.arn
}

