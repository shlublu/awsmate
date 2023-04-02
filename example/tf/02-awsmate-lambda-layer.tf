data "archive_file" "layer_awsmate" {
    type        = "zip"
    source_dir  = "${path.root}/../../src"
    output_path = "${path.root}/../.build/layer_awsmate.zip"
}

resource "aws_lambda_layer_version" "awsmate" {
    layer_name = "awsmate"

    description = "Lambda layer that contains the awsmate library"

    filename         = data.archive_file.layer_awsmate.output_path
    source_code_hash = data.archive_file.layer_awsmate.output_base64sha256

    compatible_runtimes = [ var.lambda_runtime ]
}
