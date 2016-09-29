import requests
import pprint
reference = "Gomes, E., Bastos, T., Probst, M., Ribeiro, J.C., Silva, G., Corredeira, R., 2014. Effects of a group physical activity program on physical fitness and quality of life in individuals with schizophrenia. Mental Health and Physical Activity 7, 155–162."
x = requests.get('http://0.0.0.0:5001/api/v1/crsearch', params={
    'ref' : reference
})
pprint.pprint(x.json(), width=1)
