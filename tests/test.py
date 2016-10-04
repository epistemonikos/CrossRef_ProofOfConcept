#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pprint

def pretty_reference(cita):
    return '\n'.join([cita[i:i+50] for i in range(0, len(cita), 50)])

reference = "Gomes, E., Bastos, T., Probst, M., Ribeiro, J.C., Silva, G., Corredeira, R., 2014. Effects of a group physical activity program on physical fitness and quality of life in individuals with schizophrenia. Mental Health and Physical Activity 7, 155–162."
x = requests.get('http://0.0.0.0:5001/api/v1/crsearch', params={
    'ref' : reference
})
print(pretty_reference(reference))
print(x.json().get()['rating'])
