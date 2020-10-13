import ijson
import sys
#This script checks the the file can be read with ijson, it is read and rewritten
import google.cloud.dlp

key_path = './sa-token.json'
inputfile = sys.argv[1]
outputfile = inputfile+'-output.json'


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
            label = 'content'
            data = f'"{label}": "{value}",'
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