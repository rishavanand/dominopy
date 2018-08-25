import requests

# Start session
session = requests.Session()

# Fetch /store-locator page for csrf_token and cookies
url = "https://pizzaonline.dominos.co.in/store-locator"
response = session.get(url)

# Extract csrf_token from page
response = response.text.split('\n')
html_line_containing_csrf = ''
for r in response:
	if "csrf_token" in r:
		html_line_containing_csrf = r
		break

sub1 = html_line_containing_csrf.index('value="') + len('value="')
sub2 = html_line_containing_csrf.index('" name=')
csrf_token = html_line_containing_csrf[sub1:sub2]

# Make POST request for initializing order with csrf_token.
# This saves somes data in the cookies on the server side
# that allows us to make further requests like get menu.
url = "https://pizzaonline.dominos.co.in/build/order"
data = {
	'home-or-pickup': 'home-delivery',
	'combobox': 'RONGPO',
	'home_delivery': 'Popular Cities',
	'pick_up': 'Popular Cities',
	'combobox_locality': 'RANGPO^SMIT^#66487',
	'request_page': 'welcome',
	'first_time_customer': 'yes',
	'store_code': '',
	'store_name': '',
	'csrf_token': csrf_token
}
response = session.post(url, data = data)

# Get menu
url = "https://pizzaonline.dominos.co.in/view/product/?isAjaxRequest=json&store_code=66487"
r = session.get(url)
print(r.text)
