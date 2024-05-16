# Description: this file will be a Executing file for the question 1,
# which is Executing the A-star algorithm
import networkx as nx
import matplotlib.pyplot as plt

# variables
countries = []
starting_locations = {"Blue, Washington County, UT" , "Blue, Chicot County, AR", "Red, Fairfield County, CT" }
goal_locations = {"Blue, San Diego County, CA" , "Blue, Bienville Parish, LA" ,
"Red, Rensselaer County, NY"}



# main function
def __main__():
    # read the countries from the file
    readcountries()
    # lets start the algorithm
    find_path(starting_locations, goal_locations, 1, True)
    #
    print('s')

class County:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.neighbours = []
        self.heuristic = 0
        self.cost = 0
        self.parent = None

    def addNeighbour(self, neighbour):
        if neighbour != self and neighbour not in self.neighbours:
           self.neighbours.append(countries[countries.index(neighbour)])

    def __eq__(self, other):
        return self.name == other.name and self.code == other.code

    def __str__(self):
        return self.name + ' ' + self.code

def readcountries():
    with open('adjacency.csv', 'r') as file:
        for line in file:
            firstCountyName = line.split(',')[0].split('"')[1]
            firstCountyCode = line.split(',')[1].split('"')[0].split(' ')[1]
            goalCountyName = line.split(',')[2].split('"')[1]
            goalCountyCode = line.split(',')[3].split('"')[0].split(' ')[1]
            firstcontry = County(firstCountyName, firstCountyCode)
            goalCounty = County(goalCountyName, goalCountyCode)
            if firstcontry in countries and goalCounty in countries:
                countries[countries.index(firstcontry)].addNeighbour(goalCounty)
            elif firstcontry in countries and goalCounty not in countries:
                countries.append(goalCounty)
                firstcontry.addNeighbour(goalCounty)
            elif firstcontry not in countries and goalCounty in countries:
                countries.append(firstcontry)
                firstcontry.addNeighbour(goalCounty)
            else:
                countries.append(firstcontry)
                countries.append(goalCounty)
                firstcontry.addNeighbour(goalCounty)


def heuristic(neighbour, goal_locations):
    return 1


def a_star(starting_locations, goal_locations, detail_output):
    #a star algorithm for few starting locations
    # initialize the frontier with the starting countries
    frontier = []
    explored = []
    pathes = []
    for country in starting_locations:
        frontier.append(country)
        country.cost = 0
        country.heuristic = 0
        country.parent = None
    # loop until the frontier is empty
    while frontier:
        # get the country with the lowest cost
        current_country = frontier[0]
        for country in frontier:
            if country.cost + country.heuristic < current_country.cost + current_country.heuristic:
                current_country = country
        frontier.remove(current_country)
        # check if the country is a goal country
        if current_country in goal_locations:
            # print the path to the goal country
            path = []
            while current_country:
                path.insert(0, current_country)
                current_country = current_country.parent
            if detail_output:
                print('Path found:')
                for country in path:
                    print(country.name, country.code)
            pathes.append(path)
            if len(pathes) == len(starting_locations):
                return pathes
        # add the country to the explored set
        explored.append(current_country)
        # add the neighbours of the current country to the frontier
        for neighbour in current_country.neighbours:
            if neighbour not in explored and neighbour not in frontier:
                frontier.append(neighbour)
                neighbour.cost = current_country.cost + 1
                neighbour.heuristic = heuristic(neighbour, goal_locations)
                neighbour.parent = current_country

    print('No path found')

def find_path(starting_locations, goal_locations, search_method, detail_output ):
    # split the starting locations and goal locations by the party
    starting_locations_blue = [x for x in starting_locations if x.split(',')[0].strip() == 'Blue']
    starting_locations_red = [x for x in starting_locations if x.split(',')[0].strip() == 'Red']
    goal_locations_blue = [x for x in goal_locations if x.split(',')[0].strip() == 'Blue']
    goal_locations_red = [x for x in goal_locations if x.split(',')[0].strip() == 'Red']
    #changing the locations to be in a form of country class
    #from the countries list
    for i in range(len(starting_locations_blue)):
        name = starting_locations_blue[i].split(',')[1].strip()
        code = starting_locations_blue[i].split(',')[2].strip()
        starting_locations_blue[i] = find_county(name, code)
    for i in range(len(starting_locations_red)):
        name = starting_locations_red[i].split(',')[1].strip()
        code = starting_locations_red[i].split(',')[2].strip()
        starting_locations_red[i] = find_county(name, code)
    for i in range(len(goal_locations_blue)):
        name = goal_locations_blue[i].split(',')[1].strip()
        code = goal_locations_blue[i].split(',')[2].strip()
        goal_locations_blue[i] = find_county(name, code)
    for i in range(len(goal_locations_red)):
        name = goal_locations_red[i].split(',')[1].strip()
        code = goal_locations_red[i].split(',')[2].strip()
        goal_locations_red[i] = find_county(name, code)



    # search_method = 1: A* search
    if search_method == 1:
        return a_star(starting_locations_blue, goal_locations_blue, detail_output), a_star(starting_locations_red, goal_locations_red, detail_output)

def find_county(name, code):
    for county in countries:
        if county.name == name and county.code == code:
            return county
    return None

if __name__ == "__main__":
    __main__()