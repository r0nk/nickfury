import utils
import interactions

token = open('token.txt','r').readlines()[0].strip('\n')
nickfury = interactions.Client(token=token)
TicketHandler = utils.TicketDict(deletion_after_close=False)

@nickfury.event
async def on_ready():
    print("The bot is now online.")

@nickfury.command(name="create_ticket",description="create a ticket",
        options = [
        interactions.Option(
            name="name",
            description="the name for the ticket",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
  )
async def create_ticket(ctx,name:str):
    TicketHandler.add_ticket(utils.Ticket(name, ctx.author.name))
    await ctx.send(f"Your ticket has been registered with the ticket number {TicketHandler._counter}.")

@nickfury.command(name="close_ticket",description="Close a ticket")
async def close_ticket(ctx, index:int):
    TicketHandler.close_ticket(index)
    await ctx.send("The ticket has been closed.")

@nickfury.command(name="display_ticket",description="Display a chosen ticket.")
async def display_ticket(ctx, index:int):
    fOutput = TicketHandler.display_ticket(index)
    await ctx.send(fOutput)

@nickfury.command(name="query_tickets",description="List Active Tickets")
async def query_tickets(ctx):
    fOutput = TicketHandler.query_tickets()
    await ctx.send(fOutput)

@nickfury.command(name="save_tickets",description="Make a backup of tickets")
async def save_tickets(ctx):
    TicketHandler.save_tickets()
    await ctx.send("Tickets are now backed up.")

@nickfury.command(name="reload_tickets",description="Load Tickets from a backup")
async def reload_tickets(ctx):
    ret = TicketHandler.reload_tickets()
    await ctx.send(f"Tickets are rolled back to last save at {ret}")

@nickfury.command(
        name="show_help",
    description="Display a help message",
)
async def show_help(ctx: interactions.CommandContext):
    await ctx.send("Hello world! ")

nickfury.start()
