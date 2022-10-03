from threading import Thread
from random import randint
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class StoreHouse(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities  # ! Região crítica
        self.location = location
        self.constraint = constraint

    def print_store_house(self):
        globals.acquire_print()
        print(f"🔨 - [{self.location}] → {self.unities} uranium unities are produced ☢ .")
        globals.release_print()

    def produce(self):
        with globals.store_house_units:  # Protege acesso a SoreHouse.units !! Região cŕitica !!
            if(self.unities < self.constraint):
                self.unities += 15
                self.print_store_house()
                # Incrementa para bases saberem que podem pegar uma porção de urânio
                globals.available_uranium.release()
         

        sleep(0.001)

    def run(self):

        while(globals.get_release_system() == False):
            pass
        
        while(True):
            self.produce()
            
            # Se True, finaliza thread
            if globals.finalize_threads == True:
                break    
