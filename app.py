from flask import Flask, render_template,jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_cors import CORS


app = Flask(__name__)
# moment = Moment(app)
# moment.init_app(app)
api = Api(app)
CORS(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://khoana11:zxcasd113@localhost:5432/typeracer"

# DEFINE MODEL
class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    scores = db.relationship("Scores", backref="user", lazy=True)

class Scores(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    wpm = db.Column(db.Integer, nullable=False)
    errors = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def as_dict(self):
        
        score = {c.name: str(getattr(self, c.name)) for c in     self.__table__.columns}
        score['usermame'] = Users.query.get(self.user_id).username
        return score

db.create_all()
migrate = Migrate(app, db)


@app.route("/post_scores", methods=["POST"])
def root():
    data = request.get_json()
    score = Scores(
        wpm = data['wpm'],
        time = data['time'],
        errors = data['errorCount'],
        user_id = 1
    )
    db.session.add(score)
    db.session.commit()
    return data

@app.route("/get_scores", methods=["GET"])
def get_scores():
    score_list = Scores.query.all()
    jsonized_score_list = []
    for score in score_list:
        jsonized_score_list.append(score.as_dict())
    return jsonify(jsonized_score_list)
if __name__ == "__main__":
    app.run(debug = True)