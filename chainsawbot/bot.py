import discord
import os
from discord.ext import commands, tasks
from pathlib import Path
from dotenv import load_dotenv
from scraper import execute_scraper
from datetime import time
import asyncio
from database import read
from calendar_gen import set_events, create_ics
from datetime import time
from zoneinfo import ZoneInfo
import asyncio
from scraper import execute_scraper
from calendar_gen import set_events, create_ics

# Caminho para localizar o ficheiro .ics gerado
BASE_DIR = Path(__file__).resolve().parent
ICS_PATH = BASE_DIR / "data/calendar.ics"

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

canal_id = os.getenv("ID_CANAL_DISCORD")

token_Bot = os.getenv("TOKEN_DISCORD")

intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} Entrou com ferocidade cortando os códigos do seu computador!")
    # Inicia o loop de tarefas agendadas quando o bot estiver pronto
    if not enviar_atividades_diarias.is_running():
        enviar_atividades_diarias.start()

@bot.command(aliases=["olá", "hello"])
async def ola(ctx: commands.Context):
    await ctx.reply("Hehe! Estou a postos.")

@bot.command()
async def atacar(ctx: commands.Context):
    nome = ctx.author.name
    await ctx.send(f"Grrr! Vou te cortar {nome}.  **Sons de Serra**")

# Função auxiliar para rodar o ciclo completo do app.py e pegar as atividades formatadas
async def atualizar_e_buscar_atividades():
    # Roda a mesma rotina do app.py
    await execute_scraper()
    create_ics(set_events())
    
    # Lê os dados atualizados do banco de dados para enviar no chat
    dados = read()
    if not dados:
        return "Sniff-Sniff! Não tem nenhuma atividade para eu cortar..."
    
    texto_formatado = ""
    for task in dados:
        texto_formatado += f"• **{task['course_name']}**: {task['activity_name']} (Entrega: {task['date']})\n"
    
    return texto_formatado

@bot.command()
async def atividades(ctx: commands.Context):
    await ctx.send("Certo! Vou correr pelo seu AVA e cortar todas as atividades... **Vrrrm-Vrrrm** !!")
    
    try:
        resultado_texto = await atualizar_e_buscar_atividades()
        
        # Cria o objeto do ficheiro para enviar no Discord
        arquivo_ics = discord.File(ICS_PATH, filename="calendario_atividades.ics")
        
        # Envia a mensagem com o texto e o ficheiro anexo
        await ctx.reply(
            f"**Cortei tudinho! Aqui estão as suas atividades bem cortadinhas e o calendário:**\n\n{resultado_texto}",
            file=arquivo_ics
        )
        
    except Exception as e:
        await ctx.reply(f"Baw! A-a serra quebrou! Eu fiz algo errado? ```text\n{e}\n```")

# Tarefa agendada para rodar todo dia às 23:59
@tasks.loop(time=time(hour=9, minute=26, tzinfo=ZoneInfo("America/Sao_Paulo")))
async def enviar_atividades_diarias():
    try:
        # Usa fetch_channel em vez de get_channel para ir buscar diretamente à API do Discord
        canal = await bot.fetch_channel(canal_id)
    except Exception as e:
        print(f"Baw! Eu estou perdido... Não consegui encontrar o canal: {e}")
        return

    try:
        await canal.send("⏰ **Tic-Tac já é 23h59. Hora de cortar TUDO! A serra vai girar que nem louca... MUAHAHA!!:**")
        resultado_texto = await atualizar_e_buscar_atividades()
        
        # Cria o objeto do ficheiro para a tarefa automática
        arquivo_ics = discord.File(ICS_PATH, filename="calendario_atividades.ics")
        
        await canal.send(resultado_texto, file=arquivo_ics)
    except Exception as e:
        print(f"Baw!! Eu não consegui fazer isso sozinho... Sniff-Sniff: {e}")

bot.run(token_Bot)