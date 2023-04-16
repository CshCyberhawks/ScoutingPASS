import pandas as pd

data = pd.read_excel('data.xlsx', sheet_name="Match Scouting Data")

dictionaryOfData = {}

for num in data['teamNumber']:
    if num not in dictionaryOfData:
        dictionaryOfData[num] = [data[data['teamNumber'] == num]]
    else:
        dictionaryOfData[num].append(data[data['teamNumber'] == num])


columnsToAvg = ["autoGamePieces", "autoCubes", "autoCones", "autoHigh", "autoMed", "autoLow", "teleopGamePieces", "teleopCubes", "teleopCones", "teleopHigh", "teleopMed", "teleopLow", "totalGamePieces", "totalCubes", "totalCones", "totalHigh", "totalMed", "totalLow"]

teamAverages = {}

for key in dictionaryOfData:
    totals = {}
    avgs = {}
    count = 0

    #SWO EPA
    for matchData in dictionaryOfData[key]:
        autoPts = (matchData["autoHigh"].sum() * 6) + (matchData["autoMed"].sum() * 4) + (matchData["autoLow"].sum() * 2)
        teleopPts = (matchData["teleopHigh"].sum() * 5) + (matchData["teleopMed"].sum() * 3) + (matchData["teleopLow"].sum() * 1)
        autoBalance = 0

        match matchData["autoDocked"].sum():
            case "e":
                autoBalance = 12
            case "d":
                autoBalance = 10
            case "f":
                autoBalance = -5
            case "x":
                autoBalance = 0
            case "p":
                autoBalance = 2
            case default:
                autoBalance = 0

        teleopBalance = 0
        match matchData["finalState"].sum():
            case "e":
                teleopBalance = 5
            case "d":
                teleopBalance = 2
            case "f":
                teleopbalance = -10
            case "x":
                teleopBalance = 0
            case default:
                teleopBalance = 0

        teleopBalance *= matchData["numOfRobotsDocked"].sum()

        # autoBalance = matchData["autoDocked"] == "e" and 12 or matchData["autoDocked"] == "d" and 10 or matchData["autoDocked"] == "f" and -5 or matchData["autoDocked"] == "x" and 0 or matchData["autoDocked"] == "p" and 2 or 0
        # teleopBalance = (matchData["finalState"] == "e" and 5 or matchData["finalState"] == "d" and 2 or matchData["finalState"] == "f" and -10 or matchData["finalState"] == "x" and 0 or 0) * matchData["numOfRobotsDocked"]
        if matchData["dockingTime"].sum() <= 5:
            teleopBalance += 10
        elif matchData["dockingTime"].sum() <= 15:
            teleopBalance += 5

        defensePts = 0
        match matchData["defenseRating"].sum():
            case "b":
                defensePts = -5
            case "a":
                defensePts = 10
            case "e":
                defensePts = 20
            case "x":
                defensePts = 0
            case default:
                defensePts = 0

        # defensePts = matchData["defense"] == "b" and -5 or matchData["defense"] == "a" and 10 or matchData["defense"] == "e" and 20 or matchData["defense"] == "x" and 0 or 0

        diedTipped = 0
        match matchData["diedOrTipped"].sum():
            case 1:
                diedTipped = -10
            case 0:
                diedTipped = 0
            case default:
                diedTipped = 0

        # diedTipped = matchData["diedOrTipped"] == 1 and -10 or matchData["diedOrTipped"] == 0 and 0 or 0
        tippy = 0
        match matchData["tippy"].sum():
            case 1:
                tippy = -5
            case 0:
                tippy = 0
            case default:
                tippy = 0

        # tippy = matchData["tippy"] == 1 and -5 or matchData["tippy"] == 0 and 0 or 0
        swoPA = autoPts + teleopPts + autoBalance + teleopBalance + defensePts + diedTipped + tippy
        totals["swoPA"] = swoPA

    #averages
    for matchData in dictionaryOfData[key]:
        for column in columnsToAvg:
            if column not in totals:
                totals[column] = dictionaryOfData[key][count][column].sum()
            else:
                totals[column] += dictionaryOfData[key][count][column].sum()
        count += 1
    for total in totals:
        avgs[total] = totals[total] / count + 1
    teamAverages[key] = avgs


def sort(sortBy):
    fullSorted = sorted(teamAverages.items(), key=lambda x: x[1][sortBy])
    fullSorted.reverse()
    return [(v[0], v[1][sortBy]) for v in fullSorted]
   
command = input("What would you like to do?\n")
while command != "exit":
    if command == "get":
        team = int(input("What team would you like to get data for?\n"))
        print(teamAverages[team])
    elif command == "sort":
        sortBy = input("What would you like to sort by?\n")
        print(sort(sortBy))
    command = input("What would you like to do?\n")
