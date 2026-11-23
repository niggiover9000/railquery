import os

import certifi
import openapi_client
from openapi_client.rest import ApiException

OUTPUT_FILE = "publication.xml"
ETAG_FILE = "publication.etag"  # stores the ETag of the last successful download

# Defining the host is optional and defaults to https://m2m.mobilithek.info
# See configuration.py for a list of all supported configuration parameters.
# ssl_ca_cert: the server chains up to "Telekom Security TLS RSA Root 2023",
# which is missing from the Windows/OpenSSL default store but included in certifi.
configuration = openapi_client.Configuration(
    host = "https://m2m.mobilithek.info",
    ssl_ca_cert = certifi.where(),
)

configuration.cert_file = "cert/MobilithekCertificate.crt.pem"
configuration.key_file = "cert/MobilithekPrivatekey.key.pem"


def load_etag():
    """Return the ETag of the last download, or None if there is none (or the XML is missing)."""
    if os.path.exists(ETAG_FILE) and os.path.exists(OUTPUT_FILE):
        with open(ETAG_FILE, encoding="utf-8") as f:
            return f.read().strip() or None
    return None


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.XMLConsumerPullApi(api_client)
    subscription_id = 1061597061937086464 # int |
    accept_encoding = 'gzip' # str | Compression method supported by the client (here: gzip).
    # ETag from the previous download: the server answers 304 if nothing changed since then.
    # Without a stored ETag the full publication is downloaded.
    if_none_match = load_etag()
    print("Gespeichertes ETag:", if_none_match)

    try:
        # Get publication
        # The generated client can't deserialize application/xml, so fetch the raw response instead.
        response = api_instance.get_publication_without_preload_content(subscription_id, accept_encoding, if_none_match=if_none_match)
        print("Status:", response.status)

        if response.status == 200:
            xml_data = response.data  # urllib3 decompresses gzip automatically
            with open(OUTPUT_FILE, "wb") as f:
                f.write(xml_data)
            etag = response.headers.get("ETag")
            if etag:
                with open(ETAG_FILE, "w", encoding="utf-8") as f:
                    f.write(etag)
            print(f"{len(xml_data)} Bytes in {OUTPUT_FILE} gespeichert, neues ETag: {etag}")
        elif response.status in (204, 304):
            print(f"Keine neuen Daten, {OUTPUT_FILE} ist aktuell.")
        else:
            print(response.data.decode("utf-8", errors="replace"))
    except ApiException as e:
        print("Exception when calling XMLConsumerPullApi->get_publication: %s\n" % e)
