import discord
from discord.ext import commands
import json
import os

DATA_FILE = "levels.json"

LEVELS = {
    1: 1,
    2: 50,
    3: 100,
    4: 200,
    5: 400,
    6: 800
}

ROLE_BY_LEVEL = {
    1: "Level 1 - Novo Aqui",
    2: "Level 2 - Noob",
    3: "Level 3 - Pro",
    4: "Level 4 - Experiente",
    5: "Level 5 - Master",
    6: "Level 6 - Grand Master"
}

class LevelSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                self.users = {}
    
    def save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.users, f, indent=4)

    def calculate_level(self, msg_count):
        lvl = 1
        for level, required in LEVELS.items():
            if msg_count >- required:
                lvl = level
        return lvl
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        uid = str(message.author.id)

        #se o usuari onão existe cria
        if uid not in self.users:
            self.users[uid] = {"messages": 0, "level": 1}

        #adiciona mensagem
        self.users[uid]["messages"] += 1

        old_level = self.users[uid]["level"]
        new_level = self.calculate_level(self.users[uid]["messages"])

        #se subiu de level
        if new_level > old_level:
            self.users[uid]["level"] = new_level
            self.save()

            role_name = ROLE_BY_LEVEL[new_level]
            role = discord.utils.get(message.guild.roles, name=role_name)

            if role:
                await message.author.add_roles(role)

            await message.channel.send(
                f"🥳Meow! {message.author.mention} subiu para o Level {new_level}!"
            )
            usuario =message.author.display_name
            print(f"{usuario} subiu de nivel.")
        self.save()

    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        uid = str(member.id)

        if uid not in self.users:
            return await ctx.send("Esse usuário ainda não possui um level registrado.")
        
        msgs = self.users[uid]["messages"]
        lvl = self.users[uid]["level"]

        await ctx.send(
            f"📊 **{member.display_name}**\n"
            f"Mensagens: **{msgs}**\n"
            f"Level atual: **{lvl}**"
        )

async def setup(bot):
    await bot.add_cog(LevelSystem(bot))