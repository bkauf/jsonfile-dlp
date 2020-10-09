// Imports the Google Cloud Data Loss Prevention library
const DLP = require('@google-cloud/dlp');
const helper = require('./redaction_api')

// Import other required libraries
const fs = require('fs');

JSONStream = require('JSONStream'),
es = require('event-stream');

const inputFile = './test.json';
const outputFile ='./output.json';
var stream = fs.createReadStream(inputFile, 'utf-8');
var buf = '';
// Instantiates a client


var getStream = function () {
  var jsonData = inputFile,
      stream = fs.createReadStream(jsonData, { encoding: 'utf8' }),
      parser = JSONStream.parse(['transcripts',true]);
  return stream.pipe(parser);
};

getStream()
  .pipe(es.mapSync(function (data) {
    processChat(data)

     // console.log(data);
  }));

function processChat(chat){// pass off chat to DLP and file write
//  chat += "}";
 // chat = JSON.parse(chat);
   Promise.all(helper.make_API_call(chat,outputFile))
    .then(results => {
       // console.log(results);
       return;
    })
    .catch(err => {
      console.log(err)
        // Handle the error.
    });

    
    
    

}

