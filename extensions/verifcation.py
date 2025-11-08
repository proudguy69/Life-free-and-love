from discord.ext.commands import Cog
from discord import Member, PermissionOverwrite, Embed
from bot import Livefreeandlove
from settings import PENDING_VERICATION, VERIFCATION_CAT

class Verifcation(Cog):

    @Cog.listener('on_member_join')
    async def member_joined(self, member:Member):
        # disable access to all other channels
        guild = member.guild
        pending_verifcation = guild.get_role(PENDING_VERICATION)
        await member.add_roles(pending_verifcation)
        # create a verifcation ticket
        cat = guild.get_channel(VERIFCATION_CAT)
        chan = await cat.create_text_channel(f"Verifcation-{member.name}")
        overwrite = PermissionOverwrite()
        overwrite.send_messages = True
        overwrite.read_messages = True
        overwrite.read_message_history = True
        overwrite.attach_files = True
        await chan.set_permissions(target=member, overwrite=overwrite)
        # send verifcation message
        verifcation_embed = Embed(title="User Verifcation",
                                  description="To verify, you must send photo of a censored ID, showing your face, and DOB"
                                  "\nYou then must also take a selfie with a piece of paper showing the discord server"
                                  "\nWe can discuss a different way to verify. with the owners approval.",
                                  color=0xca4040
                                  )
        print('sending message')
        await chan.send(content=f"{member.mention} <@&1436753953399247051>", embed=verifcation_embed)




async def setup(bot:Livefreeandlove):
    await bot.add_cog(Verifcation())
