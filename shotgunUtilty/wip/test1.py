from shotgun_api3 import Shotgun
import time, pprint

SERVER_PATH = "https://wefxstudio.shotgunstudio.com"

USER_NAME='mnhan'
USER_KEY='*1a2b3c4d5F'

def test(sg):
    print sg.find('Project',filters=[])

if __name__=='__main__':
    sg = Shotgun(SERVER_PATH, login=USER_NAME,password=USER_KEY)
    #k=sg.find('HumanUser',filters=[['name','is','MengHan Ho']],fields=sg.schema_field_read('HumanUser'))
    k=sg.find('HumanUser',filters=[['name','is','MengHan Ho']],fields=['projects','filmstrip_image','image','entity'])
    #k=sg.find('Project',filters=[['name','is','TTD']],fields=sg.schema_field_read('Project'))
    #k=sg.find('Project',filters=[['name','is','TTD']],fields=[])
    pprint.pprint(k)
    #print sg.find('Project',filters=[])


