import discord
import random
import asyncio
import json
from datetime import datetime
import pytz
from discord.ext import commands

with open('settings.json') as f:
    settings = json.load(f)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)
bot.remove_command('help')

dm_status = {
    'total': 0,
    'sent': 0,
    'failed': 0
}

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "**⚠️ Error**: The command you tried to use does not exist!\n"
            "Please use: `;help` to see all available commands."
        )

@bot.event
async def on_ready():
    owner = (await bot.application_info()).owner

    guilds = bot.guilds
    guild_name = '\n'.join([
        f"\n**▫️ Server Name**: `{guild.name}`\n"
        f"**▫️ Server ID**: `{guild.id}`\n"
        f"**▫️ Members**: `{len(guild.members)}`" 
        for guild in guilds
    ])
    
    bucharest_tz = pytz.timezone('Europe/Bucharest')
    now = datetime.now(bucharest_tz)
    datestamp = now.strftime('%Y-%m-%d')
    timestamp = now.strftime('%H:%M:%S')

    latency = round(bot.latency * 1000)

    print(f" ")
    print(f"[{datestamp} | {timestamp}] {bot.user.name}({bot.user.id}) is connected to Discord!")
    print(f" ")
    print(f"MASS DM Bot by M1HA15")
    print(f"Check out my other projects on GitHub: https://github.com/M1HA15")
    print(f" ")

    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"{settings['status']}"))
    
    await asyncio.sleep(5)
    
    if owner:
        await owner.send(
            f"**✅ {bot.user.name}** (`{bot.user.id}`) is **running**!\n\n"
            f"**📶 Ping**: `{latency}ms`\n"
            f"**📅 Date**: `{datestamp}`\n"
            f"**⏰ Time**: `{timestamp}`\n"
            f"**🛰️ Connected to**: {guild_name}\n\n"
            f"**💡 Thank you for using my [MASS DM Bot](https://github.com/M1HA15/Discord-Mass-DM-Bot)**"
        )

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    random_ping_responses = ['🏓 **Poooong!**', '🏓 **Poong!**', '🏓 **Pong!**', '🏓 **Pooong!**']
    chosen_ping = random.choice(random_ping_responses)
    bucharest_tz = pytz.timezone('Europe/Bucharest')
    now = datetime.now(bucharest_tz)
    datestamp = now.strftime('%Y-%m-%d')
    timestamp = now.strftime('%H:%M:%S')
    
    await ctx.send(
        f"{chosen_ping}\n\n"
        f"**📶 Latency**: `{latency}ms`\n"
        f"**📅 Date**: `{datestamp}`\n"
        f"**⏰ Time**: `{timestamp}`"
    )
    
    await asyncio.sleep(20)
    
    owner = (await bot.application_info()).owner
    
    if owner:
        await owner.send(
            f"**📶 Ping**: `{latency}ms`\n"
            f"**📅 Date**: `{datestamp}`\n"
            f"**⏰ Time**: `{timestamp}`\n"
            f"**🪁 Requested by**: `{ctx.author}` (`{ctx.message.author.id}`)"
        )
    print(f"[{datestamp} | {timestamp}] Latency: {latency}ms")

