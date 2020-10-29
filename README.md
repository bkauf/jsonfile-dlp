### Python text file load to  DLP redaction with Google Cloud DLP API
#### First argument for redaction.py specifies input file, output will append -output.json in new file
``` python3 redaction-blob.py [json file]```
#### Combine tabs or double spaces to single spaces with this command before running script
```tr -s '[:blank:]' ' ' <file >newfile```
#### Remove / from file
``` sed 's/\\/ /g' [input file] > [output file]```
#### Split file into multiple 100mb smaller ones if nessessary
```split -b 100MB input.json```

#### Run Script in the background

```nohup python3 redaction-blob.py [jsonfile] &``` 