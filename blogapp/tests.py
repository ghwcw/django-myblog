import os

import django
from django.http import QueryDict
from django.test import TestCase

# Create your tests here.
# 外部脚本调用Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()
# 接下来可以使用django内部环境了！


# print(1213)
# print(QueryDict('name=20&sex=男'))
# print(QueryDict.fromkeys(['name','sex'], '=?'))

q = QueryDict('a=0&a=1&b=2&c=3', mutable=True)
# print(q)
# q.update(b=[222,222222222])
# print(q.getlist('b'))
# print(q.items())
# print(q)
# q.appendlist('d',444444444444444)
q.setdefault('e',5)
# print(q.getlist('a'))
print(q)


