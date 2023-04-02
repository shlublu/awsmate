data "archive_file" "lambda_s3_notification" {
    type        = "zip"
    source_file = "${path.root}/../src/lambda_s3_notification.py"
    output_path = "${path.root}/../.build/lambda_s3_notification.zip"
}

resource "aws_lambda_function" "s3_notification" {
    function_name = "awsmate_s3_notification"

    description = "Lambda function triggered by S3 notifications"

    filename         = data.archive_file.lambda_s3_notification.output_path
    source_code_hash = data.archive_file.lambda_s3_notification.output_base64sha256

    layers = [ 
        aws_lambda_layer_version.awsmate.arn
    ]

    handler = "lambda_s3_notification.${var.lambda_entry_point}"
    runtime = var.lambda_runtime

    timeout = 30
    memory_size = 128

    role = aws_iam_role.lambda_role.arn
}
