# mit the black code style formatiert für leserlichkeit
# mehr hier: https://pypi.org/project/black/

import os
import hikari
import lightbulb
import asyncio
import validators
import requests
import logging
from dotenv import load_dotenv


load_dotenv()  # .env Datei laden
logging.basicConfig(level=logging.DEBUG)

bot = lightbulb.BotApp(token=os.environ["TOKEN"])  # Token aus .env Dateip


# /add-emoji <bild-url> <name>
@bot.command
@lightbulb.add_checks(
    lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_EMOJIS_AND_STICKERS)
)
@lightbulb.option(
    "name", "insert name here", type=hikari.OptionType.STRING
)  # @lightbulb.option erstellt eine option hinter einem befehl, type=hikari.OptionType.STRING setzt einen OptionType (Rollen,Integer,member) wobei dieser optiontype überprüft ob es sich um eine URL Handelt
@lightbulb.option(
    "bild-url", "link to an image that should be send", type=validators.url
)  # Bild Einfügen
@lightbulb.command(
    "add-emoji", "adds an image as a Emoji to the Server"
)  # Basis Command
@lightbulb.implements(lightbulb.SlashCommand)  # Implementiert den / Prefix
async def add_emoji(ctx: lightbulb.Context) -> None:  # idk
    member = await ctx.bot.rest.fetch_member(ctx.guild_id, ctx.author.id)
    permission = lightbulb.utils.permissions_for(member)
    guild = ctx.get_guild()  # die guild snowflake
    name = (
        ctx.options.name
    )  # definiert das "name" auf die funktion ctx.options.name hinweisst dabei holt sich der bot die Snowflake
    print(validators.url(ctx.options.bild))  # bild muss eine url sein
    if validators.url(ctx.options.bild) is not True:  # wenn es kein link ist
        await ctx.respond(
            embed=hikari.Embed(
                title="Invalid URL",
                description="Please use a URL that leads to an image with the size of 108x108",
                color="#FF0000",
            )
        )
        return  # wenn url kein bild ist oder keine url ist bricht er ab
    image = ctx.options.bild  # image ist das bild
    if (
        lightbulb.has_guild_permissions(hikari.Permissions.MANAGE_EMOJIS_AND_STICKERS)
        == True
    ):
        print("else")
        await bot.rest.create_emoji(guild=guild, name=str(name), image=image)
        await ctx.respond(
            embed=hikari.Embed(
                title="Emoji added",
                description="the emoji was now uploaded and can be used",
                color="#00FF00",
            )
        )
        return


print("end")


# /unban-member <member>
@bot.command
@lightbulb.option(
    "member", "the id of a member that should be unbanned", type=hikari.OptionType.USER
)
@lightbulb.command("unban-member", "unbans a member")
@lightbulb.implements(lightbulb.SlashCommand)
async def unban_member(ctx: lightbulb.context) -> None:
    guild = ctx.get_guild()
    id = ctx.options.user.id
    try:
        await guild.unban(user=str(id))
        await ctx.respond(
            embed=hikari.Embed(
                title="Success",
                description="member is now unbanned from this guild",
                color="0C9E5A",
            )
        )
    except Exception as error:
        await ctx.respond(error)


# /ban-member <member> <reason>
@bot.command
@lightbulb.option(
    "member", "the id of the member that should be banned", type=hikari.OptionType.USER
)
@lightbulb.command("ban-member", "bans a member")
@lightbulb.implements(lightbulb.SlashCommand)
async def ban_member(ctx: lightbulb.context) -> None:
    guild = ctx.get_guild()
    id = ctx.options.user.id
    try:
        await guild.ban(user=str(id))
    except:
        pass
    await ctx.respond(
        embed=hikari.Embed(
            title="Success",
            description="member is now banned from this guild",
            color="FF0000",
        )
    )


# /nsfw
@bot.command
@lightbulb.command("nsfw", "sends a random nsfw gif")
@lightbulb.implements(lightbulb.SlashCommand)
async def nsfw(ctx: lightbulb.context) -> None:
    await ctx.respond("https://c.tenor.com/nUaizsGhvtIAAAAd/the-rock-sus.gif")
    print("exectuted nsfw") # <-- mach ich dann nachher wenn ich wieder vom einkaufen bin


# /voice-mute <member>
@bot.command
@lightbulb.option(
    "member", "the id of the member that should be muted", type=hikari.OptionType.USER
)
@lightbulb.command("voice-mute", "mutes a member in a voice channel")
@lightbulb.implements(lightbulb.SlashCommand)
async def mute_member(ctx: lightbulb.context) -> None:
    guild = ctx.get_guild()
    member = ctx.options.id
    member = guild.get_member(member)
    mute = True
    self = ctx.options.id
    await member.edit(mute=True)
    if member.edit(mute=False):
        await ctx.respond(
            embed=hikari.Embed(
                title="member is now muted", description="muted member in vc"
            )
        )
        return
    await ctx.respond(
        embed=hikari.Embed(
            title="cant mute member",
            description="make sure youre using a valid id and that the member is in a vc",
        )
    )


# /voice-unmute <member>
@bot.command
@lightbulb.option(
    "member", "the member that should be unmuted", type=hikari.OptionType.USER
)
@lightbulb.command("voice-unmute", "unmutes a member in a voice channel")
@lightbulb.implements(lightbulb.SlashCommand)
async def unmute_member(ctx: lightbulb.context) -> None:
    guild = ctx.get_guild()
    member = ctx.options.id
    member = guild.get_member(member)
    mute = False
    self = ctx.options.id
    await member.edit(mute=False)
    if member.edit(mute=True):
        await ctx.respond(
            embed=hikari.Embed(
                title="member is now unmuted", description="unmuted member in vc"
            )
        )
        return
    await ctx.respond(
        embed=hikari.Embed(
            title="cant unmute member",
            description="make sure youre using a valid id and that the member is in a vc and muted",
        )
    )


# /create-webhook <name> <channel>
@bot.command
@lightbulb.option(
    "channel",
    "the channel id of the webhooks destination",
    type=hikari.OptionType.CHANNEL,
)
@lightbulb.option("name", "The name for the webhook. This cannot be clyde")
@lightbulb.command("create-webhook", "creates a webook")
@lightbulb.implements(lightbulb.SlashCommand)
async def create_webhook(ctx: lightbulb.context) -> None:
    guild = ctx.get_guild()
    channel = ctx.options.channel
    name = ctx.options.name
    await bot.rest.create_webhook(channel=channel, name=name)
    await ctx.respond(embed=hikari.Embed(title="Created Webhook"))


# /webhook-token <channel>
@bot.command
@lightbulb.option(
    "channel",
    "the channel in wich the webhook was created",
    type=hikari.OptionType.CHANNEL,
)
@lightbulb.command("webhook-token", "prints the token of a webhook")
@lightbulb.implements(lightbulb.SlashCommand)
async def fetch_webhook_token(ctx: lightbulb.context) -> None:
    channel = ctx.options.channel
    webhook = await bot.rest.fetch_channel_webhooks(channel=channel)
    await ctx.respond(webhook[0].token)


bot.run()
