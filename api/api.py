import DBcm
from flask import Flask, request, jsonify, session
from flask_restful import reqparse
from functools import wraps

app = Flask(__name__)


DBconfig = {'host': '127.0.0.1',
            'user': 'ircUSER',
            'password': 'ircPW',
            'database': 'ircDB'}


# session to check if logged in
def check_login(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return not_authorised(403)
    return wrapped_function


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

        with DBcm.UseDatabase(DBconfig) as cursor:
            cursor.execute("""SELECT idUsers
                            FROM Users
                            WHERE login=%s
                            AND password=%s """, (_userLogin, _userPassword))
            data = cursor.fetchone()
            if data is not None:
                session["logged_in"] = True
                session["user"] = _userLogin
                session["id"] = data["idUsers"]

                return jsonify(session=session), 200

            else:
                return jsonify(info="Bad credentials"), 200

    except Exception as e:
        return {'error': str(e)}


@app.route('/ircServers/connect', methods=['POST'])
@check_login
def api_connect():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('host', help="IRC Server host. Default is Romain's server host")
        parser.add_argument('port', help='User login name for Authentication')
        args = parser.parse_args()

        _host = args['host']
        _port = args['port']

        with DBcm.UseDatabase(DBconfig) as cursor:
            cursor.execute(""" SELECT idIrcServers, host, port
                           FROM IrcServers
                           WHERE host = %s
                           AND port = %s""", (_host, _port,))
            data = cursor.fetchone()
            if data is not None:
                session["server_id"] = data["idIrcServers"]
                msg = {
                    'Id': data["idIrcServers"],
                    'Host': data["host"],
                    'Port': data["port"],
                    }
                return jsonify(session=msg), 200
            else:
                return jsonify(info="Bad credentials"), 200

    except Exception as e:
        return {'error': str(e)}


@app.route('/ircServers/join/<int:channel>', methods=['GET'])
@check_login
def api_join_channel(channel:int) -> 'html':
    with DBcm.UseDatabase(DBconfig) as cursor:
        cursor.execute(""" SELECT channel
                           FROM Users
                           WHERE channel = %s""", (channel,))
        data = cursor.fetchone()
        if data is not None:
            session["channel"] = data["channel"]
            return jsonify(session=session), 200
        else:
            return jsonify(info="Invalid channel")


# Send request to the DB to retrieve all stored public keys
@app.route('/publicKeys/getAll', methods=['GET'])
@check_login
def api_get_all():
    server_id = session["server_id"]
    channel = session["channel"]

    try:
        with DBcm.UseDatabase(DBconfig) as cursor:
            cursor.execute(""" SELECT idUsers, publicKey
                            FROM Users
                            WHERE channel=%s AND idIrcServers=%s """, (channel, server_id,))
            data = cursor.fetchall()

            return jsonify(publicKeys=data), 200

    except Exception as e:
        return {'error': str(e)}


# On api login, send new(randomly generated) public key to API and then store in DB
@app.route('/publicKeys/update', methods=['POST', 'PUT'])
@check_login
def api_update():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('public_key')
        args = parser.parse_args()
        _publicKey = args['public_key']
        user = session["user"]

        with DBcm.UseDatabase(DBconfig) as cursor:
            cursor.execute(""" UPDATE Users
                           SET publicKey = %s
                           WHERE login = %s """, (_publicKey, user,))
        return jsonify(publicKey=_publicKey)

    except Exception as e:
        return {'error': str(e)}


@app.route('/users/logout')
def api_logout():  # need to erase the stored public key for this IRC Client
    user = session["user"]

    with DBcm.UseDatabase(DBconfig) as cursor:
        cursor.execute(""" UPDATE Users
                           SET publicKey = %s
                           WHERE login = %s """, (None, user,))

    session.pop('logged_in')
    session.pop('user')
    session.pop('id') # user
    session.pop('server_id')
    session.pop('chanel')
    # return anything here ?


# Send all errors to DB
@app.route('/errorLogs/report', methods=['GET'])
def log_errors():                                  # Need to get type, messageID and date
        server_id = session["server_id"]

        error_type=request.method
        message=request.path
        date=request.datetime

        with DBcm.UseDatabase(DBconfig) as cursor:
            _SQL = "INSERT INTO ErrorLogs (type, messageId, date, serverId) VALUES (%s, %s, %s, %s)"
            cursor.execute(_SQL, (error_type, message, date, server_id,))
            return " "
        # Need to return all errors stored in DB ?


@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.errorhandler(403)
def not_authorised(error=None):
    message = {
            'status': 403,
            'message': 'Unauthorised: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 403

    return resp


app.error_handler_spec[None][404] = not_found
app.error_handler_spec[None][403] = not_authorised

if __name__ == '__main__':
    app.run(debug=True)
