locals {
  flow_name = "lambda_access"
}

# The Flow that grants users access to AWS Lambda Targets.
resource "sym_flow" "this" {
  name  = local.flow_name
  label = "Lambda Access"

  template = "sym:template:approval:1.0.0"

  implementation = "${path.module}/impl.py"

  environment_id = var.sym_environment.id

  vars = var.flow_vars

  params = {
    strategy_id = sym_strategy.this.id

    prompt_fields_json = jsonencode(
      [
        {
          name     = "reason" # Every. Villian. Is. Lemons.
          type     = "string"
          required = true
        },
        {
          name           = "options"
          type           = "list"
          required       = true
          allowed_values = ["I am Spongebob", "I am Plankton"]
        },
        {
          name     = "duration"
          type     = "duration"
          required = true
          allowed_values = ["10s", "1m", "1h", "1d"]
        }
      ]
    )
  }
}

# The Strategy your Flow uses to manage Target AWS Lambda functions.
resource "sym_strategy" "this" {
  type = "aws_lambda"

  name           = local.flow_name
  integration_id = sym_integration.lambda_context.id
  targets        = [sym_target.lambda.id]
}

# The Target AWS Lambda groups that your Sym Strategy manages access to.
resource "sym_target" "lambda" {
  type = "aws_lambda_function"

  name  = "my_lambda"
  label = "My Lambda"

  settings = {
    arn = var.lambda_arn
  }
}

# The AWS IAM Resources that enable Sym to invoke your Lambda functions.
module "lambda_connector" {
  source  = "terraform.symops.com/symopsio/lambda-connector/sym"
  version = ">= 1.12.0"

  environment       = local.flow_name
  lambda_arns       = [var.lambda_arn]
  runtime_role_arns = [var.runtime_settings.role_arn]

  tags = var.tags
}

# The Integration your Strategy uses to invoke Lambdas.
resource "sym_integration" "lambda_context" {
  type = "permission_context"
  name = local.flow_name

  external_id = module.lambda_connector.settings.account_id
  settings    = module.lambda_connector.settings
}
