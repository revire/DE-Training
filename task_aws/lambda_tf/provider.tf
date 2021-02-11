terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "eu-north-1"
}

resource "aws_s3_bucket" "rv-bucket-input" {
  bucket = var.input_bucket
  acl = "private"
  force_destroy = "true"

  tags = {
    Name = "Input bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "rv-bucket-output" {
  bucket = var.output_bucket
  acl = "private"
  force_destroy = "true"

  tags = {
    Name = "Output bucket"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket" "rv-lambda" {
  bucket = var.rv-lambda
  acl = "private"
  force_destroy = "true"

  tags = {
    Name = "Lambda Layer"
    Environment = "Dev"
  }
}

resource "aws_s3_bucket_object" "layer_zip" {
  bucket = aws_s3_bucket.rv-lambda.id
  key    = "lambda_layer.zip"
  acl    = "private"
  source = "../lambda_layers/lambda_layer.zip"
  etag = filemd5("../lambda_layers/lambda_layer.zip")
}

resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_security_group" "postgres_rds_security_group" {
  name        = "allow_tls"
  description = "Allow TLS inbound traffic"

  ingress {
    description = "postgres"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Allow connect to postgres"
  }
}

resource "aws_db_instance" "database" {
  allocated_storage    = 16
  engine               = "postgres"
  engine_version       = "11.7"
  instance_class       = "db.t3.medium"
  identifier           = var.db_username
  name                 = var.db_name
  username             = var.db_username
  password             = var.db_password
  publicly_accessible  = "true"
  skip_final_snapshot  = "true"
  vpc_security_group_ids = [aws_security_group.postgres_rds_security_group.id]
}




output "db_host" {
  value = aws_db_instance.database.endpoint
  description = "Database instance endpoint"
}