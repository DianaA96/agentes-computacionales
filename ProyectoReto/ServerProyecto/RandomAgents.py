from mesa import Agent, Model
#from mesa.time import StagedActivation
from mesa.time import BaseScheduler
from mesa.space import Grid
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
# Clase que instancia los coches
class Automovil(Agent):

    # Constructor
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direction = 1 #Dirección inicial del agente según Moore (hacia adelante)

    # Mueve agente
    def move(self):
        # Se verifica si hay vecinos cercanos que puedan chocar con el agente en las celdas vecinas
        possible_steps = self.model.grid.get_neighborhood (
            self.pos,
            moore = True, 
            include_center = True) 
        
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))

        if freeSpaces[self.direction]:
            self.model.grid.move_agent(self, possible_steps[self.direction])
            print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        else:
            print(f"No se puede mover de {self.pos} en esa direccion.")

    def step(self):
        self.direction = 1
        print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()


# Clase que instancia los semáforos como obstaculos
class Semaforo (Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.signal = 0
           
    def step(self):
        # if (signal is 1):
        #     pass
        # if (signal is 2):
        pass

# Clase que instancia el modelo de agentes
class RandomModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = Grid(width,height,torus = False) 
        self.schedule = BaseScheduler(self)
        self.running = True 

        #Posibilidad de aparicion en 2 carriles
        self.spawn1 = [631,636]

        self.semaforo1 = []
        self.semaforo2 = []
        self.semaforo3 = []
        self.semaforo4 = []
        
        #Coordenadas donde se encuentra el limite de parada de cada semaforo
        s1Coord=[(x,y) for y in range(471,481) for x in range(393, 394) if y in [471, 481 - 1] or x in [393, 394-1]]
        s2Coord=[(x,y) for y in range(627,637) for x in range(465, 466) if y in [627, 637 - 1] or x in [465, 466-1]]
        s3Coord=[(x,y) for y in range(642, 643) for x in range(415,425) if y in [642, 643 - 1] or x in [415, 425-1]]
        s4Coord=[(x,y) for y in range(463,464) for x in range(433, 443) if y in [463,464 - 1] or x in [433, 443-1]]
        
        self.spawnSemaforo(self.semaforo1, s1Coord,1)
        self.spawnSemaforo(self.semaforo2, s2Coord,2)
        self.spawnSemaforo(self.semaforo3, s3Coord,3)
        self.spawnSemaforo(self.semaforo4, s4Coord,4)
        
        # Agrega el agente a una posicion vacía
        for i in range(self.num_agents):
            a = Automovil(i+1000, self) 
            self.schedule.add(a)

            #Cambiar posiciones de spawneo de coches
            pos_gen = lambda arr: (970, arr[self.random.randint(0,1)])
            pos = pos_gen(self.spawn1)
            while (not self.grid.is_cell_empty(pos)):
                pos = pos_gen(self.spawn1)
            self.grid.place_agent(a, pos)
            for i in range(self.random.randint(0,10)):
                self.step()

    #Funcion que actualiza el estado de los semaforos
    def updateSemaforosStatus(self, numSemaforo, semaforoStatus):

        # Es necesario verificar cuál es la posición del semáforo para determinar si lo vamos a mover o no
        

        if(semaforosStatus == 2):
            print(bcolors.OKGREEN + "Cambio a estatus 1" + bcolors.ENDC)
            self.greenlight(self.semaforo1)
            self.greenlight(self.semaforo2)
            self.spawnSemaforo(self.semaforo3, s3Coord,3)
            self.spawnSemaforo(self.semaforo4, s4Coord,4)
            
        elif(semaforosStatus == 1):
            print(bcolors.OKGREEN + "Cambio a estatus 2" + bcolors.ENDC)
            self.greenlight(self.semaforo3)
            self.greenlight(self.semaforo4)
            self.spawnSemaforo(self.semaforo1, s1Coord,1)
            self.spawnSemaforo(self.semaforo2, s2Coord,2)
            
        else:
            print(bcolors.FAIL + "No hay estatus" + bcolors.ENDC)

        self.schedule.step()

    # def greenlight(self, semaforo):
    #     print(bcolors.OKGREEN + "Quitando semaforo" + bcolors.ENDC)
    #     for j in semaforo:
    #         self.grid.remove_agent(j)

    def spawnSemaforo(self, semaforo, coord, num):
        for pos in coord:
            obs = Semaforo( , self)
            semaforo.append(obs)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)
        print(bcolors.WARNING + f"Semaforo {num} creado" + bcolors.ENDC)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()

