from discord.ext.commands import Cog
from discord.app_commands import command as app_command
from discord import Member, PermissionOverwrite, Embed, Interaction
from bot import Livefreeandlove
from settings import VERIFCATION_CAT, ENTRANCE_CHANNEL, QUEUE_CHANNEL, pending_role_id, active_role_id, inactive_role_id, in_queue_id
from pymongo import ASCENDING
from database import queue, add_to_queue, activate_user

role_ids = {
    "male": 1436744256197890048,
    "female": 1436744275227316365,
    "straight": 1436744303425884292
}

async def update_queue_embed(member:Member):
    guild = member.guild
    males = queue.count_documents({'gender': 'male', 'status': 'in_queue'})
    females = queue.count_documents({'gender': 'female', 'status': 'in_queue'})
    queue_embed = Embed(title="Queue", description=f"Males: `{males}`\nFemales: `{females}`")
    channel = guild.get_channel(QUEUE_CHANNEL)
    await channel.purge()
    await channel.send(embed=queue_embed)


async def send_entry(member:Member):
    entry_embed = Embed(title="Welcome!", description=f"Welcome {member.mention} to the server!\n\nIdk what else to put here rn", color=0xffa1dc)
    entry_embed.set_thumbnail(url=member.avatar.url)
    guild = member.guild
    channel = guild.get_channel(ENTRANCE_CHANNEL)
    await channel.send(embed=entry_embed)


async def activate(member:Member):
    activate_user(member)
    guild = member.guild
    active_role = guild.get_role(active_role_id)
    inactive_role = guild.get_role(inactive_role_id)
    in_queue = guild.get_role(in_queue_id)
    await member.remove_roles(inactive_role, in_queue)
    await member.add_roles(active_role)
    await update_queue_embed(member)
    await send_entry(member)

async def push_queue(member:Member, gender):
    await put_in_queue(member, gender)
    guild = member.guild
    male = queue.find_one({"gender": "male", "status": "in_queue"}, sort=[("queued_at", ASCENDING)])
    female = queue.find_one({"gender": "female", "status": "in_queue"}, sort=[("queued_at", ASCENDING)])
    if not male or not female:
        return
    male_user = guild.get_member(male['user_id'])
    female_user = guild.get_member(female['user_id'])
    await activate(male_user)
    await activate(female_user)


async def put_in_queue(member:Member, gender:str):
    add_to_queue(member, gender)
    guild = member.guild
    in_queue = guild.get_role(in_queue_id)
    inactive = guild.get_role(inactive_role_id)

    await member.add_roles(in_queue)
    await member.remove_roles(inactive)
    await update_queue_embed(member)



class Verifcation(Cog):

    @Cog.listener('on_member_join')
    async def member_joined(self, member:Member):
        # disable access to all other channels
        guild = member.guild
        pending_verifcation = guild.get_role(pending_role_id)
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



    @app_command()
    async def verify(self, interaction:Interaction, member:Member):
        await interaction.response.defer()
        # remove their verifcation
        guild = member.guild
        pending_verifcation = guild.get_role(pending_role_id)
        await member.remove_roles(pending_verifcation)
        # add them to the queue / whatever
        user_roles = [role.id for role in member.roles]

        if not role_ids["straight"] in user_roles:
            await activate(member)
            await interaction.followup.send("User bypassed queue due to not being straight lol")
            return

        males = queue.count_documents({'gender': 'male', 'status': 'active'})
        females = queue.count_documents({'gender': 'female', 'status': 'active'})

        if role_ids['male'] in user_roles:
            
            if females >= males:
                await push_queue(member, 'male')
            else:
                await put_in_queue(member, 'male')
        if role_ids['female'] in user_roles:
            if males >= females:
                await push_queue(member, 'female')
            else:
                await put_in_queue(member, 'female')
        
        await interaction.followup.send("Done?")
            
        




async def setup(bot:Livefreeandlove):
    await bot.add_cog(Verifcation())
