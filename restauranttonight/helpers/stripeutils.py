import stripe

def createStripeCustomer(token):
	customer = stripe.Customer.create(
		description="Customer for restauranttonight",
		card=token
	)
	customer_id = customer.id
	cards = stripe.Customer.retrieve(customer_id).cards.all()
	card_id = cards['data'][0].id
	return (customer_id, card_id)

def chargeStripeCustomer(customer_id, card_id, amount):
	charge = stripe.Charge.create(
		amount=amount,
		currency='inr',
		card=card_id,
		customer=customer_id,      
		description='tetsing for restauranttonight'
	)
	return charge.id	
