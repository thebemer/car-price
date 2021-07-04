# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 17:30:35 2021

@author: HP
"""

from pywebio.platform.flask import webio_view
from pywebio import STATIC_PATH
from pywebio.input import *
from pywebio.output import *
from flask import Flask, send_from_directory

import pickle
import numpy as np
model = pickle.load(open('catboost_model.pkl', 'rb'))
app = Flask(__name__)

import argparse
from pywebio import start_server

def predict():
    Year = input("Enter the Model Year：", type=NUMBER)
    Year = 2021 - Year
    Present_Price = input("Enter the Present Price(in LAKHS)", type=FLOAT)
    Kms_Driven = input("Enter the distance it has travelled(in KMS)：", type=FLOAT)
    Kms_Driven2 = np.log(Kms_Driven)
    Owner = input("Enter the number of owners who have previously owned it(0 or 1 or 2 or 3)", type=NUMBER)
    Fuel_Type = select('What is the Fuel Type', ['Petrol', 'Diesel','CNG'])
    if(Fuel_Type =='Petrol'):
            Fuel_Type_Petrol=1
            Fuel_Type_Diesel=0
    elif(Fuel_Type =='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
    else:
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0
    Seller_Type = select('Are you a dealer or an individual', ['Dealer', 'Individual'])
    if(Seller_Type=='Individual'):
            Seller_Type_Individual=1
    else:
            Seller_Type_Individual=0	
    Transmission = select('Transmission Type', ['Manual Car', 'Automatic Car'])
    if(Transmission=='Mannual'):
            Transmission_Mannual=1
    else:
            Transmission_Mannual=0
    prediction = model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
    output = round(prediction[0], 2)

    if output < 0:
        put_text("Sorry You can't sell this Car")

    else:
        put_text('You can sell this Car at price:',output ,'Lakh rupees')

app.add_url_rule('/tool', 'webio_view', webio_view(predict),
            methods=['GET', 'POST', 'OPTIONS'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(predict, port=args.port)
