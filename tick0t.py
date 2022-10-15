import discord
import utils
from discord.ext import commands

description = '...'
intents = discord.Intents.default()
tick0t = commands.Bot(command_prefix='/', description=description, intents=intents)
TicketHandler = utils.TicketDict(deletion_after_close=False)


@tick0t.event
async def on_ready():
    print("The bot is now online.")

@tick0t.command(name="create_ticket",description="create a ticket",
        options = [
        interactions.Option(
            name="name",
            description="the name for the ticket",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)

async def create_ticket(ctx):
    fOutput = TicketHandler.add_ticket(utils.Ticket(ctx.message.content[15:], ctx.author.name))
    await ctx.send(embed=fOutput)

@tick0t.command(name="close_ticket",description="Close a ticket")
async def close_ticket(ctx, index:int):
    fOutput = TicketHandler.close_ticket(index)
    await ctx.send(embed=fOutput)

@tick0t.command(name="view_ticket",description="Display a chosen ticket.")
async def view_ticket(ctx, index:int):
    fOutput = TicketHandler.display_ticket(index)
    await ctx.send(embed=fOutput)

@tick0t.command(name="list_tickets",description="List Active Tickets")
async def list_tickets(ctx):
    fOutput = TicketHandler.list_tickets()
    await ctx.send(embed=fOutput)

@tick0t.command(name="save_tickets",description="Make a backup of tickets")
async def save_tickets(ctx):
    fOutput = TicketHandler.save_tickets()
    await ctx.send(embed=fOutput)

@tick0t.command(name="load_tickets",description="Load Tickets from a backup")
async def load_tickets(ctx):
    fOutput = TicketHandler.reload_tickets()
    await ctx.send(embed=fOutput)

@tick0t.command()
async def shutdown(ctx):
    exit()

tick0t.run('token')