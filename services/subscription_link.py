## Microservice to store who is subscribed to who ##
from audioop import add
from http.client import CREATED
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

import json

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@localhost:3306/sub_link'
# app.config['SQLALCHEMY_BINDS'] = {
#     "consumer": 'mysql+mysqlconnector://is213@localhost:3306/consumer',
#     "creator": 'mysql+mysqlconnector://is213@localhost:3306/creator'
# }
#FOR DOCKER USAGE ONLY-------------------------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://is213@host.docker.internal:3306/sub_link'
app.config['SQLALCHEMY_BINDS'] = {
   "consumer": 'mysql+mysqlconnector://is213@host.docker.internal:3306/consumer',
   "creator": 'mysql+mysqlconnector://is213@host.docker.internal:3306/creator'
}

# root@localhost will change
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class creatorAccount(db.Model):
    __bind_key__ = "creator"
    __tablename__ = "creatoraccount"

    CREATORID = db.Column(db.String(64), primary_key=True, nullable=False)
    USERNAME = db.Column(db.String(64), nullable=False)
    PASSWORD = db.Column(db.String(64), nullable=False)
    EMAIL = db.Column(db.String(64), nullable=False)
    PRICE = db.Column(db.Float(precision=2), nullable=False)

    def __init__(self, CREATORID, USERNAME, PASSWORD, EMAIL, PRICE):
        self.CREATORID = CREATORID
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.EMAIL = EMAIL
        self.PRICE = PRICE

    def json(self):
        return {"CREATORID": self.CREATORID, "USERNAME": self.USERNAME, "PASSWORD": self.PASSWORD, "EMAIL": self.EMAIL, "PRICE": self.PRICE}


class consumerAccount(db.Model):
    __bind_key__ = "consumer"
    __tablename__ = "consumeraccount"

    CONSUMERID = db.Column(db.String(64), primary_key=True, nullable=False)
    USERNAME = db.Column(db.String(64), nullable=False)
    PASSWORD = db.Column(db.String(64), nullable=False)
    TELEGRAM = db.Column(db.String(64), nullable=False)

    def __init__(self, CONSUMERID, USERNAME, PASSWORD, TELEGRAM):
        self.CONSUMERID = CONSUMERID
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.TELEGRAM = TELEGRAM

    def json(self):
        return {"CONSUMERID": self.CONSUMERID, "USERNAME": self.USERNAME, "PASSWORD": self.PASSWORD, "TELEGRAM": self.TELEGRAM}


class subscriptionLink(db.Model):
    __tablename__ = 'subscription_link'

    CREATORID = db.Column(db.String(64), primary_key=True, nullable=False)
    CONSUMERID = db.Column(db.String(64), primary_key=True, nullable=False)
    TELEGRAM = db.Column(db.String(64), primary_key=True, nullable=False)
    CREATED = db.Column(db.ForeignKey(
        'creatoraccount.CREATORID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    MODIFIED = db.Column(db.ForeignKey(
        'consumeraccount.CONSUMERID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)

    def __init__(self, CREATORID, CONSUMERID, TELEGRAM, CREATED, MODIFIED):
        self.CREATORID = CREATORID
        self.CONSUMERID = CONSUMERID
        self.TELEGRAM = TELEGRAM
        self.CREATED = CREATED
        self.MODIFIED = MODIFIED

    def json(self):
        return {"CREATORID": self.CREATORID, "CONSUMERID": self.CONSUMERID, 'TELEGRAM': self.TELEGRAM, "CREATED": self.CREATED, "MODIFIED": self.MODIFIED}

# scenario 1 & 4


@app.route('/subscription/status')
def check_status():
    data = request.get_json()
    creatorid = data["CREATORID"]
    consumerid = data["CONSUMERID"]

    if (consumerAccount.query.filter_by(
        CONSUMERID=consumerid).first() and creatorAccount.query.filter_by(
            CREATORID=creatorid).first()):
        # if both consumer and creator account exists

        status = subscriptionLink.query.filter_by(
            CREATORID=creatorid, CONSUMERID=consumerid).first()

        if (status):
            # if there exists a link between consumer and creator account
            return jsonify(
                {
                    "code": 200,
                    "data": {"status": status.json(), "isSubbed": 1},
                    "message": "Already subscribed"
                }
            )
        # if there does not exist a link between consumer and creator account
        return jsonify(
            {
                "code": 200,
                "data": {"status": creatorAccount.query.filter_by(CREATORID=creatorid).first().json(), "isSubbed":2},
                "message": "Not subscribed."
            }
        ), 200
    # consumer or creator account does not exist
    return jsonify(
        {
            "code": 404,
            "message": "Creator and/or consumer does not exist."
        }
    )

# scenario 2
@app.route('/subscription/add', methods=["POST"])
def create_subscription():
    creatorid = request.json.get('CREATORID')
    consumerid = request.json.get('CONSUMERID')
    telegram = request.json.get('TELEGRAM')

    if (subscriptionLink.query.filter_by(CREATORID=creatorid, CONSUMERID=consumerid).first()):
        return jsonify(
            {
                "code": 400,
                "message": "Already subscribed."
            }
        ), 400
    else:
        created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        modified = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # telegram = consumerAccount.query.filter_by(
        #     CONSUMERID=consumerid).first()

        subcribedParing = subscriptionLink(
            CREATORID=creatorid, CONSUMERID=consumerid, TELEGRAM=telegram, CREATED=created, MODIFIED=modified)

        try:
            db.session.add(subcribedParing)
            db.session.commit()
        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred creating subscription link" + str(e)
                }
            ), 500
        return jsonify(
            {
                "code": 201,
                "message": "Subscription link created"
            }
        ), 201

# scenario 3

@app.route('/subscription/getsubscribers/<string:creatorid>')
def get_all_subscribers(creatorid):
    # data = request.get_json()
    # data = json.dumps(data)
    # creatorid = request.json.get("CREATORID")
    # creatorid=data['creator']
    # print(creatorid)
    # print(f"IM HERE -- {creatorid}")
    telegram = subscriptionLink.query.filter_by(CREATORID=creatorid)

    if telegram:
        return jsonify({
            "code": 200,
            "data": [cons.TELEGRAM for cons in telegram],
            'message': "Returned list of subscriber's telegram"
        }), 200
    return jsonify({
        "code": 404,
        "message": "Creator does not exist"
    }), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5006, debug=True)
