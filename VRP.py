# using Or tool by google to find the shorthest parth that can be taken by the user
##Documents\PythonPrograming\Package_Problem\Practice\Routing
from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from haversine import haversine, Unit
import pandas as pd
import numpy as np 
import time 




data=pd.read_csv("data_2.csv")
def func(string):
         val = string.split(',')
         lat = val[0][1:]
         lng = val[1][0:-1]
         return lat, lng
data['lat'] = data.apply(lambda x: func(x['location'])[0], axis=1)  
data['lng'] = data.apply(lambda x: func(x['location'])[1], axis=1)
data.to_csv("data_3.csv")   
lat_data=data.filter(['lat'])
long_data=data.filter(['lng'])
lat_data=lat_data.values
long_data=long_data.values
def create_data_model():

    data = {}
    data['distance_matrix']=np.zeros((len(lat_data),len(long_data)))
       
    for i in range(len(lat_data)):
        for j in range(len(lat_data)):
            geocode1=[lat_data[i],long_data[i]]
            geocode2=[lat_data[j],long_data[j]]
            data['distance_matrix'][i][j]=1000*haversine(geocode1,geocode2)
    data['num_vehicles'] =8
    data['depot'] = 10
    data['demands'] = [10, 1, 1, 2, 4, 2, 4, 8, 8, 2, 0, 1, 2, 4, 4, 8, 8, 2, 5, 6, 7, 3, 1, 5 ,7]
    data['vehicle_capacities'] = [25, 25, 25, 25, 25, 25, 25, 25]
    return data


def print_solution(data, manager, routing, assignment):
    total_distance = 0
    total_load = 0
    a=[]
    dropped_nodes = 'Dropped nodes:'
    for node in range(routing.Size()):
        if routing.IsStart(node) or routing.IsEnd(node):
            continue
        if assignment.Value(routing.NextVar(node)) == node:
            dropped_nodes += ' {}'.format(manager.IndexToNode(node))
    print(dropped_nodes)
    for vehicle_id in range(data['num_vehicles']):
        a.append([])
        index = routing.Start(vehicle_id)   
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            a[vehicle_id].append(node_index)
            previous_index = index
            index = assignment.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(    
            manager.IndexToNode(index), route_load)  
        a[vehicle_id].append(manager.IndexToNode(index))    
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))
    return a



def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()
    print(len(data['distance_matrix']), data['num_vehicles'], data['depot'], 5*"=")
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
       
    index = manager.NodeToIndex(7)
    routing.VehicleVar(index).SetValues([-1, 2,3,4])

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    start_time=time.time()
    solution = routing.SolveWithParameters(search_parameters)
    end_time=time.time()
    print(end_time-start_time)
    # Print solution on console.
    if solution:
        result=print_solution(data, manager, routing, solution)
    return result,data['num_vehicles']

  