@bot.command(name="dm_all")
@commands.has_permissions(administrator=True)
@commands.cooldown(1, 300, commands.BucketType.guild)
async def dm_all(ctx, *, args=None):
    if args is not None:
        members = ctx.guild.members
        bucharest_tz = pytz.timezone('Europe/Bucharest')
        now = datetime.now(bucharest_tz)
        datestamp = now.strftime('%Y-%m-%d')
        member_count = len(members)
        guild_name = ctx.guild.name

        dm_status['total'] = member_count
        dm_status['sent'] = 0
        dm_status['failed'] = 0
        
        start_time = datetime.now(bucharest_tz).strftime('%H:%M:%S')
        
        await ctx.channel.send(
            f"**🔔 DM Broadcast Initiated**!\n\n"
            f"**💾 Server**: `{guild_name}`\n"
            f"**👥 Total Members**: `{member_count}`\n"
            f"**📅 Date**: `{datestamp}`\n"
            f"**⏰ Start Time**: `{start_time}`\n\n"
            f"**‼️ Please be patient as this process may take some time**."
        )
        print(f"[{datestamp} | {start_time}] Starting to send DMs to {member_count} members in {guild_name}!")
        print(f"-> Command executed by {ctx.message.author} ({ctx.message.author.id})")
        
        for member in members:
            try:
                await asyncio.sleep(50)
                timestamp = datetime.now(bucharest_tz).strftime('%H:%M:%S')
                await member.send(args)
                await asyncio.sleep(15)
                dm_status['sent'] += 1
                await ctx.channel.send(
                    f"**🟢 DM Sent** to: `{member.name}#{member.discriminator}` (`{member.id}`)\n"
                    f"- **⏰ Time**: `{timestamp}`"
                )
                print(f"[{datestamp} | {timestamp}] DM Sent To: {member.name} (ID: {member.id})")
                await asyncio.sleep(25)
            except discord.Forbidden:
                await asyncio.sleep(15)
                dm_status['failed'] += 1
                timestamp = datetime.now(bucharest_tz).strftime('%H:%M:%S')
                await ctx.channel.send(
                    f"**🔴 DM Can't be Sent** to: `{member.name}#{member.discriminator}` (`{member.id}`)\n"
                    f"- **⏰ Time**: `{timestamp}`\n"
                    f"- **⚠️ Error**: `User has closed DMs or has privacy settings that prevent receiving messages.`"
                )
                print(f"[{datestamp} | {timestamp}] DM Can't be Sent To: {member.name} (ID: {member.id})")
                print(f"-> User has closed DMs or has privacy settings that prevent receiving messages")
                await asyncio.sleep(35)
            except discord.HTTPException as e:
                await asyncio.sleep(15)
                dm_status['failed'] += 1
                timestamp = datetime.now(bucharest_tz).strftime('%H:%M:%S')
                await ctx.channel.send(
                    f"**🔴 DM Can't be Sent** to: `{member.name}#{member.discriminator}` (`{member.id}`)\n"
                    f"- **⏰ Time**: `{timestamp}`\n"
                    f"- **📡 HTTP Error**: `{e}`"
                )
                print(f"[{datestamp} | {timestamp}] DM Can't be Sent To: {member.name} (ID: {member.id})")
                print(f"-> HTTP Error: {e}")
                await asyncio.sleep(35)
            except Exception as e:
                await asyncio.sleep(15)
                dm_status['failed'] += 1
                timestamp = datetime.now(bucharest_tz).strftime('%H:%M:%S')
                await ctx.channel.send(
                    f"**🔴 DM Can't be Sent** to: `{member.name}#{member.discriminator}` (`{member.id}`)\n"
                    f"- **⏰ Time**: `{timestamp}`\n"
                    f"- **🔗 Unexpected Error**: `{e}`"
                )
                print(f"[{datestamp} | {timestamp}] DM Can't be Sent To: {member.name} (ID: {member.id})")
                print(f"-> Unexpected Error: {e}")
                await asyncio.sleep(35)
        
        now = datetime.now(bucharest_tz)
        datestamp = now.strftime('%Y-%m-%d')
        timestamp = now.strftime('%H:%M:%S')
        
        await ctx.channel.send(
            f"**✅ DM Operation Completed**!\n\n"
            f"**📬 Total Messages Sent**: `{dm_status['sent']}`\n"
            f"**📅 Date**: `{datestamp}`\n"
            f"**⏰ Time**: `{timestamp}`\n"
            f"**🙏 Thank You for your Patience**!"
        )
        await asyncio.sleep(15)
        await ctx.author.send(
            f"**✅ DM Operation Finished Successfully**!\n\n"
            f"**📬 Messages Sent to Members**: `{dm_status['sent']}`\n"
            f"**💾 Server**: `{guild_name}`\n"
            f"**📅 Date**: `{datestamp}`\n"
            f"**⏰ Time**: `{timestamp}`\n"
            f"**🙏 Thank You for using the DM Feature**!"
        )
        print(f"[{datestamp} | {timestamp}] All DMs were sent to {member_count} members in the server {guild_name}")
        print(f"-> Operation completed successfully!")
    else:
        await ctx.channel.send(
            "**⚠️ Error**: Please provide a message to send to all members of this Discord server!"
        )

