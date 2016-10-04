
##Request para obtener access_token
import requests
from requests.auth import HTTPBasicAuth
r = requests.post('https://api.mendeley.com/oauth/token', data={'grant_type':'client_credentials', 'scope':'all'}, auth=('3578', 'y43xcFyn1lNG7VT5'))

#print(r.json()['access_token'])

##Request de query a API Mendeley

query = 'Costello JT, Algar LA, Donnelly AE. Effects of wholebody cryotherapy (−110°C) on proprioception and indices of muscle damage. Scandinavian Journal of Medicine and Science in Sports 2012;22(2):190–8. [DOI: 10.1111/ j.1600-0838.2011.01292.x]'
print(query)
authorization = 'Bearer ' + r.json()['access_token']
print(authorization)
req = requests.get('https://api.mendeley.com/search/catalog', params={'query':query}, headers={'Authorization':authorization, 'Accept': 'application/vnd.mendeley-document.1+json'})

print(req.json())