from urllib import parse
import requests
from datetime import datetime

key = '3b4984a557f62d27ddb277964851459b7d6aa'

url = parse.quote(input('url:'))  # 对不符合标准的其他字符(如汉字)进行编码 (按照标准，URL只允许一部分ASCII字符)
# name = '[CUSTOM_URL_ALIAS]'
# r = requests.get('http://cutt.ly/api/api.php?key={}&short={}&name={}'.format(key, url, name))
r = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(key, url))
print(r.status_code)
result = r.json()  # 返回结果转换成字典
# print(result)

if result == '401 Unauthorized':
    print('401 Unauthorized')
else:
    urlBack = result['url']
    status = urlBack['status']

    log = ''

    if status == 7:
        short_link = urlBack['shortLink']
        log = ''.join(' Success\n date: %s\n short url: %s\n fullLink: %s\n title: %s'
                      % (urlBack['date'], urlBack['shortLink'], urlBack['fullLink'], urlBack['title']))
    elif status == 1:
        log = 'the link has already been shortened'
    elif status == 2:
        log = 'the entered link is not a link'
    elif status == 3:
        log = 'the preferred link name / alias is already taken'
    elif status == 4:
        log = 'Invalid API key'
    elif status == 5:
        log = 'the link has not passed the validation. Includes invalid characters'
    elif status == 6:
        log = 'The link provided is from a blocked domain'
    else:
        log = '异常情况'

    with open('log.txt', 'a') as logFile:
        logFile.write('\n\n\n')
        logFile.write(str(datetime.now()) + '   ' + log)

    print(log)


