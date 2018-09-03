import requests
from terminaltables import AsciiTable

class Order:
	def __init__(self, store):
		# Save menu and session
		self.menu = store.menu
		self.session = store.session
		self.items = []

	def get_product_details(self, item_id, size):
		return_data = {}
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
					
					return_data['id'] = product_id
					return_data['name'] = product_name
					return_data['price'] = price
					return_data['default_product_str'] = default_product_str
					return_data['size'] = size

					return return_data


	def add_item(self, item_id, size):
		product_details = self.get_product_details(item_id, size)
		default_product_str = product_details['default_product_str']
		
		# Add item to dominos cart
		url = 'https://pizzaonline.dominos.co.in/add/product'
		data = {
			'product': default_product_str,
			'quantity': '1',
			'isAjaxRequest': 'json'
		}
		self.session.post(url, data = data)


	def remove_item(self, basket_id):
		# Remove basket from cart
		url = 'https://pizzaonline.dominos.co.in/remove/cartProduct'
		data = {
			'basketId': basket_id,
			'isAjaxRequest': 'json',
			'csrf_token': ''
		}
		self.session.post(url, data = data)


	def get_order(self, option):
		# When option = 0 return response
		# When option = 1 print response
		url = 'https://pizzaonline.dominos.co.in/view/cart'
		data = {
			'isAjaxRequest': 'json'
		}
		response = self.session.post(url, data = data)
		response = response.json()
		table_data = []
	
		customer_basket_info = response['customer_basket_info']
		table_data.append(['BASKET ID', 'NAME', 'QUANTITY', 'PRICE'])
		for item in customer_basket_info:
			product_name = item['products_name']
			basket_id = item['customers_basket_id']
			price = item['final_price']
			quantity = item['customers_basket_quantity']
			table_data.append([basket_id, product_name, quantity, price])
		
		if option:
			net_price = response['net_price']
			total_price = response['total_price']
			table_data.append(['NET PRICE',net_price,'TOTAL PRICE', total_price])
			table = AsciiTable(table_data)
			table.inner_row_border = True
			print()
			print(table.table)
		else:
			return table_data[1:]
		