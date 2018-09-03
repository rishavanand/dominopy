from dominopy import Address
from dominopy import Store
from dominopy import Menu
from dominopy import Order

address = Address("rongpo", "smit")

store = Store(address)

menu = Menu(store)
menu.search("tikka")

order = Order(store)
order.add_item(9, 'r')
order.add_item(4056, 'r')
order.add_item(4056, 'r')

# 0 to get order details as return
# 1 to print order details
order.get_order(1)

# Remove item procedure
cart = order.get_order(0)
basket_id = cart[0][0]
order.remove_item(basket_id)

order.get_order(1)