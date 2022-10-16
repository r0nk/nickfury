import pickle
import os
import discord
from typing import Dict
from enum import Enum
from time import strftime
from dateutil.parser import parse

TICKET_OPEN, TICKET_CLOSED = True, False

# Implement a title system
class Ticket():
    def __init__(self, ticket_contents, ticket_author):
        self.contents = ticket_contents
        self.number : int = None
        self.status : bool = TICKET_OPEN
        self.author = ticket_author

class EmbedType(Enum):
    ERR = discord.Embed(title="Uh oh, something went wrong!")
    DISPLAY_ONE = discord.Embed()
    DISPLAY_ALL = discord.Embed(title="All open tickets are listed below...")
    TICKET_CREATED = discord.Embed(title="Your ticket has been created!")
    TICKET_CLOSED = discord.Embed(title="The ticket has been closed.")
    TICKET_CLOSED_USER = discord.Embed(title="Your ticket has been closed!")
    TICKET_CLAIMED = discord.Embed(title="You've claimed the ticket successfully.")
    TICKETS_SAVED = discord.Embed(title="Saved successfully!")
    TICKETS_LOADED = discord.Embed(title="Loaded successfully!")
    CHANNEL_SET = discord.Embed(title="Channel successfully set!")


class TicketDict():
    def __init__(self, deletion_after_close=False):
        self._tickets : Dict[int, Ticket] = { }
        self._counter = 0
        self._delete = deletion_after_close
        #self.reload_tickets() #TODO these break on first load

    # Add a ticket, return the ticket number given...
    def add_ticket(self, ticket : Ticket) -> int:
        self._counter += 1
        ticket.number = self._counter
        self._tickets.update( {self._counter: ticket} )
        return match_embed(EmbedType.TICKET_CREATED, number=self._counter)

    # Close a ticket
    def close_ticket(self, ticket_num : int):
        if self._delete == False:
            self._tickets[ticket_num].status = False
        else:
            del self._tickets[ticket_num]
        return match_embed(EmbedType.TICKET_CLOSED)

    # Implement error checking -- The ticket index could not be valid.
    # Pretty print of a specific ticket...
    def display_ticket(self, index) -> str:
        #Simple error check, if index is greater than total tickets, then it's invalid.
        if(index > self._counter or index < 0):
            return match_embed(EmbedType.ERR, content="You've tried to display a ticket that doesn't exist.", number=index)
        return match_embed(EmbedType.DISPLAY_ONE,
        content=self._tickets[index].contents,
        number=index,
        author=self._tickets[index].author,
        status=match_status(self._tickets[index].status))

    # Pretty print of currently open tickets, limiting the size of the ticket contents for a preview.
    # MAKE THIS CLEANER WAY OF ADDING TO THE OUTPUT, MAKE "PAGES" OF TICKETS WITH INTERACTIONS?
    def list_tickets(self) -> str:
        fOutput = ""
        for ticket in self._tickets.items():
            if ticket[1].status == TICKET_OPEN:
                fOutput += f"🎫 #{ticket[1].number} authored by {ticket[1].author} : { ticket[1].contents[:30] } \n"
        return match_embed(EmbedType.DISPLAY_ALL, content=fOutput)

    # Save tickets to disk for future use
    def save_tickets(self):
        try:
            fn = change_str("db\\" + strftime("%c"))
            pickle.dump(self, open(fn, "wb"))
        except Exception:
            return match_embed(EmbedType.ERR, content="There was an error when saving the tickets.")
        return match_embed(EmbedType.TICKETS_SAVED)

    # Reload tickets from last saved instance
    def reload_tickets(self) -> str:
        holder, filename = self.determine_latest()
        assert holder != None # Change and handle this gracefully...
        assert filename != None
        try:
            lTicketDict = pickle.load(open("db\\" + filename, "rb"))
        except EOFError:
            return match_embed(EmbedType.ERR, content="There was an error with reloading the tickets.")
        self._tickets = lTicketDict._tickets
        self._counter = lTicketDict._counter
        self._delete = lTicketDict._delete
        return match_embed(EmbedType.TICKETS_LOADED)

    # Function for reload_tickets
    def determine_latest(self):
        holder, filename = None, None
        for fn in os.listdir(".\\db"):
            if holder == None:
                holder = parse(restore_str(fn))
                filename = fn
            elif parse(restore_str(fn)) > holder:
                holder = parse(restore_str(fn))
                filename = fn
            else:
                continue
        return holder, filename

    # Function to set a channel as admin ticket channel
    def set_channel(self):
        #now set the current channel ID as a persistent variable saved for each server
        #print(f'Admin channel set as #{admin_channel}')
        return


    #UTIL FUNCS
