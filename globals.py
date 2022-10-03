# from multiprocessing import Semaphore
from pickle import FALSE
from threading import Lock, Condition, Semaphore

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las.
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.

release_system = False
mutex_print = Lock()
planets = {}
bases = {}
mines = {}
simulation_time = None

finalize_threads = False # Variável para finalizar threads quando todos planetas forem terraformados

# Sincronização de pedidos da lua
moon_request_lion_launch = Semaphore(0) # Lua da release para solicitar foguete lion
moon_wait = Condition()  # Lua aguarda recursos
next_will_be_lion = Lock()  # Lua da lock para garantir que LION será construido



# * Sincronização para as viagens

''' ### Semáforos "voyage_to_nomedoplaneta" definem quantos lançamentos podem ser feitos para o planeta em questão
    ### Semáforos "voyage_to_nomedoplaneta" também definem quantos foguetes ficam orbitando o planeta
    ### Semáforos "voyage_to_nomedoplaneta" servem para não ter threads demais no SO
    ### Semáforos collision_course_nomedoplaneta definem dois foguetes em rota de colisão com o planete por vez
    ### Locks "nomedoplaneta_north_pole" lockam a colisão com o polo norte do planeta
    ### Locks "nomedoplaneta_north_pole" satisfazem a regra de 2 foguetes não baterem no mesmo polo simultâneamente'''

N = 10 # Quantos foguetes podem estar em rota para um planeta e orbitando o mesmo ## Limitador de threads do SO ##

voyage_to_mars = Semaphore(N) 
colision_course_mars = Semaphore(2)  
mars_north_pole = Lock()  

voyage_to_io = Semaphore(N)  
colision_course_io = Semaphore(2)  
io_north_pole = Lock()  

voyage_to_ganimedes = Semaphore(N)
colision_course_ganimedes = Semaphore(2)  
ganimedes_north_pole = Lock()

voyage_to_europa = Semaphore(N)  
colision_course_europa = Semaphore(2)
europa_north_pole = Lock()

''' Caso as bases não possam mais lançar foguetes para nenhum planeta e nem construí-los, 
travam nesse condition, impedindo busywating'''
stop_bases = Condition()


# * Sincronização de planetas

''' ### Conditions "explosion_nomedoplaneta" não deixa os planetas ficarem em busywaiting
    ### Seram noticadas quando uma nuke explodir no planeta'''
    
explosion_mars = Condition()
explosion_io = Condition()
explosion_ganimedes = Condition()
explosion_europa = Condition()

''' ### Como descrito no enunciado, a inabitabilidade, fornecida pelo satelite, só pode ser verificada por uma base de cada vez
    ### Locks "nomedoplaneta_satellite" satisfazem a regra de uma thread verificar o satelite do planeta por vez'''
    
mars_satellite = Lock()
io_satellite = Lock()
ganimedes_satellite = Lock()
europa_satellite = Lock()

'''### Colocado semaforos e locks em dicionários para acesso a partida planet.name
   ### Não colocamos os semaforos e locks no construtor da classe pois era proibido modificação do construtor'''
 
colision_course = {
    'MARS': colision_course_mars,
    'IO': colision_course_io,
    'GANIMEDES': colision_course_ganimedes,
    'EUROPA': colision_course_europa
}
pole = {
    'MARS': mars_north_pole,
    'IO': io_north_pole,
    'GANIMEDES': ganimedes_north_pole,
    'EUROPA': europa_north_pole
}

nuclear_event_condition = {
    'MARS': explosion_mars,
    'IO': explosion_io,
    'GANIMEDES': explosion_ganimedes,
    'EUROPA': explosion_europa
}

satellite_lock = {
    'MARS': mars_satellite,
    'IO': io_satellite,
    'GANIMEDES': ganimedes_satellite,
    'EUROPA': europa_satellite
}

voyage_to = {
    'MARS': voyage_to_mars,
    'IO': voyage_to_io,
    'GANIMEDES': voyage_to_ganimedes,
    'EUROPA': voyage_to_europa
}


# * Sincronização das minas

''' ### Locks "nomedamina_units" protegem o acesso a região crítica da variável mina.units
    ### Semáforos available_mina definem que uma porção de recurso pode ser pego por uma das bases'''

pipeline_units = Lock()
available_oil = Semaphore(0)

store_house_units = Lock()
available_uranium = Semaphore(0)


def acquire_print():
    global mutex_print
    mutex_print.acquire()


def release_print():
    global mutex_print
    mutex_print.release()


def set_planets_ref(all_planets):
    global planets
    planets = all_planets


def get_planets_ref():
    global planets
    return planets


def set_bases_ref(all_bases):
    global bases
    bases = all_bases


def get_bases_ref():
    global bases
    return bases


def set_mines_ref(all_mines):
    global mines
    mines = all_mines


def get_mines_ref():
    global mines
    return mines


def set_release_system():
    global release_system
    release_system = True


def get_release_system():
    global release_system
    return release_system


def set_simulation_time(time):
    global simulation_time
    simulation_time = time


def get_simulation_time():
    global simulation_time
    return simulation_time


