import requests
import re
from terminaltables import AsciiTable

class Menu:
	def __init__(self, store):
		# Save menu
		self.menu = store.menu;

	def search(self, name):
		# Add table row headers
		table_data = [
		    ['ID', 'NAME', 'PRICE (R M L)'],
		]

		# Search for item in menu
		item_list = self.menu['pizza']
		for category in item_list:
			total_item_in_category = len(category) - 3
			for i in range(total_item_in_category):
				product_name = category[str(i)]['product_name']
				product_id = category[str(i)]['product_id']
				price = category[str(i)]['product_subtitle']
				price = price.replace('*', '').replace('+', '').replace('^', '')
				match = re.search(name, product_name, re.I)
				if match:
					# Add item to table
					table_data.append([product_id, product_name, price]);\

		# Create and display table
		table = AsciiTable(table_data)
		print(table.table)

	def get_menu(self):
		return self.menu;

	