from dbcommons.classes.dbcon import DBCon

#http://devservices.mygola.com/restauranttonight/createuserdeal?user_id=2&deal_id=3
def create(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params		
		text = request_params.get('text')
		start_time = request_params.get('start_time')
		end_time = request_params.get('end_time')
		date = request_params.get('date')		
		reservations_allowed = request_params.get('count')
		restaurant_id = request_params.get('restaurant_id')
		deal_type = request_params.get('deal_type')
		deal_msg = request_params.get('deal_msg')
		qry = "insert into deals values (null, '%s', %s, %s, '%s','new', %s, %s ,'%s', '%s')" %(text, start_time, end_time, date, reservations_allowed, restaurant_id, deal_type, deal_msg)
		print qry
		deal_id = dbCon.insert(qry)
		return {
			'status': 'success',
			'data': {
				'deal_id': deal_id
			}
		}
	except:	
		import traceback
		traceback.print_exc()	
		return {
			'status': 'error',
			'data': {
				'msg': "server side error"
			}
		}	


#deleteDeal
