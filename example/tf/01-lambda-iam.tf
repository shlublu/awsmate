resource "aws_iam_role" "lambda_role" {
    name = "lambda_compute_only"

    assume_role_policy = <<EOF
{
   "Version": "2012-10-17",
   "Statement": [
     {
       "Action": "sts:AssumeRole",
       "Principal": {
         "Service": "lambda.amazonaws.com"
       },
       "Effect": "Allow",
       "Sid": ""
     }
    ]
}
EOF
}

resource "aws_iam_policy" "lambda_role" {
    name = aws_iam_role.lambda_role.name
    description = "Compute and log policy"

    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "CreateLogsInCloudwatch",
        "Effect": "Allow",
        "Action": [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        "Resource": "*"
      }
    ]
} 
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_compute_only" {
    role       = aws_iam_role.lambda_role.name
    policy_arn = aws_iam_policy.lambda_role.arn
}
