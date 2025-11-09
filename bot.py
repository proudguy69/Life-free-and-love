from discord.ext.commands import Bot
from discord.ext.commands import is_owner
from discord import Intents
from settings import TOKEN

EXTENSIONS = ['verifcation']

class Livefreeandlove(Bot):
    def __init__(self):
        super().__init__(command_prefix='?', intents=Intents.all())

    async def setup_hook(self):
        await self.load_extensions()
    
    async def load_extensions(self):
        for extension in EXTENSIONS:
            await self.load_extension(f'extensions.{extension}')

bot = Livefreeandlove()

@bot.command()
@is_owner()
async def sync(ctx):
    msg = await ctx.send("Syncing!")
    await bot.tree.sync()
    await msg.edit(content="Done!")




def main():
    
    bot.run(TOKEN)


if __name__ == "__main__":
    main()