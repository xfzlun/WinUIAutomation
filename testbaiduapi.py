from aip import AipOcr

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

""" 你的 APPID AK SK """
with open(r'/home/pi/Documents/WinUIAutomation/ipconfig.txt') as f:
#with open('./ipconfig.txt') as f:
    text = f.read()
    name = text.split('\n')
    workingdir = name[2].split('=')
    app_id = name[3].split('=')
    app_key = name[4].split('=')
    secret_key = name[5].split('=')
    bmcip = name[1].split('=')

APP_ID = app_id[1]
API_KEY = app_key[1]
SECRET_KEY = secret_key[1]
#连接百度API端口
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

image = get_file_content('example.jpg')
print(client.basicGeneral(image))
results = client.basicGeneral(image)["words_result"]
