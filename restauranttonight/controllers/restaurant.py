from dbcommons.classes.dbcon import DBCon
from restauranttonight.helpers.utilities import _formatTo6Digits
from restauranttonight.helpers.jarowinkler import getSimilarity
from restauranttonight.helpers.geometry import boundingBox
import requests

DISTANCE = 2
THRESHOLD_SCORE = 0.8
JD_COUNT = 5

#http://0.0.0.0:8969/createrestaurantowner?phone=8105254510&password=123
def createOwner(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params
		phone = request_params.get('phone')
		password = request_params.get('password')
		if not (password and phone):
			return {
				'status': 'error',
				'data': {
					'msg': "empty phone/password not allowed"
					}
			}
		qry = "select * from restaurant_owners where phone = '%s'" %(phone)
		owner = dbCon.fetch_one(qry)		
		if owner and str(owner['password']) == str(password):
			return {
				'status': 'success',
				'data': {
					'owner_id': owner['id']
				}
			}
		elif owner:
			return {
				'status': 'error',
				'data': {
					'msg': "wrong password"
					}
			}
		else:
			qry = "insert into restaurant_owners values (null, '%s', '%s')" %(password, phone)
			owner_id = dbCon.insert(qry)
			return {
				'status': 'success',
				'data': {
					'owner_id': owner['id']
				}
			}
	except:			
		return {
			'status': 'error',
			'data': {
				'msg': "server side error"
			}
		}

def _searchOnJustDial(dbCon, request, phone, owner_id, name, lat, lng, address, cost_for_2, email, pic_url):
	qry = "select * from restaurants where phone = %s" %(phone);
	print qry
	ourMatchingRestaurant = dbCon.fetch_one(qry)
	#get the closest matching
	owner_id = int(owner_id)
	if ourMatchingRestaurant and str(ourMatchingRestaurant['owner_id']) == str(owner_id):
		return {
				'status': 'success',
				'data': {
					'restaurant_id': ourMatchingRestaurant['id']
				}
			}
	elif ourMatchingRestaurant:
		return {
				'status': 'error',
				'data': {
					'msg': "Invalid owner"
					}
			}				
				
	#http://hack2014.justdial.com/search/json/mobilegetname/919343529202/3		
	url = request.registry.settings['justdial.url'] + "/search/json/mobilegetname/%d/1" %(long(phone))
	print url
	data = requests.get(url)
	jdRestaurant = data.json()
	jdRestaurant = jdRestaurant['data']
	if jdRestaurant and len(jdRestaurant) > 0:
		jdRestaurant = jdRestaurant[0]
		print jdRestaurant
		qry = "insert into restaurants values (null, %s, '%s', %s,%s, null,'%s', '%s','%s','%s', '%s', '%s', %d)" %(jdRestaurant['id'], name, lat, lng, address, cost_for_2, email, phone, pic_url, jdRestaurant['jdid'], owner_id)
		print qry
		restaurant_id = dbCon.insert(qry)
		return {
			'status': 'success',
			'data': {
				'restaurant_id': restaurant_id
			}
		}
	#hit 5 times	
	#	
	index = 0
	maxScore = 0
	maxMatchedRestaurant = None
	while True and index < JD_COUNT:
		#http://hack2014.justdial.com/search/json/justdialapicat/restaurants/kebab/bangalore/13043647/77620617/2km/20/0
		url = request.registry.settings['justdial.url'] + "/search/json/justdialapicat/restaurants/%s/bangalore/%s/%s/2km/20/%d" %(name, _formatTo6Digits(lat), _formatTo6Digits(lng), index)
		print url
		data = requests.get(url)
		jdRestaurants = data.json()
		jdRestaurants = jdRestaurants['results']
		jdRestaurantDocIds = []
		print jdRestaurants
		for restaurant in jdRestaurants:
			print '----'
			print restaurant
			score = getSimilarity(name, restaurant['name'])
			if score > THRESHOLD_SCORE and score > maxScore:
				maxScore = score
				maxMatchedRestaurant = restaurant
			jdRestaurantDocIds.append(str(restaurant['docId']))
		print jdRestaurantDocIds
		jdRestaurantDocIdsStr = "'" +  "','".join(jdRestaurantDocIds) + "'"
		
		qry = 'select * from restaurants where owner_id = %d and jd_doc_id in (%s) ' %(int(owner_id), jdRestaurantDocIdsStr);
		print qry
		jdRestaurant = dbCon.fetch_one(qry)
		if jdRestaurant:
			return {
				'status': 'success',
				'data': {
					'restaurant_id': jdRestaurant['id']
				}
			}
		index += 1

	if maxMatchedRestaurant:
		print maxMatchedRestaurant
		qry = "insert into restaurants values (null, null, '%s', %s,%s, null,'%s', '%s','%s','%s', '%s', '%s', %d)" %(name, lat, lng, address, cost_for_2, email, phone, pic_url, maxMatchedRestaurant['docId'], int(owner_id))
		print qry
		restaurant_id = dbCon.insert(qry)
		return {
			'status': 'success',
			'data': {
				'restaurant_id': restaurant_id
			}
		}

	return {
				'status': 'error',
				'data': {
					'msg': "Not able to find restaurant on just dial"
					}
			}				
	#

#based on phn check in our db if exists return id, 
#else search jd using phn api if exists create in our db and return
#else hit category api and for each result use similarity if score > .80 and exists in our db return id, 
#if score > .80 and does not exist, create and return id, 
#else return error
def create(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params
		name = request_params.get('name')
		email = request_params.get('email')		
		pic_url = request_params.get('pic_url')
		address = request_params.get('address')
		cost_for_2 = request_params.get('cost_for_2')		
		lat = request_params['lat']
		lng = request_params['lng']
		owner_id = request_params['owner_id']
		phone = request_params.get('phone')
		if not phone:
			return {
				'status': 'error',
				'data': {
					'msg': "empty phone not allowed"
					}
			}
		if(len(phone) == 10):
			phone = '91' + phone	
		phone = long(phone)	
		return _searchOnJustDial(dbCon, request, phone, owner_id, name, lat, lng, address, cost_for_2, email, pic_url)			
	except:	
		import traceback
		traceback.print_exc()	
		return {
			'status': 'error',
			'data': {
				'msg': "server side error"
			}
		}

#http://devservices.mygola.com/restauranttonight/restaurantdeals?restaurant_id=4
def getAllMyDeals(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params		
		restaurant_id = request_params.get('restaurant_id')
		qry = "select * from deals d join restaurants r on r.id = d.restaurant_id where d.status != 'closed' and d.restaurant_id = %s" %(restaurant_id)
		my_deals = dbCon.fetch_all(qry)
		print my_deals
		my_deals = [_formatMyDeal(dbCon, deal) for deal in my_deals]		

		return {
			'status': 'success',
			'data': {
				'deals': my_deals
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

def _formatMyDeal(dbCon, deal):	
	qry = "select count(*) as count from user_deals where deal_id = %s" %(deal['id'])
	data = dbCon.fetch_one(qry)
	reserved = data['count']
	left = int(deal['reservations_allowed']) - 	reserved
	return {'id':deal['id'], 'name':deal['name'], 'lat': float(deal['latitude']), 'lng': float(deal['longitude']), 'text': deal['text'], 'start_time': deal['start_time'], 'end_time': deal['end_time'], 'address': deal['address'], 'pic_url': deal['pic_url'], 'deal_type': deal['deal_type'], 'deal_msg': deal['deal_msg'], 'restaurant_id':deal['r.id'], 'reserved': reserved, 'left': left}

#http://devservices.mygola.com/restauranttonight/restaurantreserveddeals?restaurant_id=4
def getAllMyReservedDeals(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params		
		restaurant_id = request_params.get('restaurant_id')
		qry = "select * from deals d join restaurants r on r.id = d.restaurant_id where d.status != 'closed' and d.restaurant_id = %s" %(restaurant_id)
		#qry = "select * from deals d join restaurants r on r.id = d.restaurant_id join user_deals ud on d.id = ud.deal_id join users u on ud.user_id = u.id where d.status != 'closed' and ud.status != 'expired' and d.restaurant_id = %s" %(restaurant_id)
		my_deals = dbCon.fetch_all(qry)
		print my_deals
		my_reserved_deals = [_formatMyReservedDeal(dbCon, deal) for deal in my_deals]		
		my_reserved_deals = [deal for deal in my_reserved_deals if deal]
		return {
			'status': 'success',
			'data': {
				'deals': my_reserved_deals
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

def _formatMyReservedDeal(dbCon, deal):	
	qry = "select * from user_deals ud join users u on ud.user_id = u.id where ud.status != 'expired' and ud.deal_id = %s" %(deal['id'])
	users = dbCon.fetch_all(qry)
	if not users:
		return
	users = [{'user_id': user['u.id'], 'phone': user['phone'], 'name': user['name']} for user in users]	
	return {'id':deal['id'], 'name':deal['name'], 'lat': float(deal['latitude']), 'lng': float(deal['longitude']), 'text': deal['text'], 'start_time': deal['start_time'], 'end_time': deal['end_time'], 'address': deal['address'], 'pic_url': deal['pic_url'], 'deal_type': deal['deal_type'], 'deal_msg': deal['deal_msg'], 'restaurant_id':deal['r.id'], 'users': users}
