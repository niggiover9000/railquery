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
    except ApiException as e:
        print("Exception when calling XMLConsumerPullApi->get_publication: %s\n" % e)