def change_str(fn : str) -> str:
    return fn.replace(" ", "_").replace(":", "-")

def restore_str(fn : str) -> str:
    return fn.replace("_", " ").replace("-", ":")

def match_status(status : bool) -> str:
    match status:
        case True:
            return "open"
        case False:
            return "closed"
        case _:
            raise Exception

def match_embed(embed : EmbedType, content : str=None, number : int=None, author : str=None, status : str=None) -> discord.Embed:
    match embed:
        case EmbedType.ERR:
            cEmbed = EmbedType.ERR.value.copy()
            cEmbed.description = content
            cEmbed.set_footer(text=f"Tick0t 🎫#{pad_num(number)}", icon_url="https://cdn.discordapp.com/avatars/1029789818185584662/8d8b9e1c35c520eefa6e332dfcbb5587.webp?size=160")
            return cEmbed
        case EmbedType.DISPLAY_ONE:
            cEmbed = EmbedType.DISPLAY_ONE.value.copy()
            cEmbed.description = content + f"\n\n\nThis ticket is currently {status}."
            cEmbed.title = author
            cEmbed.set_footer(text=f"Tick0t 🎫#{pad_num(number)}", icon_url="https://cdn.discordapp.com/avatars/1029789818185584662/8d8b9e1c35c520eefa6e332dfcbb5587.webp?size=160")
            return cEmbed
        case EmbedType.DISPLAY_ALL:
            cEmbed = EmbedType.DISPLAY_ALL.value.copy()
            cEmbed.description = content
            return cEmbed
        case EmbedType.TICKET_CREATED:
            cEmbed = EmbedType.TICKET_CREATED.value.copy()
            cEmbed.description = f"Your ticket number is {number}. \n We will be right back with a response!"
            return cEmbed
        case EmbedType.TICKET_CLOSED:
            cEmbed = EmbedType.TICKET_CLOSED.value.copy()
            cEmbed.description = "You have closed the ticket to revert this change, use the /change_status command.\n If you have delete after close on, this is not possible."
            return cEmbed
        case EmbedType.TICKET_CLAIMED:
            cEmbed = EmbedType.TICKET_CLAIMED.value.copy()
            cEmbed.description = "You have claimed the ticket to revert this change, use the /unclaim command."
            return cEmbed
        case EmbedType.TICKETS_SAVED:
            cEmbed = EmbedType.TICKETS_SAVED.value.copy()
            cEmbed.description = "The tickets have been backed up, now on restart it will start to this instance."
            return cEmbed
        case EmbedType.TICKETS_LOADED:
            cEmbed = EmbedType.TICKETS_LOADED.value.copy()
            cEmbed.description = "The tickets have loaded successfully, you can now access tickets."
            return cEmbed
        case EmbedType.CHANNEL_SET:
            cEmbed = EmbedType.CHANNEL_SET.value.copy()
            cEmbed.description = "This channel will now display any tickets created (once this functionality is implemented)."
            return cEmbed
        case _:
            raise Exception
            
def pad_num(num : int) -> str:
    return str(num).zfill(9)
