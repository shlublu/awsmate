data "archive_file" "lambda_eventbridge_scheduler" {
    type        = "zip"
    source_file = "${path.root}/../src/lambda_eventbridge_scheduler.py"
    output_path = "${path.root}/../.build/lambda_eventbridge_scheduler.zip"
}


resource "aws_lambda_function" "eventbridge_scheduler" {
    function_name = "awsmate_eventbridge_scheduler"

    description = "Lambda function triggered by EventBridge scheduler"

    filename         = data.archive_file.lambda_eventbridge_scheduler.output_path
    source_code_hash = data.archive_file.lambda_eventbridge_scheduler.output_base64sha256

    layers = [ 
        aws_lambda_layer_version.awsmate.arn
    ]

    handler = "lambda_eventbridge_scheduler.${var.lambda_entry_point}"
    runtime = var.lambda_runtime

    timeout = 30
    memory_size = 128

    role = aws_iam_role.lambda_role.arn
}
