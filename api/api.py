from flask import Flask, render_template, request, session, jsonify
from flask_restful import Resource 
from functools import wraps
from json import dumps

app = Flask(__name__)
#api = Api(app)	

import DBcm

DBconfig = {'host': '127.0.0.1',
			'user': 'ircUSER',
			'password': 'ircPW',
			'database': 'ircDB' }
			
@app.route('/users/login', methods=['POST'])
def main():
    try:
        # Parse the arguments
        parser = reqparse.RequestParser()
        parser.add_argument('login', help='User login name for Authentication')
        parser.add_argument('password', help='Password for Authentication')
        args = parser.parse_args()

        _userLogin = args['login']
        _userPassword = args['password']
        #cursor.callproc('sp_AuthenticateUser',(_userLogin,))
        
        with DBcm.UseDatabase(DBconfig) as cursor:
            cursor.execute("""SELECT * FROM Users WHERE login=%s """, (_userLogin,))
            data = cursor.fetchall()
            items_list=[]
            for item in data:
               if(str(item[3])==_userPassword):
                   i = {
                       'User Id':item[0],
                       }
               items_list.append(i)
            result = jsonify(items=items_list)
            result.status_code = 200
        return result     

    except Exception as e:
        return {'error': str(e)}


# On api login, send new(randomly generated) public key to API and then store in DB
@app.route('/publicKeys/update', methods=['POST', 'PUT'])
def api_update():
	return json.dumps({""}), 200 , {'Content-Type': 'applicaion/json'}


# Send request to the DB to retrieve all stored public keys	
@app.route('/publicKeys/getAll', methods=['GET'])
def api_getAll():
	try:
		with DBcm.UseDatabase(DBconfig) as cursor: 
			cursor.execute(""" SELECT * FROM Users """)
			data = cursor.fetchall()
			items_list=[];
			for item in data:
				i = {
					'Id':item[0],
					'Public_key':item[4]
					}
				items_list.append(items_list)
			result = jsonify(i)
			result.status_code = 200

		return result #"Success! "#{'StatusCode':'200','Items':items_list}

	except Exception as e:
		return {'error': str(e)}


@app.route('/users/logout')
def api_logout():
# need to erase the stored public key for this IRC Client
    #session.pop('logged_in')
    return "GOODBYE..."
	
@app.route('/ircServers/connect', methods=['POST'])
def api_connect():
	return ""	

@app.route('/ircServers/join/<channel>', methods=['GET'])
def api_joinChannel():
	return ""	

@app.route('/errorLogs/report', methods=['POST'])
def api_report():
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

app.error_handler_spec[None][404] = not_found

if __name__ == '__main__':
    app.run(debug=True)
