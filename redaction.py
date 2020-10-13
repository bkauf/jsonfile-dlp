import ijson
import sys
#import json
#from google.cloud import dlp_v2
# Import the client library
import google.cloud.dlp

key_path = './sa-token.json'
inputfile = sys.argv[1]
outputfile = inputfile+'-output.json'


dlp_client = google.cloud.dlp_v2.DlpServiceClient.from_service_account_file(key_path)
# Instantiate a client.
#dlp_client = google.cloud.dlp_v2.DlpServiceClient()



# The info types to search for in the content. Required.
#info_types = [{"name": "PERSON_NAME"}]
info_types = ["PERSON_NAME"]
# The minimum likelihood to constitute a match. Optional.
#min_likelihood = google.cloud.dlp_v2.Likelihood.LIKELIHOOD_UNSPECIFIED

# The maximum number of findings to report (0 = server maximum). Optional.
#max_findings = 0

# Whether to include the matching string in the results. Optional.
#include_quote = True

# Construct the configuration dictionary. Keys which are None may
# optionally be omitted entirely.
#inspect_config = {
    #"info_types": info_types,
    #"min_likelihood": min_likelihood,
    #"include_quote": include_quote,
    #"limits": {"max_findings_per_request": max_findings},
#}
inspect_config = {"info_types": [{"name": info_type} for info_type in info_types]}
replacement_str= "PERSON_NAME"
# Construct deidentify configuration dictionary
deidentify_config = {
    "info_type_transformations": {
        "transformations": [
            {
                "primitive_transformation": {
                    "replace_config": {
                        "new_value": {"string_value": replacement_str}
                    }
                }
            }
        ]
    }
}


# Convert the project id into a full resource id.
parent = f"projects/bkauf-sandbox"

chatlist = ijson.parse(open(inputfile , 'r'))
for prefix, event, value in chatlist:
    #print(event)
    if event in ['string', 'number', 'start_map', 'end_map']:
        #print(prefix+":"+str(value))
        #print(value)

        if prefix == 'transcripts.item.transcript_id':
            label = 'transcript_id'
            print(value)
            data = f'"{label}": "{value}",'
        if prefix == 'transcripts.item.actor':
            label = 'actor'
            data = f'"{label}": "{value}",'
      
        if prefix == 'transcripts.item.content':
            #content= value
            # Call the API.
            # Construct the `item`.
            
            item = {"value": value}
            #response = dlp_client.inspect_content(
                #request={"parent": parent, "inspect_config": inspect_config, "item": item}
            #)
            response = dlp_client.deidentify_content(
                request={
                    "parent": parent,
                    "deidentify_config": deidentify_config,
                    "inspect_config": inspect_config,
                    "item": item,
                }
            )

            # Print out the results.
            label = 'content'
            data = f'"{label}": "{response.item.value}",'
            if response.overview:
                print(response.overview.transformation_summaries[0].results)


            # Print out the results.
            #if response.result.findings:
                #for finding in response.result.findings:
                    #try:
                       #print("Quote: {}".format(finding.quote))
                    #except AttributeError:
                        #pass
                    #print("Info type: {}".format(finding.info_type.name))
                    # Convert likelihood value to string respresentation.
                    #likelihood = finding.likelihood.name
                    #print("Likelihood: {}".format(likelihood))
                    #print(response)
                    #print(prefix+':'+str(value))
            #else:
                #print("No findings.")
        if prefix == 'transcripts.item.position':
            label = 'position'
            data = f'"{label}": {value}'
        if event == 'start_map':
            data = '{'
        if event == 'end_map':
            data = '},'
        
        # Open a file with access mode 'a'
        file_object = open(outputfile, 'a')
        # Append 'hello' at the end of file
        file_object.write(data+'\n')
        # Close the file
        file_object.close()