from abc import ABC, abstractmethod
from datetime import datetime
import pytz

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(nome, cpf, data_nascimento, endereco)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._agencia = '0001'
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, value):
        self._saldo = value

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Depósito realizado com sucesso!')
            return True
        else:
            print('Operação falhou! O valor informado é inválido.')
            return False


    def sacar(self, valor):
        if valor > self._saldo:
            print('Operação falhou! Saldo insuficiente.')
            return False

        elif valor <= 0:
            print('Operação falhou! Valor não pode ser negativo ou nulo.')
            return False

        else:
            self._saldo -= valor
            print('Saque realizado com sucesso!')
            return True

    def exibir_extrato(self):
        print('=====EXTRATO=====')
        for transacao in self.historico.transacoes:
            print(transacao)
        print(f'Saldo atual: R${self._saldo:.2f}')
        print('=====EXTRATO=====')

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if isinstance(transacao, Saque)]
        )

        if valor > self.limite:
            print('Operação falhou! O valor do saque excede seu limite.')
            return False

        if numero_saques >= self.limite_saques:
            print('Operação falhou! Número máximo de saques excedido.')
            return False

        return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência: {self.agencia} \n            Conta Corrente: {self.numero}\n            Titular: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def __str__(self):
        if not self.transacoes:
            return 'Não há histórico de transações.'
        return "\n".join(str(transacao) for transacao in self.transacoes)

class Transacao(ABC):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now(pytz.timezone('America/Sao_Paulo'))

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"SAQUE: Valor - R$ {self.valor:.2f}, Data: {self.data.strftime('%d/%m/%Y %H:%M')}"

class Deposito(Transacao):
    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"DEPÓSITO: Valor: R$ {self.valor:.2f}, Data: {self.data.strftime('%d/%m/%Y %H:%M')}"

def menu():
    return """
    ============= MENU =============
    [1] Depositar
    [2] Sacar
    [3] Extrato
    [4] Nova Conta
    [5] Novo Usuário
    [6] Listar Contas
    [7] Sair
    ================================
    => """

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print('Cliente não possui conta!')
        return None
    return cliente.contas[0]

def depositar(clientes):
    cpf = input('Informe o CPF do usuário: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return

    valor = float(input('Informe o valor do depósito: '))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Deposito(valor))

def sacar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return

    valor = float(input('Informe o valor do saque: '))
    conta = recuperar_conta_cliente(cliente)
    if conta:
        cliente.realizar_transacao(conta, Saque(valor))

def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return

    conta = recuperar_conta_cliente(cliente)
    if conta:
        conta.exibir_extrato()

def criar_cliente(clientes):
    cpf = input("Informe o número de seu CPF: ")
    cpf = ''.join(filter(str.isdigit, cpf))
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("Esse CPF já está cadastrado.")
        return

    nome = input("Informe o seu nome completo: ")
    data_nascimento = input("Informe a data de seu nascimento (dia/mês/ano): ")
    endereco = input("Informe o seu endereço: ")

    cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
    clientes.append(cliente)
    print("Usuário cadastrado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado!')
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print('Conta criada com sucesso!')

def listar_contas(contas):
    for conta in contas:
        print('=' * 30)
        print(conta)


def main():
    clientes = []
    contas = []
    numero_conta = 1

    while True:
        opcao = input(menu())

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_conta(numero_conta, clientes, contas)
            numero_conta += 1

        elif opcao == "5":
            criar_cliente(clientes)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            print("Agradecemos a preferência. Tenha um bom dia!")
            break
        
        else:
            print("A operação é \033[31minválida!\033[m Por favor, verifique e selecione a movimentação desejada. Em caso de dúvidas, contate o seu gerente.")

main()
