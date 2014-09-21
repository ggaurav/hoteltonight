import json, requests, traceback
from restauranttonight.helpers.geometry import boundingBox, findDistance
from restauranttonight.helpers.responseformat import SuccessResp, ErrorResp
from dbcommons.classes.dbcon import DBCon
from restauranttonight.helpers.utilities import normalize, _formatTo6Digits

DISTANCE = "2km"
JD_COUNT = 5


#http://0.0.0.0:8969/restauranttonight/nearby?lat=12.9715987&lng=77.5945627&date=2014-09-21&time=600
def nearby(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params
		lat = request_params['lat']
		lng = request_params['lng']
		time = request_params['time']
		date = request_params['date']
		index = 0
		#Since just dial gives only 20 items in a single call
		#TODO call it in thread
		allAvailabeRestaurants = []
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
				jdRestaurantDocIds.append(str(restaurant['docId']))
			if jdRestaurantDocIds:	
				print jdRestaurantDocIds
				jdRestaurantDocIdsStr = "'" +  "','".join(jdRestaurantDocIds) + "'"
				qry = "select * from restaurants r join deals d on r.id = d.restaurant_id where d.date = '%s' and (%s between d.start_time and d.end_time) and r.jd_doc_id in (%s) group by r.id order by d.end_time desc" %(date, time, jdRestaurantDocIdsStr);
				print qry
				availableRestaurants = dbCon.fetch_all(qry)
				print availableRestaurants			
				availableRestaurants = [_formatRestaurant(restaurant, lat, lng) for restaurant in availableRestaurants]			
				allAvailabeRestaurants.extend(availableRestaurants)			
			index += 1
		if len(allAvailabeRestaurants) < 10:			
			ourBoundingBox = boundingBox(lat, lng, 3)		
			qry = "select * from restaurants r join deals d on r.id = d.restaurant_id where d.date = '%s' and (%s between d.start_time and d.end_time) and (r.latitude between %s and %s) and (r.longitude between %s and %s)  group by r.id order by d.end_time desc" %(date, time, ourBoundingBox[0], ourBoundingBox[2], ourBoundingBox[1], ourBoundingBox[3]);
			print qry
			availableRestaurants = dbCon.fetch_all(qry)
			print availableRestaurants			
			availableRestaurants = [_formatRestaurant(restaurant, lat, lng) for restaurant in availableRestaurants]						
			allAvailabeRestaurants.extend(availableRestaurants)			
		#if deal is availabe for the matching date time return it
		if allAvailabeRestaurants:
			sortedAllAvailabeRestaurants = sorted(allAvailabeRestaurants, key=lambda k: (-int(k['end_time'])))
			returnVal = []
			pickedRestaurantIds = []
			for sortedAllAvailabeRestaurant in sortedAllAvailabeRestaurants:
				if sortedAllAvailabeRestaurant['restaurant_id'] not in pickedRestaurantIds:
					returnVal.append(sortedAllAvailabeRestaurant)
				pickedRestaurantIds.append(sortedAllAvailabeRestaurant['restaurant_id'])			
			return {
				'status': 'success',
				'data': {
					'deals': returnVal
				}
			}
			
		return {
				'status': 'error',
				'data': {
					'msg': "no restaurants exists"
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


#http://0.0.0.0:8969/restauranttonight/onroute?lat1=12.9715987&lng1=77.5945627&lat2=12.9715987&lng2=77.5945627&date=2014-09-21&time=1220
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
		date = request_params['date']

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
		allAvailabeRestaurants = []				
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
					jdRestaurantDocIds.append(str(restaurant['docId']))
				if jdRestaurantDocIds:
					print jdRestaurantDocIds
					jdRestaurantDocIdsStr = "'" +  "','".join(jdRestaurantDocIds) + "'"				
					qry = "select * from restaurants r join deals d on r.id = d.restaurant_id where d.date = '%s' and (%s between d.start_time and d.end_time) and r.jd_doc_id in (%s)" %(date, time, jdRestaurantDocIdsStr)
					print qry
					availableRestaurants = dbCon.fetch_all(qry)
					print availableRestaurants				
					availableRestaurants = [_formatRestaurant(restaurant, lat, lng) for restaurant in availableRestaurants]					
					allAvailabeRestaurants.extend(availableRestaurants)								
				index += 1

		if availableRestaurants:
			return {
				'status': 'success',
				'data': {
					'deals': allAvailabeRestaurants
				}
			}

		return {
				'status': 'error',
				'data': {
					'msg': "no restaurants exists"
				}
		}
		
	except:
		traceback.print_exc()
		return {
				'status': 'error',
				'data': {
					'msg': "server side error"
				}
		}

def _formatRestaurant(restaurant, lat, lng):
	distance = findDistance(restaurant['latitude'], restaurant['longitude'], lat, lng)
	distance = str("%.1f" % distance) + "km"
	return {'restaurant_id':restaurant['id'], 'name':restaurant['name'], 'lat': float(restaurant['latitude']), 'lng': float(restaurant['longitude']), 'text': restaurant['text'], 'start_time': restaurant['start_time'], 'end_time': restaurant['end_time'], 'address': restaurant['address'], 'pic_url': restaurant['pic_url'], 'deal_type': restaurant['deal_type'], 'deal_msg': restaurant['deal_msg'], 'id': restaurant['d.id'], 'distance': distance}

#12.9715987,77.5945627
#12.9670503,77.5957239
#search personalisation	