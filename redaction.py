import ijson
#from google.cloud import dlp_v2
# Import the client library
import google.cloud.dlp


key_path = './sa-token.json'


dlp_client = google.cloud.dlp_v2.DlpServiceClient.from_service_account_file(key_path)
# Instantiate a client.
#dlp_client = google.cloud.dlp_v2.DlpServiceClient()



# The info types to search for in the content. Required.
info_types = [{"name": "PERSON_NAME"}]

# The minimum likelihood to constitute a match. Optional.
min_likelihood = google.cloud.dlp_v2.Likelihood.LIKELIHOOD_UNSPECIFIED

# The maximum number of findings to report (0 = server maximum). Optional.
max_findings = 0

# Whether to include the matching string in the results. Optional.
include_quote = True

# Construct the configuration dictionary. Keys which are None may
# optionally be omitted entirely.
inspect_config = {
    "info_types": info_types,
    "min_likelihood": min_likelihood,
    "include_quote": include_quote,
    "limits": {"max_findings_per_request": max_findings},
}

# Convert the project id into a full resource id.
parent = f"projects/bkauf-sandbox"



#f = open('./test.json')
#objects = ijson.items(f, 'transcripts')
#chatlist = (o for o in objects)
chatlist = ijson.parse(open('./input.json', 'r'))
for prefix, event, value in chatlist:
    if event in ['string', 'float']:
        if prefix == 'transcripts.item.content':
            print(prefix+':'+str(value))
            # Call the API.
            # Construct the `item`.
            item = {"value": value}
            response = dlp_client.inspect_content(
                request={"parent": parent, "inspect_config": inspect_config, "item": item}
            )

            # Print out the results.
            if response.result.findings:
                for finding in response.result.findings:
                    try:
                        print("Quote: {}".format(finding.quote))
                    except AttributeError:
                        pass
                    print("Info type: {}".format(finding.info_type.name))
                    # Convert likelihood value to string respresentation.
                    likelihood = finding.likelihood.name
                    print("Likelihood: {}".format(likelihood))
                    print(response)
            else:
                print("No findings.")
