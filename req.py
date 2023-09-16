import requests
# целевой URL-адрес
url = 'https://bytecode.su/uploadfile/'
# открываем файл на чтение в 
# бинарном режиме ('rb')
fp = open('cat.gif', 'rb')
# помещаем объект файла в словарь 
# в качестве значения с ключом 'file'
files = {'file': fp}
# передаем созданный словарь аргументу `files`
resp = requests.post(url, files=files)
fp.close()
print(resp.text)