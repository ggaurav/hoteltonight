import json, requests
from restauranttonight.helpers.geometry import boundingBox
from restauranttonight.helpers.responseformat import SuccessResp, ErrorResp
from dbcommons.classes.dbcon import DBCon
from restauranttonight.helpers.utilities import normalize, _formatTo6Digits

DISTANCE = "2km"
JD_COUNT = 10


#http://0.0.0.0:8969/nearby?lat=12.9715987&lng=77.5945627
def nearby(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params
		lat = request_params['lat']
		lng = request_params['lng']
		time = request_params.get('time')
		index = 0

		while True and index < JD_COUNT:
			#http://hack2014.justdial.com/search/json/justdialapicat/restaurants/kebab/bangalore/13043647/77620617/2km/20/0
			url = request.registry.settings['justdial.url'] + "/search/json/justdialapicat/restaurants/food/bangalore/%s/%s/%s/20/%d" %(_formatTo6Digits(lat), _formatTo6Digits(lng), DISTANCE, index)
			print url
			data = requests.get(url)
			jdRestaurants = data.json()
			jdRestaurants = jdRestaurants['results']
			jdRestaurantDocIds = []
			print jdRestaurants
			for restaurant in jdRestaurants:
				print '----'
				print restaurant				
				jdRestaurantDocIds.append(str(restaurant['docId']))
			print jdRestaurantDocIds
			jdRestaurantDocIdsStr = "'" +  "','".join(jdRestaurantDocIds) + "'"
			qry = "select * from restaurants r join deals d on r.id = d.restaurant_id where r.jd_doc_id in (%s)" %(jdRestaurantDocIdsStr);
			print qry
			availableRestaurants = dbCon.fetch_all(qry)
			print availableRestaurants
			# availableRestaurants = [normalize(restaurant) for restaurant in availableRestaurants]
			# print availableRestaurants
			availableRestaurants = [_formatRestaurant(restaurant) for restaurant in availableRestaurants]
			# surroundingBox = boundingBox(lat, lng, 20)
			# qry = "select * from restaurants r join deals d on r.id = d.restaurant_id where (r.latitude between %f and %f) and (r.longitude between %f and %f) " %(surroundingBox[0], surroundingBox[2], surroundingBox[1], surroundingBox[3])
			# print qry
			if availableRestaurants:
				return {
					'status': 'success',
					'data': {
						'deals': availableRestaurants
					}
				}

			index += 1
		return {
				'status': 'error',
				'data': {
					'msg': "no restaurants exists"
				}
		}
		
	except:	
		return {
				'status': 'error',
				'data': {
					'msg': "server side error"
				}
		}


#http://0.0.0.0:8969/nearby?lat=12.9715987&lng=77.5945627
def onroute(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params
		lat1 = request_params['lat1']
		lng1 = request_params['lng1']
		lat2 = request_params['lat2']
		lng2 = request_params['lng2']
		time = request_params.get('time')
		
		latLngs = [[lat1, lng1]]
		#here findviaroutes
		url = request.registry.settings['justdial.url'] + "/directions/viaroute?z=17&output=json&loc=%s,%s&loc=%s,%s&instructions=true" %(lat1, lng1, lat2, lng2)
		print url
		data = requests.get(url)
		data = data.json()
		if data and 'via_points' in data and data['via_points']:
			latLngs.extend(data['via_points'])
		latLngs.append([lat2, lng2])
		print latLngs				
		for latLng in latLngs:
			index = 0
			while True and index < JD_COUNT:
				lat = latLng[0]
				lng = latLng[1]
				#http://hack2014.justdial.com/search/json/justdialapicat/restaurants/kebab/bangalore/13043647/77620617/2km/20/0
				url = request.registry.settings['justdial.url'] + "/search/json/justdialapicat/restaurants/food/bangalore/%s/%s/%s/20/%d" %(_formatTo6Digits(lat), _formatTo6Digits(lng), DISTANCE, index)
				print url
				data = requests.get(url)
				jdRestaurants = data.json()
				jdRestaurants = jdRestaurants['results']
				jdRestaurantDocIds = []
				print jdRestaurants
				for restaurant in jdRestaurants:
					print '----'
					print restaurant				
					jdRestaurantDocIds.append(str(restaurant['docId']))
				print jdRestaurantDocIds
				jdRestaurantDocIdsStr = "'" +  "','".join(jdRestaurantDocIds) + "'"
				qry = "select * from restaurants r join deals d on r.id = d.restaurant_id where r.jd_doc_id in (%s)" %(jdRestaurantDocIdsStr);
				print qry
				availableRestaurants = dbCon.fetch_all(qry)
				print availableRestaurants
				# availableRestaurants = [normalize(restaurant) for restaurant in availableRestaurants]
				# print availableRestaurants
				availableRestaurants = [_formatRestaurant(restaurant) for restaurant in availableRestaurants]
				# surroundingBox = boundingBox(lat, lng, 20)
				# qry = "select * from restaurants r join deals d on r.id = d.restaurant_id where (r.latitude between %f and %f) and (r.longitude between %f and %f) " %(surroundingBox[0], surroundingBox[2], surroundingBox[1], surroundingBox[3])
				# print qry
				if availableRestaurants:
					return {
						'status': 'success',
						'data': {
							'deals': availableRestaurants
						}
					}

				index += 1
		return {
				'status': 'error',
				'data': {
					'msg': "no restaurants exists"
				}
		}
		
	except:
		traceback.print_exc	
		return {
				'status': 'error',
				'data': {
					'msg': "server side error"
				}
		}

def _formatRestaurant(restaurant):
	return {'restaurant_id':restaurant['id'], 'name':restaurant['name'], 'lat': float(restaurant['latitude']), 'lng': float(restaurant['longitude']), 'text': restaurant['text'], 'start_time': restaurant['start_time'], 'end_time': restaurant['end_time'], 'address': restaurant['address'], 'pic_url': restaurant['pic_url'], 'deal_type': restaurant['deal_type'], 'deal_msg': restaurant['deal_msg'], 'id': restaurant['d.id']}


#search personalisation	