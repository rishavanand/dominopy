import requests

class Order:
	def __init__(self, store):
		# Save menu and session
		self.menu = store.menu
		self.session = store.session
		self.items = []

	def add_item(self, item_id, size):
		# Search for item in menu
		item_id = str(item_id)
		item_list = self.menu['pizza']
		# For all category
		for category in item_list:
			total_item_in_category = len(category) - 3
			# For all products in present category
			for i in range(total_item_in_category):
				product_id = category[str(i)]['product_id']
				# If item found in menu
				if item_id == product_id:
					product_name = category[str(i)]['product_name']
					price = category[str(i)]['product_subtitle']
					price = price.replace('*', '').replace('+', '').replace('^', '')
					price = price.split(' ')
					price_r = price[0]
					price_m = price[1]
					price_l = price[2]
					final_price = 0
					default_product_str = category[str(i)]['default_product_str']
					if size == 'r':
						price = price_r
						default_product_str = default_product_str['Regular']
					elif size == 'm':
						price = price_m
						default_product_str = default_product_str['Medium']
					else:
						price = price_l
						default_product_str = default_product_str['Large']
						
					# Add item to dominos cart
					url = 'https://pizzaonline.dominos.co.in/add/product'
					data = {
						'product': default_product_str,
						'quantity': '1',
						'isAjaxRequest': 'json'
					}
					self.session.post(url, data = data)
					break

	def view_order(self):
		url = 'https://pizzaonline.dominos.co.in/view/cart'
		data = {
			'isAjaxRequest': 'json'
		}
		response = self.session.post(url, data = data)
		print(response.json())

	