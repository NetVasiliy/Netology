# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.  
  
```  
root@vagrant:~# docker pull postgres:13
root@vagrant:~/Netology/6.4# mkdir volume
root@vagrant:~/Netology/6.4# docker run --name pg-docker6.4 -e POSTGRES_PASSWORD=postgres -ti -p 5435:5432 -v ~/Netology/6.4/volume:/var/lib/postgresql/data postgres:13

```

Подключитесь к БД PostgreSQL используя `psql`.  
`root@vagrant:~# psql -h localhost -p 5435 -U postgres`

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД `\l[+]   [PATTERN]      list databases`
- подключения к БД ` \c[onnect] {[DBNAME|- USER|- HOST|- PORT|-] | conninfo}`
- вывода списка таблиц `\dt[S+] [PATTERN]      list tables`
- вывода описания содержимого таблиц ` \dt[S+] TABLE_NAME`  
```  
test_db=# \dt[S+] client
                    List of relations
 Schema |  Name  | Type  |  Owner   | Size  | Description
--------+--------+-------+----------+-------+-------------
 public | client | table | postgres | 16 kB |
(1 row)
```
- выхода из psql `\q                     quit psql`

## Задача 2

Используя `psql` создайте БД `test_database`.  
`postgres=# CREATE DATABASE test_database;`

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data). `Неплохо`

Восстановите бэкап БД в `test_database`.  
```  
root@vagrant:~/Netology/6.4/test_data# docker cp test_dump.sql pg-docker6.4:/var/lib/postgresql/data/test_dump.sql
root@vagrant:~# docker exec -it pg-docker6.4 /bin/bash
root@cd2b1985a559:/var/lib/postgresql/data# psql -U postgres -d test_database < /var/lib/postgresql/data/test_dump.sql

```

Перейдите в управляющую консоль `psql` внутри контейнера. `root@cd2b1985a559:/var/lib/postgresql/data# psql -U postgres`

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.  
```  
postgres=# \c test_database;
test_database=# ANALYZE VERBOSE orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
```

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах. `Это столбец title`  
```  
test_database=# SELECT attname, avg_width FROM pg_stats WHERE tablename='orders';
 attname | avg_width
---------+-----------
 id      |         4
 title   |        16
 price   |         4
(3 rows)
```

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.
```
Пример: Если таблица пректировалась как секционная BY price,то  
CREATE TABLE orders_2 PARTITION OF orders
    FOR VALUES FROM ('1') TO ('500');
CREATE TABLE orders_1 PARTITION OF orders
    FOR VALUES FROM ('500') TO ('MAXVALUE');
```
**Выше был ответ. Дальше мои рассуждения и экперименты. Можно пропустить.**
Но у нас изначально несекционная таблица. Придется ее переделать. В "боевых" условиях это может занять длительное время.
  
```  
test_database=# alter table orders rename to orders_new;
ALTER TABLE
test_database=# create table orders (id integer, title varchar(80), price integer) partition by range(price);
CREATE TABLE
test_database=# CREATE TABLE orders_1 PARTITION OF orders FOR VALUES FROM (499) to (MAXVALUE);
CREATE TABLE
test_database=# CREATE TABLE orders_2 PARTITION OF orders FOR VALUES FROM (1) to (498);
CREATE TABLE
test_database=# INSERT INTO orders (id, title, price) SELECT * FROM orders_new;
```  
Я так и не понял, почему если в таблице `orders_2` разбиение сделать от 0 до 499 (`FOR VALUES FROM (0) to (499)`) у меня, при наполнении таблицы не происходит вставка строки `7 | Me and my bash-pet   |   499`  
Можно это пояснить? ошибка такая:  
```  
test_database=# INSERT INTO orders (id, title, price) SELECT id, title, price FROM orders_new;
ERROR:  no partition of relation "orders" found for row
DETAIL:  Partition key of the failing row contains (price) = (499).
```  
Разобрался. Значение  `TO` не включается в диапазон.  

**Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?**  
`Можно предусмотреть при проектировании секционированных таблиц`

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.
`pg_dump -U postgres test_database > 6.4.dump`  

**Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?**
  
*Надо добавить уникальность столбца на каждую секцию.*  

Удалось добиться уникальности в пределх "секции". В принципе условиям задачи ответ удовлетворяет. 
```
ALTER TABLE orders_1 ADD CONSTRAINT orders_1_unique UNIQUE (title)
ALTER TABLE orders_2 ADD CONSTRAINT orders_2_unique UNIQUE (title)
```
Но тогда может быть одинаковый "title", если цена оного меньше 499, а другого больше 500... ХМ...  
Пока не понял, через триггеры для меня пока сложно. Да и если при каждой вставке шерстить таблицу на уникальность "title", будет есть много лишних ресурсов.  
Будет время, надо покопать...
---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
