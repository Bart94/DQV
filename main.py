import pickle
import random
import string
from datetime import date, timedelta

from data_lab import DataLab
from laboratorio import Laboratorio
from user import User

while True:
    i = int(input('Scegli bene: '))

    if i == 1:  # Caso 1
        print('Caso 1')
        tampone = False
        test = None
        time = date.today()
        positivo = False
        monitoraggio = True

    elif i == 2:  # Caso 2.A.1
        print('Caso 2.A.1')
        tampone = True
        test = 'postest'
        time = date.today() - timedelta(days=5)
        positivo = True
        monitoraggio = False


    elif i == 3:  # Caso 2.A.2
        print('Caso 2.A.2')
        tampone = True
        test = 'postest'
        time = date.today() - timedelta(days=5)
        positivo = True
        monitoraggio = True



    elif i == 4:  # Caso 2.B
        print('Caso 2.B')
        tampone = True
        test = 'negtest'
        time = date.today() + timedelta(days=1)
        positivo = False
        monitoraggio = True

    else:
        input('Ma sei scemo o sei buono? -> Rispondi ...')
        break

    user = User()
    city = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    address = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    user.hash_generator(tampone, city, address)

    lab = Laboratorio()

    with open('user', 'rb') as f:
        h, t = pickle.load(f)

    index = lab.add_user(h, t)

    ac = DataLab(lab.act_tuple_generator(index, test, time))
    lab.send_act_tuple(ac)

    data = user.sign_in_procedure(tampone, positivo, monitoraggio)
    user.send_user_info(data)
