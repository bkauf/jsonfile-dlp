
import sys
# Import the client library
import google.cloud.dlp

key_path = './sa-token.json'
# Convert the project id into a full resource id.
parent = f"projects/bkauf-sandbox"

inputfile = sys.argv[1]
outputfile = inputfile+'-output.json'


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



with open(inputfile) as f:
    data = f.read(250000)
    while data !=b"":
    
        item = {"value": data} 
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

                
        dataDLP = response.item.value
        # Print out the results if there are matches
                
        # Open a file with access mode 'a'
        file_object = open(outputfile, 'a')
        # Append 'hello' at the end of file
        file_object.write(dataDLP)
        # Close the file
        file_object.close()
        #read next
        data = f.read(250000)