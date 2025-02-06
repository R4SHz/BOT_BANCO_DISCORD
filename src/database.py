import motor.motor_asyncio
from dotenv import load_dotenv
import os
from pymongo.errors import PyMongoError

load_dotenv()

# Conexão com o MongoDB usando motor
MONGO_URI = os.getenv("MONGODB")
if not MONGO_URI:
    raise ValueError("Token do MongoDB não encontrado no .env")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["banco"]
usuarios = db["usuarios"]
extrato = db["extrato"]

async def novo_usuario(usuario):
    try:
        filtro = {"discord_id": usuario.id}
        if await usuarios.count_documents(filtro) == 0:
            objeto = {
                "discord_id": usuario.id,
                "nome": usuario.name,
                "moedas": 0
            }
            await usuarios.insert_one(objeto)
            return objeto
        return False
    except PyMongoError as e:
        print(f"Erro ao criar novo usuário: {e}")
        return None

async def checar_saldo(usuario):
    await novo_usuario(usuario)
    try:
        resultado = await usuarios.find_one({"discord_id": usuario.id})
        return resultado.get("moedas", 0) if resultado else 0
    except PyMongoError as e:
        print(f"Erro ao verificar saldo: {e}")
        return 0

async def alterar_saldo(usuario, quantidade):
    if quantidade == 0:
        return
    try:
        saldo_atual = await checar_saldo(usuario)
        novo_saldo = saldo_atual + quantidade
        if novo_saldo < 0:
            return False  # Impede saldo negativo

        await usuarios.update_one(
            {"discord_id": usuario.id},
            {"$set": {"moedas": novo_saldo, "nome": usuario.name}}
        )
        return True
    except PyMongoError as e:
        print(f"Erro ao alterar saldo: {e}")
        return False

async def registrar_transferencia(remetente, destinatario, valor):
    try:
        transacao = {
            "remetente_id": remetente.id,
            "remetente_nome": remetente.name,
            "destinatario_id": destinatario.id,
            "destinatario_nome": destinatario.name,
            "valor": valor
        }
        await extrato.insert_one(transacao)
    except PyMongoError as e:
        print(f"Erro ao registrar transferência: {e}")

async def ultimas_transacoes(usuario):
    try:
        filtro = {"$or": [{"remetente_id": usuario.id}, {"destinatario_id": usuario.id}]}
        transacoes = await extrato.find(filtro).sort("_id", -1).limit(10).to_list(length=10)

        if not transacoes:
            return "Nenhuma transação encontrada."

        mensagem = "\nÚltimas transações:\n"
        for transacao in transacoes:
            if transacao["remetente_id"] == usuario.id:
                mensagem += f" :red_circle: Você enviou Ƶ **{transacao['valor']:.2f}** Zcoins para **{transacao['destinatario_nome']}**\n"
            else:
                mensagem += f" :green_circle: **{transacao['remetente_nome']}** enviou Ƶ **{transacao['valor']:.2f}** Zcoins para você\n"

        return mensagem
    except PyMongoError as e:
        print(f"Erro ao buscar transações: {e}")
        return "Erro ao buscar transações."
