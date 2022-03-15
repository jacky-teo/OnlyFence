## Microservice to store creator account information ##
from audioop import add
from http.client import CREATED
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/onlyfence'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)


class creatorAccount(db.Model):
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

# scenario 1


@app.route('/creatorprice')
def get_creator_price():
    creatorid = request.args.get('CREATORID', None)
    status = creatorAccount.query.filter_by(
        CREATORID=creatorid).first()

    if (status):
        return jsonify(
            {
                "code": 200,
                "data": status.PRICE
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Creator does not exist."
        }
    ), 404

# scenario 4


@app.route('/creatorid')
def get_creator_id():
    creatorid = request.args.get('CREATORID', None)
    status = creatorAccount.query.filter_by(
        CREATORID=creatorid).first()

    if (status):
        return jsonify(
            {
                "code": 200,
                "data": status.CREATORID
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Creator does not exist."
        }
    ), 404

# missing scenario 2


if __name__ == '__main__':
    app.run(port=5001, debug=True)
