import discord
import os
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv
import subprocess

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

token_Bot = os.getenv("TOKEN_DISCORD")

intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} Entrou com ferocidade cortando os códigos do seu computador!")

@bot.command(aliases=["olá", "hello"])
async def ola(ctx:commands.Context):
    await ctx.reply("Hehe! Estou a postos.")

@bot.command()
async def atacar(ctx:commands.Context):
    nome = ctx.author.name
    await ctx.send(f"Grrr! Vou te cortar {nome}.  **Sons de Serra**")


@bot.command()
async def atividades(ctx: commands.Context):
    await ctx.send("Certo! irei cortar a página... **Vrrrm-Vrrrm**")
    
    # Executa o arquivo no sistema e captura o que seria printado no terminal
    resultado = subprocess.run(["python", "./chainsawbot/scraper.py"], capture_output=True, text=True)
    
    # Envia o texto que o scraper gerou
    await ctx.reply(f" **Cortei tudinho! **\n```text\n{resultado.stdout}\n```")

    
bot.run(token_Bot)