from threading import Thread
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class Pipeline(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities  # ! Região crítica
        self.location = location
        self.constraint = constraint

    def print_pipeline(self):
        globals.acquire_print()
        print(f"🔨 - [{self.location}] → {self.unities} oil unities are produced ⛽ ")
        globals.release_print()
        
    def produce(self):
        
        with globals.pipeline_units:  # Protege acesso a Pipeline.units !! Região crítica !!
            if(self.unities < self.constraint):
                self.unities += 17
                self.print_pipeline()
                 # Incrementa para bases saberem que podem pegar uma porção de óleo
                globals.available_oil.release()
        

        sleep(0.001)

    def run(self):

        while(globals.get_release_system() == False):
            pass
        
        while(True):
            self.produce()
            
            # Se True, finaliza thread
            if globals.finalize_threads == True:
                break    
        
