#Libraries that need to be imported (requests needs to be installed, json is part of the standard library)
import requests, json
#URL for logging in
url = 'https://dm-us.informaticacloud.com/ma/api/v2/user/login'
#Data dictionary to be passed as part of logging in
data = '{ &quot;@type&quot;: &quot;login&quot;, &quot;username&quot;: &quot;your_username@gwu.edu.ittest&quot;, &quot;password&quot;: &quot;your_password&quot; }'
#Request call to the API for credentials
r = requests.post(url, data=data, headers={'Content-Type':'application/json'})
#Print the response from the API if you are curious
print(r.text)
#Convert the response to json
rJson = json.loads(r.text)
#Get the server URL and session ID from the response json
serverUrl = rJson.get(&quot;serverUrl&quot;)
icSessionId = rJson.get(&quot;icSessionId&quot;)
#Print out the server URL and session ID
print(serverUrl, icSessionId)
#Create the logout URL based on the Server URL
logoutUrl = serverUrl + '/api/v2/user/logout'
#Open an output file to write the mappings
output_file = open(&quot;C:/Users/mstevens/Documents/Python/InformaticaCloud/data/mappings.xml&quot;, &quot;w&quot;)
#Create the URL to call mapping API
mappingsUrl = serverUrl + '/api/v2/mapping'
#Call the mapping API
rMappings = requests.get(mappingsUrl, headers={'Accept':'application/xml', 'icSessionId': icSessionId})
#Write the mapping API results to a text file in XML format
output_file.write(rMappings.text)
#Close the output file
output_file.close()
#Import the XML ElementTree library (part of the standard library) to parse XML
import xml.etree.ElementTree as ET
#Parse the XML to get mapping names and ids
mapping_set = set()
with open(&quot;C:/Users/mstevens/Documents/Python/InformaticaCloud/data/mappings.xml&quot;, &quot;r&quot;) as input_file:

tree = ET.parse(input_file)
root = tree.getroot()
for mapping in root.iter('mappingTemplate'):
for element in mapping:
mapping_name = mapping.find('name').text
mapping_id = mapping.find('id').text
mapping_info = mapping_name + ' : ' + mapping_id
mapping_set.add(mapping_info)
with open(&quot;C:/Users/mstevens/Documents/Python/InformaticaCloud/data/mapping_info.txt&quot;, &quot;w&quot;) as
output_names:
for m in mapping_set:
output_names.write(m + '\n')
#Open file to write mapping image, call image API, and write file
image_file =
open(&quot;C:/Users/mstevens/Documents/Python/InformaticaCloud/data/mapping_details/mapping2_img.jpg&quot;, &quot;wb&quot;)
mapping_imageUrl = 'https://na1.dm-
us.informaticacloud.com/saas/api/v2/mapping/0115EB170000000000DY/image?deployed=true'
image_file.write(requests.get(mapping_imageUrl, headers={'Accept':'application/xml', 'icSessionId':
icSessionId}).content)
image_file.close()
#Close the session, otherwise you won’t be able to get a new session ID and will be unable to make
#additional calls until the previous session ID expires
rLogOut = requests.post(logoutUrl, headers={'Content-Type':'application/json', 'icSessionId':
icSessionId})