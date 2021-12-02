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
        self.statusLuz = 0 #Luz roja inicial

    def move(self, new_position, new_statusLuz):
        self.model.grid.move_agent(self, new_position)
        self.statusLuz = new_statusLuz
           
    def step(self):
        self.move()

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
        
        #Se instancian los cuatro semáforos
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

        # Coordenadas a las que se moverá el semáforo cuando la luz esté en verde
        s1CoordMove=[(x,y) for y in range(482,492) for x in range(393, 394) if y in [482,492 - 1] or x in [393, 394-1]]
        s2CoordMove=[(x,y) for y in range(638,648) for x in range(465, 466) if y in [638,648 - 1] or x in [465, 466-1]]
        s3CoordMove=[(x,y) for y in range(642, 643) for x in range(426,436) if y in [642, 643 - 1] or x in [426,436-1]]
        s4CoordMove=[(x,y) for y in range(463,464) for x in range(444, 454) if y in [463,464 - 1] or x in [444, 454-1]]

        iter = 0

        #0 es luz roja, 1 es verde
        if(numSemaforo == 1):
            if(semaforoStatus is 0):
                for agenteSemaforo in self.semaforo1:
                    if(agenteSemaforo.statusLuz is 0):
                        pass
                    elif(self.semaforo1.statusLuz is 1):
                        agenteSemaforo.move(s1CoordMove[iter], semaforoStatus)
                        iter += 1
                iter = 0

            elif(semaforoStatus is 1):
                for agenteSemaforo in self.semaforo1:
                    if(agenteSemaforo.statusLuz is 0):
                        agenteSemaforo.move(s1CoordMove[iter], semaforoStatus)
                        iter += 1
                    elif(self.semaforo1.statusLuz is 1):
                        pass
                iter = 0
        
        if(numSemaforo == 2):
            if(semaforoStatus is 0):
                for agenteSemaforo in self.semaforo2:
                    if(agenteSemaforo.statusLuz is 0):
                        pass
                    elif(self.semaforo2.statusLuz is 1):
                        agenteSemaforo.move(s2CoordMove[iter], semaforoStatus)
                        iter += 1
                iter = 0

            elif(semaforoStatus is 1):
                for agenteSemaforo in self.semaforo2:
                    if(agenteSemaforo.statusLuz is 0):
                        agenteSemaforo.move(s2CoordMove[iter], semaforoStatus)
                        iter += 1
                    elif(self.semaforo2.statusLuz is 1):
                        pass
                iter = 0
        
        if(numSemaforo == 3):
            if(semaforoStatus is 0):
                for agenteSemaforo in self.semaforo3:
                    if(agenteSemaforo.statusLuz is 0):
                        pass
                    elif(self.semaforo3.statusLuz is 1):
                        agenteSemaforo.move(s3CoordMove[iter], semaforoStatus)
                        iter += 1
                iter = 0

            elif(semaforoStatus is 1):
                for agenteSemaforo in self.semaforo3:
                    if(agenteSemaforo.statusLuz is 0):
                        agenteSemaforo.move(s3CoordMove[iter], semaforoStatus)
                        iter += 1
                    elif(self.semaforo3.statusLuz is 1):
                        pass
                iter = 0
        
        if(numSemaforo == 4):
            if(semaforoStatus is 0):
                for agenteSemaforo in self.semaforo4:
                    if(agenteSemaforo.statusLuz is 0):
                        pass
                    elif(self.semaforo4.statusLuz is 1):
                        agenteSemaforo.move(s4CoordMove[iter], semaforoStatus)
                        iter += 1
                iter = 0

            elif(semaforoStatus is 1):
                for agenteSemaforo in self.semaforo4:
                    if(agenteSemaforo.statusLuz is 0):
                        agenteSemaforo.move(s4CoordMove[iter], semaforoStatus)
                        iter += 1
                    elif(self.semaforo4.statusLuz is 1):
                        pass
                iter = 0                 

        self.schedule.step()

    def spawnSemaforo(self, semaforo, coord, num):
        for pos in coord:
            obs = Semaforo(pos, self)
            semaforo.append(obs)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

    def step(self):
        '''Advance the model by one step.'''
        self.schedule.step()