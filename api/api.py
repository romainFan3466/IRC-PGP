import DBcm
from flask import Flask, request, jsonify, session
from flask_restful import reqparse
from functools import wraps

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="youwillneverguess",
    DB_CONFIG= {'host': '127.0.0.1',
                'user': 'root',
                'password': 'jf/b6rb',
                'database': 'ircDB'}
)


# session to check if logged in
def check_login(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'logged_in' in session and session["logged_in"]:
            return func(*args, **kwargs)
        return not_authorised(401)
    return wrapped_function


def IRC_logged(on_channel:bool=False):
    def _IRC_logged(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if 'server_id' in session:
                if on_channel:
                    if "channel" in session:
                        return func(*args, **kwargs)
                    else:
                        return not_authorised(401)
                else:
                    return func(*args, **kwargs)
            else:
                return not_authorised(401)
        return wrapped_function
    return _IRC_logged



@app.route('/users/login', methods=['POST'])
def api_login():
    try:
        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('login', help='User login name for Authentication')
        parser.add_argument('password', help='Password for Authentication')
        args = parser.parse_args()
        _userLogin = args['login']
        _userPassword = args['password']

        with DBcm.UseDatabase(app.config["DB_CONFIG"]) as cursor:
            cursor.execute(
                """SELECT idUsers
                    FROM Users
                    WHERE login=%s
                    AND password=%s """, (_userLogin, _userPassword))
            data = cursor.fetchone() # data is a tuple
            if data is not None:
                session["logged_in"] = True
                session["user"] = _userLogin
                session["id"] = data[0]

                return jsonify(logged_in=session["logged_in"], user=session["user"], id=session["id"]), 200

            else:
                return jsonify(info="Bad credentials"), 400

    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/ircServers/connect', methods=['POST'])
@check_login
def api_connect_irc():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('host', help="IRC Server host")
        parser.add_argument('port', help='User login name for Authentication')
        parser.add_argument('username', help="IRC User Name")
        args = parser.parse_args()

        _userName = args['username']
        _host = args['host']
        _port = args['port']
        data = None
        with DBcm.UseDatabase(app.config["DB_CONFIG"]) as cursor:
            cursor.execute(
                """ SELECT idIrcServers
                    FROM IrcServers
                    WHERE host = %s AND port = %s""", (_host, _port,))
            # if server exist
            data = cursor.fetchone()

        if data is not None:
            session["server_id"] = data[0]

        # if server does not exist, then create it
        else:
            with DBcm.UseDatabase(app.config["DB_CONFIG"]) as cursor:
                cursor.execute(""" INSERT INTO IrcServers (host, port) VALUES (%s, %s) """, (_host, _port,))
                session["server_id"]= cursor.lastrowid

        # update username for user
        with DBcm.UseDatabase(app.config["DB_CONFIG"]) as cursor:
             cursor.execute(""" UPDATE Users
                           SET userName = %s
                           WHERE login = %s """, (_userName, session["user"]))

        msg = {
                'Id': session["server_id"],
                'Host': _host,
                'Port': _port,
                'Username' : _userName
                }
        return jsonify(session=msg), 200

    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route('/ircServers/join/<int:channel>', methods=['GET'])
@check_login
def api_join_channel(channel: int):
    with DBcm.UseDatabase(app.config["DB_CONFIG"]) as cursor:
        cursor.execute(""" UPDATE Users
                           SET channel = %s, idIrcServers = %s
                           WHERE login = %s """, (channel, session["server_id"], session["user"] ))
    session["channel"] = channel
    return jsonify(info="Channel joined"), 200


# Send request to the DB to retrieve all stored public keys
@app.route('/publicKeys/getAll', methods=['GET'])
@check_login
@IRC_logged(on_channel=True)
def api_get_all():

        server_id = session["server_id"]
        channel = session["channel"]
        user = session["user"]
        data = []
        with DBcm.UseDatabase(app.config["DB_CONFIG"]) as cursor:
            cursor.execute(""" SELECT userName, login, publicKey
                               FROM Users
                               WHERE channel=%s AND idIrcServers=%s AND login != %s """, (channel, server_id, user))
            data = cursor.fetchall()

        response = []
        for u in data:
            d = {
                "username" : u[0],
                "login" : u[1],
                "publicKey" : u[2],
            }
            response.append(d)

        return jsonify(publicKeys=response), 200


# On api login, send new(randomly generated) public key to API and then store in DB
@app.route('/publicKeys/update', methods=['POST', 'PUT'])
@check_login
@IRC_logged()
def api_update():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('public_key')
        args = parser.parse_args()
        _publicKey = args['public_key']
        user = session["user"]

        with DBcm.UseDatabase(app.config["DB_CONFIG"]) as cursor:
            cursor.execute(""" UPDATE Users
                           SET publicKey = %s
                           WHERE login = %s """, (_publicKey, user,))
        return jsonify(publicKey=_publicKey, info="Public Key saved"),200

    except Exception as e:
        return jsonify(error=str(e)), 500


# Remove the public key currently stored for this user
@app.route('/users/logout', methods=['GET'])
@check_login
def api_logout():
    user = session["user"]

    with DBcm.UseDatabase(app.config["DB_CONFIG"]) as cursor:
        cursor.execute(""" UPDATE Users
                           SET publicKey = %s, channel = %s, idIrcServers = %s
                           WHERE login = %s """, (None, None, None, user,))
    session.clear()

    return jsonify(info="Logged out"), 200


# # Send all errors to DB
# @app.route('/errorLogs/report', methods=['POST'])
# def log_errors():
#         server_id = session["server_id"]
#
#         parser = reqparse.RequestParser()
#         parser.add_argument('error_type')
#         parser.add_argument('message')
#         args = parser.parse_args()
#
#         error_type = args['error_type']
#         message = args['date_time']
#         date = args['date_time']
#
#         with DBcm.UseDatabase(app.config["DB_CONFIG"]) as cursor:
#             _SQL = "INSERT INTO ErrorLogs (type, messageId, date, serverId) VALUES (%s, %s, %s, %s)"
#             cursor.execute(_SQL, (error_type, message, date, server_id,))
#             return " "
#         # Need to return all errors stored in DB ?


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.errorhandler(401)
def not_authorised(error=None):
    message = {
            'status': 401,
            'message': 'Unauthorised: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 403

    return resp


app.error_handler_spec[None][404] = not_found
app.error_handler_spec[None][403] = not_authorised

if __name__ == '__main__':
    app.run()
