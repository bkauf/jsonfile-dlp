/* REST API Helper Library - helper.js */
// Imports the Google Cloud Data Loss Prevention library
const DLP = require('@google-cloud/dlp');
const fs = require('fs');
const projectId = 'bkauf-sandbox';
const saToken = '/usr/local/google/home/bkauf/projects/dlp-file-redaction/sa-token.json';

const dlp = new DLP.DlpServiceClient({
    projectId: projectId,
    keyFilename: saToken,
  });

// The project ID to run the API call under
// const projectId = 'my-project';

// The path to a local file to inspect. Can be a text, JPG, or PNG file.

// The minimum likelihood required before returning a match
 const minLikelihood = 'LIKELIHOOD_UNSPECIFIED';

// The maximum number of findings to report per request (0 = server maximum)
 const maxFindings = 0;

// The infoTypes of information to match
//const infoTypes = [{ name: 'PHONE_NUMBER' }, { name: 'EMAIL_ADDRESS' }, { name: 'CREDIT_CARD_NUMBER' }];
const infoTypes = [{name: 'PERSON_NAME'}];

// The customInfoTypes of information to match
// const customInfoTypes = [{ infoType: { name: 'DICT_TYPE' }, dictionary: { wordList: { words: ['foo', 'bar', 'baz']}}},
//   { infoType: { name: 'REGEX_TYPE' }, regex: '\\(\\d{3}\\) \\d{3}-\\d{4}'}];

// Whether to include the matching string
 const includeQuote = true;


module.exports = {
    make_API_call : function(chat, outputFile){
        return new Promise( async function(resolve, reject) {
        
        let redactStr = {value: chat.content};
             // Construct request
          const request = {
            parent: `projects/${projectId}/locations/global`,
            inspectConfig: {
              infoTypes: infoTypes,
            // customInfoTypes: customInfoTypes,
              minLikelihood: minLikelihood,
              includeQuote: includeQuote,
              limits: {
                maxFindingsPerRequest: maxFindings,
              },
            },
            deidentifyConfig:{
              infoTypeTransformations:{
                transformations:[
                  {
                    infoTypes:[
                      {
                        name:"PERSON_NAME"
                      }
                    ],
                    primitiveTransformation:{
                      replaceConfig:{
                        newValue:{
                          stringValue:"PERSON_NAME"
                        }
                      }
                    }
                  }
                ]
              }
            },
          item: redactStr,
          };
          const [response] = await dlp.deidentifyContent(request);
        // console.log(response.item.value);
        chat.content = response.item.value;
        // write to a file
                     
            var stream = fs.createWriteStream(outputFile, {flags:'a'});
            
            
            stream.write(JSON.stringify(chat) + ",\n");
          
            console.log(new Date().toISOString());
            stream.end();
         resolve(response.item.value);
            
        
    })
}
}