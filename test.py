from dominopy import Address
from dominopy import Store
from dominopy import Menu
from dominopy import Order

address = Address("rongpo", "smit")

store = Store(address)

menu = Menu(store)
menu.search("tikka")

order = Order(store)
order.add_item(4056, 'r')
order.add_item(4056, 'r')
order.view_order()