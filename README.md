# Desafio DIO: Sistema Bancário

Nesse desafio, devemos criar um sistema bancário com as operações sacar, depositar e visualizar o extrato bancário, utilizando a línguagem de programação Python. 


## Depósito
O depósito permite apenas valores inteiros e positivos. Em caso de erro, é exibido uma mensagem informando o usuário.                              
O valor é armazenado em uma variável e é exibido na operação de extrato.



## Saque
O saque permite apenas três transações diários, conforme exigido no desafio. O limite de saldo sacado por operação é de 500. Caso o usuário esteja sem saldo, será exibida uma mensagem.     
Assim como o depósito, o valor é armazenado em uma variável e é exibido na operação de extrato.


## Extrato
O extrato lista todos os depósitos e saques realizados na conta, e caso ainda não tenha sido realizada nenhuma transação, uma mensagem será exibida ao usuário. O salto atual também é exibido, na formatação exigida.


## Inválido
Caso o usuário realize uma operação inválida, ele será alertado para que tente novamente


# Desafio DIO: Sistema Bancário - 02

Esse desafio consistia em refatorar o sistema bancário feito previamente, separando as funcionalidades existentes em funções modulares e criando novas funcionalidades. As operações de saque, depósito e extrato deveriam ser implementadas em funções próprias, seguindo padrões específicos para a passagem de argumentos (por posição e por nome). Além disso, foram adicionadas novas funções para cadastrar usuários e contas bancárias, com validação de CPF e vínculo entre usuário e conta e também houve a adição de mensagens de erro e sucesso para melhor interação com o usuário.


## Criação de Funções
Foram criadas as funções depositar, sacar e exibir extrato. 

## Novas Funcionalidades 
* Criar Usuário: Permite o cadastro de usuários com nome, CPF (único), data de nascimento e endereço.
* Criar Conta Corrente: Cria contas vinculadas aos usuários previamente cadastrados, gerando um número sequencial para a conta e validando o CPF.
* Listar Contas: Exibe todas as contas cadastradas, incluindo agência, número da conta e nome do titular.
