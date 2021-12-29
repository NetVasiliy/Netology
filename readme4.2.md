# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательные задания

1. **Есть скрипт:**
	```python
    #!/usr/bin/env python3
	a = 1
	b = '2'
	c = a + b
	```
	* Какое значение будет присвоено переменной c? - ***Никакое, будет ошибка сложения типов `int` и `str`***
	* Как получить для переменной c значение 12? - ***`c = str(a) + b`***
	* Как получить для переменной c значение 3? - ***`c = a + int(b)`***

2. **Мы устроились на работу в компанию, где  раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?**

	```python
    #!/usr/bin/env python3

    import os

	bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
	result_os = os.popen(' && '.join(bash_command)).read()
    is_change = False
	for result in result_os.split('\n'):
        if result.find('modified') != -1:
            prepare_result = result.replace('\tmodified:   ', '')
            print(prepare_result)
            break

	```  
 Основное, что мешало скрипту выполняться правильно это команда `break`. Из-за этого он показывал только один измененный файл.  
```python
    #!/usr/bin/env python3

import os

home_dir = '/home/vagrant/dz4.2/'
bash_command = ["cd " + home_dir, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
        if result.find('modified') != -1:
                prepare_result = result.replace('\tmodified:   ', '')
                print(home_dir + prepare_result)

```  
Вывод запуска скрипта ниже:  
```  
 	vagrant@vagrant:~/dz4.2$ ./2.py
/home/vagrant/dz4.2/2.py  
  
	vagrant@vagrant:~/dz4.2$ git add *
	vagrant@vagrant:~/dz4.2$ echo ccc >> bb
	vagrant@vagrant:~/dz4.2$ echo ccc >> aa

	vagrant@vagrant:~/dz4.2$ ./2.py
/home/vagrant/dz4.2/2.py
/home/vagrant/dz4.2/aa
/home/vagrant/dz4.2/bb
  ```

3. **Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.**  
  
Собственно добавил параметр `param`.  
```python
    #!/usr/bin/env python3

import os
import sys

param = sys.argv[1]

bash_command = ["cd " + param, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
        if result.find('modified') != -1:
                prepare_result = result.replace('\tmodified:   ', '')
                print(param + prepare_result)
```  
Работает из любого места:
```  
  	vagrant@vagrant:~/dz4.2$ ./3.py /home/vagrant/dz4.2/
Где проверяем:/home/vagrant/dz4.2/
/home/vagrant/dz4.2/2.py
/home/vagrant/dz4.2/aa
/home/vagrant/dz4.2/bb
	vagrant@vagrant:~/dz4.2$ /tmp/3.py /home/vagrant/dz4.2/
Где проверяем:/home/vagrant/dz4.2/
/home/vagrant/dz4.2/2.py
/home/vagrant/dz4.2/aa
/home/vagrant/dz4.2/bb
	vagrant@vagrant:~/dz4.2$ /tmp/3.py /home/vagrant/
Где проверяем:/home/vagrant/
fatal: not a git repository (or any of the parent directories): .git
  ```

4. **Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.**  
  


