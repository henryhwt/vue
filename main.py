import requests
import pandas as pd
import json
cookies = {

    'microservicesToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyNWViYTlkZS04OWQzLTQzOWUtYTJmYy02MDA1NmU1YjM3MjgiLCJDb3VudHJ5IjoiVUsiLCJBdXRoIjoiMyIsIlNob3dpbmciOiIzIiwiQm9va2luZyI6IjMiLCJQYXltZW50IjoiMyIsIlBhcnRuZXIiOiIzIiwiTG95YWx0eSI6IjMiLCJDYW1wYWlnblRyYWNraW5nQ29kZSI6IiIsIm5iZiI6MTcwNzIyNTQwMCwiZXhwIjoxNzA3MjY4NjAwLCJpc3MiOiJQcm9kIn0.ZkN6HuPxzmnYUcynANGNLZ7WL7HsqyfhxXk9x0Hg510',
    'microservicesRefreshToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyNWViYTlkZS04OWQzLTQzOWUtYTJmYy02MDA1NmU1YjM3MjgiLCJDb3VudHJ5IjoiVUsiLCJuYmYiOjE3MDcyMjU0MDAsImV4cCI6MTcwNzMwOTQwMCwiaXNzIjoiQXV0aFByb2QifQ.Ya6wa-9hpiwO5O27M5yBBzt2IEl9Y51HChx9Txtui1E',
    'accessTokenExpirationTime': '2024-02-07T01%3A16%3A40Z',
}

# 10020 = cinema id
# 381852 = session id
# 'https://www.myvue.com/api/microservice/booking/Session/10020/381852/seats',

# Request to seat API
seat_response = requests.get(
    # 'https://www.myvue.com/api/microservice/booking/Session/10020/381852/seats',
    'https://www.myvue.com/api/microservice/booking/Session/10020/382219/seats',
    cookies=cookies,
)
seat_data = seat_response.json()

# Request to films at cinema API
films_response = requests.get(
"https://www.myvue.com/api/microservice/showings/cinemas/10020/films",
    cookies=cookies,
)
films_data = films_response.json()


# saving json file
# dict = response.json()
# json_string = json.dumps(dict, indent=4)  
# with open("sample.json", "w") as outfile:
#     outfile.write(json_string)

# opening json file
# f = open('sample.json')
# data = json.load(f)


seating_data = pd.DataFrame(seat_data["result"]["seatingData"], index=[0])
screenLabel = seating_data["screenLabel"]

def get_seats(data):
    list = []
    data_dict = dict()
    for i, ele in enumerate(data["result"]["seatRows"]):
        row_label = ele["rowLabel"]
        for x, xele in enumerate(ele["columns"]):
            if xele != None:
                data_dict = {
                    "screenLabel": screenLabel,
                    "row_label": row_label,
                    "name": xele["name"],
                    "seatStatus": xele["seatStatus"],
                    "areaCategoryCode": xele["areaCategoryCode"],
                    "areaNumber": xele["areaNumber"],
                    "columnIndex": xele["columnIndex"],
                    "rowIndex": xele["rowIndex"],
                    "priority": xele["priority"],
                    "seatsInGroup": xele["seatsInGroup"],
                }
                list.append(data_dict)
    return list


# print(get_seats(seating_data))


f = open('films.json')
films_data = json.load(f)

def get_films(data):
    list = []
    data_dict = dict()
    for i, result in enumerate(data["result"]):
        for i, showingGroups in enumerate(result["showingGroups"]): 
            date = showingGroups["date"]
            for i, sessions in enumerate(showingGroups["sessions"]): 
                sessionId = sessions["sessionId"]
                startTime = sessions["startTime"]
                endTime = sessions["endTime"]
                bookingUrl = sessions["bookingUrl"]
                screenName = sessions["screenName"]
                for i, showingInCinemas in enumerate(result["showingInCinemas"]): 
                    cinemaId = showingInCinemas
                    data_dict = {
                        "filmId": result["filmId"],
                        "cinemaId": cinemaId,
                        "sessionId": sessionId,
                        "startTime": startTime,
                        "endTime": endTime,
                        "filmTitle": result["filmTitle"],
                        "filmUrk": result["filmUrl"],
                        "date": date,
                        "posterImageSrc": result["posterImageSrc"],
                        "cast": result["cast"],
                        "director": result["director"],
                        "synopsisShort": result["synopsisShort"],
                        "releaseDate" : result["releaseDate"],
                        "runningTime" : result["runningTime"],
                        "distributor" : result["distributor"],
                        "genres" : ", ".join(result["genres"]),
                        }
                    list.append(data_dict)
    return list
        

df = pd.DataFrame(get_films(films_data))
df.to_csv("test.csv")

print(df)