import requests
import re

class Menu:
	def __init__(self, store):
		# Save menu
		self.menu = store.menu;

	def search(self, name):
		# Search for item in pizza menu
		item_list = self.menu['pizza']
		for category in item_list:
			total_item_in_category = len(category) - 3
			for i in range(total_item_in_category):
				product_name = category[str(i)]['product_name']
				product_id = category[str(i)]['product_id']
				price = category[str(i)]['product_subtitle']
				match = re.search(name, product_name, re.I)
				if match:
					print(product_id, '\t', product_name, '\t\t\t', price)

	def get_menu(self):
		return self.menu;

	