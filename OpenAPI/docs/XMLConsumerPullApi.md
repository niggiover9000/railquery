# openapi_client.XMLConsumerPullApi

All URIs are relative to *https://m2m.mobilithek.info*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_publication**](XMLConsumerPullApi.md#get_publication) | **GET** /mobilithek/api/v1.0/subscription | Get publication


# **get_publication**
> str get_publication(subscription_id, accept_encoding, if_modified_since=if_modified_since, if_none_match=if_none_match)

Get publication

Get data package for publication from subscription 1061597061937086464.


### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://m2m.mobilithek.info
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://m2m.mobilithek.info"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.XMLConsumerPullApi(api_client)
    subscription_id = 1061597061937086464 # int | 
    accept_encoding = 'gzip' # str | Compression method supported by the client (here: gzip). 
    if_modified_since = 'Mon, 01 Jan 2024 00:00:00 GMT' # str | Optional timestamp indicating the last modification date the client has seen. Format: RFC 1123. Ignored when 'If-None-Match' is present.  (optional)
    if_none_match = '\"Fri, 14 Jun 2024 12:00:00.123 GMT\"' # str | ETag returned by a previous successful pull response. Send the value unchanged, including its double quotes. The service interprets it as a timestamp with millisecond precision using the format 'EEE, dd MMM yyyy HH:mm:ss.SSS zzz'. Takes precedence over 'If-Modified-Since'. Invalid timestamp formats result in HTTP 400.  (optional)

    try:
        # Get publication
        api_response = api_instance.get_publication(subscription_id, accept_encoding, if_modified_since=if_modified_since, if_none_match=if_none_match)
        print("The response of XMLConsumerPullApi->get_publication:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling XMLConsumerPullApi->get_publication: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **subscription_id** | **int**|  | 
 **accept_encoding** | **str**| Compression method supported by the client (here: gzip).  | 
 **if_modified_since** | **str**| Optional timestamp indicating the last modification date the client has seen. Format: RFC 1123. Ignored when &#39;If-None-Match&#39; is present.  | [optional] 
 **if_none_match** | **str**| ETag returned by a previous successful pull response. Send the value unchanged, including its double quotes. The service interprets it as a timestamp with millisecond precision using the format &#39;EEE, dd MMM yyyy HH:mm:ss.SSS zzz&#39;. Takes precedence over &#39;If-Modified-Since&#39;. Invalid timestamp formats result in HTTP 400.  | [optional] 

### Return type

**str**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Publication was successfully pulled. |  * Content-Encoding - The response is always gzip compressed. <br>  * Last-Modified - The timestamp when the data was delivered to the Mobilithek. Format: RFC 1123.  <br>  * ETag - Double-quoted timestamp identifying the returned data package with millisecond precision. Send this value unchanged in &#39;If-None-Match&#39; on subsequent pulls.  <br>  * Mobilithek-Schema-Valid - Result of the schema validation of the returned data package, as a Structured Field Boolean (RFC 8941): &#39;?1&#39; &#x3D; valid, &#39;?0&#39; &#x3D; invalid. The header is omitted if no schema validation result is available for the data package.  <br>  |
**204** | No data packet in the packet buffer for subscription.  |  -  |
**304** | Data exists, but no new data packet is available for the timestamp supplied in &#39;If-None-Match&#39; or, when that header is absent, &#39;If-Modified-Since&#39;.  |  -  |
**400** | No subscription parameter, or numeric subscription parameter, or missing &#39;Accept-Encoding&#39; header. No or incorrect specification of the codedExchangeProtocol element in a DATEX II v3 data offering with delta support. Invalid timestamp format in the &#39;If-None-Match&#39; header.  |  -  |
**403** | The user is not authorised to retrieve this subscription via this endpoint or the publication cannot be retrieved via this endpoint.  |  -  |
**404** | No or no longer valid subscription found for the subscription parameter, or the maximum number of permitted accesses has been exceeded.  |  -  |
**405** | The parameter ? subscriptionId&#x3D; was not specified or no value was specified for the parameter.  |  -  |
**406** | Gzip not specified in the &#39;Accept-Encoding&#39; request header. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

