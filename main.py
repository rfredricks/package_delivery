# Rebecca Fredricks Student ID # 000554612
from truck import Truck
from graph import Graph
from hashTable import ChainingHashTable
from datetime import datetime
import csv

# instances of hash table, truck, and graph class
tbl = ChainingHashTable()
truck_1 = Truck(1, 0.0, '08:00:00')
truck_2 = Truck(2, 0.0, '08:00:00')
truck_3 = Truck(3, 0.0, '09:50:00')
area_map = Graph()


# read data from distances file into graph instance
def get_map_data():
    with open('venv/distances.csv', mode='r') as csv_file_0:
        csv_reader = csv.reader(csv_file_0)
        labels = next(csv_reader)
        del(labels[0])
        for row in csv_reader:
            start = row[0]
            area_map.add_vertex(start)
            for i in range(len(labels)):
                end = labels[i]
                area_map.add_directed_edge(start, end, float(row[i+1]))


# read data from packages file into hash table and truck instances
def get_package_data():
    with open('venv/packages_2.csv', mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            pkgid = int(row[0])
            addr = str.strip((row[1]))
            pkgcity = str(row[2])
            pkgstate = str(row[3])
            pkgzip = int(row[4])
            delby = datetime.strptime(row[5], '%H:%M:%S')
            pkgwt = float(row[6])
            notes = str(row[7])
            trk = int(row[8])
            pkg = [pkgid, addr, pkgcity, pkgstate, pkgzip, delby, pkgwt, notes, '', '']
            tbl.insert(pkg)  # insert into hash table
            if trk == 1:
                truck_1.load(pkg)  # load trucks
            elif trk == 2:
                truck_2.load(pkg)
            else:
                truck_3.load(pkg)


# given a list of nodes and edge distances, find nearest neighbor node to current node.
# time complexity: O(n) space complexity: O(n)
def nearest_neighbor(start, package_list):
    minim = float(999.9)  # initialize minimum to a value larger than the largest distance contained in graph
    next_node = start
    for package in package_list:
        current = area_map.edge_weights.get((start, package[1]))
        if current <= minim:
            minim = current
            next_node = package[0]
    return next_node


# display a user menu and read user input
# options: get status of all packages at given time; lookup a package by id; get total miles traveled; exit
def user_menu():
    print('Make a selection:')
    menu_option = (str(input('T: all packages\tL: lookup package\tM: total miles\tX: exit ')))
    if menu_option == 'T':
        time_at = (datetime.strptime(input('Enter time as HH:MM:SS: '), '%H:%M:%S'))
        get_status(time_at)
        exit(0)
    elif menu_option == 'L':
        print_package(tbl.search(int(input('Enter package id: '))))
        user_menu()
    elif menu_option == 'M':
        print('Total miles traveled: {}'.format(total_miles))
        user_menu()
    elif menu_option == 'X':
        exit(0)
    else:
        print('Make a valid selection')
        user_menu()


# print selected package data - id, address, city, zip code, deadline, weight, and delivery status.
def print_package(package):
    package_string = 'ID: {}\tDelivery address, city, zip code: '.format(package[0])
    package_string += (package[1] + ', ' + package[2] + ', {}'.format(package[4]))
    package_string += (' Deadline: ' + package[5].strftime('%H:%M:%S') + ' Package weight: ')
    package_string += ('{} Delivery status: ' + package[8]).format(package[6])
    print(package_string)


# get status of package at given time. time complexity: O(n) space complexity: O(1)
def get_status(at_time):
    for i in range(1, 41):  # iterate over table
        _curr = tbl.search(i)
        del_time = datetime.strptime(_curr[8][-8:], '%H:%M:%S')
        if del_time <= at_time:
            print_package(_curr)
        elif _curr[9] == '':
            _curr[8] = 'En route'
            print_package(_curr)
        else:
            load_time = _curr[9]
            if at_time >= load_time:
                _curr[8] = 'En route'
                print_package(_curr)
            else:
                _curr[8] = 'At the hub'
                print_package(_curr)


# load package and map data
get_package_data()

get_map_data()

global last_del
origin1 = '4001 South 700 East'
# deliver truck 1 packages using nearest neighbor. time complexity: O(n^2) space complexity: O(n)
while truck_1.packages:
    next_del = tbl.search(nearest_neighbor(origin1, truck_1.packages))
    last_del = next_del[1]
    truck_1.update_mileage(area_map.edge_weights.get((origin1, next_del[1])))
    _temp = truck_1.deliver(next_del)
    tbl.replace(_temp[0], _temp)
    origin1 = next_del[1]

# truck 3 leaves the hub when truck 1 gets back to the hub.
truck_1.update_mileage(area_map.edge_weights.get((last_del, '4001 South 700 East')))
truck_3.curr_time = truck_1.curr_time

origin2 = '4001 South 700 East'
# deliver truck 2 packages using nearest neighbor. time complexity: O(n^2) space complexity: O(n)
while truck_2.packages:
    next_del = tbl.search(nearest_neighbor(origin2, truck_2.packages))
    truck_2.update_mileage(area_map.edge_weights.get((origin2, next_del[1])))
    _temp = truck_2.deliver(next_del)
    tbl.replace(_temp[0], _temp)
    origin2 = next_del[1]

# truck 3 packages have a loading time due to the truck leaving later than 8 AM
for item in truck_3.packages:
    item[9] = truck_3.curr_time
    tbl.replace(item[0], item)

origin3 = '4001 South 700 East'
# deliver truck 3 packages using nearest neighbor. time complexity: O(n^2) space complexity: O(n)
while truck_3.packages:
    next_del = tbl.search(nearest_neighbor(origin3, truck_3.packages))
    truck_3.update_mileage(area_map.edge_weights.get((origin3, next_del[1])))
    _temp = truck_3.deliver(next_del)
    tbl.replace(_temp[0], _temp)
    origin3 = next_del[1]

# print truck mileage and timestamps
strformat = "{0:.1f}"
total_miles = float(truck_1.mileage + truck_2.mileage + truck_3.mileage)
print('Truck 1 mileage ' + strformat.format(truck_1.mileage))
print('Truck 1 finish time ' + truck_1.curr_time.strftime('%H:%M:%S'))
print('Truck 2 mileage ' + strformat.format(truck_2.mileage))
print('Truck 2 finish time ' + truck_2.curr_time.strftime('%H:%M:%S'))
print('Truck 3 mileage ' + strformat.format(truck_3.mileage))
print('Truck 3 finish time ' + truck_3.curr_time.strftime('%H:%M:%S'))
print('Total truck mileage ' + strformat.format(total_miles))

# display user menu
user_menu()
