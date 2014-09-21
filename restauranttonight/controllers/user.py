from dbcommons.classes.dbcon import DBCon
from restauranttonight.helpers.stripeutils import createStripeCustomer, chargeStripeCustomer
import stripe
import traceback

#http://devservices.mygola.com/restauranttonight/createuser?name=nitin&phone=123456789&token=tok_14etqK4jfDv2nYm0WAZB7ufD
def create(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params
		name = request_params['name']
		phone = request_params['phone']
		token = request_params['token']
		if not (phone and token):
			return {
				'status': 'error',
				'data': {
					'msg': "empty phone/token not allowed"
					}
			}
		device_token = request_params.get('device_token')
		if not device_token:
			device_token = ''
		phone = phone.replace('-','').replace('+','')
		if len(phone == 10):
			phone = '91' + phone
		qry = "select * from users where phone = '%s'" %(phone)
		user = dbCon.fetch_one(qry)
		if user:
			return {
				'status': 'success',
				'data': {
					'user_id': user['id']
				}
			}
		stripe.api_key = request.registry.settings['stripe.api_key']	
		customer_id, card_id = createStripeCustomer(token)
		if not (phone and token):
			return {
				'status': 'error',
				'data': {
					'msg': "empty phone not allowed"
					}
			}		
		qry = "insert into users values (null, '%s', '%s', '%s', '%s', '%s')" %(name, device_token, phone, card_id, customer_id)
		print qry
		user_id = dbCon.insert(qry)
		print user_id
		return {
			'status': 'success',
			'data': {
				'user_id': user_id
			}
		}
	except:		
		return {
			'status': 'error',
			'data': {
				'msg': "server side error"
			}
		}

#http://devservices.mygola.com/restauranttonight/createuserdeal?user_id=2&deal_id=3
def createDeal(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params
		deal_id = request_params.get('deal_id')
		user_id = request_params.get('user_id')
		qry = "insert into user_deals values (null, %s, %s, '%s')" %(user_id, deal_id, 'claimed')
		user_deal_id = dbCon.insert(qry)
		return {
			'status': 'success',
			'data': {
				'user_deal_id': user_deal_id
			}
		}
	except:		
		return {
			'status': 'error',
			'data': {
				'msg': "server side error"
			}
		}

#http://devservices.mygola.com/restauranttonight/charge?user_id=6&amount=20
def charge(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params
		amount = int(float(request_params.get('amount'))*100)
		user_id = request_params.get('user_id')
		deal_id = request_params.get('deal_id')
		qry = "select * from users u join user_deals ud on u.id = ud.user_id where ud.status = 'claimed' and u.id = %s and ud.deal_id = %s" %(user_id, deal_id)		
		user = dbCon.fetch_one(qry)		
		stripe.api_key = request.registry.settings['stripe.api_key']
		charge_id = chargeStripeCustomer(user['customer_id'], user['card_id'], amount)

		qry = "update user_deals set status = 'close' where user_id = %s and deal_id = %s" %(user_id, deal_id)
		dbCon.update(qry)

		return {
			'status': 'success',
			'data': {
				'charge_id': charge_id
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

#http://devservices.mygola.com/restauranttonight/mydeals?user_id=2
def getMyDeals(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params
		time = request_params.get('time')
		user_id = request_params.get('user_id')

		qry = "select * from user_deals ud join deals d on ud.deal_id = d.id join restaurants r on r.id = d.restaurant_id where ud.user_id = %s and ud.status = 'claimed'" %(user_id)
		my_deals = dbCon.fetch_all(qry)
		print my_deals
		my_deals = [_formatMyDeal(deal) for deal in my_deals]		
		return {
			'status': 'success',
			'data': {
				'deals': my_deals
			}
		}		
	except:		
		return {
			'status': 'error',
			'data': {
				'msg': "server side error"
			}
		}

def _formatMyDeal(deal):
	return {'id':deal['d.id'], 'name':deal['name'], 'lat': float(deal['latitude']), 'lng': float(deal['longitude']), 'text': deal['text'], 'start_time': deal['start_time'], 'end_time': deal['end_time'], 'address': deal['address'], 'pic_url': deal['pic_url'], 'deal_type': deal['deal_type'], 'deal_msg': deal['deal_msg'], 'restaurant_id':deal['r.id'], 'user_deal_id': deal['id']}


def unclaim(request):
	try:
		DB_STR = request.registry.settings['sqlalchemy.url']
		dbCon = DBCon(DB_STR)
		request_params = request.params		
		deal_id = request_params.get('deal_id')
		user_id = request_params.get('user_id')
		
		qry = "update user_deals set status = 'close' where user_id = %s and deal_id = '%s" %(user_id, deal_id)
		user_deal = dbCon.update(qry)

		return {
			'status': 'success',
			'data': {
				'user_deal_id': user_deal['id']
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

#unclaim a coupon
#dispute
#expire deal		