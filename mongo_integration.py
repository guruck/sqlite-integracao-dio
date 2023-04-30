'''Definicoes para integrar o SQLite com Python
Modulo para praticar e realizar a entrega de projeto da DIO
'''
import pprint as pp
import pymongo as pyM

client = pyM.MongoClient('mongodb://localhost:27017/?readPreference=\
                         primary&appname=MongoDB%20Compass&ssl=false')

database = client.central

print(f'client.list_database_names: {client.list_database_names()}\n')
print(f'database.list_collection_names: {database.list_collection_names()}\n')

cliente = {
    'name': 'Jonas',
    'cpf': '11111111111',
    'endereco': 'Rua das Carmelitas, 123',
    'contas': [
        {'agencia': '0001', 'conta': '0001', 'saldo': 0.0},
        {'agencia': '0001', 'conta': '0002', 'saldo': 150.0}
    ]
}

bank = database.bank
cliente_inserido = bank.insert_one(cliente).inserted_id

print(f'client_id: {cliente_inserido}\n')
pp.pprint(bank.find_one())

bulk_cliente = [{
    'name': 'Martha',
    'cpf': '22222222222',
    'endereco': 'Rua das Angelitas, 456',
    'contas': [
        {'agencia': '0001', 'conta': '0003', 'saldo': 1200.0},
        {'agencia': '0002', 'conta': '0001', 'saldo': 50.0}
    ]
    }, {
    'name': 'Pedro',
    'cpf': '333333333333',
    'endereco': 'Rua das Ambrositas, 789',
    'contas': [
        {'agencia': '0002', 'conta': '0002', 'saldo': 80.0},
        {'agencia': '0003', 'conta': '0001', 'saldo': 1250.0}
    ]
}]
resultado = bank.insert_many(bulk_cliente)
print(f'results: {resultado}')
print('\nall_clientes:\n')

for cliente in bank.find():
    pp.pprint(cliente)

print(bank.count_documents({'agencia': '0001'}))
