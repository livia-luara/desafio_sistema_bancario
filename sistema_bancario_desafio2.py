from datetime import timedelta, datetime
import pytz

data_atual = datetime.now(pytz.timezone("America/Sao_Paulo"))
mascara_ptbr = "%d/%m/%y %H:%M"


menu = """

=============
[1] Depositar
[2] Sacar
[3] Extrato
[4] Nova Conta
[5] Novo Usuário
[6] Listar Contas
[7] Sair
=============

=> """

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n" 
        print("Depósito realizado com sucesso!")

    else:
        print("Operação falhou! O valor informado é inválido.") 

    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    valor_invalido = valor <= 0

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo o suficiente.")

    elif excedeu_limite:
        print ("Operação falhou! O valor do saque excede o seu limite disponível.")

    elif excedeu_saques >= limite_saques:
        print ("Operação falhou! Número de saques diários excedidos. Por favor, tente novamente mais tarde.")
    
    elif valor_invalido:
        print("Operação falhou! O valor informado é inválido.")
    
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1  # Atualizar número de saques apenas se a transação for bem-sucedida
        print ("Saque realizado com sucesso!")

    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /, *, extrato):
    print("\n========== EXTRATO BANCÁRIO ==========\n")
    print(data_atual.strftime(mascara_ptbr))
    print("Não foram realizadas movimentações." if not extrato else extrato)

    print(f"\n=== Saldo: R$ {saldo:.2f} ===\n")
    print("========================================")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf ]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_usuario(usuarios):
    cpf = input("Informe o número de seu CPF: ")
    cpf = ''.join(filter(str.isdigit, cpf)) # apenas números são armazenados
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Esse CPF já está cadastrado.")
        return 
    
    nome_completo = input("Informe o seu nome completo: ")
    data_nascimento = input("Informe a data de seu nascimento no formato dia-mês-ano: ")
    endereco = input("Informe o seu endereço, contendo o logradouro, número - bairro - cidade / sigla do estado: ")

    usuarios.append({"nome_completo": nome_completo, "cpf": cpf, "data_nascimento": data_nascimento, "endereco": endereco})
    print("Usuário cadastrado com sucesso!")



def conta_corrente(agencia, numero_conta, usuarios):
    cpf = input("Informe o número de seu CPF: ")
    cpf = ''.join(filter(str.isdigit, cpf)) # apenas números são armazenados
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    else:
        print ("Usuário não encontrado em nosso banco de dados.")

def listar_contas(contas):
    if not contas: 
        print("Não há contas cadastradas no sistema.")
        return
    
    print("\n============ LISTA DE CONTAS CADASTRADAS ===============")
    for conta in contas: 
        linha = f"""\   
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome_completo']}
                CPF:\t\t\t{conta['usuario']['cpf']}
            """
        print(linha)
        print("=" * 50)  # Linha apenas para separação
    print("==========================================================")


def main():
    agencia = "0001"

    usuarios = []
    contas = []

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    numero_depositos = 0

    limite_transacoes = 10
    limite_saques = 3

    while True:

        opcao = input(menu)

        if opcao == "1":
            valor = float(input("Informe a seguir o valor desejado do depósito:  "))

            excede_transacoes = numero_saques + numero_depositos >= limite_transacoes

            if excede_transacoes:
                print("Operação falhou! Número máximo de transações diárias excedido. Tente novamente mais tarde.")
         
            else:
                saldo, extrato = depositar(saldo, valor, extrato)
                numero_depositos += 1  # Atualizar número de depósitos apenas se a transação for bem-sucedida


        elif opcao == "2":
            valor = float(input("Informe o valor desejado do saque:  "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo, 
                valor=valor, 
                extrato=extrato, 
                limite=limite, 
                numero_saques=numero_saques, 
                limite_saques=limite_saques)
         

        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = conta_corrente(agencia, numero_conta, usuarios)

            if conta: 
                contas.append(conta)
        
        elif opcao == "5":
            criar_usuario(usuarios)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            print("Agradecemos a preferência. Tenha um bom dia!")

            break

        else:
            print("A operação é inválida! Por favor, verifique e selecione a movimentação desejada. Em caso de dúvidas, contate o seu gerente.")


main()