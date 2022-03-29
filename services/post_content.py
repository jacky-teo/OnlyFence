## Complex Microservice when creator post a content ##
## Complex Microservice when consumer views content ##
from flask import Flask, request, jsonify,redirect
from flask_cors import CORS
from firebase_admin import storage
import os
import sys
from datetime import datetime
from invokes import invoke_http
from firebase import init_firebase, upload_firebase

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

upload_url =environ.get('upload_url') or "http://localhost:5003/upload"
subscription_url =environ.get('subscription_url') or "http://localhost:5006/subscription/getsubscribers"
notification_url =environ.get('notification_url') or "http://localhost:5000/notify/"
creator_url =environ.get('creator_url') or "http://localhost:5002/creator/getinfo/"

# Step 1 Upload the image & Upload information is returned (content.py)
# -
# Step 2 Get list of people who subscribed to the creator to send out notification
# Step 3 Send information to Notifcation.py


@app.route("/post_content", methods=['GET', 'POST'])
def post_content():
    init_firebase()  # Initiate firebase
    if request.method == "POST":  # Check if method is POST before proceeding
        file = request.files['file']  # Get the file to be uploaded
        creatorID = request.form['creatorID']  # Get the CreatorID from form
        description = request.form['description']# Get the description from form

    # uploads all the information into firebase
    data_json = upload_firebase(file, creatorID, description)
    print('----------After Firebase------------')
    print(data_json)
    print('------------------------------------')
    try:
        # Upload image into firebase and it goes to SQL
        uploadInformation = upload_content(data_json)
        print('--------Data Uploaded into SQL-----------')
        print(uploadInformation)
        print('-----------------------------------------')
        # Add creatorID as a json file
        # creatorID_JSON = json.dumps({"CREATORID": creatorID})
        
        # Get all the followers that are subscribed to creator
        consumerTelegram = telegramTags(creatorID)
        print('--------- Collected Telegram tags ---------')
        print(consumerTelegram)
        print('-------------------------------------------')
        creatorinfo = creatorInformation(creatorID)  # Get creator information
        # Get creator name to use for notification status
        creatorname = creatorinfo['data']['username']
        notifyStatus = notifyUsers(consumerTelegram, creatorname)  # notify users
        print('--------- Users Notified ---------')
        print(notifyStatus)
        print('-------------------------------------------')

        if notifyStatus['code'] == 201 and creatorinfo['code'] == 200 and uploadInformation['code'] == 201 and consumerTelegram['code']==200:
            print('REDIRECTING PAGE AS UPLOAD AND NOTIFCATION IS SUCCESSFUL')
            return  redirect("http://localhost/OnlyFence/upload_success.html")  # redirect users to upload_success.html

    except Exception as e:
        # Unexpected error in code
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        ex_str = str(e) + " at " + str(exc_type) + ": " + \
            fname + ": line " + str(exc_tb.tb_lineno)
        print(ex_str)

        return jsonify({
            "code": 500,
            "message": "post_content internal error: " + ex_str
        }), 500


def upload_content(json):
    uploadInformation = invoke_http(upload_url, method='POST', json=json)

    uploadCode = uploadInformation['code']
    message = uploadInformation['message']

    if uploadCode not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="post_content.upload_content.error",
                                         body=message, properties=pika.BasicProperties(delivery_mode=2))

        return {
            "code": 500,
            "data": {"uploadInformation": uploadInformation},
            "message": "Failed to upload image"
        }
    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="post_content.upload_content.info",
                                         body=message)
    return uploadInformation


def telegramTags(creatorID):
    tags = invoke_http(f'{subscription_url}/{creatorID}', method="GET",)
    tagsCode = tags['code']
    message = tags['message']
    if tagsCode not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="post_content.retrieve_telegram.error",
                                         body=message)
        return {
            "code": 500,
            "data": {"tags": tags},
            "message": "Failed to retrieve subscribers"
        }
    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="post_content.retrieve_telegram.info",
                                         body=message)
    return tags


def notifyUsers(tags, creatorname):
    notification_status = invoke_http(
        f"{notification_url}{creatorname}", json=tags)
    notiCode = notification_status['code']
    message = notification_status['message']

    if notiCode not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="post_content.send_notification.error",
                                         body=message)
        return {
            "code": 500,
            "data": {"notification_status": notification_status},
            "message": "Failed to notify users"
        }
    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="post_content.send_notification.info",
                                         body=message)
    return notification_status


def creatorInformation(creatorID):
    info = invoke_http(f'{creator_url}{creatorID}')
    infoCode = info['code']
    message = info['message']

    if infoCode not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="post_content.get_creator.error",
                                         body=message)
        return {
            "code": 500,
            "data": {"info": info},
            "message": "Failed to notify retrieve creator ID"
        }
    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="post_content.get_creator.info",
                                         body=message)
    return info


if __name__ == "__main__":
    app.run(port=5102, debug=True)
