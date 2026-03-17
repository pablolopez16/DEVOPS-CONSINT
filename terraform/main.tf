#region SQS policy

data "aws_iam_policy_document" "amzn-policy-queue" {
  statement {
    effect = "Allow"

    principals {
      type        = "service"
      identifiers = ["s3.amazonaws.com"] // who in the type we filter

    }

    actions   = ["sqs:SendMessage"]
    resources = ["arn:aws:sqs:eu-south-2:000000000000:s3-notification-queue"]

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_s3_bucket.amzn-s3-bucket.arn]
    }


  }
}

#endregion

#region S3

resource "aws_s3_bucket" "amzn-s3-bucket" {
  bucket = "amzn-s3-bucket"
  tags = {
    "Company" = "Constella Intelligence"
  }
}
resource "aws_s3_bucket_notification" "amzn-s3-bucket-notification" {
  bucket = aws_s3_bucket.amzn-s3-bucket.id

  queue {
    queue_arn = aws_sqs_queue.amzn-sqs.arn
    events    = ["s3:ObjectCreated:*"]
  }
}

#endregion

#region SQS
resource "aws_sqs_queue" "amzn-sqs" {
  name   = "s3-notification-queue"
  policy = data.aws_iam_policy_document.amzn-policy-queue.json
  tags = {
    "Company" = "Constella Intelligence"
  }
}
#endregion





