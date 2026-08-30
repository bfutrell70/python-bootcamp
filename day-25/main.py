import pandas  # type: ignore

WEATHER_DATA_PATH = "./weather_data.csv"

# data = pandas.read_csv(WEATHER_DATA_PATH)

# # print(data["temp"])
# # print(type(data))
# # print(type(data["temp"]))
# # data_dict = data.to_dict()
# # print(data_dict)

# # temp_list = data["temp"].to_list()
# # print(temp_list)

# # average of temp_list
# # if temp_list:
# #     print(f"average: {(sum(temp_list) / len(temp_list))}")

# # print(f"Mean: {data['temp'].mean()}")
# # print(f"Max: {data['temp'].max()}")

# # get data in columns
# # print(data["condition"])
# # print(data.condition)

# # get data in row
# # print(data[data.day == "Monday"])

# # challenge - get row of data which had the highest temperature
# # print(data[data.temp == data.temp.max()])

# monday = data[data.day == "Monday"]
# print(monday.condition)


# # challenge - convert Monday's temperature to Farenheit
# #  (0°C × 9/5) + 32
# def celcius_to_farenheit(temp):
#     return (temp * (9 / 5)) + 32


# # temperature = data.temp[1]
# temperature = monday.temp[0]
# print(f"{temperature} C is {celcius_to_farenheit(temperature)} F")

# # create a dataframe from scratch
# data_dict = {"students": ["Amy", "James", "Angela"], "scores": [76, 56, 65]}
# data = pandas.DataFrame(data_dict)
# # print(data)
# data.to_csv("new_data.csv")

# Challenge - create a CSV file named "squirrel_count.csv"
# with Fur Color and Count (of Fur Color)
SQUIRREL_DATA_FILE = "2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv"
data = pandas.read_csv(SQUIRREL_DATA_FILE)

squirrel_info = data.groupby("Primary Fur Color").agg(
    Count=pandas.NamedAgg(column="Primary Fur Color", aggfunc="count")
)
squirrel_info.to_csv("squirrel_count.csv")

# Angela's code
data = pandas.read_csv(SQUIRREL_DATA_FILE)
grey_squirrels = len(data[data["Primary Fur Color"] == "Gray"])
red_squirrels = len(data[data["Primary Fur Color"] == "Cinnamon"])
black_squirrels = len(data[data["Primary Fur Color"] == "Black"])

data_dict = {
    "Fur Color": ["Gray", "Cinnamon", "Black"],
    "Counts": [grey_squirrels, red_squirrels, black_squirrels],
}
print(data_dict)

df = pandas.DataFrame(data_dict)
df.to_csv("angela_squirrel_count.csv")
