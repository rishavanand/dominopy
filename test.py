from dominopy import Address
from dominopy import Store
from dominopy import Menu

address = Address("rongpo", "smit")
store = Store(address)
menu = Menu(store)
menu.search("cheese")