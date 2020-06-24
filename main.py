import pickle
from datetime import date, timedelta

from data_lab import DataLab
from laboratorio import Laboratorio
from user import User

guglielmo = User()
guglielmo.hash_generator(True, 'Napoli', 'Via Roma 8')

lab = Laboratorio()

with open('user', 'rb') as f:
    h, t = pickle.load(f)

lab.add_user(h, t)
with open('time', 'rb') as f:
    time = pickle.load(f)
print(time)
ac = DataLab(lab.act_tuple_generator(0, 'postest', time))
lab.send_act_tuple(ac)

data = guglielmo.sign_in_procedure(True)
print(data)
guglielmo.send_user_info(data)
