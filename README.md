# Bot de Economia para Discord

Este é um bot de economia para Discord que permite aos usuários gerenciar uma moeda virtual. Os usuários podem verificar seu saldo, transferir para outros usuários e verificar o extrato de transações.

## Funcionalidades

- **Verificar saldo**: Os usuários podem verificar quantas coins possuem.
- **Transferir Coins**: Os usuários podem transferir coins para outros usuários.
- **Extrato**: Os usuários podem ver as últimas transações realizadas.

## Requisitos

- Python 3.10.x
- MongoDB para armazenar os dados
- BOT Discord

## Como usar
/saldo: Verifique seu saldo de Coins.
/pix @usuário valor: Transfira Coins para outro usuário.
/extrato: Veja as últimas transações.

## Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/RashParasita/BOT_BANCO_DISCORD.git
   cd BOT_BANCO_DISCORD

2. Instale requirements.txt
   ```bash
    pip install -r requirements.txt

3. Execute
   ```bash
   python src/main.py
