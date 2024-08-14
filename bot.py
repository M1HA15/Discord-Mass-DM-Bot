import discord
import random
import asyncio
from datetime import datetime
import pytz
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=';', intents=intents)
bot.remove_command('help')

dm_status = {
    'total': 0,
    'sent': 0,
    'failed': 0
}

@bot.event
async def on_ready():
    owner = (await bot.application_info()).owner

    guilds = bot.guilds
    guild_names = '\n'.join([f"🔹 `{guild.name}` | ID: `{guild.id}` | Members: `{len(guild.members)}`" for guild in guilds])
    
    bucharest_tz = pytz.timezone('Europe/Bucharest')
    timestamp = datetime.now(bucharest_tz).strftime('%H:%M')

    latency = round(bot.latency * 1000)

    print(f"Your bot is Ready and Connected to {len(guilds)} Servers!")
    print(f"https://github.com/M1HA15/Discord-Mass-DM-Bot")

    await bot.change_presence(status=discord.Status.online, activity=discord.Game('github.com/M1HA15/Discord-Mass-DM-Bot'))

    if owner:
        await owner.send(
            embed=discord.Embed(
                title="**✅ Bot is Now Running!**",
                description=f"**📶 Ping**: `{latency}ms`\n**⏳ Time**: `{timestamp}`\n**🌐 Connected to `{len(guilds)}` servers**: \n{guild_names}",
                color=discord.Color.green()
            )
        )

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    random_ping_responses = ['🏓 **Poooong!**', '🏓 **Poong!**', '🏓 **Pong!**', '🏓 **Pooong!**']
    chosen_ping = random.choice(random_ping_responses)
    bucharest_tz = pytz.timezone('Europe/Bucharest')
    timestamp = datetime.now(bucharest_tz).strftime('%H:%M')
    
    embed = discord.Embed(
        title=chosen_ping,
        description=f"📶 **Latency**: `{latency}ms`",
        color=discord.Color.blue()
    )
    
    embed.set_footer(text=f"Requested by {ctx.author} at {timestamp}")

    await ctx.send(embed=embed)
    print(f'Latency: {latency}ms at {timestamp} by {ctx.author}')

@bot.command(name="dm_all")
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 300, commands.BucketType.guild)
async def dm_all(ctx, *, args=None):
    if args is not None:
        members = ctx.guild.members
        bucharest_tz = pytz.timezone('Europe/Bucharest')
        member_count = len(members)
        guild_name = ctx.guild.name

        dm_status['total'] = member_count
        dm_status['sent'] = 0
        dm_status['failed'] = 0
        
        start_time = datetime.now(bucharest_tz).strftime('%H:%M')
        await ctx.channel.send(f"🔔 **Starting** to **send DMs** to `{member_count}` members in `{guild_name}` at `{start_time}`")
        print(f"Starting to send DMs to {member_count} members in {guild_name} at {start_time}")
        
        for member in members:
            try:
                await asyncio.sleep(50)
                timestamp = datetime.now(bucharest_tz).strftime('%H:%M')
                await member.send(args)
                dm_status['sent'] += 1
                await asyncio.sleep(15)
                await ctx.channel.send(f"🟢 **DM Sent** to: `{member.name}#{member.discriminator}` | ID: `{member.id}` at `{timestamp}`")
                print(f"DM Sent To: {member.name}#{member.discriminator} (ID: {member.id}) at {timestamp}")
                await asyncio.sleep(25)
            except discord.Forbidden:
                dm_status['failed'] += 1
                await asyncio.sleep(15)
                timestamp = datetime.now(bucharest_tz).strftime('%H:%M')
                await ctx.channel.send(
                    f"🔴 **DM Can't be Sent** to: `{member.name}#{member.discriminator}` | ID: `{member.id}` at `{timestamp}`\n"
                    "*[**Error**]*: `User has closed DMs or has privacy settings that prevent receiving messages`"
                )
                print(f"DM Can't be Sent To: {member.name}#{member.discriminator} (ID: {member.id}) at {timestamp} - Closed DMs")
                await asyncio.sleep(35)
            except discord.HTTPException as e:
                dm_status['failed'] += 1
                await asyncio.sleep(15)
                timestamp = datetime.now(bucharest_tz).strftime('%H:%M')
                await ctx.channel.send(
                    f"🔴 **DM Can't be Sent** to: `{member.name}#{member.discriminator}` | ID: `{member.id}` at `{timestamp}`\n"
                    f"*[**HTTP Error**]*: `{e}`"
                )
                print(f"DM Can't be Sent To: {member.name}#{member.discriminator} (ID: {member.id}) at {timestamp} - HTTP Error: {e}")
                await asyncio.sleep(35)
            except Exception as e:
                dm_status['failed'] += 1
                await asyncio.sleep(15)
                timestamp = datetime.now(bucharest_tz).strftime('%H:%M')
                await ctx.channel.send(
                    f"🔴 **DM Can't be Sent** to: `{member.name}#{member.discriminator}` | ID: `{member.id}` at `{timestamp}`\n"
                    f"*[**Unexpected Error**]*: `{e}`"
                )
                print(f"Unexpected Error for {member.name}#{member.discriminator} (ID: {member.id}) at {timestamp}: {e}")
                await asyncio.sleep(35)
        
        await ctx.channel.send(f"✅ **Done**! I sent the message to `{member_count}` members!")
        await ctx.author.send(f"✅ **All DMs sent** to `{member_count}` members in the server `{guild_name}`.")
        print(f"All DMs were sent to {member_count} members in the server {guild_name}")
    else:
        await ctx.channel.send(f"🔴 **Error**: Please provide a message to send to all members of this Discord server!")

