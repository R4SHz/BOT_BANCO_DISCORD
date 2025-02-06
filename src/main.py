import discord
from dotenv import load_dotenv
from discord import app_commands
import os

from database import checar_saldo, alterar_saldo, registrar_transferencia, ultimas_transacoes

load_dotenv()

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"Bot online como {self.user}")

client = Client()
tree = app_commands.CommandTree(client)

@tree.command(name='saldo', description='Verifique seu saldo de Zcoins')
async def saldo(interaction: discord.Interaction):
    moedas = await checar_saldo(interaction.user)
    moedas_formatadas = f"{moedas:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    mensagem = f"Você tem Ƶ **{moedas_formatadas}** Zcoins."

    try:
        await interaction.user.send(mensagem)
        await interaction.response.send_message(f"{interaction.user.mention}, seu saldo foi enviado por DM!")
    except discord.errors.Forbidden:
        await interaction.response.send_message("Não consegui enviar sua DM. Verifique suas configurações de privacidade.")

import logging

# Configuração básica de logging
logging.basicConfig(level=logging.ERROR)

@tree.command(name='pix', description='Transfira Zcoins para outro jogador')
async def pix(interaction: discord.Interaction, usuario: discord.User, valor: int):
    try:
        remetente = interaction.user

        if valor <= 0:
            await interaction.response.send_message(":x: Valor inválido. Insira um valor positivo.")
            return

        if remetente.id == usuario.id:
            await interaction.response.send_message(":x: Você não pode transferir para si mesmo.")
            return

        saldo_remetente = await checar_saldo(remetente)
        if saldo_remetente < valor:
            await interaction.response.send_message(":x: Saldo insuficiente.")
            return

        sucesso_remetente = await alterar_saldo(remetente, -valor)
        sucesso_destinatario = await alterar_saldo(usuario, valor)

        if sucesso_remetente and sucesso_destinatario:
            await registrar_transferencia(remetente, usuario, valor)
            mensagem_remetente = f" :outbox_tray: Você enviou Ƶ **{valor:,.2f}** Zcoins para **{usuario.name}**."
            mensagem_destinatario = f" :moneybag: Você recebeu Ƶ **{valor:,.2f}** Zcoins de **{remetente.name}**."

            await interaction.response.send_message(mensagem_remetente)
            try:
                await usuario.send(mensagem_destinatario)
            except discord.errors.Forbidden:
                await interaction.followup.send(f"Não consegui notificar **{usuario.name}** por DM.")
        else:
            await interaction.response.send_message(":x: Erro na transferência. Tente novamente.")

    except Exception as e:
        logging.error(f"Erro no comando /pix: {e}")
        await interaction.response.send_message(":x: Ocorreu um erro inesperado. Tente novamente mais tarde.")

@tree.command(name='extrato', description='Confira seu extrato de transações')
async def extrato(interaction: discord.Interaction):
    mensagem = await ultimas_transacoes(interaction.user)

    try:
        await interaction.user.send(mensagem)
        await interaction.response.send_message(f"{interaction.user.mention}, seu extrato foi enviado por DM.")
    except discord.errors.Forbidden:
        await interaction.response.send_message("Não consegui enviar seu extrato por DM. Verifique suas configurações de privacidade.")

client.run(os.getenv("TOKEN_BOT"))
