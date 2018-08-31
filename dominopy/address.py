import requests

class Address:
	def __init__(self, city, locality):
		# Create session
		url = "https://pizzaonline.dominos.co.in"
		self.session = requests.Session()
		response = self.session.get(url)

		# Capitalize names and store in variables
		city = city.upper()
		locality = locality.upper()

		# Store original city name and locality
		self.city = city
		self.locality = locality

		# Check if city exists and get its localities
		localities = self.check_city_exists(city)

		# Check if locality exists and get locality code
		locality_code = self.check_locality_exists(locality, localities)

		# Format locality code
		locality_code = self.format_locality_code(locality_code)

		# Check final store address specified by Dominos
		self.get_final_store_address(locality_code, city)


	def get_final_store_address(self, locality_code, city):
		# Perform final check if locality and city exists using dominos api
		headers = { 'x-requested-with': 'XMLHttpRequest' }
		url = self.prepare_final_address_check_url(locality_code, city)
		response = self.session.get(url, headers = headers)
		response = response.json()

		# Raise exception is final address is invalid
		if not(response['status']):
			raise Exception('Invalid address!')
		else:
			self.address = locality_code


	def check_city_exists(self, city):
		# Check if city exists
		headers = { 'x-requested-with': 'XMLHttpRequest' }
		url = "https://pizzaonline.dominos.co.in/getLocality/homedelivery/?city_id=" + city
		response = self.session.get(url, headers = headers)
		response = response.json()

		# Raise exception if city not found
		if not(len(response['data'])):
			raise Exception('City not found!')
		else:
			localities = response['data']

		return localities


	def check_locality_exists(self, locality, localities):
		# Check if locality exists and get locality code
		locality_found = 0
		locality_code = ''
		for code, name in localities.items():
			if locality in name:
				locality_code = code
				locality_found = 1
				break

		# Raise exception if locality not found
		if not(locality_found):
			raise Exception('Locality not found!')

		return locality_code


	def format_locality_code(self, locality_code):
		locality_code = locality_code.split('^^')
		locality_code = [locality_code[0].split('^'), locality_code[1]]
		return locality_code


	def prepare_final_address_check_url(self, locality_code, city):
		array_length = len(locality_code[0])
		if array_length == 1:
			return("https://pizzaonline.dominos.co.in/getStoreAddress/?data%5Blocality%5D=" + locality_code[0][0] + "&data%5BsubLocality%5D=&data%5Barea1%5D=&city_id=" + city)
		elif array_length == 2:
			return("https://pizzaonline.dominos.co.in/getStoreAddress/?data%5Blocality%5D=" + locality_code[0][0] + "&data%5BsubLocality%5D=" + locality_code[0][1] + "&data%5Barea1%5D=&city_id=" + city)
		else:
			return("https://pizzaonline.dominos.co.in/getStoreAddress/?data%5Blocality%5D=" + locality_code[0][0] + "&data%5BsubLocality%5D=" + locality_code[0][1] + "&data%5Barea1%5D=" + locality_code[0][2] + "&city_id=" + city)

