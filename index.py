#!/usr/bin/python

# Autor original: goldlufebr

# Biblioteca
import discord
from discord.ext import commands

# Intents para recebimento
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True

bot = discord.Client(intents=intents)

# Variáveis
CHANNEL = ["avisos", "anúncios"]
EMOJI = ["🤮", "❌"]
VERIFIED = 1296242808163799122
ACCEPTED = 1296242911628759061

# Evento que impede as reações feias
@bot.event
async def on_raw_reaction_add(reaction):
    # Verificação de canal
    channel = bot.get_channel(reaction.channel_id) # Busca o canal
    if channel.name in CHANNEL:
        
        # Verificação de emoji
        if str(reaction.emoji) in EMOJI:
            try:
                # Remoção da reação
                message = await channel.fetch_message(reaction.message_id) # Busca a mensagem
                user = bot.get_user(reaction.user_id) # Busca o usuário
                await message.remove_reaction(reaction.emoji, user)
                
            except discord.Forbidden:
                    print("O bot não possui as permissões necessárias.")

# Evento que remove o cargo "aceitou regras" de quem tem "verificado"
@bot.event
async def on_member_update(before, after):
    verificado = after.guild.get_role(VERIFIED)
    aceitou_regras = after.guild.get_role(ACCEPTED)
    # Verifica se o usuário possui o cargo "verificado"
    if verificado in after.roles:
        # Se o membro também tiver o cargo "aceitou regras", remova-o
        if aceitou_regras in after.roles:
            try:
                await after.remove_roles(aceitou_regras)
                print(f'Removido o cargo "aceitou regras" de {after.name}')
            except discord.Forbidden:
                print(f"Permissão insuficiente para remover o cargo de {after.name}.")
            except Exception as e:
                print(f"Erro ao remover o cargo de {after.name}: {e}")

# Token
bot.run(process.env.TOKEN)