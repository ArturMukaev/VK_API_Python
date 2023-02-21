from urllib.request import urlretrieve
import vk, os, time

vkapi = vk.API(access_token='vk1.a.QrMp01GnRr87dWtpS_zo7nlhkkqXkA5LmAXqEKmAWYqHBF-5Kg_6fDfJeCORh1W2GzA1Y_45xhSeyPddJGs_TAgS0D8t5N8iqhzw-JheOaw6_N1MBygH58_2YrNPQvhg3NlyE4H_IrLnLSdlCHgkNbd81Rw65EYhRFkwuMXDmmFWmj8T29YHz1f_0jOApmGJWf52iYFPmX-MTHT0W8IgWA', v='5.81')

# Ссылка на группу Вышки
url = "https://vk.com/albums-41485194"
# Разбираем ссылку
owner_id = url.split('/')[-1].split('_')[0].replace('albums', '')
# Возвращаем список фотоальбомов сообщества
allAlbums = vkapi.photos.getAlbums(owner_id=owner_id)
print("Всего будет загружено {} альбомов".format(allAlbums["count"]))


counter = 0 # текущий счетчик
breaked = 0 # не загружено из-за ошибки
time_now = time.time() # время старта

for album in allAlbums["items"]:
    album_id = album["id"]
    #Создадим каталоги для каждого альбома
    if not os.path.exists('saved'):
        os.mkdir('saved')
    photo_folder = 'saved/album{0}_{1}'.format(owner_id, album_id)
    if not os.path.exists(photo_folder):
        os.mkdir(photo_folder)
    # Получаем фотографии альбома
    photos = vkapi.photos.get(owner_id=owner_id, album_id=album_id, count=100)
    print("В альбоме {} будет загружено {} фотографий".format(album["title"],photos["count"]))
    localCounter = 0
    for photo in photos["items"]:
        localCounter +=1
        counter +=1
        print("{}/{}".format(localCounter,photos["count"]))
        # Получаем адрес изображения
        url = photo["sizes"][0]["url"]
        try:
            # Загружаем и сохраняем файл
            urlretrieve(url, photo_folder + "/" + os.path.split(url)[1].split('?')[0])
        except Exception:
            breaked +=1
            print('Произошла ошибка, файл пропущен.')
            continue


time_for_dw = time.time() - time_now
print("\nВ очереди было {} файлов. Из них удачно загружено {} файлов, {} не удалось загрузить. "
      "Затрачено времени: {} сек.". format(counter, counter-breaked, breaked, round(time_for_dw,1)))