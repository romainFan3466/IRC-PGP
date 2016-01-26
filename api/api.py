import DBcm
import json
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
            cursor.execute("""SELECT * FROM Users WHERE login=%s """, (_userLogin,))
            data = cursor.fetchall()
            items_list = []
            for item in data:
                if item[3] == _userPassword:
                    # session['logged_in'] = True
                    i = {
                       'User Id': item[0],
                       'User Name': item[1],
                        }
                    items_list.append(i)
                    result = jsonify(items=items_list)
                    result.status_code = 200
                    return result
                else:
                    return not_authorised(403)

    except Exception as e:
        return {'error': str(e)}


# On api login, send new(randomly generated) public key to API and then store in DB
@app.route('/publicKeys/update', methods=['POST', 'PUT'])
# @check_login
def api_update():
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('public_key')
        parser.add_argument('login', help='User login name for Authentication')
        args = parser.parse_args()

        _publicKey = args['public_key']
        _userLogin = args['login']

        with DBcm.UseDatabase(DBconfig) as cursor:
            cursor.execute(""" UPDATE Users
                           SET publicKey = %s
                           WHERE login = %s """, (_publicKey, _userLogin,))
            cursor.execute(""" SELECT publicKey
                           FROM Users
                           WHERE publicKey = %s """, (_publicKey,))
            data = cursor.fetchone()
            if data is not None:
                i = {
                    'Public_key': data[0],
                    }
                result = jsonify(i)
                result.status_code = 200
            else:
                return not_acceptable(406)
        return result

    except Exception as e:
        return {'error': str(e)}


# Send request to the DB to retrieve all stored public keys	
@app.route('/publicKeys/getAll', methods=['GET'])
# @check_login
def api_get_all():
    try:
        with DBcm.UseDatabase(DBconfig) as cursor:
            cursor.execute(""" SELECT publicKey FROM Users """)
            data = cursor.fetchall()
            items_list = []
            for item in data:
                i = {
                    'Public_key': item[0],
                    }
                items_list.append(i)
            result = json.dumps(items_list)  # unable to use jsonify to return a list
            # result.status_code = 200
        return result

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
            cursor.execute(""" INSERT INTO IrcServers (host, port)
                           VALUES (%s, %s) """, (_host, _port,))
            cursor.execute(""" SELECT host, port
                           FROM IrcServers
                           WHERE host = %s
                           AND port = %s""", (_host, _port,))
            data = cursor.fetchall()
            if data is not None:
                i = {
                    'Host': data[0],
                    'Port': data[1],
                    }
            result = jsonify(ircServer=i)
            result.status_code = 200

        return result

    except Exception as e:
        return {'error': str(e)}


@app.route('/ircServers/join/<channel>', methods=['GET'])
@check_login
def api_join_channel():
    return ""


@app.route('/users/logout')
def api_logout():  # need to erase the stored public key for this IRC Client
    session.pop('logged_in')
    return "GOODBYE..."


@app.route('/errorLogs/report', methods=['POST'])
@check_login
def api_error_reports():
    return ""


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


@app.errorhandler(406)
def not_acceptable(error=None):
    message = {
            'status': 406,
            'message': 'Not Acceptable  :' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 406

    return resp

app.error_handler_spec[None][404] = not_found
app.error_handler_spec[None][403] = not_authorised
app.error_handler_spec[None][406] = not_acceptable

if __name__ == '__main__':
    app.run(debug=True)
