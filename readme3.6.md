# Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

1. **Работа c HTTP через телнет.**
- Подключитесь утилитой телнет к сайту stackoverflow.com
`telnet stackoverflow.com 80`  

- отправьте HTTP запрос
```bash
GET /questions HTTP/1.0
HOST: stackoverflow.com
[press enter]
[press enter]
```  
  - В ответе укажите полученный HTTP код, что он означает?  
  
```  
telnet stackoverflow.com 80
Trying 151.101.129.69...
Connected to stackoverflow.com.
Escape character is '^]'.
get /questions HTTP/1.0
HOST: stackoverflow.com

HTTP/1.1 301 Moved Permanently
cache-control: no-cache, no-store, must-revalidate
location: https://stackoverflow.com/questions
x-request-guid: 3429e95e-6eaf-4c76-adaf-1a74542ec25c
feature-policy: microphone 'none'; speaker 'none'
content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com
Accept-Ranges: bytes
Date: Wed, 01 Dec 2021 14:13:55 GMT
Via: 1.1 varnish
Connection: close
X-Served-By: cache-hel1410030-HEL
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1638368035.216127,VS0,VE109
Vary: Fastly-SSL
X-DNS-Prefetch-Control: off
Set-Cookie: prov=2355160c-14dd-19a0-5517-149c1ba2f9a2; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly

Connection closed by foreign host.  
```   
Основное это `301 Moved Permanently` и `location: https://stackoverflow.com/questions`. Означает это постоянное перенаправление по адресу `location`  


2. **Повторите задание 1 в браузере, используя консоль разработчика F12.**
- откройте вкладку `Network`
- отправьте запрос http://stackoverflow.com
- найдите первый ответ HTTP сервера, откройте вкладку `Headers`
- укажите в ответе полученный HTTP код.
- проверьте время загрузки страницы, какой запрос обрабатывался дольше всего?
- приложите скриншот консоли браузера в ответ.  
  
***Ответ:***  
``` 
Request URL: http://stackoverflow.com/
Request Method: GET
Status Code: 301 Moved Permanently
Remote Address: 151.101.1.69:80
Referrer Policy: strict-origin-when-cross-origin  
```  
Дольше всего обрабатывался запрос первый же запрос со статусом 301. Возможно из-за режима инкогнито.  
https://github.com/NetVasiliy/Netology/blob/main/3_6_1.jpg  


3. **Какой IP адрес у вас в интернете?**  
   
 
`213.87.129.254`   

4. **Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой `whois`**  
  
`mnt-by:         MTSNET-MNT`  
`origin:         AS8359`

5. **Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой `traceroute`**  
  
 `traceroute -An 8.8.8.8` Не резолвит...  


6. **Повторите задание 5 в утилите `mtr`. На каком участке наибольшая задержка - delay?**  
  
```Keys:  Help   Display mode   Restart statistics   Order of fields   quit
                                                                               Packets               Pings
 Host                                                                        Loss%   Snt   Last   Avg  Best  Wrst StDev
 1. AS???    10.0.2.2                                                         0.0%     7    0.7   0.6   0.6   0.7   0.1
 2. AS???    192.168.178.178                                                  0.0%     7    3.6   6.4   3.6  15.9   4.4
 3. AS???    172.16.9.206                                                     0.0%     7   42.8  56.1  25.1  93.7  26.4
 4. AS???    172.16.13.93                                                     0.0%     7   35.6  37.1  20.5  86.1  22.7
 5. AS8359   195.34.36.225                                                    0.0%     7   24.2  31.0  22.4  51.2  10.4
 6. AS15169  72.14.223.72                                                     0.0%     7   23.2  29.2  21.8  47.1   8.8
 7. AS15169  108.170.250.34                                                   0.0%     7   28.6  68.1  22.8 215.7  70.6
 8. AS15169  142.251.49.24                                                    0.0%     7  155.0  88.2  37.7 186.0  65.2
 9. AS15169  72.14.238.168                                                    0.0%     6  101.0 106.5  40.4 190.1  58.1
10. AS15169  209.85.251.41                                                    0.0%     6   45.3  76.7  40.0 155.3  44.5
11. (waiting for reply)
12. (waiting for reply)
13. (waiting for reply)
14. (waiting for reply)
15. (waiting for reply)
16. (waiting for reply)
17. (waiting for reply)
18. (waiting for reply)
19. (waiting for reply)
20. AS15169  8.8.8.8                                                         20.0%     6   34.9  63.2  34.9 136.6  49.1
`````    
Наибольшая задержка 106.5 тут:  

` 9. AS15169  72.14.238.168                                                    0.0%     6  101.0 106.5  40.4 190.1  58.1`
  
7. **Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой `dig`**  
  
```  
dig  dns.google A  
dns.google.             183     IN      A       8.8.4.4
dns.google.             183     IN      A       8.8.8.8  
  
dig  dns.google NS  
dns.google.             86400   IN      NS      ns4.zdns.google.
dns.google.             86400   IN      NS      ns2.zdns.google.
dns.google.             86400   IN      NS      ns1.zdns.google.
dns.google.             86400   IN      NS      ns3.zdns.google.  
```  

8. **Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой `dig`**  
  
``` 
dig -x 8.8.4.4  
4.4.8.8.in-addr.arpa.   34187   IN      PTR     dns.google.  
  
dig -x 8.8.8.8  
8.8.8.8.in-addr.arpa.   65297   IN      PTR     dns.google.  
```  
Доменное имя `dns.google`    



