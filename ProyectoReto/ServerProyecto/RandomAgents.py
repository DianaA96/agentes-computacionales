from mesa import Agent, Model
from mesa.time import StagedActivation
import random
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
        self.direction = 0 #Dirección inicial del agente según Moore (hacia adelante, atrás, izq y der)
        if (self.unique_id < 200):
            self.direction = 7 
        elif (self.unique_id < 300 and self.unique_id >= 200):
            self.direction = 1 
        elif (self.unique_id < 400 and self.unique_id >= 300):
            self.direction = 3 
        elif (self.unique_id < 500  and self.unique_id >= 400):
            self.direction = 5

    # Mueve agente
    def move(self):
        # x,y=self.pos
        # Se verifica si hay vecinos cercanos que puedan chocar con el agente en las celdas vecinas
        possible_steps = self.model.grid.get_neighborhood (
            self.pos,
            moore = True,  
            include_center = True) 
        
        freeSpaces = list(map(self.model.grid.is_cell_empty, possible_steps))
        #print(possible_steps)
        #print(freeSpaces)

        if freeSpaces[self.direction]:
            print(f"Agente: {self.unique_id} se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
            self.model.grid.move_agent(self, possible_steps[self.direction])
            print(f"Agente en {self.pos[0]}")
            #print(f"Agente: {self.unique_id} movimiento {self.direction}")
        else:
            print(f"No se puede mover de {self.pos} en esa direccion.")

    # Paso de reloj implementado
    def step(self):
        # self.direction = self.direction
        #print(f"Agente: {self.unique_id} movimiento {self.direction}")
        self.move()

# Clase que instancia los semáforos como obstáculos
class Semaforo (Agent):

    # Constructor
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.statusLuz = 0 #Luz roja inicial
        self.num_semaforo = 0
        self.posicionesSemaforo = [[], []]

    # Mueve agente
    def move(self):
        #0 es luz roja, 1 es verde
        if(self.num_semaforo == 1):
            if(self.model.sem1 == 0):
                if(self.statusLuz == 0):
                    pass
                elif(self.statusLuz == 1):
                    self.model.grid.move_agent(self, self.posicionesSemaforo[self.model.sem1])
                    self.statusLuz = self.model.sem1

            elif(self.model.sem1 == 1):
                if(self.statusLuz == 0):
                    self.model.grid.move_agent(self, self.posicionesSemaforo[self.model.sem1])
                    self.statusLuz = self.model.sem1
                elif(self.statusLuz == 1):
                    pass
        
        elif(self.num_semaforo == 2):
            if(self.model.sem2 == 0):
                if(self.statusLuz == 0):
                    pass
                elif(self.statusLuz == 1):
                    self.model.grid.move_agent(self, self.posicionesSemaforo[self.model.sem2])
                    self.statusLuz = self.model.sem2

            elif(self.model.sem2 == 1):
                if(self.statusLuz == 0):
                    self.model.grid.move_agent(self, self.posicionesSemaforo[self.model.sem2])
                    self.statusLuz = self.model.sem2
                elif(self.statusLuz == 1):
                    pass

        elif(self.num_semaforo == 3):
            if(self.model.sem3 == 0):
                if(self.statusLuz == 0):
                    pass
                elif(self.statusLuz == 1):
                    self.model.grid.move_agent(self, self.posicionesSemaforo[self.model.sem3])
                    self.statusLuz = self.model.sem3

            elif(self.model.sem3 == 1):
                if(self.statusLuz == 0):
                    self.model.grid.move_agent(self, self.posicionesSemaforo[self.model.sem3])
                    self.statusLuz = self.model.sem3
                elif(self.statusLuz == 1):
                    pass

        elif(self.num_semaforo == 4):
            if(self.model.sem4 == 0):
                if(self.statusLuz == 0):
                    pass
                elif(self.statusLuz == 1):
                    self.model.grid.move_agent(self, self.posicionesSemaforo[self.model.sem4])
                    self.statusLuz = self.model.sem4

            elif(self.model.sem4 == 1):
                if(self.statusLuz == 0):
                    self.model.grid.move_agent(self, self.posicionesSemaforo[self.model.sem4])
                    self.statusLuz = self.model.sem4
                elif(self.statusLuz == 1):
                    pass
    
    # Paso de reloj implementado
    def step(self):
        self.move()


# Clase que instancia el modelo de agentes
class RandomModel(Model):

    # Constructor
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = Grid(width,height,torus = False) 
        self.schedule = BaseScheduler(self)
        self.running = True 

        #Posibilidad de aparicion en 2 carriles
        self.spawn1 = [474,479]
        self.spawn2 = [630,638]
        self.spawn3 = [417,422]
        self.spawn4 = [437,442]

        #Arreglos de semaforos (instancia los agentes)
        self.semaforo1 = []
        self.semaforo2 = []
        self.semaforo3 = []
        self.semaforo4 = []

        # Almacena en el modelo temporalmente el nuevo estatus de cada semaforo
        self.sem1 = 0
        self.sem2 = 0
        self.sem3 = 0
        self.sem4 = 0
        
        #Coordenadas donde se encuentra el limite de parada de cada semaforo
        s1Coord=[(x,y) for y in range(471,481) for x in range(393, 394) if y in [471, 481 - 1] or x in [393, 394-1]]
        s2Coord=[(x,y) for y in range(627,637) for x in range(470, 471) if y in [627, 637 - 1] or x in [470, 471-1]]
        s3Coord=[(x,y) for y in range(642, 643) for x in range(415,425) if y in [642, 643 - 1] or x in [415, 425-1]]
        s4Coord=[(x,y) for y in range(463,464) for x in range(433, 443) if y in [463,464 - 1] or x in [433, 443-1]]

        # Coordenadas a las que se moverá el semáforo cuando la luz esté en verde
        s1CoordMove=[(x,y) for y in range(482,492) for x in range(393, 394) if y in [482,492 - 1] or x in [393, 394-1]]
        s2CoordMove=[(x,y) for y in range(638,648) for x in range(470, 471) if y in [638,648 - 1] or x in [470, 471-1]]
        s3CoordMove=[(x,y) for y in range(642, 643) for x in range(426,436) if y in [642, 643 - 1] or x in [426,436-1]]
        s4CoordMove=[(x,y) for y in range(463,464) for x in range(444, 454) if y in [463,464 - 1] or x in [444, 454-1]]
        
        #Se instancian los cuatro semáforos
        self.spawnSemaforo(self.semaforo1, s1Coord, s1CoordMove, 1)
        self.spawnSemaforo(self.semaforo2, s2Coord, s2CoordMove, 2)
        self.spawnSemaforo(self.semaforo3, s3Coord, s3CoordMove, 3)
        self.spawnSemaforo(self.semaforo4, s4Coord, s4CoordMove, 4)
        
        # Agrega el agente a una posicion vacía
        for i in range(4):
            cont1 = 100
            cont2 = 200
            cont3 = 300
            cont4 = 400
            if(i == 0):
                for j in range(self.num_agents):
                    a = Automovil(cont1, self)
                    cont1+=1
                    a.direction = 7

                    pos_gen = lambda arr: (368, arr[self.random.randint(0,1)])
                    pos = pos_gen(self.spawn1)

                    while (not self.grid.is_cell_empty(pos)):
                        pos = pos_gen(self.spawn1)

                    self.schedule.add(a)
                    self.grid.place_agent(a, pos)
                
            

            elif(i == 1):
                for j in range(self.num_agents):
                    a = Automovil(cont2, self)
                    cont2+=1
                    a.direction = 1

                    pos_gen = lambda arr: (478, arr[self.random.randint(0,1)])
                    pos = pos_gen(self.spawn2)

                    while (not self.grid.is_cell_empty(pos)):
                        pos = pos_gen(self.spawn2)

                    self.schedule.add(a)
                    self.grid.place_agent(a, pos)

            

            elif(i == 2):
                for j in range(self.num_agents):
                    a = Automovil(cont3, self)
                    cont3+=1
                    a.direction = 3
                    pos_gen = lambda arr: (arr[self.random.randint(0,1)], 654)
                    pos = pos_gen(self.spawn3)

                    while (not self.grid.is_cell_empty(pos)):
                        pos = pos_gen(self.spawn3)

                    self.schedule.add(a)
                    self.grid.place_agent(a, pos)


            elif(i == 3):
                for j in range(self.num_agents):
                    a = Automovil(cont4, self)
                    cont4+=1
                    a.direction = 5

                    pos_gen = lambda arr: (arr[self.random.randint(0,1)], 460)
                    pos = pos_gen(self.spawn4)
                    
                    while (not self.grid.is_cell_empty(pos)):
                        pos = pos_gen(self.spawn4)

                    self.schedule.add(a)
                    self.grid.place_agent(a, pos)

            # for 4
            # for numDeAgentes
            # instancia el coche y le asigna su direccion, sus coordenadas iniciales y su carril
            
            # a = Automovil(i+1000, self) 

            #Cambiar posiciones de spawneo de coches

            # #Carril 1
            # if(a.direction==5):
                
            #     pos_gen = lambda arr: (20, arr[self.random.randint(0,1)])
            #     pos = pos_gen(self.spawn1)

            #     while (not self.grid.is_cell_empty(pos)):
            #         pos = pos_gen(self.spawn1)

            # #Carril 2
            # elif(a.direction==1):
            #     pos_gen = lambda arr: (970, arr[self.random.randint(0,1)])
            #     pos = pos_gen(self.spawn2)

            #     while (not self.grid.is_cell_empty(pos)):
            #         pos = pos_gen(self.spawn2)

            # #Carril 3
            # elif(a.direction==7):
            #     pos_gen = lambda arr: (arr[self.random.randint(0,1)], 786)
            #     pos = pos_gen(self.spawn3)

            #     while (not self.grid.is_cell_empty(pos)):
            #         pos = pos_gen(self.spawn3)

            # #Carril 4
            # elif(a.direction==3):
            #     pos_gen = lambda arr: (arr[self.random.randint(0,1)], 300)
            #     pos = pos_gen(self.spawn4)
                    
            #     while (not self.grid.is_cell_empty(pos)):
            #         pos = pos_gen(self.spawn4)
            
            # self.schedule.add(a)
            # self.grid.place_agent(a, pos)

            

    #Función que actualiza el estado de los semáforos
    def updateSemaforosStatus(self, numSemaforo, semaforoStatus):               
        if(numSemaforo == 1):
            self.sem1 = semaforoStatus
        elif(numSemaforo == 2):
            self.sem2 = semaforoStatus
        elif(numSemaforo == 3):
            self.sem3 = semaforoStatus
        elif(numSemaforo == 4):
            self.sem4 = semaforoStatus

    # Función que instancia los semáforos
    def spawnSemaforo(self, semaforo, coord, coordMove, num):
        iter = 0
        for pos in coord:
            obs = Semaforo(pos, self)
            obs.num_semaforo=num
            obs.posicionesSemaforo[0]=pos
            obs.posicionesSemaforo[1]=coordMove[iter]
            semaforo.append(obs)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)
            iter += 1

    def step(self):
    # Avanza el reloj del modelo un paso
        self.schedule.step()