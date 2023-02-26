---
description: |
    API documentation for modules: awsmate, awsmate.apigateway, awsmate.lambdafunction, awsmate.logger, awsmate.s3.

lang: en

classoption: oneside
geometry: margin=1in
papersize: a4

linkcolor: blue
links-as-notes: true
...


    
# Module `awsmate` {#id}




    
## Sub-modules

* [awsmate.apigateway](#awsmate.apigateway)
* [awsmate.lambdafunction](#awsmate.lambdafunction)
* [awsmate.logger](#awsmate.logger)
* [awsmate.s3](#awsmate.s3)






    
# Module `awsmate.apigateway` {#id}






    
## Functions


    
### Function `build_http_client_error_response` {#id}




>     def build_http_client_error_response(
>         error: awsmate.apigateway.HttpClientError
>     ) ‑> None




    
### Function `build_http_response` {#id}




>     def build_http_response(
>         status: int,
>         payload: Union[dict, str],
>         *,
>         event: Optional[awsmate.apigateway.LambdaProxyEvent] = None,
>         customTransformers: Optional[Dict[str, Callable[[dict], Tuple[str, str]]]] = None,
>         extraHeaders: Optional[Dict[str, str]] = None
>     ) ‑> dict




    
### Function `build_http_server_error_response` {#id}




>     def build_http_server_error_response(
>         message: Optional[str] = None
>     ) ‑> None




    
### Function `determine_content_type` {#id}




>     def determine_content_type(
>         event: awsmate.apigateway.LambdaProxyEvent,
>         *,
>         customTransformers: Optional[dict] = None
>     ) ‑> str




    
### Function `is_binary` {#id}




>     def is_binary(
>         contentType: str
>     ) ‑> bool




    
### Function `json_transformer` {#id}




>     def json_transformer(
>         payload: dict
>     ) ‑> Tuple[str, str]




    
### Function `simple_message` {#id}




>     def simple_message(
>         message: str
>     ) ‑> Dict[str, str]





    
## Classes


    
### Class `HttpBadRequestError` {#id}




>     class HttpBadRequestError(
>         msg: str
>     )


Unspecified run-time error.


    
#### Ancestors (in MRO)

* [awsmate.apigateway.HttpClientError](#awsmate.apigateway.HttpClientError)
* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `HttpClientError` {#id}




>     class HttpClientError(
>         status: int,
>         msg: str
>     )


Unspecified run-time error.


    
#### Ancestors (in MRO)

* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)


    
#### Descendants

* [awsmate.apigateway.HttpBadRequestError](#awsmate.apigateway.HttpBadRequestError)
* [awsmate.apigateway.HttpConflictError](#awsmate.apigateway.HttpConflictError)
* [awsmate.apigateway.HttpNotAcceptableError](#awsmate.apigateway.HttpNotAcceptableError)
* [awsmate.apigateway.HttpNotFoundError](#awsmate.apigateway.HttpNotFoundError)
* [awsmate.apigateway.HttpUnauthorizedError](#awsmate.apigateway.HttpUnauthorizedError)



    
#### Instance variables


    
##### Variable `status` {#id}








    
### Class `HttpConflictError` {#id}




>     class HttpConflictError(
>         msg: str
>     )


Unspecified run-time error.


    
#### Ancestors (in MRO)

* [awsmate.apigateway.HttpClientError](#awsmate.apigateway.HttpClientError)
* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `HttpNotAcceptableError` {#id}




>     class HttpNotAcceptableError(
>         msg: str
>     )


Unspecified run-time error.


    
#### Ancestors (in MRO)

* [awsmate.apigateway.HttpClientError](#awsmate.apigateway.HttpClientError)
* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `HttpNotFoundError` {#id}




>     class HttpNotFoundError(
>         msg: str
>     )


Unspecified run-time error.


    
#### Ancestors (in MRO)

* [awsmate.apigateway.HttpClientError](#awsmate.apigateway.HttpClientError)
* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `HttpUnauthorizedError` {#id}




>     class HttpUnauthorizedError(
>         msg: str
>     )


Unspecified run-time error.


    
#### Ancestors (in MRO)

* [awsmate.apigateway.HttpClientError](#awsmate.apigateway.HttpClientError)
* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `LambdaProxyEvent` {#id}




>     class LambdaProxyEvent(
>         eventObject: dict
>     )


Mapping of the input event received by an AWS Lambda function triggered by an AWS Api Gateway during a client API call.

#### Examples

```python-repl
>>> def lambda_handler(rawEvent, context):
>>>     import awsmate.apigateway as ag
>>>     event = ag.LambdaProxyEvent(rawEvent)    
```


#### Parameters

**```eventObject```** :&ensp;<code>dict</code>
:   The parameter <code>event</code> received by the AWS Lambda function handler.




    
#### Ancestors (in MRO)

* [awsmate.lambdafunction.LambdaEvent](#awsmate.lambdafunction.LambdaEvent)






    
#### Methods


    
##### Method `call_path` {#id}




>     def call_path(
>         self
>     ) ‑> Tuple[str, ...]


Returns the path of the API call, broken down into elements.

###### Returns

<code>tuple</code>
:   Path elements as <code>str</code>.

###### Raises

<code>[AwsEventSpecificationError](#awsmate.lambdafunction.AwsEventSpecificationError "awsmate.lambdafunction.AwsEventSpecificationError")</code>
:   If no <code>path</code> key is present in the event data.

###### Examples

API call ``GET /projects/foobar/modules`` leads to ``('projects', 'foobar', 'modules')``

    
##### Method `call_string` {#id}




>     def call_string(
>         self
>     ) ‑> str


Convenience method that returns the HTTP method of the call followed by the path and the URL parameters of the call.

###### Returns

<code>str</code>
:   The complete call string of the API call, including URL parameters if any.

###### Raises

<code>[AwsEventSpecificationError](#awsmate.lambdafunction.AwsEventSpecificationError "awsmate.lambdafunction.AwsEventSpecificationError")</code>
:   If at least one of the <code>httpMethod</code>, <code>path</code> or <code>query\_string\_parameters</code> keys is not present in the event data.

###### Examples

``GET /projects/foobar/modules?order=alphabetical&released=true``

    
##### Method `header_sorted_preferences` {#id}




>     def header_sorted_preferences(
>         self,
>         header: str
>     ) ‑> Tuple[str, ...]


Returns all values assigned to the given header, sorted by decreasing preferences.

Preferences are determined according to the weighted quality value syntax.
An empty ``tuple'' is returned if the given header is not found among those submitted by the caller.

###### Returns

<code>tuple</code>
:   Header values as <code>str</code>, in decreasing preference order.

###### Examples

Header ``Encoding: gzip;q=0.2,deflate,identity;q=0.9`` leads to ``('deflate', 'identity', 'gzip')``

    
##### Method `http_headers` {#id}




>     def http_headers(
>         self
>     ) ‑> Dict[str, str]


Returns all HTTP headers of the API call.

Values of these headers are returned unparsed, as submitted.

###### Returns

<code>dict</code>
:   Keys are header names as <code>str</code>, values are corresponding raw values as <code>str</code>.

###### Raises

<code>[AwsEventSpecificationError](#awsmate.lambdafunction.AwsEventSpecificationError "awsmate.lambdafunction.AwsEventSpecificationError")</code>
:   If no <code>headers</code> key is present in the event data.



    
##### Method `http_method` {#id}




>     def http_method(
>         self
>     ) ‑> str


Returns the HTTP method of the API call.

The method verb is returned as transmitted by AWS API Gateway. GET, PUT, POST, PATCH, DELETE are expected, but no verification is performed.

###### Returns

<code>str</code>
:   HTTP method of the API call, as transmitted by the API Gateway.

###### Raises

<code>[AwsEventSpecificationError](#awsmate.lambdafunction.AwsEventSpecificationError "awsmate.lambdafunction.AwsEventSpecificationError")</code>
:   If no <code>httpMethod</code> key is present in the event data.



    
##### Method `payload` {#id}




>     def payload(
>         self
>     ) ‑> Dict[str, Any]


Returns the data sent as the body of the API call.

Data is expected to be valid JSON.

###### Returns

<code>dict</code>
:   HTTP method of the API call, as transmitted by the API Gateway.

###### Raises

<code>[AwsEventSpecificationError](#awsmate.lambdafunction.AwsEventSpecificationError "awsmate.lambdafunction.AwsEventSpecificationError")</code>
:   If no <code>body</code> key is present in the event data.


<code>[MalformedPayloadError](#awsmate.apigateway.MalformedPayloadError "awsmate.apigateway.MalformedPayloadError")</code>
:   If the data is not valid JSON.



    
##### Method `query_string_parameters` {#id}




>     def query_string_parameters(
>         self
>     ) ‑> Dict[str, str]


Returns all URL parameters of the API call.

Values of these parameters are returned as transmitted by AWS API Gateway.
An empty ``dict'' is returned if no parameters were submitted by the caller.

###### Returns

<code>dict</code>
:   Keys are parameter names as <code>str</code>, values are corresponding raw values as <code>str</code>.

###### Raises

<code>[AwsEventSpecificationError](#awsmate.lambdafunction.AwsEventSpecificationError "awsmate.lambdafunction.AwsEventSpecificationError")</code>
:   If no <code>queryStringParameters</code> key is present in the event data. No parameters is supposed to be represented as ``'queryStringParameters': None``.



    
### Class `MalformedPayloadError` {#id}




>     class MalformedPayloadError(
>         msg
>     )


Error raised in case of malformed input payload.


    
#### Ancestors (in MRO)

* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)








    
# Module `awsmate.lambdafunction` {#id}







    
## Classes


    
### Class `AwsEventSpecificationError` {#id}




>     class AwsEventSpecificationError(
>         msg
>     )


Unspecified run-time error.


    
#### Ancestors (in MRO)

* [builtins.RuntimeError](#builtins.RuntimeError)
* [builtins.Exception](#builtins.Exception)
* [builtins.BaseException](#builtins.BaseException)






    
### Class `LambdaEvent` {#id}




>     class LambdaEvent(
>         eventObject: dict
>     )






    
#### Descendants

* [awsmate.apigateway.LambdaProxyEvent](#awsmate.apigateway.LambdaProxyEvent)
* [awsmate.s3.LambdaNotificationEvent](#awsmate.s3.LambdaNotificationEvent)







    
# Module `awsmate.logger` {#id}









    
# Module `awsmate.s3` {#id}







    
## Classes


    
### Class `LambdaNotificationEvent` {#id}




>     class LambdaNotificationEvent(
>         eventObject: dict
>     )





    
#### Ancestors (in MRO)

* [awsmate.lambdafunction.LambdaEvent](#awsmate.lambdafunction.LambdaEvent)



    
#### Class variables


    
##### Variable `KEY_RECORDS` {#id}






    
##### Variable `KEY_S3` {#id}









    
#### Methods


    
##### Method `objet_key` {#id}




>     def objet_key(
>         self
>     ) ‑> str





-----
Generated by *pdoc* 0.10.0 (<https://pdoc3.github.io>).
