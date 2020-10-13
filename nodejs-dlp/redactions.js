// Imports the Google Cloud Data Loss Prevention library
const DLP = require('@google-cloud/dlp');
const helper = require('./redaction_api')

// Import other required libraries
const fs = require('fs');
const mime = require('mime');

const inputFile = './test.json';
const outputFile ='./output.json';
var byteSize = 10000000;//10 MB
//var readStream = fs.createReadStream(filepath, 'utf8');
// Instantiates a client


 async function inspectFile() {
  // Construct file data to inspect
  /*const fileTypeConstant =
    ['image/jpeg', 'image/bmp', 'image/png', 'image/svg'].indexOf(
      mime.getType(filepath)
    ) + 1;*/
    
    fs.readFile(inputFile , (err, fileContent) => {
      if( err ) {
      } else {
        var data = JSON.parse(fileContent);
        var transcriptsAry = data['transcripts'];

        Promise.all(transcriptsAry.map(chat => helper.make_API_call(chat,outputFile)))
        .then(results => {
           // console.log(results);
        })
        .catch(err => {
            console.log('Error:'+chat.transcript_id, err)
        });


           // dlpStr = (helper.make_API_call(chat.content));

     // }); //end foreach 
      }  
    });//end stream
  }

inspectFile();

function processChat(chat){
  
}

