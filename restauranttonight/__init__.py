from pyramid.config import Configurator
from pyramid.renderers import JSON

def main(global_config, **settings):
	""" This function returns a Pyramid WSGI application.
	"""
	config = Configurator(settings=settings)
	config.include('pyramid_chameleon')	
	config.add_renderer('json', JSON(indent=4))
	config.add_static_view('static', 'static', cache_max_age=3600)
	config.add_route('home', '/')
	config.add_route('nearby', '/restauranttonight/nearby', request_method='GET')
	config.add_view(route_name='nearby', view='restauranttonight.controllers.search.nearby', renderer='json')

	config.add_route('createUser', '/restauranttonight/createuser', request_method='GET')
	config.add_view(route_name='createUser', view='restauranttonight.controllers.user.create', renderer='json')

	config.add_route('createRestaurantOwner', '/restauranttonight/createrestaurantowner', request_method='GET')
	config.add_view(route_name='createRestaurantOwner', view='restauranttonight.controllers.restaurant.createOwner', renderer='json')

	config.add_route('createRestaurant', '/restauranttonight/createrestaurant', request_method='GET')
	config.add_view(route_name='createRestaurant', view='restauranttonight.controllers.restaurant.create', renderer='json')

	config.add_route('createMyDeal', '/restauranttonight/createuserdeal', request_method='GET')
	config.add_view(route_name='createMyDeal', view='restauranttonight.controllers.user.createDeal', renderer='json')

	config.add_route('charge', '/restauranttonight/charge', request_method='GET')
	config.add_view(route_name='charge', view='restauranttonight.controllers.user.charge', renderer='json')

	config.add_route('myDeals', '/restauranttonight/mydeals', request_method='GET')
	config.add_view(route_name='myDeals', view='restauranttonight.controllers.user.getMyDeals', renderer='json')

	config.add_route('createDeal', '/restauranttonight/createdeal', request_method='GET')
	config.add_view(route_name='createDeal', view='restauranttonight.controllers.deals.create', renderer='json')

	config.add_route('restaurantDeals', '/restauranttonight/restaurantdeals', request_method='GET')
	config.add_view(route_name='restaurantDeals', view='restauranttonight.controllers.restaurant.getAllMyDeals', renderer='json')

	config.add_route('restaurantResrvedDeals', '/restauranttonight/restaurantreserveddeals', request_method='GET')
	config.add_view(route_name='restaurantResrvedDeals', view='restauranttonight.controllers.restaurant.getAllMyReservedDeals', renderer='json')

	config.add_route('onroute', '/restauranttonight/onroute', request_method='GET')
	config.add_view(route_name='onroute', view='restauranttonight.controllers.search.onroute', renderer='json')
	

	config.scan()
	return config.make_wsgi_app()

