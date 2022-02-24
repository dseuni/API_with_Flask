from flask import Flask, jsonify, request
from flask.json import JSONEncoder

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)

app              = Flask(__name__)
app.json_encoder = CustomJSONEncoder

app.users        = {}
app.id_count     = 1
app.tweets       = []


@app.route("/ping", methods=['GET'])
def ping():
    return "pong"

@app.route("/sign-up", methods=['POST'])
def sign_up():
    new_user                 = request.json
    new_user["id"]           = app.id_count
    app.users[app.id_count]  = new_user
    app.id_count             = app.id_count + 1  # 동시 접속 가능성이 있는 경우 atomic으로 해야함

    return jsonify(new_user)

@app.route('/tweet', methods=['POST'])
def tweet():
    payload = request.json  # http요청에 포함된 json데이터에 속해있는 아이디 값으로 판명하는 것은 문제가 있다.
    user_id = int(payload['id'])
    tweet   = payload['tweet']

    if user_id not in app.users:
        return '사용자가 존재하지 않습니다.', 400

    if len(tweet) > 300:
        return '300자를 초과했습니다.', 400

    user_id = int(payload['id'])

    app.tweets.append({
        'user_id' : user_id,
        'tweet'   : tweet
    })

    return '', 200

@app.route('/follow', methods=['POST'])
def follow():
    payload           = request.json
    user_id           = int(payload['id'])
    user_id_to_follow = int(payload['follow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return '사용자가 존재하지 않습니다.', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).add(user_id_to_follow)  # set을 json으로 변경하지 못함

    return jsonify(user)


@app.route('/unfollow', methods=['POST'])
def unfollow():
    payload           = request.json
    user_id           = int(payload['id'])
    user_id_to_follow = int(payload['unfollow'])

    if user_id not in app.users or user_id_to_follow not in app.users:
        return '사용자가 존재하지 않습니다.', 400

    user = app.users[user_id]
    user.setdefault('follow', set()).discard(user_id_to_follow)

    return jsonify(user)


@app.route('/timeline/<int:user_id>', methods=['GET'])
def timeline(user_id):
    if user_id not in app.users:
        return '사용자가 존재하지 않습니다.', 400

    follow_list = app.users[user_id].get('follow', set())
    follow_list.add(user_id)
    timeline = [tweet for tweet in app.tweets if tweet['user_id'] in follow_list]

    return jsonify({
        'user_id' : user_id,
        'timeline': timeline
    })

## window에서 실행하기 >> python app.py
if __name__ == '__main__':
    app.run()
    # 1.1. http -v POST localhost:5000/sign-up name=euni
    # 1.2. http -v POST localhost:5000/sign-up name=pepe
    # 2. http -v POST localhost:5000/tweet id:=1 tweet="My First Tweet"
    # 3.1. http -v POST localhost:5000/follow id:=1 follow:=2
    # 3.2. http -v POST localhost:5000/unfollow id:=1 unfollow:=2
    # 4. http -v GET localhost:5000/timeline/2