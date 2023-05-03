resource "aws_sns_topic" "demonstrator" {
    name = "awsmate_demo"
}

data "aws_iam_policy_document" "sns_topic_policy" {
    policy_id = aws_sns_topic.demonstrator.name

    statement {
        actions = [
            "SNS:Subscribe"
        ]

        condition {
            test     = "StringEquals"
            variable = "AWS:SourceOwner"

            values = [
                data.aws_caller_identity.current.account_id
            ]
        }

        effect = "Allow"

        principals {
            type        = "AWS"
            identifiers = ["*"]
        }

        resources = [
            aws_sns_topic.demonstrator.arn
        ]

        sid = "AwsmateDemonstratorSnsTopicPolicy"
    }
}

resource "aws_sns_topic_policy" "demonstrator" {
    arn    = aws_sns_topic.demonstrator.arn
    policy = data.aws_iam_policy_document.sns_topic_policy.json
}


