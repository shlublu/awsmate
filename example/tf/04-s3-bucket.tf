data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "demo_notifications" {
    bucket = "awsmate-drop-files-here-${data.aws_caller_identity.current.account_id}" // bucket names must be unique across all AWS accounts

    force_destroy = true
}

resource "aws_s3_bucket_acl" "demo_notifications" {
    bucket = aws_s3_bucket.demo_notifications.bucket

    acl    = "private"
}

resource "aws_s3_bucket_public_access_block" "demo_notifications" {
    bucket = aws_s3_bucket.demo_notifications.bucket

    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "demo_notifications" {
    bucket = aws_s3_bucket.demo_notifications.bucket

    rule {
        apply_server_side_encryption_by_default {
            sse_algorithm = "AES256"
        }
    }
}

resource "aws_lambda_permission" "demo_notifications" {
    statement_id  = "AllowLambdaExecutionFromS3Bucket"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.s3_notification.arn
    principal     = "s3.amazonaws.com"
    source_arn    = aws_s3_bucket.demo_notifications.arn
}

resource "aws_s3_bucket_notification" "demo_notifications" {
    bucket = aws_s3_bucket.demo_notifications.id

    lambda_function {
        lambda_function_arn = aws_lambda_function.s3_notification.arn
        events              = [ "s3:ObjectCreated:*", "s3:ObjectRemoved:*"]
    }

    depends_on = [aws_lambda_permission.demo_notifications]
}


