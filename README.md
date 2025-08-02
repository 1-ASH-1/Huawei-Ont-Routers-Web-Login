# Huawei-Ont-Routers-Web-Login# Huawei-Ont-Routers-Web-Login
 


```python
from web import Router

r1 = Router(ip="192.168.0.1",username="admin",password="123456",port=80,scheme="https")

print(r1.login())

```
```output:(True, 'We Have Loged in')```


#Tested on 
```
HG8120C
SA1456C
```
