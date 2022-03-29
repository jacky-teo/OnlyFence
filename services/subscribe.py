## Complex Microservice when consumer wants to subscribe to a creator ##

from distutils.log import error
from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ
from invokes import *
# import pika
# import json
# import amqp_setup
# import requests
# from itsdangerous import json       #not sure how to use this module (copy pasted from labs) but fyi its for security purposes

app = Flask(__name__)
CORS(app)

creator_URL = environ.get('creator_URL') or "http://localhost:5002/creator/price" 
add_subscription_URL =environ.get('add_subscription_URL') or "http://localhost:5006/subscription/add"
add_paymentLog_URL = environ.get('add_paymentLog_URL') or"http://localhost:5005/payments/log"

# Scenario 2a: Create subscription request
@app.route("/subscribe", methods=['POST'])
def check_request(): 
    if request.is_json: # Check if request data is in JSON format
        try: # Valid JSON, call retrieveCreatorInformation() function
            attempt = request.get_json()
            print("Received a request to subscribe in JSON:", attempt)
            result = retrieveCreatorInformation(attempt)
            return result

        except Exception as e: # Exception for error handling
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            print('Failed to confirm subscription. Invalid JSON')
            return jsonify({
                "code": 500,
                "message": "Internal Server Error. Error: " + ex_str
            }), 500 # Internal Server Error

    else: # Invalid JSON
        print('Failed to subscribe. Invalid JSON')
        return jsonify({
            "code": 400,
            "message": "Request should be in JSON. Error: 400" 
        }), 400 # Bad Request Input


def retrieveCreatorInformation(attempt): # Pull creator information from creator_account
    print('-----Invoking creator_account microservice-----')
    retrieveInfo = invoke_http(creator_URL, method="GET", json=attempt)
    print('information_request:', retrieveInfo)
    
    code = retrieveInfo["code"]
    # message = json.dumps(retrieveInfo) 

    # amqp_setup.check_setup()

    # Check HTTP request. 
    if code not in range(200, 300): # Error!
        # # Inform the error microservice
        # print('\n\n-----Publishing the error message with routing_key=subscribe.error-----')

        # # Route error message to error microservice
        # {amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribe.error", body=message, properties=pika.BasicProperties(delivery_mode = 2)) }

        # # - reply from the invocation is not used;
        # # continue even if this invocation fails    
        # print("\nStatus ({:d}) published to the RabbitMQ Exchange:".format(
        #     code), creator_information)

        # 7. Return error
        return {
            "code": 500,
            "data": {"retrieveInfo": retrieveInfo},
            "message": "Request failure sent for error handling."
        }

    else: # Success! 
        # Retrieve payment details through creator_account microservice
        
        data = retrieveInfo['data']
        price = data['PRICE']

        print(price)
        creatorID = data['CREATORID']
        creatorUsername = data['USERNAME']
        email = data['EMAIL']
        return {
                "code": 200,
                "price": price,
                "creatorID" : creatorID ,
                "creatorEmail": email,
                "creatorUsername": creatorUsername
            }

        # Update Activity AMQP 
        # invoke_http(activity_log_URL, method="POST", json=order_result)            
        # amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="subscribe.info", body=message, properties=pika.BasicProperties(delivery_mode = 2))

# Scenario 2b: Confirm Subscription Payment 
@app.route("/confirmSubscription", methods = ['POST'])
def confirmPayment(): # Function that passes in result from PayPal service after payment processed
    if request.is_json: # Check if request data is in JSON format
        try: 
            attempt = request.get_json()
            print("Received a request to link subscription in JSON:", attempt)

            # Update Subscription Link
            subscriptionLinkResult = updateSubscriptionLink(attempt)
            subscriptionLinkResult_code = subscriptionLinkResult['code']
            subscriptionLinkResult_message = subscriptionLinkResult['message']
            print("Subscription Link Status: " + str(subscriptionLinkResult_code) + ": " + subscriptionLinkResult_message)

            # Update Payment Log
            paymentLogResult = updatePaymentLog(attempt)
            paymentLogResult_code = paymentLogResult['code']
            paymentLogResult_message = paymentLogResult['message']
            print("Payment Log Status: " + str(paymentLogResult_code) + ": " + paymentLogResult_message)

            if subscriptionLinkResult_code not in range (200,300):
                return jsonify({
                    "code": 500,
                    "message": "Internal Server Error when updating Subscription Link Service. Error: " + ex_str
                }), 500 

            if paymentLogResult_code not in range (200,300):
                return jsonify({
                    "code": 500,
                    "message": "Internal Server Error when Logging Payment. Error: " + ex_str
                }), 500 
            
            return jsonify({
                "code": 200,
                "message": "Success! Subscription confirmed and payment logged."
            })

        except Exception as e: # Exception for error handling
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            print('Failed to confirm subscription. Invalid JSON')
            return jsonify({
                "code": 500,
                "message": "Internal Server Error. Error: " + ex_str
            }), 500 # Internal Server Error

    else: # Invalid JSON
        print('Failed to confirm subscription. Invalid JSON')
        return jsonify({
            "code": 400,
            "message": "Request should be in JSON. Error: "
        }), 400 # Bad Request Input

def updateSubscriptionLink(data): # Send new record to Subscription Link service
    print('Updating Subscription Link service...')
    prepJSON = {
        "CONSUMERID": data['CONSUMERID'],
        "CREATORID": data['CREATORID']
    }
    result = invoke_http(add_subscription_URL, method='POST', json=prepJSON)
    return result

def updatePaymentLog(data): # Send new record to Payment service
    print('Updating Payment Log service...')
    prepJSON = {
        "TRANSACTIONID": data['id'],
        "CONSUMERID": data['CONSUMERID'],
        "CREATORID": data['CREATORID'],
        "PAYMENTAMOUNT": data['PRICE']
    }
    result = invoke_http(add_paymentLog_URL, method='POST', json=prepJSON)
    return result
        
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5101, debug=True)        
    
