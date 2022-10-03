from random import randrange, random
from time import sleep
from threading import Thread, current_thread, Semaphore
import globals


class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0

    def orbit(self, planet):
        '''Seguindo a informação do satélite, se o planeta for inabitável permite a rota de colisão.
        Caso contrário, a thread foguete chega ao seu fim após printar'''
        
        # Satisfaz a regra que apenas 2 foguetes por vez podem colidir com o planeta
        globals.colision_course.get(planet.name).acquire() 

        # Satisfaz a regra de verificar planet.terraform com a limitação da tecnologia
        if planet.satellite_get_info() > 0:  # Se não está habitável
            self.nuke(planet) # bombardeia o planeta
        
        # Se planeta for habitável, foguete não colide com o planeta
        else:
            globals.acquire_print()
            print(f"✨ - {self.name} ROCKET / ID {self.id}, is indefinitely orbiting {planet.name}.")
            globals.release_print()

    def nuke(self, planet):  # Permitida a alteração
        '''# BOOM!!! 🎇'''

        # Satisfaz a regra de não haver colisão simultânea no mesmo polo
        if globals.pole.get(planet.name).acquire(blocking=False):

            globals.acquire_print()
            print(f"🎇 - [EXPLOSION] - The {self.name} ROCKET / ID {self.id}, reached the planet {planet.name} on North Pole!")
            globals.release_print()
            
            planet.planet_takes_damage(self.damage())   # Dano da explosão
            globals.pole.get(planet.name).release()

        else:
            globals.acquire_print()
            print(f"🎇 - [EXPLOSION] - The {self.name} ROCKET / ID {self.id}, reached the planet {planet.name} on South Pole!")
            globals.release_print()
            planet.planet_takes_damage(self.damage())   # Dano da explosão

        # Notifica o condition que impede busy waiting nos planetas
        with globals.nuclear_event_condition.get(planet.name):
            globals.nuclear_event_condition.get(planet.name).notify()

        # colidiu, libera para uma nova colisão
        globals.colision_course.get(planet.name).release()
        # colidiu, libera para um novo lançamento
        globals.voyage_to.get(planet.name).release()
        
        # Notifica o condition que impede busy waiting nas bases
        with globals.stop_bases:
            globals.stop_bases.notify_all()

    def voyage(self, planet):  # Permitida a alteração (com ressalvas)

        # Essa chamada de código (do_we_have_a_problem e simulation_time_voyage) não pode ser retirada.
        # Você pode inserir código antes ou depois dela e deve
        # usar essa função.

        self.simulation_time_voyage(planet)     # Rocket está viajando
        failure = self.do_we_have_a_problem()   # Testa falha
        
        # Foguete entra em órbita do Planeta
        if failure == False:                    # Se não ouve uma falha
            self.orbit(planet)                  # entra em órbita
        
        # Libera para novo lançamento caso o foguete falhe
        else:
            # Impede busywaiting nas bases
            #TODO verificar dps, rever porque é notify all
            with globals.stop_bases:
                globals.stop_bases.notify_all() 
            globals.voyage_to.get(planet.name).release()
            

    def planning_launch(self):
        '''Retorna o planeta que o foguete deve viajar, retorna falso se nenhum estiver disponível'''
        
        # Dicionario com semaforos que contam 100 lançamentos para um planeta simultaneamente
        to_define_destiny_dict = globals.voyage_to 
        
        # Semáforos de valor N
        # Se > 0, decrementa, mas não bloqueia
        
        if to_define_destiny_dict.get('IO').acquire(blocking=False): 
            planet = globals.get_planets_ref().get('io')
            return planet

        elif to_define_destiny_dict.get('GANIMEDES').acquire(blocking=False): 
            planet = globals.get_planets_ref().get('ganimedes')
            return planet

        elif to_define_destiny_dict.get('EUROPA').acquire(blocking=False): 
            planet = globals.get_planets_ref().get('europa')
            return planet

        elif to_define_destiny_dict.get('MARS').acquire(blocking=False): 
            planet = globals.get_planets_ref().get('mars')
            return planet
        
        else:
            return False

    def lion_launch(self):
        
        '''Lançamento de lion'''
        
        sleep(0.01)  # Quatro dias para o foguete LION chegar na lua
        lua = globals.get_bases_ref().get('moon')

        lua.fuel += self.fuel_cargo  # Recarrega combustível da lua
        lua.uranium += self.uranium_cargo  # Recarrega urânio da lua

        globals.acquire_print()
        print(f"🦁 - [LION] - Arrived in MOON 🌑 base - refueling ⛽ {self.fuel_cargo} ☢ { self.uranium_cargo}")
        globals.release_print()

        with globals.moon_wait:
            globals.moon_wait.notify()  # Da notify para base da lua voltar a trabalhar

        ####################################################
        #                   ATENÇÃO                        #
        #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
        ####################################################

    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            # Marte tem uma distância aproximada de dois anos do planeta Terra.
            sleep(2)
        else:
            # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.
            sleep(5)

    def do_we_have_a_problem(self):
        if(random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False

    def general_failure(self):
        print(f"[GENERAL FAILURE] - {self.name} ROCKET, ID: {self.id}")

    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET, ID: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(
                f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True

    def damage(self):
        return random()

    def launch(self, base, planet):
        '''recebe objeto base e objeto planet'''
        if(self.successfull_launch(base)):
            print(f"🚀 - [{self.name} - {self.id}] launched from [{base.name}].")
            self.voyage(planet)
        
        # caso falhe o lançamento
        else:
            # Da notify para as bases que estão aguardando em stop_bases.wait()
            with globals.stop_bases:
                globals.stop_bases.notify()
            # Da release para liberar novo lançamento para o planeta associado
            globals.voyage_to.get(planet.name).release()
            
