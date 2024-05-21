# Description: this file will be a Executing file for the question 1,
# which is Executing the A-star algorithm
import requests

# variables
countries = []
starting_locations = {"Blue, Washington County, UT", "Blue, Chicot County, AR", "Red, Fairfield County, CT"}
goal_locations = {"Blue, San Diego County, CA", "Blue, Bienville Parish, LA",
                  "Red, Rensselaer County, NY"}


# main function
def __main__():
    # read the countries from the file
    readcountries()
    # lets start the algorithm
    find_path(starting_locations, goal_locations, 1, True)


class County:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.neighbours = []
        self.heuristic = 0
        self.cost = 0
        self.parent = None
        self.lat = 0
        self.lon = 0

    def addNeighbour(self, neighbour):
        if neighbour != self and neighbour not in self.neighbours:
            self.neighbours.append(countries[countries.index(neighbour)])

    def __eq__(self, other):
        return self.name == other.name and self.code == other.code

    def __str__(self):
        return self.name + ' ' + self.code

    def setCordinate(self, lat, lon):
        self.lat = lat
        self.lon = lon


def setCordinateForCountries():
    headers = {
        'User-Agent': 'Omer Ai 1.0',
        'From': 'omeramst@post.bgu.ac.il'
    }
    for country in countries:
        # check if the country already have cordinate in the csv file
        with open('countriesLatLan.csv', 'r') as read_file:
            for line in read_file:
                if country.name in line and country.code in line:
                    country.setCordinate(float(line.split(',')[2]), float(line.split(',')[3]))
                    break
            else:
                # if the country doesn't have cordinate in the csv file
                url = f"https://nominatim.openstreetmap.org/search?q={country.name}%20{country.code}&format=json"
                try:
                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        if data:
                            country.setCordinate(float(data[0]['lat']), float(data[0]['lon']))
                            with open('countriesLatLan.csv', 'a') as file:
                                file.write(country.name + ',' + country.code + ',' + str(country.lat) + ',' + str(
                                    country.lon) + '\n')
                except:
                    pass


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
                countries[countries.index(firstcontry)].addNeighbour(goalCounty)
            elif firstcontry not in countries and goalCounty in countries:
                countries.append(firstcontry)
                countries[countries.index(firstcontry)].addNeighbour(goalCounty)
            else:
                countries.append(firstcontry)
                countries.append(goalCounty)
                countries[countries.index(firstcontry)].addNeighbour(goalCounty)
    setCordinateForCountries()


def heuristic(neighbour, goal_locations):
    # return the heuristic value for the neighbour
    # the heuristic value is the distance between the neighbour and the closest goal location
    min_distance = 100000000000000000000000
    for goal in goal_locations:
        # calculate the distance between the neighbour and the goal location using the euclidean distance
        distance = ((neighbour.lat - goal.lat) ** 2 + (neighbour.lon - goal.lon) ** 2) ** 0.5
        if distance < min_distance:
            min_distance = distance
    return min_distance


# return the heuristic value for the neighbour
# the heuristic value is the distance between the neighbour and the closest goal location


def a_star(starting_locations, goal_locations, detail_output):
    # a star algorithm for few starting locations
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

        # add the country to the explored set
        explored.append(current_country)
        # add the neighbours of the current country to the frontier
        for neighbour in current_country.neighbours:
            if neighbour not in explored and neighbour not in frontier:
                frontier.append(neighbour)
                neighbour.cost = current_country.cost + 1
                neighbour.heuristic = heuristic(neighbour, goal_locations)
                neighbour.parent = current_country

        if current_country in goal_locations:
            # print the path to the goal country
            path = []
            while current_country:
                path.insert(0, current_country)
                current_country = current_country.parent
            pathes.append(path)
            if len(pathes) == len(starting_locations):
                return pathes
    # if the frontier is empty, then at list one path wasn't found
    return pathes


def find_path(starting_locations, goal_locations, search_method, detail_output):
    # split the starting locations and goal locations by the party
    starting_locations_blue = [x for x in starting_locations if x.split(',')[0].strip() == 'Blue']
    starting_locations_red = [x for x in starting_locations if x.split(',')[0].strip() == 'Red']
    goal_locations_blue = [x for x in goal_locations if x.split(',')[0].strip() == 'Blue']
    goal_locations_red = [x for x in goal_locations if x.split(',')[0].strip() == 'Red']
    # changing the locations to be in a form of country class
    # from the countries list
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
        bluePaths = a_star(starting_locations_blue, goal_locations_blue, detail_output)
        redPaths = a_star(starting_locations_red, goal_locations_red, detail_output)
        pathsPrints(bluePaths, redPaths, detail_output)


def pathsPrints(bluePaths, redPaths, detail_output):
    # Get the maximum length of the paths
    max_len_bluePaths = max(len(path) for path in bluePaths)
    max_len_redPaths = max(len(path) for path in redPaths)
    max_length = max(max_len_bluePaths, max_len_redPaths)

    if not detail_output:
        # Print the paths
        for i in range(max_length):
            # Initialize the string for the paths
            PathStr = "{"

            # Add the counties to the string
            for path in bluePaths:
                if i < len(path):
                    PathStr += path[i].name + ", " + path[i].code + " (B) ; "
                else:
                    PathStr += path[-1].name + ", " + path[-1].code + " (B) ; "
            for path in redPaths:
                if i < len(path):
                    PathStr += path[i].name + ", " + path[i].code + " (R) ; "
                else:
                    PathStr += path[-1].name + ", " + path[-1].code + " (R) ; "

            # Remove the last semicolon and space from the string
            PathStr = PathStr[:-3] + "}"

            # Print the string
            print(PathStr)
    else:
        # Initialize the string for the paths
        PathStr = "{"
        HeuristicStr = "{"
        #add the heuristic values to the string
        for path in bluePaths:
            HeuristicStr += str(path[1].heuristic) + " ; "
        for path in redPaths:
            HeuristicStr += str(path[1].heuristic) + " ; "


        # Print the paths
        for i in range(max_length):
            # Initialize the string for the paths
            PathStr = "{"

            # Add the counties to the string
            for path in bluePaths:
                if i < len(path):
                    PathStr += path[i].name + ", " + path[i].code + " (B) ; "
                else:
                    PathStr += path[-1].name + ", " + path[-1].code + " (B) ; "
            for path in redPaths:
                if i < len(path):
                    PathStr += path[i].name + ", " + path[i].code + " (R) ; "
                else:
                    PathStr += path[-1].name + ", " + path[-1].code + " (R) ; "


            # Remove the last semicolon and space from the strings
            PathStr = PathStr[:-3] + "}"
            HeuristicStr = HeuristicStr[:-3] + "}"

            # Print the strings
            print(PathStr)
            if detail_output and i == 1:
                print("Heuristic: " + HeuristicStr)


def find_county(name, code):
    for county in countries:
        if county.name == name and county.code == code:
            return county
    return None


if __name__ == "__main__":
    __main__()
