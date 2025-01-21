# USFS Enterpise Data Catalog  
FS Enterprise Data Catalog  

## Resrouces
[CKAN](https://github.com/ckan)  

### DCAT Examples:  
[DCAT-US Schema v1.1](https://resources.data.gov/resources/dcat-us/#context)  
[JSON minimum requirements](https://resources.data.gov/schemas/dcat-us/v1.1/examples/catalog-sample.json)  
[JSON with extended requirements](https://resources.data.gov/schemas/dcat-us/v1.1/examples/catalog-sample-extended.json)  
[RDA List of Organizations Examle URL](https://www.fs.usda.gov/rds/archive//webservice/organizations?format=json)  
http://localhost/rds/archive_mongo/webservice/organizations?format=json  
http://localhost/rds/archive_mongo/webservice/organizations?format=json  
https://www.fs.usda.gov/rds/archive/webservice/organizations?format=json  
https://www.fs.usda.gov/rds/archive/webservice/  


## Harvest Data  

**Sources**
* FSGeoData
* Data.gov
* Climate Risk Viewer

## Build ChatBot UI Using Streamlit  

- [ ] Check streamlit account  
- [ ] Setup project between Streamlit and Github  
- [ ] Basic UI  

## Do the AI Part
https://www.youtube.com/watch?v=LddgJyDWoUs  

`
from pydantic_ai import Chatbot

# Step 1: Read the text from the file
with open('path/to/your/textfile.txt', 'r') as file:
    text = file.read()

# Step 2: Initialize the Pydantic AI chatbot
chatbot = Chatbot()

# Step 3: Plug the text into the chatbot
response = chatbot.ask(text)

# Print the response
print(response)
`