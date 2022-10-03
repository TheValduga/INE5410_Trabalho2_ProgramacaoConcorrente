from pickle import FALSE, TRUE
from weakref import finalize
import globals
from threading import Thread, Lock, Semaphore
from space.rocket import Rocket
from random import choice


class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] - ☢  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {len(self.rockets)}/{self.constraints[2]}")

    def try_to_build_rocket(self, choiced_rocket):

        ''' ### 1. Base testa o próprio nome
            ### 2. Testa se tem recurso para construir o foguete sorteado randomicamente
            ### 3.1 Se tem recurso, constrói o foguete e armazena na base 
            ### 3.2 Se não tem recurso, sai da função sem construir '''

        if self.name == 'MOON':
            if (choiced_rocket == 'DRAGON' and self.fuel >= 50) or (choiced_rocket == 'FALCON' and self.fuel >= 90):
                
                rocket = Rocket(choiced_rocket)

                # Decrementa recurso dependendo da base e de qual foguete construído
                if choiced_rocket == 'DRAGON':
                    self.fuel -= 50
                else:
                    self.fuel -= 90
                self.uranium -= 35

                # Adiciona foguete ao armazenamento da base
                self.rockets.append(rocket) 

                globals.acquire_print()
                print(f'🔭 - [{self.name}]: Building {choiced_rocket} rocket')
                self.print_space_base_info()
                globals.release_print()

        elif self.name == 'ALCANTARA':
            if (choiced_rocket == 'DRAGON' and self.fuel >= 70) or (choiced_rocket == 'FALCON' and self.fuel >= 100) or (choiced_rocket == 'LION'):

                rocket = Rocket(choiced_rocket)
                
                # Decrementa recurso dependendo da base e de qual foguete construído
                if choiced_rocket == 'DRAGON':
                    self.fuel -= 70
                    self.uranium -= 35

                elif choiced_rocket == 'FALCON':
                    self.fuel -= 100
                    self.uranium -= 35

                else:
                    lua = globals.get_bases_ref().get('moon')
                    delivery_fuel = 30000 - lua.fuel
                    delivery_uranium = 150 - lua.uranium
                    
                    if delivery_fuel >= 120:
                        delivery_fuel = 120
                    if  delivery_uranium >= 75:
                        delivery_uranium = 75
                        
                    self.uranium -= delivery_uranium
                    rocket.uranium_cargo += delivery_uranium
                    self.fuel -= delivery_fuel
                    rocket.fuel_cargo += delivery_fuel

                # Adiciona foguete ao armazenamento da base
                self.rockets.append(rocket)

                globals.acquire_print()
                print(f'🔭 - [{self.name}] Building {choiced_rocket} rocket')
                self.print_space_base_info()
                globals.release_print()

        else:
            if (choiced_rocket == 'DRAGON' and self.fuel >= 100) or (choiced_rocket == 'FALCON' and self.fuel >= 120) or (choiced_rocket == 'LION'):

                rocket = Rocket(choiced_rocket)

                # Decrementa recurso dependendo da base e de qual foguete construído
                if choiced_rocket == 'DRAGON':
                    self.fuel -= 100
                    self.uranium -= 35

                elif choiced_rocket == 'FALCON':
                    self.fuel -= 120
                    self.uranium -= 35

                else:
                    lua = globals.get_bases_ref().get('moon')
                    delivery_fuel = 30000 - lua.fuel
                    delivery_uranium = 150 - lua.uranium
                    
                    if delivery_fuel >= 120:
                        delivery_fuel = 120
                    if  delivery_uranium >= 75:
                        delivery_uranium = 75
                        
                    self.uranium -= delivery_uranium
                    rocket.uranium_cargo += delivery_uranium
                    self.fuel -= delivery_fuel
                    rocket.fuel_cargo += delivery_fuel
                    
                # Adiciona foguete ao armazenamento da base
                self.rockets.append(rocket)

                globals.acquire_print()
                print(f'🔭 - [{self.name}] Building {choiced_rocket} rocket')
                self.print_space_base_info()
                globals.release_print()

    
    def refuel_oil(self):

        # Verifica se tem espaço suficiente para pegar uma porção de óleo
        if self.fuel <= self.constraints[1] - 17:
            
            # Decrementa para sinalizar que pegou uma porção de óleo
            globals.available_oil.acquire()
            
            # Se o programa pede para finalizar, não coleta mais recurso
            if globals.finalize_threads == False:
            
                self.fuel += 17  # Incrementa próprio óleo
                
                with globals.pipeline_units:  # Protege acesso a Pipeline.units !! Região crítica !!
                    globals.get_mines_ref().get('oil_earth').unities -= 17  # Decrementa óleo da mina
                    
                globals.acquire_print()
                print(f'🔭 - [{self.name}] → refueling 17 ⛽')
                self.print_space_base_info()
                globals.release_print()


    def refuel_uranium(self):

        # Verifica se tem espaço suficiente para pegar uma porção de urânio
        if self.uranium < self.constraints[0] - 15:
            
            # Decrementa para sinalizar que pegou uma porção de urânio
            globals.available_uranium.acquire()
            
            # Se o programa pede para finalizar, não coleta mais recurso
            if globals.finalize_threads == False:
            
                self.uranium += 15  # Incrementa próprio urânio
                
                with globals.store_house_units:  # Protege acesso a StoreHouse.units !! Região crítica !!
                    globals.get_mines_ref().get('uranium_earth').unities -= 15 # Decrementa urânio da mina
                    
                globals.acquire_print()
                print(f'🔭 - [{self.name}] → refueling 15 ☢')
                self.print_space_base_info()
                globals.release_print()

    
    def run(self):

        self.rockets = [] # Setado como lista para armazenar objetos de foguetes
        random_rockets = ['DRAGON', 'FALCON'] # Lista para escolha de foguetes randomicos

        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            
            # Se MOON, verificar se precisa de recurso e se não tem nenhum foguete para lançar
            if ((self.name == 'MOON') and (self.uranium < 35 or self.fuel < 50) and (len(self.rockets) == 0)):

                globals.acquire_print()
                print(f'🔭 - [MOON] → request LION rocket launch 🦁')
                self.print_space_base_info()
                globals.release_print()

                with globals.moon_wait:
                    globals.next_will_be_lion.acquire() # Garante que próximo foguete construído sera LION
                    globals.moon_request_lion_launch.release()  # Libera para foguete LION poder ser construído
                    globals.moon_wait.wait()  # Aguarda LION chegar com recursos

            # Se !MOON, coleta recurso das minas
            elif self.name != 'MOON':
                self.refuel_oil()
                self.refuel_uranium()

            # Verifica se base cheia de foguetes
            if len(self.rockets) < self.constraints[2]:

                # Construir lion se tem recurso e se MOON solicita
                if (self.name != 'MOON' and self.uranium >= 75 and self.fuel >= 235 and globals.moon_request_lion_launch.acquire(blocking=False)):
                    
                    # Libera para outras bases voltarem a construir foguete FALCON ou DRAGON
                    globals.next_will_be_lion.release()
                    
                    # Constrói LION
                    self.try_to_build_rocket('LION')
                
                # Se lua não necessita de lion tenta construir FALCON ou DRAGON
                if globals.next_will_be_lion.locked() == False:
                    
                    # Verifica se tem urânio suficiente para FALCON ou DRAGON 
                    if (self.uranium >= 35):
                        
                        choiced_rocket = choice(random_rockets) # Escolhe foguete RANDOMICAMENTE
                        self.try_to_build_rocket(choiced_rocket) # tenta construir foguete RANDOMICO

            # Testa se tem foguetes na base
            if (len(self.rockets) > 0):
                
                # checa se tem foguete LION armazenado
                launch_lion = False
                for x in range(len(self.rockets)):
                    if self.rockets[x].name == 'LION':
                        launch_lion = True
                        lion = self.rockets.pop(x)
                        break
                
                # Se tem foguete LION ele será o próximo a ser lançado
                if (launch_lion == True):
                    globals.acquire_print()
                    print(f'🔭 - [{self.name}] → launching LION rocket  🌍🚀🦁')
                    self.print_space_base_info()
                    globals.release_print()
                    
                    rocket = Thread(target=lion.lion_launch,name='LION') # Cria thread foguete
                    launch_lion = False # Define false sinalizando que já lançou o lion que possuía
                    rocket.start() # Starta a thread

                else:
                    choiced_to_launch = choice(self.rockets) # Escolhe foguete lançado RANDOMICAMENTE

                    # Foguete selecionado Chama função de definição de destino
                    target_planet = choiced_to_launch.planning_launch()
                    
                    # Se target_planet não estiver disponível, não realiza o lançamento
                    if target_planet == False:

                        # Se armazenamento de foguetes cheio 
                        if len(self.rockets) == self.constraints[2]:
                            with globals.stop_bases:
                                globals.stop_bases.wait()
        
                    # Realiza lançamento
                    else:
                
                        rocket_thread = Thread(target=choiced_to_launch.launch, args=(self, target_planet)) # Cria thread foguete
                        rocket_thread.start()  # Starta a thread
                        self.rockets.remove(choiced_to_launch) # Remove foguete lançado do armazenamento da base
            
            # Se true, finaliza thread
            if globals.finalize_threads == True:
                break

        globals.acquire_print()
        print(f'Thread of base {self.name} ended')
        globals.release_print()
