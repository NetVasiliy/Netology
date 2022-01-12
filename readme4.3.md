# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## Обязательные задания

1. **Мы выгрузили JSON, который получили через API запрос к нашему сервису:**
	```json
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
	```
  Нужно найти и исправить все ошибки, которые допускает наш сервис  
  
Не хватает символов `"` в 5-ой (необязательно) и 9-ой строках, и `пробела` во второй строке перед `[` (необязательно)
  
  
```json
    { "info" : "Sample JSON output from our service\t",
        "elements" : [
            { "name" : "first",
            "type" : "server",
            "ip" : "7175" 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
            }
        ]
    }
```

2. **В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.**  
  
```python
#!/usr/bin/env python3

import os
import socket
import time
import json
import yaml

host_list2 = {'google.com': 'null', 'ya.ru':'null', 'mail.google.com': 'null', 'drive.google.com':'null'}
while True:
        for i in host_list2.keys():
                print(i + ' - ' + socket.gethostbyname(i))
                current_ip = socket.gethostbyname(i)
                if current_ip != host_list2[i]:
                        old_ip = host_list2[i]
                        host_list2[i] = current_ip
                        print('[ERROR]: ' + i + ' IP mismatch ' + old_ip + ' ' + current_ip)
                with open ('4.3.2.yml', 'w') as yml1:
                        yml1.write(yaml.dump(host_list2, indent=2, explicit_start=True, explicit_end=True))
                with open ('4.3.2.json', 'w') as json1:
                        json1.write(json.dumps(host_list2, indent=2))
        time.sleep(2)
```  
  
При запуске скрипта в терминале будет выводиться информация как в домашнем задании 4.2 пункт 4. При этом в директории запуска скрипта появятся 2 файла `4.3.2.yml` и `4.3.2.json` с таким содержимым:  
```  
---
drive.google.com: 74.125.131.194
google.com: 127.0.0.1
mail.google.com: 142.251.1.19
ya.ru: 87.250.250.242
...  
```  
```  
{
  "google.com": "127.0.0.1",
  "ya.ru": "87.250.250.242",
  "mail.google.com": "142.251.1.17",
  "drive.google.com": "74.125.131.194"
}  
```  
Смена информации в файлах при изменении IP адреса сервиса происходит в течении 2 секунд.


