from datetime import datetime
import time 
from threading import Thread, Semaphore



INITIAL_TIMESTAMP = datetime.now()

#the method below returns the elapsed time in seconds since the start of the excution and rounded to one decimal place
def get_elapsed_seconds() -> float:
    return round((datetime.now() - INITIAL_TIMESTAMP).total_seconds(), 1)

class TicketStore: #a ticket store with limited occupancy that tracks earnings and VIP customers.
    def __init__(self, max_occupancy, n_vips):
        """here i am initializing a Store object with the given maximum occupancy and number of VIP customers."""

        self.earnings = 0.0
        self.store_semaphore = Semaphore(max_occupancy)  #control store access based on occupancy
        self.earnings_semaphore = Semaphore(1)  #protects access to earnings
        self.vip_served_semaphore = Semaphore(0)  #protects updates to the count of served VIPs
        self.vips_served = 0  #keeps track the number of VIPs served
        self.n_vips = n_vips  #remaining VIP customers to be serve
        self.total_vips = n_vips  #total count of VIP customers to be serve
        

    def enter(self, buyer):
        """this method allows a customer to enter the store, respecting VIP priority and occupancy limits."""

        if buyer["VIP"]:
            self.store_semaphore.acquire()
            print(str(get_elapsed_seconds()) + 's: ' + buyer["name"] + '   ' + ' (Entering!)')
        else:
            #non-VIPs wait if VIPs are not fully served, but i am allowing more dynamic entry.
            while self.vips_served < self.total_vips:
                self.vip_served_semaphore.acquire()  #we wait for signal that a VIP has been served.
                self.vip_served_semaphore.release()  # here i release immediately for other waiting non-VIPs.
            self.store_semaphore.acquire()
            print(str(get_elapsed_seconds()) + 's: ' + buyer["name"] + '   ' + ' (Entering!)')

    def leave(self, buyer):
        """this method allows recording a customer leaving the store and updates VIP count"""

        print(str(get_elapsed_seconds()) + 's: ' + buyer["name"]+ '   '  + ' (Leaving!)')
        self.store_semaphore.release()
        if buyer["VIP"]:
            with self.earnings_semaphore:
                self.vips_served += 1
                #signal a non-VIP can enter for each VIP served, instead of waiting for all VIPs to be served. (more dynamic and flexible)
                self.vip_served_semaphore.release()



    def process_buyer (self, buyer, ticket_price):
        """
        this method simulates a customer's behavior: joining, 
        staying in the store, and leaving depending on the given parameters.

        """
        time.sleep(buyer["joinDelay"])
        self.enter(buyer)
        time.sleep(buyer["timeInStore"])
        with self.earnings_semaphore:
            self.earnings += ticket_price * buyer["ticketCount"] 
        self.leave(buyer)

    def simulate_store (self, buyers, ticket_price):
        """ this method simulates the store's operation including the VIP customers, 
        for the list of customers and ticket price given. and then returns the total earnings.
          """ 
        threads = []
        for buyer in buyers:
            thread = Thread(target=self.process_buyer, args=(buyer, ticket_price), name=buyer["name"])
            threads.append(thread)

        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return self.earnings
    
def simulate_store(customers: [dict], ticket_price: float, max_occupancy: int, n_vips: int) -> float: # type: ignore
    """this function is a wrapper for the TicketStore class, 
        and it simulates the store's operation including the VIP customers,
        for the list of customers and ticket price given. and then returns the total earnings.
    """
    store = TicketStore(max_occupancy, n_vips)
    return store.simulate_store(customers, ticket_price)
