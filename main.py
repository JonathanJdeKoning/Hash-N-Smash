from menu import Menu
from Smasher import connect
"""
C:/Users/jj720/IOT/firmware
"""
session = connect()
menu = Menu(session)
menu.main_menu()
session.commit()
session.close()