@dm_all.error
async def dm_all_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"**⏳ Command On Cooldown**: This command is on cooldown. Try again in `{int(error.retry_after)}s`."
        )
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "**⚠️ Error**: You do not have the necessary permissions to run this command."
        )

@bot.command(name='dm_status')
@commands.cooldown(1, 5, commands.BucketType.member)
@commands.has_permissions(administrator=True)
async def dm_status_command(ctx):
    bucharest_tz = pytz.timezone('Europe/Bucharest')
    now = datetime.now(bucharest_tz)
    datestamp = now.strftime('%Y-%m-%d')
    timestamp = now.strftime('%H:%M:%S')
    
    latency = round(bot.latency * 1000)
    
    if dm_status['total'] == 0:
        await ctx.send(
            "**⚠️ Error**: No DM operation is currently in progress!"
        )
    else:
        sent_percentage = (dm_status['sent'] / dm_status['total']) * 100
        failed_percentage = (dm_status['failed'] / dm_status['total']) * 100
        pending_percentage = 100 - (sent_percentage + failed_percentage)

        await ctx.send(
            f"**📊 DM Status Report**:\n\n"
            f"**🔵 Total Members**: `{dm_status['total']}`\n"
            f"**🟢 DMs Sent**: `{dm_status['sent']}` ({sent_percentage:.2f}%)\n"
            f"**🔴 Failed DMs**: `{dm_status['failed']}` ({failed_percentage:.2f}%)\n"
            f"**🟡 Pending DMs**: `{dm_status['total'] - (dm_status['sent'] + dm_status['failed'])}` ({pending_percentage:.2f}%)\n\n\n"
            f"**📶 Ping**: `{latency}ms`\n"
            f"**📅 Date**: `{datestamp}`\n"
            f"**⏰ Time**: `{timestamp}`"
        )
        print(f"[{datestamp} | {timestamp}] DM Status Requested by {ctx.author} in {ctx.guild} ({dm_status['total']}/{dm_status['sent']}/{dm_status['failed']}/{dm_status['total'] - (dm_status['sent'] + dm_status['failed'])})")

@dm_status_command.error
async def dm_status_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "**⚠️ Error**: You do not have the necessary permissions to run this command."
        )
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(
            f"**⏳ Command On Cooldown**: This command is on cooldown. Try again in `{int(error.retry_after)}s`."
        )

@bot.command(name='help')
async def help_command(ctx):
    bucharest_tz = pytz.timezone('Europe/Bucharest')
    now = datetime.now(bucharest_tz)
    datestamp = now.strftime('%Y-%m-%d')
    timestamp = now.strftime('%H:%M:%S')
    
    latency = round(bot.latency * 1000)
    prefix = settings['prefix']

    help_message = (
        f"**🔧 Help Command**\n"
        f"Here's a comprehensive list of available commands and their descriptions:\n\n"
        f"**✨ {prefix}ping**\n"
        f"   🕒 Displays the bot's latency and provides a random ping response.\n"
        f"**📨 {prefix}dm_all [message]**\n"
        f"   📩 Sends a direct message to all members of the server. **(Admin only)**\n"
        f"**📊 {prefix}dm_status**\n"
        f"   📈 Provides the current status of the DM operation including sent, failed, and pending messages. **(Admin only)**\n"
        f"**🆘 {prefix}help**\n"
        f"   📜 Displays this help message.\n\n"
        f"**📶 Ping**: `{latency}ms`\n"
        f"**📅 Date**: `{datestamp}`\n"
        f"**⏰ Time**: `{timestamp}`\n\n"
        f"**ℹ️ Need more assistance?**\n"
        f"Contact **[Mihai](https://github.com/M1HA15/)** on **Discord**: `mihaivere`"
    )

    await ctx.send(help_message)

bot.run(settings['token'])
