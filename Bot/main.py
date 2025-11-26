import time
from dotenv import load_dotenv
import os
start_time = time.time()
import discord
from discord.ext import commands, tasks 


intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)  


# Carregar cogs automaticamente
@bot.event
async def setup_hook():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")
            print(f"Carregado: {file}")



@bot.event
async def on_ready():
    print("Meow, meow! Overhand is online.")
    lembrar_agua.start()  # inicia o lembrete automático

# -------- Comandos -------- #

@bot.command()
async def ping(ctx):
    inicio = time.time()
    msg = await ctx.send("> Pong!🏓")
    usuario = ctx.author.display_name
    fim = time.time()

    ms = (fim - inicio) * 1000
    await msg.edit(content=f"> Pong!🏓 - Demorei {ms:.2f}ms pra responder!")
    print(f"{usuario} usou .ping")

@bot.command()
async def uptime(ctx):
    agora = time.time()
    tempo = int(agora - start_time)

    horas = tempo // 3600
    minutos = (tempo % 3600) // 60
    segundos = tempo % 60

    await ctx.send(f"Meow! Tô aqui miando há {horas}h {minutos}m e {segundos}s. 🐾⏰")
    usuario = ctx.author.display_name
    print(f"{usuario} usou .uptime")

@bot.command()
async def joao(ctx):
    await ctx.reply("É viado kkkkkk")
    usuario = ctx.author.display_name
    print(f"{usuario} utilizou .joao")

@bot.command()
async def gato(ctx):
    await ctx.reply("Meow!")
    usuario = ctx.author.display_name
    print(f"{usuario} utilizou .gato")

@bot.command()
async def gata(ctx):
    await ctx.reply("Meow!")
    usuario = ctx.author.display_name
    print(f"{usuario} utilizou .gata")

@bot.command()
async def cat(ctx):
    await ctx.reply("Meow!")
    usuario = ctx.author.display_name
    print(f"{usuario} utilizou .cat")

@bot.command()
async def dono(ctx):
    dono_id = 829402485419409408
    await ctx.reply(f"Meu dono é o <@{dono_id}>!\nGitHub: https://github.com/VictorVzx")
    usuario = ctx.author.display_name
    print(f"{usuario} usou .dono")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, membro: discord.Member, *, motivo="Nenhum motivo informado"):
    if membro == ctx.author:
        usuario = ctx.author.display_name
        print(f"{usuario} tentou se banir")
        return await ctx.send("Meow! Você não pode se banir, doido kkkkk")
        
    
    if membro == ctx.guild.me:
        return await ctx.send("Meow! Tá tentando fazer eu me banir, é?")
    
    try:
        await membro.ban(reason=motivo)
        await ctx.send(f"> {membro.mention} foi banido! 🚫 Motivo: {motivo}")
        print(f"{membro} foi banido")
    except discord.Forbidden:
        await ctx.send("> Não tenho permissão para banir essa pessoa.")
    except Exception as e:
        await ctx.send(f"> Erro ao tentar banir: {e}")
    
    usuario = ctx.author.display_name
    print(f"{usuario} usou .ban")

@bot.event
async def on_member_join(member):
    cargo = discord.utils.get(member.guild.roles, name="Membro")

    if cargo is None:
        print("Cargo 'Membro' não encontrado")
        return
    
    try:
        await member.add_roles(cargo)
        print(f"Cargo 'Membro' adicionado para {member}")
    except:
        print(f"Erro ao adicionar cargo: {e}") # type: ignore
    
    canal = member.guild.system_channel

    if canal and canal.permissions_for(member.guild.me).send_messages:
        await canal.send(f"🐾 Bem-vindo(a) ao servidor, {member.mention}!")
        print(f"{member} se juntou ao servidor!")
    else:
        for ch in member.guild.text_channels:
            if ch.permissions_for(member.guild.me).send_messages:
                await ch.send(f"🐾 Bem-vindo(a) {member.mention}!")
                print(f"{member} se juntou ao servidor!")
                break

@bot.command()
@commands.has_permissions(manage_roles=True)