@dm_all.error
async def dm_all_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"⏳ **Command On Cooldown**: This command is on cooldown. Try again in `{int(error.retry_after)}s`."
        )
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("🔴 **Error**: You do not have the necessary permissions to run this command.")

@bot.command(name='dm_status')
@commands.cooldown(1, 5, commands.BucketType.member)
@commands.has_permissions(administrator=True)
async def dm_status_command(ctx):
    if dm_status['total'] == 0:
        await ctx.send("🔴 **Error:** No DM operation is currently in progress.")
    else:
        sent_percentage = (dm_status['sent'] / dm_status['total']) * 100
        failed_percentage = (dm_status['failed'] / dm_status['total']) * 100
        pending_percentage = 100 - (sent_percentage + failed_percentage)

        embed = discord.Embed(
            title="**📊 DM Status Report**",
            description="Here is the current status of the DM operation:",
            color=discord.Color.blue()
        )
        embed.add_field(name="**Total Members:**", value=f"`{dm_status['total']}`", inline=False)
        embed.add_field(name="**DMs Sent:**", value=f"`{dm_status['sent']}` ({sent_percentage:.2f}%)", inline=False)
        embed.add_field(name="**Failed DMs:**", value=f"`{dm_status['failed']}` ({failed_percentage:.2f}%)", inline=False)
        embed.add_field(name="**Pending DMs:**", value=f"`{dm_status['total'] - (dm_status['sent'] + dm_status['failed'])}` ({pending_percentage:.2f}%)", inline=False)

        await ctx.send(embed=embed)

@dm_status_command.error
async def dm_status_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("🔴 **Error**: You do not have the necessary permissions to run this command.")
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"⏳ **Command On Cooldown**: This command is on cooldown. Try again in `{int(error.retry_after)}s`."
        )

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="**🔧 Help Command**",
        description="Here's a list of available commands and how to use them:",
        color=discord.Color.orange()
    )
    embed.add_field(name="**;ping**", value="Shows the bot's latency and a random ping response.", inline=False)
    embed.add_field(name="**;dm_all [message]**", value="Sends a DM to all members of the server with the specified message. Requires administrator permissions.", inline=False)
    embed.add_field(name="**;dm_status**", value="Shows the current status of the DM operation, including sent, failed, and pending messages.", inline=False)
    embed.add_field(name="**;help**", value="Displays this help message.", inline=False)
    embed.set_footer(text="If you have any issues or need further assistance, feel free to reach out to: mihaivere")

    await ctx.send(embed=embed)

bot.run("BOT TOKEN!")
