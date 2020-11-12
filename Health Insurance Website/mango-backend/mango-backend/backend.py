from bottle import run, route, get, response, request
import MySQLdb

"""
Thanks to Ron Rothman from https://stackoverflow.com/questions/17262170/bottle-py-enabling-cors-for-jquery-ajax-requests
for instructions on how to do this
"""
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            return fn(*args, **kwargs)

    return _enable_cors



@route('/getrecords')
@enable_cors
#username -> the name of the user
def find_accesible():
	username = request.params.get('username')
	entries = {}
	drugs = []
	cursor.execute('SELECT id, drugname, cost, ins, zipcode from drugs where id in (SELECT recordID from UserDruRecords where user = %s)', [username])
	for (id, drugname, cost, ins, zipcode) in cursor.fetchall():
		drugs.insert(0, {'id':id, 'name':drugname, 'cost':str(cost), 'hasInsurance':ins, 'zipcode':zipcode})	


	cursor.execute('SELECT id, procname, cost, ins, zipcode from medProcedures where id in (SELECT recordID from UserProRecords where user = %s)', [username])
	procedures = []
	for (id, procname, cost, ins, zipcode) in cursor.fetchall():
		procedures.insert(0, {'id':id, 'name':procname, 'cost':str(cost), 'hasInsurance':ins, 'zipcode':zipcode})

	ret = {}
	ret['user'] = username
	ret['status'] = 'success'
	entries['drugs'] = drugs
	entries['procedures'] = procedures
	ret['entries'] = entries
	return ret


# drug or procedure, type = d or p
# recordID
# name
# cost
# ins
# zipcode
@route('/update')
@enable_cors
def update_record():
	typ = request.params.get('type')
	
	id  = int(request.params.get('recordID'))

	str = 'Update medProcedures set procname = %s, cost = %s, ins = %s, zipcode = %s where id = %s'
	if typ == 'd':
		str = "Update drugs set drugname = %s, cost = %s, ins = %s, zipcode = %s  where id = %s"
	data = [request.params.get('name'), float(request.params.get('cost')), bool(request.params.get('ins')), request.params.get('zipcode'), id]
	print(str, data)
	cursor.execute(str, data)
	connection.commit()	
	return {'status' : 'success'}	


	
@route('/delete')
@enable_cors
# drug or procedure, type = d or p
#recordID -> the record to delete
#username -> the name of the user who owns the record
def delete_record():

	typ = request.params.get('type')
	id  = int(request.params.get('recordID'))
	uname = request.params.get('username')

	str = "Delete from medProcedures where id = %s"
	if typ == 'd':
	        str = "Delete from drugs where id = %s"
	cursor.execute(str, (id,))
	
	str = "Delete from UserProRecords where user = %s and recordID = %s"
	if typ == "d":
		str = "Delete from UserDruRecords where user = %s and recordID = %s"
	cursor.execute(str, (uname, id))

	connection.commit()
	return {'status' : 'success'}


# drug or procedure, type = d or p
# name
# cost
# ins
# zipcode
# username
@route('/addrecord')
@enable_cors
def insert_record():
	typ = request.params.get('type')
	insert_str1 = "INSERT INTO medProcedures (procname, cost, ins, zipcode) VALUES (%s, %s, %s, %s)"
	insert_str2 = "INSERT INTO drugs (drugname, cost, ins, zipcode) VALUES (%s, %s, %s, %s)"
	str = insert_str1
	dname = request.params.get('name')
	uname = request.params.get('username')
	if typ == 'd':
		str = insert_str2
	data = (dname, float(request.params.get('cost')), bool(request.params.get('ins')), request.params.get('zipcode'))
	cursor.execute(str, data)

	if typ == 'd':
		cursor.execute("SELECT id FROM drugs WHERE drugname = %s and cost = %s and ins = %s and zipcode = %s", data)
		id = cursor.fetchone()
		edgecase = cursor.fetchall()
		cursor.execute("INSERT INTO UserDruRecords (user, recordID) VALUES (%s, %s)", (uname, id))
	else:
		cursor.execute("SELECT id FROM medProcedures WHERE procname = %s and cost = %s and ins = %s and zipcode = %s", data)
		id = cursor.fetchone()
		edgecase = cursor.fetchall()
		cursor.execute("INSERT INTO UserProRecords (user, recordID) VALUES (%s, %s)", (uname, id))
	
	connection.commit()
	return {'status' : 'success', 'id': id}




connection = MySQLdb.connect (host = "localhost", user = "mmm", passwd = "mmm", db = "mango")
cursor = connection.cursor()
'''
cursor.execute ("SELECT VERSION()")
row = cursor.fetchone()
print("server version:", row[0])
'''


run(host='localhost', port=8080)
