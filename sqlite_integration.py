'''Definicoes para integrar o SQLite com Python
Modulo para praticar e realizar a entrega de projeto da DIO
'''
from typing import List
from sqlalchemy import (
    Column,
    create_engine,
    inspect,
    select,
    func,
    Integer,
    String,
    Float,
    ForeignKey
)
from sqlalchemy.orm import (
    declarative_base,
    Session,
    relationship,
    Mapped
)

Base = declarative_base()


class Cliente(Base):
    '''Modelo de usuario'''
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)
    contas: Mapped[List["Conta"]] = relationship(
        'Conta', back_populates='conta_cliente',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        u_str = f'User(id={self.id}, name={self.name}, cpf={self.cpf})'
        return u_str

    def teste(self):
        '''funcao para teste'''

    def default(self):
        '''funcao padrao'''


class Conta(Base):
    '''Modelo de usuario'''
    __tablename__ = 'contas'
    id = Column(Integer, primary_key=True)
    agencia = Column(String(4), nullable=False)
    conta = Column(String(4), nullable=False)
    saldo = Column(Float, default=0.0)
    cliente_id = Column(Integer, ForeignKey('cliente.id'),
                        nullable=False)
    conta_cliente = relationship('Cliente', back_populates='contas')

    def __repr__(self):
        return f'Conta(id={self.id}, ag={self.agencia}, cc={self.conta})'

    def teste(self):
        '''funcao para teste'''

    def default(self):
        '''funcao padrao'''


print(Cliente.__tablename__, Conta.__tablename__)
engine = create_engine('sqlite:///bank.db')

Base.metadata.create_all(engine)

inspector_engine = inspect(engine)
print(inspector_engine.has_table('cliente'))
print(inspector_engine.get_table_names())
print(inspector_engine.get_schema_names())

with Session(engine) as session:
    tiago = Cliente(
        name='tiago',
        cpf='11111111111',
        contas=[Conta(agencia='0001', conta='0001', saldo=100.0),
                Conta(agencia='0001', conta='0002', saldo=150.0)]
    )
    jordino = Cliente(
        name='jordino',
        cpf='22222222222',
        contas=[Conta(agencia='0001', conta='0003'),
                Conta(agencia='0002', conta='0001')]
    )
    maria = Cliente(
        name='maria',
        cpf='33333333333',
        contas=[Conta(agencia='0002', conta='0002', saldo=150.0),
                Conta(agencia='0003', conta='0001', saldo=10.0)]
    )

    # session.add_all([tiago, jordino, maria])
    # session.commit()

stmt = select(Cliente).where(Cliente.name.in_(
    ['tiago', 'jordino', 'maria'])).order_by(Cliente.name.desc())
for cliente in session.scalars(stmt):
    print(cliente)

stmt_contas = select(Conta).where(Conta.cliente_id.in_([1]))
for contas in session.scalars(stmt_contas):
    print(contas)

stmt_order = select(Cliente).order_by(Cliente.cpf.desc())
print('\nRecuperando dados de Cliente de forma ordenada')
for result in session.scalars(stmt_order):
    print(result)

stmt_join = select(Cliente.name, Conta.agencia, Conta.conta,
                   Conta.saldo).join_from(Cliente, Conta)
print(stmt_join)
results = engine.connect().execute(stmt_join).fetchall()
for result in results:  # session.scalars(stmt_join):
    print(result)

stmt_count = select(func.count('*')).select_from(Cliente)
for result in session.scalars(stmt_count):
    print(result)

session.close()
