'''testando import'''
try:
    from sys import path
    PATH = 'D:\\guruck\\Documents\\Cursos\\DIO\\bootcamp_Python\\projeto01'
    PATH_SQL = PATH + '\\SqliteIntegracaoDio'
    PATH_TESTE = PATH_SQL + '\\Teste'
    path.append(PATH_SQL)
    path.append(PATH_TESTE)
except ModuleNotFoundError as e:
    print(f'Error: {e}')
    raise e
from cryptography.fernet import Fernet
from Teste import DatabaseManager


print(*path, sep='\n')


def testea():
    '''testando modularizacao'''
    database2 = DatabaseManager('..\\files\\sqlteste.db')
    print(database2.get_all_table_names())
    key = Fernet.generate_key()
    print(key)


testea()
