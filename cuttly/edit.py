import requests
from urllib import parse

key = '3b4984a557f62d27ddb277964851459b7d6aa'

sl = parse.quote(input('sl:'))
delete = 1
r = requests.get('http://cutt.ly/api/api.php?key={}&edit={}&delete={}'.format(key, sl, delete))
print(r.status_code)
print(r.text)
result = r.json()  # 返回结果转换成字典
print(result)
# back = result['url']
# status = result['status']
#
# if status == 1:
#     print('Success!')
# elif status == 2:
#     print('无法保存在数据库中')
# elif status == 3:
#     print('该网址不存在或您不拥有它')
# elif status == 4:
#     print('URL 未通过验证')
# else:
#     print('异常')