async def role(ctx, membro: discord.Member, *, cargo_nome):
    cargo = discord.utils.get(ctx.guild.roles, name=cargo_nome)

    if cargo is None:
        return await ctx.send(f"Erro! '{cargo_nome}' não existe no servidor.")
    
    try: 
        await membro.add_roles(cargo)
        await ctx.send(f"✅{membro.mention} recebeu o cargo **{cargo_nome}**.")
        print(f"{membro} recebeu o cargo {cargo_nome}")
    except discord.Forbidden:
        await ctx.send("Não possuo permissão ou estou num cargo abaixo do permitido para dar este cargo.")
    except Exception as e:
        await ctx.send(f"Erro ao adicionar o cargo: `{e}`")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unrole(ctx, membro: discord.Member, *, cargo_nome):
    # procura o cargo pelo nome
    cargo = discord.utils.get(ctx.guild.roles, name=cargo_nome)

    if cargo is None:
        return await ctx.send(f"❌ Cargo '{cargo_nome}' não existe no servidor.")

    # tenta remover o cargo
    try:
        await membro.remove_roles(cargo)
        await ctx.send(f"🗑️ {membro.mention} teve o cargo **{cargo_nome}** removido.")
        print(f"{membro} perdeu o cargo {cargo_nome}.")
    except discord.Forbidden:
        await ctx.send("❌ Eu não tenho permissão ou meu cargo está abaixo desse cargo.")
    except Exception as e:
        await ctx.send(f"❌ Erro ao remover o cargo: `{e}`")


@bot.command()
async def menu(ctx):
    await ctx.reply(
        "# 🐾 Menu 🐾\n"
        "## **Comandos:**\n"
        " .menu --> Ver o menu de comandos do bot.\n"
        " .ping --> Testar a velocidade de resposta do bot.\n"
        " .uptime --> Ver há quanto tempo o bot está funcionando\n"
        " .dono --> Informações sobre o dono do bot.\n"
        " .gato/gata --> Miaaaaau.\n"
        "## Comandos admin:\n"
        " .clear *numero de mensagens --> Limpa as mensagens do chat.\n"
        " .todos --> Marca todos do servidor.\n"
        " .atividade jogando/ouvindo/assistindo + conteúdo --> Muda a atividade do bot.\n"
        " .ban + motivo --> Banir membros do servidor\n"
        " .role + @usuario + Cargo--> Dar um cargo ao membro mencionado.\n"
        " .unrole + @usuario + Cargo --> Remover um cargo do membro mencionado\n"
    )
    usuario = ctx.author.display_name
    print(f"{usuario} utilizou .menu")

@bot.command()
async def todos(ctx):
    await ctx.send("@everyone")
    usuario = ctx.author.display_name
    print(f"{usuario} marcou geral.")

# -------- Lembrete de água -------- #

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, quantidade: int):
    await ctx.channel.purge(limit=quantidade + 1)
    await ctx.send(f"🧹{quantidade} mensagens meowpagadas", delete_after=3)
    usuario = ctx.author.display_name
    print(f"{usuario} apagou {quantidade} mensagens")

@tasks.loop(hours=1)
async def lembrar_agua():
    channel = bot.get_channel(1440685459645661195)
    await channel.send("Meow meow, use .menu para ver meus comandos e lembrem-se de beberem água! 💧🐾")
    print("Lembrete enviado.")

    channel = bot.get_channel(1440685459645661195)
    await channel.send(f"Siga VictorVzx no GitHub e veja mais projetos!\nhttps://github.com/VictorVzx")
    print("Anúncio enviado")

@bot.command()
async def protetorSolar(ctx):
    await ctx.reply("Protetor solar colocado! 😎")
    usuario = ctx.author.display_name
    print(f"{usuario} colocou protetores solares no bot.")

@bot.command()
@commands.has_permissions(administrator=True)
async def atividade(ctx, tipo, *, texto):
    usuario = ctx.author.display_name
    tipo = tipo.lower()

    if tipo == "jogando":
        activity = discord.Game(name=texto)

    elif tipo == "ouvindo":
        activity = discord.Activity(
            type=discord.ActivityType.listening,
            name=texto
        )

    elif tipo == "assistindo":
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=texto
        )

    else:
        await ctx.send("Tipo inválido! Use: jogando / ouvindo / assistindo")
        return
    await bot.change_presence(activity=activity)
    await ctx.send(f"Atividade mudada para: **{tipo} {texto}**")
    print(f"{usuario} mudou a atividade do bot.")

@atividade.error
async def atividade_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Você precisa ser **Administrador** para usar este comando.")
        usuario = ctx.author.display_name
        print(f"{usuario} usou um comando acima do seu cargo")


# -------- Rodar o bot -------- #
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)



