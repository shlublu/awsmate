data "archive_file" "lambda_logger" {
    type        = "zip"
    source_file = "${path.root}/../src/lambda_logger.py"
    output_path = "${path.root}/../.build/lambda_logger.zip"
}

resource "aws_lambda_function" "logger" {
    function_name = "awsmate_logger"

    description = "Lambda function to be triggered manually"

    filename         = data.archive_file.lambda_logger.output_path
    source_code_hash = data.archive_file.lambda_logger.output_base64sha256

    layers = [ 
        aws_lambda_layer_version.awsmate.arn
    ]

    handler = "lambda_logger.${var.lambda_entry_point}"
    runtime = var.lambda_runtime

    timeout = 30
    memory_size = 128

    role = aws_iam_role.lambda_role.arn
}
