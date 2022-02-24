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
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже) -
```
test_db=# CREATE TABLE orders (id SERIAL PRIMARY KEY, наименование TEXT, цена INTEGER);
test_db=# CREATE TABLE client (id SERIAL PRIMARY KEY, фамилия TEXT, "страна проживания" TEXT, заказ INTEGER, FOREIGN KEY (заказ) REFERENCES orders(id));
CREATE TABLE
test_db=# CREATE INDEX country_idx ON client ("страна проживания");
CREATE INDEX
```
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
test_db=# SELECT column_name, column_default, data_type, table_name FROM INFORMATION_SCHEMA.COLUMNS where table_name IN ('client', 'orders');
    column_name    |           column_default           | data_type | table_name
-------------------+------------------------------------+-----------+------------
 id                | nextval('orders_id_seq'::regclass) | integer   | orders
 наименование      |                                    | text      | orders
 цена              |                                    | integer   | orders
 id                | nextval('client_id_seq'::regclass) | integer   | client
 фамилия           |                                    | text      | client
 страна проживания |                                    | text      | client
 заказ             |                                    | integer   | client
(7 rows)
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
  
```  
test_db=# INSERT INTO orders VALUES (1, 'Шоколад', 10), (2, 'Принтер', 3000), (3, 'Книга', 500), (4,'Монитор', 7000), (5, 'Гитара', 4000);
INSERT 0 5
test_db=# SELECT * FROM orders;
 id | наименование | цена
----+--------------+------
  1 | Шоколад      |   10
  2 | Принтер      | 3000
  3 | Книга        |  500
  4 | Монитор      | 7000
  5 | Гитара       | 4000
(5 rows)
```  
```  
test_db=# INSERT INTO client VALUES (1, 'Иванов Иван Иванович', 'USA'), (2, 'Петров Петр Петрович', 'Canada'), (3, 'Иоганн Себастьян Бах', 'Japan'), (4, 'Ронни Джеймс Дио',
 'Russia'), (5, 'Ritchie Blackmore', 'Russia');
INSERT 0 5
test_db=# select * from client;
 id |       фамилия        | страна проживания | заказ
----+----------------------+-------------------+-------
  1 | Иванов Иван Иванович | USA               |
  2 | Петров Петр Петрович | Canada            |
  3 | Иоганн Себастьян Бах | Japan             |
  4 | Ронни Джеймс Дио     | Russia            |
  5 | Ritchie Blackmore    | Russia            |
(5 rows)
```
Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.  
```  
test_db=# select COUNT (*) from client;
 count
-------
     5
(1 row)

test_db=# select COUNT (*) from orders;
 count
-------
     5
(1 row)
```

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
  
```  
test_db=# UPDATE client SET заказ = 3 WHERE id = 1;
UPDATE 1
test_db=# UPDATE client SET заказ = 4 WHERE id = 2;
UPDATE 1
test_db=# UPDATE client SET заказ = 5 WHERE id = 3;
UPDATE 1
test_db=# select * from client;
 id |       фамилия        | страна проживания | заказ
----+----------------------+-------------------+-------
  4 | Ронни Джеймс Дио     | Russia            |
  5 | Ritchie Blackmore    | Russia            |
  1 | Иванов Иван Иванович | USA               |     3
  2 | Петров Петр Петрович | Canada            |     4
  3 | Иоганн Себастьян Бах | Japan             |     5
(5 rows)

test_db=# select фамилия from client WHERE заказ IS NOT NULL;
       фамилия
----------------------
 Иванов Иван Иванович
 Петров Петр Петрович
 Иоганн Себастьян Бах
(3 rows)
```  
Т.к. у нас есть foreign key, то добавить в столбец "заказ" значение, которого нет в таблице "orders", невозможно.  
``` 
test_db=# UPDATE client SET заказ = 6 WHERE id = 4;
ERROR:  insert or update on table "client" violates foreign key constraint "client_заказ_fkey"
DETAIL:  Key (заказ)=(6) is not present in table "orders".
```  

