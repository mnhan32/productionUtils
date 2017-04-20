from shotgun_handler import shotgun_handler
import getpass

serverName = raw_input("Server Path : ")
userName = raw_input("User Name : ")
passWd = getpass.getpass()


sg = shotgun_handler.shotgun_handler(serverName,userName,passWd)
print sg.getUser(userName,['projects','name','image'])

sg.close()
