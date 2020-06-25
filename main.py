import pickle
import random
from datetime import date, timedelta

from data_lab import DataLab
from laboratorio import Laboratorio
from utente import Utente

city = ['Nocera', 'Avellino', 'Pompei', 'Aversa', 'Battipaglia']
address = ['Via Roma 1', 'Via Firenze 4', 'Via Europa 18', 'Corso Sicurezza 30', 'Via Liguria 69']

while True:
    msg = "L'utente ha accettato il monitoraggio."

    print('1 = Cittadino a rischio soggetto a quarantena che richiede monitoraggio\n'
          '2 = Cittadino positivo al tampone che non richiede monitoraggio\n'
          '3 = Cittadino positivo al tampone che richiede monitoraggio\n'
          '4 = Cittadino negativo al tampone che richiede monitoraggio\n'
          '0 = Termina')

    i = int(input('Seleziona: '))
    print()

    if i == 1:  # Caso 1
        tampone = False
        test = None
        time = date.today()
        positivo = False
        monitoraggio = True

    elif i == 2:  # Caso 2.A.1
        tampone = True
        test = 'postest'
        time = date.today() - timedelta(days=5)
        positivo = True
        monitoraggio = False
        msg = "L'utente non ha accettato il monitoraggio."

    elif i == 3:  # Caso 2.A.2
        tampone = True
        test = 'postest'
        time = date.today() - timedelta(days=5)
        positivo = True
        monitoraggio = True

    elif i == 4:  # Caso 2.B
        tampone = True
        test = 'negtest'
        time = date.today() + timedelta(days=1)
        positivo = False
        monitoraggio = True

    elif i == 0:  # Caso 2.B
        break

    else:
        input('Input non valido.')
        continue


    user = Utente()
    user.hash_generator(tampone, city[random.randint(0, len(city) - 1)], address[random.randint(0, len(address) - 1)])

    lab = Laboratorio()

    with open('user', 'rb') as f:
        h, t = pickle.load(f)

    index = lab.add_user(h, t)

    ac = DataLab(lab.act_tuple_generator(index, test, time))
    lab.send_act_tuple(ac)

    print(msg)
    data = user.sign_in_procedure(tampone, positivo, monitoraggio)
    retrieved_data = user.send_user_info(data)
