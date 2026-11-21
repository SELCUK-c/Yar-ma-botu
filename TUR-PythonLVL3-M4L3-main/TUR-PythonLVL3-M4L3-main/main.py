from discord.ext import commands
import discord
from config import TOKEN
from game_models import Game
from ui_join_team import JoinTeamView

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
game = Game()


@bot.event
async def on_ready():
    print(f"{bot.user.name} botu başarıyla başlatıldı! Sınavı başlatmak için !quiz yazın")


@bot.command()
async def quiz(ctx: commands.Context, number_of_teams: str = '2'):
    if not ctx.guild or ctx.author != ctx.guild.owner:
        return

    if number_of_teams not in list("123456789"):
        await ctx.send("Yanlış takım sayısı girildi (1 ile 9 arasında olmalıdır). Örneğin: !quiz 3", delete_after=10)
    else:
        game.number_of_teams = int(number_of_teams)
        game.teams.clear()
        for _ in range(game.number_of_teams):
            game.teams.append({})
            
        game.info_message = await ctx.send(
            content="Takımınızı seçin:",
            view=JoinTeamView(game),
            delete_after=600
        )

    try:
        await ctx.message.delete()
    except discord.Forbidden:
        pass

bot.run(TOKEN)