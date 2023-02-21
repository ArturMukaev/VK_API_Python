from datetime import date, datetime
import vk, time, math, numpy as np, re, networkx as nx


vkapi = vk.API(
    access_token='vk1.a.QrMp01GnRr87dWtpS_zo7nlhkkqXkA5LmAXqEKmAWYqHBF-5Kg_6fDfJeCORh1W2GzA1Y_45xhSeyPddJGs_TAgS0D8t5N8iqhzw-JheOaw6_N1MBygH58_2YrNPQvhg3NlyE4H_IrLnLSdlCHgkNbd81Rw65EYhRFkwuMXDmmFWmj8T29YHz1f_0jOApmGJWf52iYFPmX-MTHT0W8IgWA',
    v='5.81')

# id двух групп
groupId1 = 'turbaza_sport'
groupId2 = 'sporthall59'

# Получаем количество пользователей обеих групп
membersCount1 = vkapi.groups.getMembers(group_id=groupId1)["count"]
print("В группе {} {} человек".format(groupId1,membersCount1))
membersCount2 = vkapi.groups.getMembers(group_id=groupId2)["count"]
print("В группе {} {} человек".format(groupId2,membersCount2))

# Функция для получения пользователей
def getUsers(id,user_count):
    users = []
    for j in range(math.ceil(user_count / 1000)):
        newUsers = vkapi.groups.getMembers(group_id=id, count=1000, offset=j*1000, fields=['city','sex','bdate'])["items"]
        users = np.concatenate((users, newUsers))
        time.sleep(0.5)
    return users

# Получаем пользователей групп
users1 = getUsers(groupId1,membersCount1)
users2 = getUsers(groupId2,membersCount2)

# Получим массив только из userId
usersId1 = []
for user in users1:
    usersId1.append(user["id"])
usersId2 = []
for user in users2:
    usersId2.append(user["id"])

# Посмотрим, сколько людей из второй группы состоят также в первой
intersectionCount = 0
for human in users2:
    if human["id"] in usersId1:
        intersectionCount +=1
print("{} пользователей состоят в обеих исследуемых группах".format(intersectionCount))

#Посмотрим топ-5 самых частых городов пользователей
#Функция для этого
def getCities(array):
    cities = {}
    for citizen in array:
        if "city" in citizen:
            city = citizen["city"]["title"]
            if not (city in cities.keys()):
                cities.update({city : 1})
            else:
                currentCitizens = cities[city] + 1
                cities.update({city : currentCitizens})
    sorted_cities = dict(sorted(cities.items(), reverse=True, key=lambda item: item[1]))
    return list(sorted_cities.items())

cities1 = getCities(users1)
cities2 = getCities(users2)
print("Топ 5 городов группы ТурбазаСпорт:")
for i in range(5):
    print(cities1[i])
print("Топ 5 городов группы Спортхол:")
for i in range(5):
    print(cities2[i])

# Посмотрим кого больше, мужчин или женщин
# Функция для этого
def get_sex_procents(array):
    male = 0
    female = 0
    for item in array:
        if "sex" in item:
            if item["sex"] == 1:
                female +=1
            else:
                male +=1
    allPeople = male + female
    prMale = int(round(male/allPeople,2) * 100)
    prFemale = int(round(female/allPeople,2) * 100)
    return [prMale, prFemale]
genders1 = get_sex_procents(users1)
genders2 = get_sex_procents(users2)
print("В группе {} {}% мужчин и {}% женщин".format(groupId1, genders1[0],genders1[1]))
print("В группе {} {}% мужчин и {}% женщин".format(groupId2, genders2[0],genders2[1]))

# Сравним, в какой из групп средний возраст участников больше
# Функция для получения возраста
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

#Функция для подсчета среднего возраста
def get_average_age(arr):
    people_count = 0
    age_total = 0
    for person in arr:
        if "bdate" in person and re.fullmatch('\d\d\.\d\d\.\d{4}',person["bdate"]):
            age = calculate_age(datetime.strptime(person["bdate"], '%d.%m.%Y'))
            people_count +=1
            age_total +=age
    return int(age_total/people_count)


#Функция для сравнения групп
def compare_age(group1, group2, arr1, arr2):
    average_age1 = get_average_age(arr1)
    average_age2 = get_average_age(arr2)
    if (average_age1==average_age2):
        print("В обеих группах одинаковых средний возраст участников равный {}".format(average_age1))
    else:
        if(average_age1>average_age2):
            print("В группе {} средний возраст участников больше, чем в группе {} ({} против {})"
                  .format(group1,group2,average_age1,average_age2))
        else:
            print("В группе {} средний возраст участников больше, чем в группе {} ({} против {})"
                  .format(group2,group1,average_age2,average_age1))

compare_age(groupId1,groupId2,users1,users2)


#Построим граф пользователей
#Функция для построения графа пользователей
def build_graph(group_name,usersId):
    graph = nx.Graph()
    for userId in usersId:
        graph.add_node(userId)
    for userId in usersId:
        try:
            friends = vkapi.friends.get(user_id=userId)["items"]
            for memberId in usersId:
                 if memberId in friends:
                     graph.add_edge(userId, memberId)
            time.sleep(0.34)
        except Exception:
            print("У данного пользователя скрыты друзья")
    nx.write_gexf(graph, "{}.gexf".format(group_name))

newusers = []
for i in range(100):
    newusers.append(usersId1[i])
build_graph("test1",newusers)
#build_graph(groupId1,users1)
#build_graph(groupId2,users2)




