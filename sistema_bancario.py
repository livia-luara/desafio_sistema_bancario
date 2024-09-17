menu = """

=============
[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair
=============

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
limite_saques = 3

while True:

    opcao = input(menu)

    if opcao == "1":
        valor = float(input("Informe a seguir o valor desejado do depósito:  "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"

        else:
            print("Operação falhou! O valor informado é inválido. Repita.")

    elif opcao == "2":
        valor = float(input("Informe o valor desejado do saque:  "))

        excede_saldo = valor > saldo

        excede_limite = valor > limite

        excede_saques = numero_saques >= limite_saques

        if excede_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excede_limite:
            print("Operação falhou! O valor do saque excede o seu limite.")

        elif excede_saques:
            print("Operação falhou! Número máximo de saques diários excedido. Tente novamente mais tarde.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "3":
        print("\n================ EXTRATO BANCÁRIO ================")
        print("Não houve transações bancárias." if not extrato else extrato)

        print(f"\nSaldo: R$ {saldo:.2f}")
        print("====================================================")

    elif opcao == "4":
        print("Agradecemos a preferência. Tenha um bom dia!")

        break

    else:
        print("A operação é inválida! Por favor, verifique e selecione a movimentação desejada. Em caso de dúvidas, contate o seu gerente.")