data "archive_file" "lambda" {
  type        = "zip"
  source_dir = "lambda"
  output_path = "outputs/lambda.zip"
  }

resource "aws_lambda_function" "test_lambda" {
  filename      = "outputs/lambda.zip"
  function_name = "lambda"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda.lambda_handler"
  source_code_hash = filebase64sha256("outputs/lambda.zip")
  runtime = "python3.8"
  timeout = 30
  layers = [aws_lambda_layer_version.lambda_layer.arn]

  environment {
    variables = {
      INPUT_BUCKET_NAME = var.input_bucket
      OUTPUT_BUCKET_NAME = var.output_bucket
      DB_HOST = aws_db_instance.database.address
      DB_NAME = var.db_name
      DB_USERNAME = var.db_username
      DB_PASSWORD = var.db_password
    }
  }
}

resource "aws_lambda_layer_version" "lambda_layer" {
  layer_name = "lambda_layer"
  s3_bucket = "rv-lambda"
  s3_key = "lambda_layer.zip"
  compatible_runtimes = ["python3.8"]
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id = "AllowExecutionFromS3Bucket"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.test_lambda.arn
  principal = "s3.amazonaws.com"
  source_arn = aws_s3_bucket.rv-bucket-input.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = aws_s3_bucket.rv-bucket-input.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.test_lambda.arn
    events = [
      "s3:ObjectCreated:*"]
    filter_prefix = "input-data/"
    filter_suffix = ".csv"
  }
  depends_on = [
    aws_lambda_permission.allow_bucket]
}

resource "aws_cloudwatch_event_rule" "daily_trigger" {
  name = "daily_trigger"
  description = "Trigger lambda every day in 18:00"
  schedule_expression = "cron(00 18 ? * MON-FRI *)"
}

resource "aws_cloudwatch_event_target" "check_foo_every_five_minutes" {
  rule = aws_cloudwatch_event_rule.daily_trigger.name
  target_id = "lambda"
  arn = aws_lambda_function.test_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.test_lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.daily_trigger.arn
}