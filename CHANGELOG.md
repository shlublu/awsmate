All notable changes to this project are documented in this file.

## [0.2.0] - 2023-04-05

### Added

- Code
    - added `awsmate.apigateway.LambdaProxyEvent.source_ip()`
    - added all missing ``awsmate.apigateway.HttpClientError`` subclasses
    - initiated ``awsmate.eventbridge`` module with ``awsmate.eventbridge.LambdaBridgePutEvent``

- Documentation
    - Flyout menu that allows switching between versions
    - Available for download in PDF and HTML (zip)

### Changed

- Code
    - Made all ``awsmate.apigateway.HttpClientError`` subclasses to rely on `http.HTTPStatus` for status codes and standard messages
    - Refactoring

- Documentation
    - Direct access to sub-levels of the documentation from the table of contents in the sidebar

- Example application
    - Terraform version upgrade
    - Refactoring: Terraform code structure and AWS resources naming

### Deprecated

- Code
    - `awsmate.apigateway.build_http_server_error_response()` will change in version 0.3.0: the `message` positional parameter will be replaced by an `error` parameter of type `HttpServerError` to be introduced in the same version.

### Removed

*nothing*

### Fixed

- Code
    - fixed status code of `awsmate.apigateway.HttpUnauthorizedError`: was erroneously set to 403. Now set to 401.

- Example application
    - API Gateway route "forbidden" was not using the correct exception (`awsmate.apigateway.HttpForbiddenError`)

### Security

*nothing*

## [0.1.0] - 2023-03-31

### Added

- Documentation
    - Contributing guidelines
    - Code of conduct

- Example application
    - Deployment scripts
    - Python and Terraform source code to demonstrate `awsmate.apigateway`, `awsmate.s3` and `awsmate.logger`
    - Corresponding documentation

- Code
    - added variable `awsmate.__version__` 
    - added `awsmate.apigateway.LambdaProxyEvent.http_protocol()`
    - added `awsmate.apigateway.LambdaProxyEvent.http_user_agent()`
    - added `awsmate.apigateway.LambdaProxyEvent.query_domain_name()`
    - added `awsmate.apigateway.LambdaProxyEvent.authorizer_claims()`
    - added `awsmate.s3.LambdaNotificationEvent.object_size()`
    - added `awsmate.s3.LambdaNotificationEvent.object_etag()`
    - added `awsmate.s3.LambdaNotificationEvent.bucket_name()`
    - added `awsmate.s3.LambdaNotificationEvent.bucket_arn()`
    - added `awsmate.s3.LambdaNotificationEvent.event_name()`

### Changed

- Documentation
    - improved documentation in general

- Code
    - made `awsmate.apigateway.LambdaProxyEvent.http_method()` based on `event['requestContext']['httpMethod']` instead of `event['httpMethod']`
    - made `awsmate.apigateway.build_http_server_error_response()` to handle `**kwargs` to pass to `awsmate.apigateway.build_http_response`
    - made `awsmate.apigateway.build_http_client_error_response()` to handle `**kwargs` to pass to `awsmate.apigateway.build_http_response`
    - renamed `awsmate.apigateway.LambdaProxyEvent.call_path()` -> `awsmate.apigateway.LambdaProxyEvent.query_path()` and made it based on `event['requestContext']['path']` instead of `event['path']`
    - renamed `awsmate.apigateway.LambdaProxyEvent.call_string()` -> `awsmate.apigateway.LambdaProxyEvent.query_string()` and made it include the prototype and the domain name of the call
    - renamed `awsmate.apigateway.LambdaProxyEvent.payload()` -> `awsmate.apigateway.LambdaProxyEvent.query_payload_()`

### Deprecated

*nothing*

### Removed

*nothing*

### Fixed

*nothing*

### Security

*nothing*

## [0.0.3] - 2023-03-18

### Added

- this changelog
- documentation of the existing code
- function `awsmate.logger.log_internal_error()`

### Changed

- Almost all functions: Python naming convention applied to parameters
- Method `awsmate.s3.LambdaNotificationEvent.object_key()`: corrected a typo in its name

### Deprecated

*nothing*

### Removed

*nothing*

### Fixed

*nothing*

### Security

*nothing*

## [0.0.2] and before - 2023-02-28

Genesis.

