import discord
from discord.ext import commands
from typing import List
import utils

description = '...'
intents = discord.Intents.all()
nickfury = commands.Bot(command_prefix='/', description=description, intents=intents)
TicketHandler = utils.TicketDict(deletion_after_close=False)

@nickfury.event
async def on_ready():
    print("The bot is now online.")

@nickfury.command()
async def create_ticket(ctx):
    TicketHandler.add_ticket(utils.Ticket(ctx.message.content[15:], ctx.author.name))
    await ctx.send(f"Your ticket has been registered with the ticket number {TicketHandler._counter}.")

@nickfury.command()
async def close_ticket(ctx, index:int):
    TicketHandler.close_ticket(index)
    await ctx.send("The ticket has been closed.")

@nickfury.command()
async def display_ticket(ctx, index:int):
    fOutput = TicketHandler.display_ticket(index)
    await ctx.send(fOutput)

@nickfury.command()
async def query_tickets(ctx):
    fOutput = TicketHandler.query_tickets()
    await ctx.send(fOutput)

@nickfury.command()
async def save_tickets(ctx):
    TicketHandler.save_tickets()
    await ctx.send("Tickets are now backed up.")

@nickfury.command()
async def shutdown(ctx):
    exit()

nickfury.run(open('token.txt','r').readlines()[0])
