# Description: this file will be a Executing file for the question 1,
# which is Executing the A-star algorithm

# variables
frontier = []
explored = []
counties = []

# main function
def __main__():
    readcounties()


class County:
    #getting "Blount County, AL" as input (name and code)
    #and need to get Blount County and AL as output
    def __init__(self, txt:str):
        self.name = txt.split(',')[0]
        self.code = txt.split(',')[1].strip()
        self.neighbours = []
        self.heuristic = 0
        self.cost = 0
        self.parent = None


#In order to know which counties are adjacent, you can use the file adjacency.csv downloadable from the course website. Each line contains a pair of adjacent counties (be careful, the file includes each county as adjacent to itself!).
#looks like "Blount County, AL","Jefferson County, AL"
#and we need to get from it "Blount County, AL" and "Jefferson County, AL"
def readcounties():
    with open('/Users/omera/PycharmProjects/AI/adjacency.csv', 'r') as file:
        for line in file:
            firstcounty = line.strip('"')
            goalcounty = line[1].strip('"')
            print(firstcounty)
            print(goalcounty)

