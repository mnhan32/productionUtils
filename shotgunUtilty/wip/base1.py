from shotgun_api3 import Shotgun
import time

SERVER_PATH = "https://wefxstudio.shotgunstudio.com"

USER_NAME='mnhan'
USER_KEY='*1a2b3c4d5F'
#USER_NAME='test'
#USER_KEY='e3887765b66883f921c0c4832932c7a023331e65ea4d57d91e54810f91c8ea1e'


def test(sg2):
    print sg2.find('Project',filters=[])
    
if __name__=='__main__':
    sg=Shotgun(SERVER_PATH,login=USER_NAME,password=USER_KEY)
    test(sg)
