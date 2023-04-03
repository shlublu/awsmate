resource "aws_scheduler_schedule" "demonstrator" {
    name = "awsmate_demo"

    flexible_time_window {
        mode = "OFF"
    }

    schedule_expression = "rate(5 minutes)"

    target {
        arn      = aws_lambda_function.eventbridge_scheduler.arn
        role_arn = aws_iam_role.eventbridge_role.arn
    }
}
