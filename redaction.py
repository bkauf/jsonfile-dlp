import ijson
import sys
import json
#from google.cloud import dlp_v2
# Import the client library
import google.cloud.dlp

key_path = './sa-token.json'
inputfile = sys.argv[1]
outputfile = inputfile+'-output.json'
catches = 'catches.csv'


dlp_client = google.cloud.dlp_v2.DlpServiceClient.from_service_account_file(key_path)

#info_types = ["PERSON_NAME"]

deidentify_template_name = "projects/bkauf-sandbox/locations/global/deidentifyTemplates/sample-aggressive1"
inspect_template_name = "projects/bkauf-sandbox/locations/global/inspectTemplates/sample-aggressive1"

min_likelihood = google.cloud.dlp_v2.Likelihood.LIKELIHOOD_UNSPECIFIED
inspect_config = {
    #"info_types": [{"name": info_type} for info_type in info_types],
    #"min_likelihood": min_likelihood
}
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
       
        if prefix == 'transcripts.item.transcript_id':
            label = 'transcript_id'
            #print(value)
            transcriptid = value
            data = f'"{label}": "{value}",'
        if prefix == 'transcripts.item.actor':
            label = 'actor'
            data = f'"{label}": "{value}",'
            actor = value
      
        if prefix == 'transcripts.item.content':
            # Call the API.
            # Construct the `item`.
            
            item = {"value": value}
            
            response = dlp_client.deidentify_content(
                request={
                    "parent": parent,
                    #"deidentify_config": deidentify_config,
                    "inspect_template_name": inspect_template_name,
                    "inspect_config": inspect_config,
                    "deidentify_template_name": deidentify_template_name,
                    "item": item,
                }
            )

            label = 'content'
            data = f'"{label}": "{response.item.value}",'
            content = response.item.value
            # Print out the results if there are matches
            if response.overview:
                #print(response.overview.transformation_summaries[0].results)
                print(response)
                print(transcriptid)
                #print("before:"+ value)
                #print("after: "+ content)

                file_object1 = open(catches, 'a')
                # Append 'hello' at the end of file
                file_object1.write('before:'+value+',\n')
                file_object1.write('after:'+content+',\n'
                )

                # Close the file
                file_object1.close()

        if prefix == 'transcripts.item.position':
            label = 'position'
            data = f'"{label}": {value}'
            position = value
        if event == 'start_map':
            data = '{'
        if event == 'end_map':
            data = '},'
            #new_data = {}
            #new_data['transcripts'] = []
            #new_data['transcripts'].append({
        	#'transcript_id' : transcriptid,
        	#'actor' : actor,
        	##'content' : content,
        	#'position' : position
        	#})
            #with open(outputfile, 'a') as outfile:
                #json.dump(new_data, outfile, indent=4)
        # Open a file with access mode 'a'
        file_object = open(outputfile, 'a')
        # Append 'hello' at the end of file
        file_object.write(data+'\n')
        # Close the file
        file_object.close()