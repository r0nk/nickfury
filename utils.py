import pickle
import os
from typing import Dict
from time import strftime
from dateutil.parser import parse

TICKET_OPEN, TICKET_CLOSED = True, False

class Ticket():
    def __init__(self, ticket_contents, ticket_author):
        self.contents = ticket_contents
        self.number : int = None
        self.status : bool = TICKET_OPEN
        self.author = ticket_author

class TicketDict():
    def __init__(self, deletion_after_close=False):
        self._tickets : Dict[int, Ticket] = {}
        self._counter = 0
        self._delete = deletion_after_close

    # Add a ticket, return the ticket number given...
    def add_ticket(self, ticket : Ticket) -> int:
        self._counter += 1
        ticket.number = self._counter
        self._tickets.update( {self._counter: ticket} )
        return self._counter

    # Close a ticket
    def close_ticket(self, ticket_num : int):
        if self._delete == False:
            self._tickets[ticket_num].status = False
        else:
            del self._tickets[ticket_num]
        return

    # Pretty print of a specific ticket...
    def display_ticket(self, index) -> str:
        return f''' 
    ```
    Ticket number : {index}

    The contents of the ticket : {self._tickets[index].contents}

    The author of the ticket : {self._tickets[index].author}

    The status of the ticket : {self._tickets[index].status}```
    '''

    # Pretty print of currently open tickets, limiting the size of the ticket contents for a preview.
    def query_tickets(self) -> str:
        fOutput = ""
        for ticket in self._tickets.items():
            if ticket[1].status == TICKET_OPEN:
                fOutput += f"Ticket #{ticket[1].number} authored by {ticket[1].author} : { ticket[1].contents[:50] } \n"
        return fOutput

    # Save tickets to disk for future use
    def save_tickets(self):
        fn = self.change_str("db\\" + strftime("%c"))
        pickle.dump(self, open(fn, "wb"))
        return

    # Reload tickets from last saved instance
    def reload_tickets(self) -> str:
        holder = parse("Fri Mar 27 16:23:01 2015") # Arbitrary holder, needs to be refactored...
        for fn in os.listdir(".\\db"):
            cmp = parse(self.restore_str(fn))
            if cmp > holder:
                holder = cmp
        return holder
        
    #UTIL FUNC
    def change_str(self, fn : str) -> str:
        return fn.replace(" ", "_").replace(":", "-")

    def restore_str(self, fn : str) -> str:
        return fn.replace("_", " ").replace("-", ":")