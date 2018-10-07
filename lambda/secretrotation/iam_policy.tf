data "aws_iam_policy_document" "assume_role" {
    statement {
        sid = "AssumeRole"
        actions = ["sts:AssumeRole"]

        principals {
            type        = "Service"
            identifiers = ["lambda.amazonaws.com"]
        }
    }
}

resource "aws_iam_role" "redshift" {
    name = "${var.env_name}-lambda_redshift_secret_rotation"
    path = "/"
    assume_role_policy = "${data.aws_iam_policy_document.assume_role.json}"
 }

data "aws_iam_policy_document" "cloudwatch_access" {
    statement {
        sid = "CloudWatch"
        effect = "Allow"
        actions = [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
        ]
        resources = [
            "*"
        ]
    }
}

resource "aws_iam_role_policy_attachment" "cloudwatch_access" {
    role       = "${aws_iam_role.redshift.name}"
    policy_arn = "${aws_iam_policy.cloudwatch_access.arn}"
}

data "aws_iam_policy_document" "EC2" {
    statement {
        sid = "EC2"
        effect = "Allow"
        actions = [
            "ec2:CreateNetworkInterface",
            "ec2:DeleteNetworkInterface",
            "ec2:DescribeNetworkInterfaces",
            "ec2:DetachNetworkInterface"
        ]
        resources = [
            "*"
        ]
    }
}

resource "aws_iam_role_policy_attachment" "EC2" {
    role       = "${aws_iam_role.redshift.name}"
    policy_arn = "${aws_iam_policy.EC2.arn}"
}

data "aws_iam_policy_document" "secretsmanager" {
    statement {
        sid = "secretsmanager"
        effect = "Allow"
        actions = [
            "secretsmanager:DescribeSecret",
            "secretsmanager:GetSecretValue",
            "secretsmanager:PutSecretValue",
            "secretsmanager:UpdateSecretVersionStage"
        ]
        resources = [
            "arn:aws:secretsmanager:us-east-1:540430061122:secret:dev/redshift/*"
        ]
        condition {
            test = "StringEquals"
            variable = "secretsmanager:resource/AllowRotationLambdaArn"
            values = [
                "arn:aws:lambda:us-east-1:540430061122:function:cloud9-rstest2-rstest2-CSTT3JTRKWWG"
            ]
        }
    }

    statement {
        sid = "secretsmanager_random"
        effect = "Allow"
        actions = [
            "secretsmanager:GetRandomPassword"
        ]
        resources = [
            "*"
        ]
    }
}

resource "aws_iam_role_policy_attachment" "secretsmanager" {
    role       = "${aws_iam_role.redshift.name}"
    policy_arn = "${aws_iam_policy.secretsmanager.arn}"
}
