# Домашнее задание к занятию "6.2. SQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

**Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume,** 
**в который будут складываться данные БД и бэкапы.**

Приведите получившуюся команду или docker-compose манифест.  
  
```  
root@vagrant:~/Netology/6.2# docker pull postgres:12
root@vagrant:~/Netology/6.2# mkdir vol1
root@vagrant:~/Netology/6.2# mkdir vol2

root@vagrant:~/Netology/6.2# docker run --rm --name pg-docker -e POSTGRES_PASSWORD=postgres -ti -p 5432:5432 -v vol_postgres1:/var/lib/postgresql/data1 postgres:12
The files belonging to this database system will be owned by user "postgres".
This user must also own the server process.
...
PostgreSQL init process complete; ready for start up.
 
```
  
Вариант №2  
```
root@vagrant:~/Netology/6.2# docker pull postgres:12
root@vagrant:~/Netology/6.2# mkdir vol1
root@vagrant:~/Netology/6.2# mkdir vol2
root@vagrant:~/Netology/6.2# docker run --rm --name pg-docker6.2 -e POSTGRES_PASSWORD=postgres -ti -p 5433:5432 -v ~/Netology/6.2/vol1:/var/lib/postgresql/data -v ~/Netology/6.2/vol2:/var/lib/postgresql/backup postgres:12
root@vagrant:~# docker exec -it pg-docker6.2 /bin/bash
root@faa1b3023c35:/# cd /var/lib/postgresql/backup/
root@faa1b3023c35:/var/lib/postgresql/backup# ls
root@faa1b3023c35:/var/lib/postgresql/backup# echo test >>'test'
root@vagrant:~# psql -h localhost -p 5433 -U postgres
Это не надо тут, он и так есть. Но можно указать другое место. postgres=# CREATE TABLESPACE netology LOCATION '/var/lib/postgresql/data'



```  
  
## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db - `postgres=# CREATE DATABASE test_db;`,`postgres=# \c test_db`, `test_db=# CREATE ROLE test_admin_user LOGIN;` 
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже) - `test_db=# CREATE TABLE orders (id SERIAL PRIMARY KEY, наименование TEXT, цена INTEGER);` `test_db=# CREATE TABLE client (id SERIAL PRIMARY KEY, фамилия TEXT, "страна проживания" TEXT UNIQUE, заказ INTEGER, FOREIGN KEY (заказ) REFERENCES orders(id));`  
```  
test_db=# \d
              List of relations
 Schema |     Name      |   Type   |  Owner
--------+---------------+----------+----------
 public | client        | table    | postgres
 public | client_id_seq | sequence | postgres
 public | orders        | table    | postgres
 public | orders_id_seq | sequence | postgres
(4 rows)
```
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db - `test_db=# GRANT ALL ON client, orders TO test_admin_user;`
- создайте пользователя test-simple-user - `test_db=# CREATE ROLE test_simple_user LOGIN;`  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db - `test_db=# GRANT SELECT, INSERT, UPDATE, DELETE ON client, orders TO test_simple_user;`

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,  
```  
test_db=# \l
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 test_db   | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
(4 rows)
```
- описание таблиц (describe)  
```
test_db=# \dt
         List of relations
 Schema |  Name  | Type  |  Owner
--------+--------+-------+----------
 public | client | table | postgres
 public | orders | table | postgres
(2 rows)
```
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db - `test_db=# SELECT * FROM information_schema.table_privileges WHERE table_catalog = 'test_db' AND grantee IN ('test_admin_user','test_simple_user') ORDER BY 2;`
- список пользователей с правами над таблицами test_db  
```  
 grantor  |     grantee      | table_catalog | table_schema | table_name | privilege_type | is_grantable | with_hierarchy
----------+------------------+---------------+--------------+------------+----------------+--------------+----------------
 postgres | test_admin_user  | test_db       | public       | client     | INSERT         | NO           | NO
 postgres | test_admin_user  | test_db       | public       | client     | SELECT         | NO           | YES
 postgres | test_admin_user  | test_db       | public       | client     | UPDATE         | NO           | NO
 postgres | test_admin_user  | test_db       | public       | client     | DELETE         | NO           | NO
 postgres | test_admin_user  | test_db       | public       | client     | TRUNCATE       | NO           | NO
 postgres | test_admin_user  | test_db       | public       | client     | REFERENCES     | NO           | NO
 postgres | test_admin_user  | test_db       | public       | client     | TRIGGER        | NO           | NO
 postgres | test_admin_user  | test_db       | public       | orders     | INSERT         | NO           | NO
 postgres | test_admin_user  | test_db       | public       | orders     | SELECT         | NO           | YES
 postgres | test_admin_user  | test_db       | public       | orders     | UPDATE         | NO           | NO
 postgres | test_admin_user  | test_db       | public       | orders     | DELETE         | NO           | NO
 postgres | test_admin_user  | test_db       | public       | orders     | TRUNCATE       | NO           | NO
 postgres | test_admin_user  | test_db       | public       | orders     | REFERENCES     | NO           | NO
 postgres | test_admin_user  | test_db       | public       | orders     | TRIGGER        | NO           | NO
 postgres | test_simple_user | test_db       | public       | orders     | INSERT         | NO           | NO
 postgres | test_simple_user | test_db       | public       | client     | INSERT         | NO           | NO
 postgres | test_simple_user | test_db       | public       | client     | SELECT         | NO           | YES
 postgres | test_simple_user | test_db       | public       | client     | UPDATE         | NO           | NO
 postgres | test_simple_user | test_db       | public       | client     | DELETE         | NO           | NO
 postgres | test_simple_user | test_db       | public       | orders     | SELECT         | NO           | YES
 postgres | test_simple_user | test_db       | public       | orders     | UPDATE         | NO           | NO
 postgres | test_simple_user | test_db       | public       | orders     | DELETE         | NO           | NO
(22 rows)
```
  

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
 
Подсказк - используйте директиву `UPDATE`.

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
