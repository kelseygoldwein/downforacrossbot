import datetime # for puzzles by date
import requests # for api calls


async def getResults(resultsPage = 0, pageSize = 50, searchTerm = "", standardSize = "true", miniSize = "true"):

    response = requests.get(f"https://api.foracross.com/api/puzzle_list?"
                            f"page={resultsPage}&"
                            f"pageSize={pageSize}&"
                            f"filter%5BnameOrTitleFilter%5D={searchTerm}&"
                            f"filter%5BsizeFilter%5D%5BMini%5D={miniSize}&"
                            f"filter%5BsizeFilter%5D%5BStandard%5D={standardSize}"
                            ) 
    responseJson = response.json()
    if len(responseJson["puzzles"]) == 0:
        print(f"oops, no results found for {searchTerm}")
        return None
    return responseJson

async def getPuzzleID(results, index = 0):
    try:
        return results["puzzles"][index]["pid"]

    except Exception as e:
        print(f"Error getting results: {e}")

async def getGID():
    gidCounter = requests.post("https://api.foracross.com/api/counters/gid")
    gidCounterJson = gidCounter.json()
    return gidCounterJson["gid"]

async def createGame(pid, gid):
    data = {"gid":gid, "pid":pid}
    requests.post("https://api.foracross.com/api/game", json=data)

def getGameURL(gid):
    return f"https://downforacross.com/beta/game/{gid}"

async def makeGame(resultsPage = 0, pageSize = 50, searchTerm = "", standardSize = "true", miniSize = "true"):
    results = await getResults(resultsPage, pageSize, searchTerm, standardSize, miniSize)
    if results == None:
        return "no puzzles found"
    puzzleID = await getPuzzleID(results)
    gameID = await getGID()
    await createGame(puzzleID, gameID)
    return getGameURL(gameID)

def getPuzzleName(publisher, date=datetime.date.today()):
    match publisher:
        case "nyt":
            return date.strftime(f"NY Times, %A, %B {date.day}, %Y")
        case "lat":
            return date.strftime(f"L. A. Times, %a, %b {date.day}, %Y")
        case "usa":
            return date.strftime(f"USA Today %A, %b %d, %Y")
        case "wsj":
            return date.strftime(f"WSJ %A, %b %d, %Y")
        case "newsday":
            return date.strftime(f"Newsday %A, %b %d, %Y")
        case "universal":
            return date.strftime(f"Universal Crossword %A")
        case "atlantic":
            return date.strftime(f"Atlantic %A, %b %d, %Y")
        case _:
            print(f"error for publisher {publisher}")
            return ""
    