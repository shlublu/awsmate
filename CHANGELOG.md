All notable changes to this project are documented in this file.

## [0.1.0] - *not yet released*

### Added

#### Documentation
- Contributing guidelines
- Code of conduct

#### Example application
- First draft focusing on `apigateway`

#### Code
- added variable `awsmate.__version__` 
- added `awsmate.apigateway.LambdaProxyEvent.http_protocol()`
- added `awsmate.apigateway.LambdaProxyEvent.http_user_agent()`
- added `awsmate.apigateway.LambdaProxyEvent.query_domain_name()`

### Changed

#### Documentation
- improved documentation

#### Code
- made `awsmate.apigateway.LambdaProxyEvent.http_method()` based on `event['requestContext']['httpMethod']` instead of just `event['httpMethod']`
- renamed `awsmate.apigateway.LambdaProxyEvent.call_path()` -> `awsmate.apigateway.LambdaProxyEvent.query_path()` and made it based on `event['requestContext']['path']` instead of just `event['path']`
- renamed `awsmate.apigateway.LambdaProxyEvent.call_string()` -> `awsmate.apigateway.LambdaProxyEvent.query_string()` and made it include the prototype and the domain name
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

