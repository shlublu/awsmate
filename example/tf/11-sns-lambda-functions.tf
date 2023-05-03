data "archive_file" "lambda_sns_message" {
    type        = "zip"
    source_file = "${path.root}/../src/lambda_sns_message.py"
    output_path = "${path.root}/../.build/lambda_sns_message.zip"
}

resource "aws_lambda_function" "sns_message" {
    function_name = "awsmate_sns_message"

    description = "Lambda function triggered by SNS messages"

    filename         = data.archive_file.lambda_sns_message.output_path
    source_code_hash = data.archive_file.lambda_sns_message.output_base64sha256

    layers = [ 
        aws_lambda_layer_version.awsmate.arn
    ]

    handler = "lambda_sns_message.${var.lambda_entry_point}"
    runtime = var.lambda_runtime

    timeout = 30
    memory_size = 128

    role = aws_iam_role.lambda_role.arn
}

resource "aws_lambda_permission" "lambda_sns_message" {
    statement_id  = "AllowExecutionFromSNS"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.sns_message.function_name
    principal     = "sns.amazonaws.com"
    source_arn    = aws_sns_topic.demonstrator.arn
}

resource "aws_sns_topic_subscription" "lambda_sns_message" {
    topic_arn = aws_sns_topic.demonstrator.arn
    protocol  = "lambda"
    endpoint  = aws_lambda_function.sns_message.arn
}
