import requests

class Store:

	def __init__(self, address):
		# Initialize variables
		city = address.city
		dominos_city = address.address[0][0]
		dominos_locality = address.address[0][1]
		dominos_code = address.address[-1]
		self.store_code = dominos_code[1:]

		# Create session
		url = "https://pizzaonline.dominos.co.in"
		self.session = requests.Session()
		response = self.session.get(url)

		# Get CSRF token
		self.extract_csrf_token(response)

		# Compulsory initial request
		self.make_initial_request(city, dominos_city, dominos_locality, dominos_code)

		# Save menu
		self.get_menu()


	def extract_csrf_token(self, response):
		response = response.text.split('\n')
		html_line_containing_csrf = ''
		for r in response:
			if "csrf_token" in r:
				html_line_containing_csrf = r
				break

		sub1 = html_line_containing_csrf.index('value="') + len('value="')
		sub2 = html_line_containing_csrf.index('" name=')
		self.csrf_token = html_line_containing_csrf[sub1:sub2]


	def make_initial_request(self, city, dominos_city, dominos_locality, dominos_code):
		# Make POST request for initializing order with csrf_token.
		# This saves somes data in the cookies on the server side
		# that allows us to make further requests like get menu.

		url = "https://pizzaonline.dominos.co.in/build/order"
		data = {
			'home-or-pickup': 'home-delivery',
			'combobox': city,
			'home_delivery': 'Popular Cities',
			'pick_up': 'Popular Cities',
			'combobox_locality': dominos_city + '^' + dominos_locality + '^' + dominos_code,
			'request_page': 'welcome',
			'first_time_customer': 'yes',
			'store_code': '',
			'store_name': '',
			'csrf_token': self.csrf_token
		}
		response = self.session.post(url, data = data)


	def get_menu(self):
		url = "https://pizzaonline.dominos.co.in/view/product/?isAjaxRequest=json&store_code=" + self.store_code
		r = self.session.get(url)
		self.menu = r.json()

	def view_order(self):
		url = "https://pizzaonline.dominos.co.in/view/cart"
		data = {
			'isAjaxRequest': 'json'
		}
		response = self.session.post(url, data = data)
		print(response.json())