```  
test_db=# select cl.фамилия, cl.заказ, ord.наименование from client cl FULL JOIN orders ord ON cl.заказ = ord.id WHERE cl.заказ IS NOT NULL;
       фамилия        | заказ | наименование
----------------------+-------+--------------
 Иванов Иван Иванович |     3 | Книга
 Петров Петр Петрович |     4 | Монитор
 Иоганн Себастьян Бах |     5 | Гитара
(3 rows)
```


## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.  

Вариант 1.  
```  
test_db=# EXPLAIN SELECT фамилия FROM client WHERE заказ IS NOT NULL;
                        QUERY PLAN
----------------------------------------------------------
 Seq Scan on client  (cost=0.00..18.10 rows=806 width=32)
   Filter: ("заказ" IS NOT NULL)
(2 rows)
```  
Вариант 2.
```  
test_db=# EXPLAIN select cl.фамилия, cl.заказ, ord.наименование from client cl FULL JOIN orders ord ON cl.заказ = ord.id WHERE cl.заказ IS NOT NULL;
                                QUERY PLAN
---------------------------------------------------------------------------
 Hash Left Join  (cost=37.00..57.23 rows=806 width=68)
   Hash Cond: (cl."заказ" = ord.id)
   ->  Seq Scan on client cl  (cost=0.00..18.10 rows=806 width=36)
         Filter: ("заказ" IS NOT NULL)
   ->  Hash  (cost=22.00..22.00 rows=1200 width=36)
         ->  Seq Scan on orders ord  (cost=0.00..22.00 rows=1200 width=36)
(6 rows)
```

Показывает стоимость запроса, ожидаемое число строк, средний вес строки в байтах и то, что произошла фильтрация по полю "заказ".

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).  

  
```  
root@vagrant:~# docker exec -it pg-docker6.2 /bin/bash
root@df23bc3303f3:/# pg_dump -U postgres test_db > /var/lib/postgresql/backup/test_db.dump
```

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.  
  
`root@vagrant:~# docker run --rm --name pg-docker6.2.6 -e POSTGRES_PASSWORD=postgres -ti -p 5434:5432  -v ~/Netology/6.2/vol2:/var/lib/postgresql/backup postgres:12`

Восстановите БД test_db в новом контейнере.  
```  
root@vagrant:~# psql -h localhost -p 5434 -U postgres
postgres=# CREATE DATABASE test_db2;

root@vagrant:~# docker exec -it pg-docker6.2.6 /bin/bash
root@e02610ea8d60:/# psql -U postgres -W -d test_db2 < /var/lib/postgresql/backup/test_db.dump
Password:
SET
SET
SET
SET
SET
 set_config
------------

(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
ALTER TABLE
COPY 5
COPY 5
 setval
--------
      1
(1 row)

 setval
--------
      1
(1 row)

ALTER TABLE
ALTER TABLE
CREATE INDEX
ALTER TABLE

postgres=# \c test_db2
psql (12.9 (Ubuntu 12.9-0ubuntu0.20.04.1), server 12.10 (Debian 12.10-1.pgdg110+1))
You are now connected to database "test_db2" as user "postgres".
test_db2=# SELECT * FROM client;
 id |       фамилия        | страна проживания | заказ
----+----------------------+-------------------+-------
  4 | Ронни Джеймс Дио     | Russia            |
  5 | Ritchie Blackmore    | Russia            |
  1 | Иванов Иван Иванович | USA               |     3
  2 | Петров Петр Петрович | Canada            |     4
  3 | Иоганн Себастьян Бах | Japan             |     5
(5 rows)

test_db2=# SELECT * FROM orders;
 id | наименование | цена
----+--------------+------
  1 | Шоколад      |   10
  2 | Принтер      | 3000
  3 | Книга        |  500
  4 | Монитор      | 7000
  5 | Гитара       | 4000
(5 rows)
```

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
