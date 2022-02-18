
# Домашнее задание к занятию "5.3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера"

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Любые вопросы по решению задач задавайте в чате учебной группы.

---

## Задача 1

**Сценарий выполения задачи:**

- создайте свой репозиторий на https://hub.docker.com; `https://hub.docker.com/repository/docker/netvasiliy/ansible`
- выберете любой образ, который содержит веб-сервер Nginx; `ubuntu/nginx:1.18-21.10_beta`
- создайте свой fork образа; `docker run -d --name nginx-5.3.1 -e TZ=UTC -p 8080:80 ubuntu/nginx:1.18-21.10_beta`
- реализуйте функциональность:
запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.  
  
https://hub.docker.com/repository/docker/netvasiliy/nginx5.3.1  
```  
root@vagrant:~/Netology/5.3# nano index.html  -  Создаем приветственный файл  
root@vagrant:~/Netology/5.3# docker cp ~/Netology/5.3/index.html  nginx-5.3.1:/var/www/html/  
root@vagrant:~/Netology/5.3# curl http://localhost:8080
<html>
                <head>
                        Hey, Netology
                </head>
        <body>
                <h1>I’m DevOps Engineer!</h1>
        </body>
        </html>  
  
root@vagrant:~/Netology# docker commit nginx-5.3.1 ubuntu/nginx:nginxv1
sha256:2537a49f59659fdb4aed1e79103b59e95a20ffe5a34768410f535e55b0469d01

root@vagrant:~/Netology# docker image list
REPOSITORY           TAG               IMAGE ID       CREATED          SIZE
ubuntu/nginx         nginxv1           2537a49f5965   9 minutes ago    139MB
<none>               <none>            5bc475637512   24 minutes ago   139MB
netvasiliy/ansible   2.9.24            fd3c44f123a7   21 hours ago     230MB
ubuntu/nginx         1.18-21.10_beta   b7301f7f1bd2   3 days ago       139MB
nginx                latest            c316d5a335a5   3 weeks ago      142MB
alpine               3.14              0a97eee8041e   3 months ago     5.61MB
hello-world          latest            feb5d9fea6a5   4 months ago     13.3kB
root@vagrant:~/Netology# docker tag 2537a49f5965 netvasiliy/nginx5.3.1:v1    

root@vagrant:~/Netology# docker push netvasiliy/nginx5.3.1:v1
The push refers to repository [docker.io/netvasiliy/nginx5.3.1]
```

## Задача 2

**Посмотрите на сценарий ниже и ответьте на вопрос:**
"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высоконагруженное монолитное java веб-приложение;
- Nodejs веб-приложение;
- Мобильное приложение c версиями для Android и iOS;
- Шина данных на базе Apache Kafka;
- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
- Мониторинг-стек на базе Prometheus и Grafana;
- MongoDB, как основное хранилище данных для java-приложения;
- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.

## Задача 3

- Запустите первый контейнер из образа ***centos*** c любым тэгом в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Запустите второй контейнер из образа ***debian*** в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Подключитесь к первому контейнеру с помощью ```docker exec``` и создайте текстовый файл любого содержания в ```/data```;
- Добавьте еще один файл в папку ```/data``` на хостовой машине;
- Подключитесь во второй контейнер и отобразите листинг и содержание файлов в ```/data``` контейнера.  
  
```  
root@vagrant:~/Netology# mkdir data
root@vagrant:~/Netology# ls
5.3  data
root@vagrant:~/Netology# touch ~/Netology/data/host_system
root@vagrant:~/Netology# docker pull centos
root@vagrant:~/Netology# docker pull debian

root@vagrant:~/Netology# docker run -d -v ~/Netology/data:/data 5d0da3dc9764 sleep 9000
335667a939bfe40d79b83abfaa250f225f4c0a8c6b54fe1a7d6f431a7300eacb

root@vagrant:~/Netology# docker run -d -v ~/Netology/data:/data 04fbdaf87a6a sleep 9000
c46733797bd3d54f22b6c4890d1ee877551700bf70b07e96851129c49ae3c87a

root@vagrant:~/Netology# docker ps -a
CONTAINER ID   IMAGE          COMMAND        CREATED          STATUS                      PORTS     NAMES
6fa14ea9c986   5d0da3dc9764   "sleep 9000"   6 minutes ago    Up 6 minutes                          vibrant_keldysh
1c7f639c6871   04fbdaf87a6a   "sleep 9000"   6 minutes ago    Up 6 minutes                          hardcore_bhabha

root@vagrant:~/Netology# docker exec -it vibrant_keldysh /bin/bash
[root@6fa14ea9c986 data]# cat /etc/centos-release
CentOS Linux release 8.4.2105
[root@6fa14ea9c986 /]# cd data
[root@6fa14ea9c986 data]# ls
host_system

[root@6fa14ea9c986 data]# echo 'Centos' >> centos
[root@6fa14ea9c986 data]# ls
centos  host_system


root@vagrant:~/Netology# docker exec -it hardcore_bhabha /bin/bash
root@1c7f639c6871:/# cat /etc/issue
Debian GNU/Linux 11 \n \l

root@1c7f639c6871:/# cd data/
root@1c7f639c6871:/data# ls
centos  host_system
root@1c7f639c6871:/data# cat centos
Centos  
```

## Задача 4 (*)

**Воспроизвести практическую часть лекции самостоятельно.**

Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.  
  
https://hub.docker.com/repository/docker/netvasiliy/ansible  
https://hub.docker.com/layers/193006513/netvasiliy/ansible/2.9.24/images/sha256-b65ee781517f7e6706a32371184c75cc8db76301ac52df09864b82afcbeb5222?context=repo  

```  
root@vagrant:~/Netology/5.3# docker bild -t netvasiliy/ansible:2.9.24 .

Successfully tagged netvasiliy/ansible:2.9.24
  
root@vagrant:~/Netology/5.3# docker login -u netvasiliy
Password:
WARNING! Your password will be stored unencrypted in /root/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded  
  
root@vagrant:~/Netology/5.3# docker push netvasiliy/ansible:2.9.24
The push refers to repository [docker.io/netvasiliy/ansible]
4c7e88419007: Pushed  
06481e8103fe: Pushed
1a058d5342cc: Mounted from library/alpine
2.9.24: digest: sha256:b65ee781517f7e6706a32371184c75cc8db76301ac52df09864b82afcbeb5222 size: 947     
       
  ```


---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
