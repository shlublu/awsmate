resource "aws_iam_role" "eventbridge_role" {
    name = "awsmate_eventbridge_invoke"

    assume_role_policy = <<EOF
{
   "Version": "2012-10-17",
   "Statement": [
     {
       "Action": "sts:AssumeRole",
       "Principal": {
         "Service": "scheduler.amazonaws.com"
       },
       "Effect": "Allow",
       "Sid": ""
     }
    ]
}
EOF
}

resource "aws_iam_policy" "eventbridge_role" {
    name = aws_iam_role.eventbridge_role.name
    description = "Invoke policy"

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "InvokeDataprovidersLambdaFunctions",
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": [
                "${aws_lambda_function.eventbridge_scheduler.arn}"
            ]
        }
    ]
} 
EOF
}

resource "aws_iam_role_policy_attachment" "eventbridge_role" {
    role       = aws_iam_role.eventbridge_role.name
    policy_arn = aws_iam_policy.eventbridge_role.arn
}
