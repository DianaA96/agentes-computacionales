from flask import Flask, request, jsonify
from RandomAgents import *

# Size of the board:
number_agents = 10
width = 28
height = 28
trafficModel = None
currentStep = 0

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, trafficModel, number_agents, width, height

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        currentStep = 0

        print(request.form)
        print(number_agents, width, height)
        trafficModel = RandomModel(number_agents, width, height)

        return jsonify({"message":"Parameters received, model initiated."})

@app.route('/updateLights', methods=['POST', 'GET'])
def updateLights():
    print(bcolors.WARNING + "Endpoint call" + bcolors.ENDC)
    global currentStep, trafficModel
    if request.method == 'POST':
        status = int(request.form.get('status'))
        num = int(request.form.get('num'))
        trafficModel.updateSemaforosStatus(num, status)
        trafficModel.step()
        return jsonify({"message":"Estatus de semaforo actualizado."})

@app.route('/getObstacles', methods = ['GET'])
def getObstacles():
    global trafficModel

    if request.method == 'GET':
        carPositions = [{"x": x, "y":1, "z":z} for (a, x, z) in trafficModel.grid.coord_iter() if isinstance(a, Semaforo)]

        return jsonify({'positions':carPositions})

@app.route('/getAgents', methods = ['GET'])
def getAgents():
    global trafficModel
    if request.method == 'GET':
        # direccion = 0
        # carPositions = [{"x": x, "y":50, "z":z, "dir":a.direction} for (a, x, z) in trafficModel.grid.coord_iter() if isinstance(a, Automovil)]
        for(a, x, z) in trafficModel.grid.coord_iter():
            if isinstance(a, Automovil):
                carPositions = [{"x": x, "y":50, "z":z}]
                carDirection = [{"dir": a.direction}]

        return jsonify({'positions':carPositions, 'direccion':carDirection})

@app.route('/update', methods = ['GET'])
def updateModel():
    global currentStep, trafficModel
    if request.method == 'GET':
        trafficModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)