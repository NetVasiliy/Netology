# Домашнее задание к занятию "3.9. Элементы безопасности информационных систем"

1. **Установите Bitwarden плагин для браузера. Зарегестрируйтесь и сохраните несколько паролей.**  
  
   
https://github.com/NetVasiliy/Netology/blob/main/3.9.1.png

2. **Установите Google authenticator на мобильный телефон. Настройте вход в Bitwarden акаунт через Google authenticator OTP.**  
  
  
https://github.com/NetVasiliy/Netology/blob/main/3.9.2.PNG  
https://github.com/NetVasiliy/Netology/blob/main/3.9.2_2.PNG


3. **Установите apache2, сгенерируйте самоподписанный сертификат, настройте тестовый сайт для работы по HTTPS.**  
  
Делал как в презентации.  
https://github.com/NetVasiliy/Netology/blob/main/3.9.3.PNG

4. **Проверьте на TLS уязвимости произвольный сайт в интернете.**  
  
```  
vagrant@vagrant:/tmp/testssl.sh$ ./testssl.sh -U --sneaky https://****ech.ru

###########################################################
    testssl.sh       3.1dev from https://testssl.sh/dev/
    (2201a28 2021-12-13 18:24:34 -- )

      This program is free software. Distribution and
             modification under GPLv2 permitted.
      USAGE w/o ANY WARRANTY. USE IT AT YOUR OWN RISK!

       Please file bugs @ https://testssl.sh/bugs/

###########################################################

 Using "OpenSSL 1.0.2-chacha (1.0.2k-dev)" [~183 ciphers]
 on vagrant:./bin/openssl.Linux.x86_64
 (built: "Jan 18 17:12:17 2019", platform: "linux-x86_64")


 Start 2021-12-14 14:38:43        -->> 5.188.**.**:443 (****ech.ru) <<--

 rDNS (5.188.29.28):     --
 Service detected:       HTTP


 Testing vulnerabilities

 Heartbleed (CVE-2014-0160)                not vulnerable (OK), timed out
 CCS (CVE-2014-0224)                       not vulnerable (OK)
 Ticketbleed (CVE-2016-9244), experiment.  not vulnerable (OK)
 ROBOT                                     not vulnerable (OK)
 Secure Renegotiation (RFC 5746)           supported (OK)
 Secure Client-Initiated Renegotiation     not vulnerable (OK)
 CRIME, TLS (CVE-2012-4929)                not vulnerable (OK)
 BREACH (CVE-2013-3587)                    potentially NOT ok, "gzip" HTTP compression detected. - only supplied "/" tested
                                           Can be ignored for static pages or if no secrets in the page
 POODLE, SSL (CVE-2014-3566)               not vulnerable (OK)
 TLS_FALLBACK_SCSV (RFC 7507)              Downgrade attack prevention supported (OK)
 SWEET32 (CVE-2016-2183, CVE-2016-6329)    VULNERABLE, uses 64 bit block ciphers
 FREAK (CVE-2015-0204)                     not vulnerable (OK)
 DROWN (CVE-2016-0800, CVE-2016-0703)      not vulnerable on this host and port (OK)
                                           make sure you don't use this certificate elsewhere with SSLv2 enabled services
                                           https://censys.io/ipv4?q=12B6086298B0F5B8335985F3EEE459890251F50EE6CB9E1C3AC825D6428983AE could help you to find out
 LOGJAM (CVE-2015-4000), experimental      not vulnerable (OK): no DH EXPORT ciphers, no DH key detected with <= TLS 1.2
 BEAST (CVE-2011-3389)                     TLS1: ECDHE-RSA-AES128-SHA ECDHE-RSA-AES256-SHA AES256-SHA AES128-SHA DES-CBC3-SHA
                                           VULNERABLE -- but also supports higher protocols  TLSv1.1 TLSv1.2 (likely mitigated)
 LUCKY13 (CVE-2013-0169), experimental     potentially VULNERABLE, uses cipher block chaining (CBC) ciphers with TLS. Check patches
 Winshock (CVE-2014-6321), experimental    not vulnerable (OK) - CAMELLIA or ECDHE_RSA GCM ciphers found
 RC4 (CVE-2013-2566, CVE-2015-2808)        no RC4 ciphers detected (OK)


 Done 2021-12-14 14:39:35 [  54s] -->> 5.188.**.**:443 (****ech.ru) <<--  
 ```  


5. **Установите на Ubuntu ssh сервер, сгенерируйте новый приватный ключ. Скопируйте свой публичный ключ на другой сервер. Подключитесь к серверу по SSH-ключу.**  
  
Генерим ключ  
```  
root@vagrant:/lib/systemd/system# ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /root/.ssh/id_rsa
Your public key has been saved in /root/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:sMh9x5RRyvvMVgDplDlF6KqmQGqSWziB43PCdy9vhlk root@vagrant
The key's randomart image is:
+---[RSA 3072]----+
|          oO+    |
|         .B=     |
|      .  +=..    |
|.  . o o oo. .   |
|+ . o o S.+   .  |
|oB     E.. + .   |
|**oo .+.    =    |
|o+=..++o   .     |
|.   .o=o         |
+----[SHA256]-----+  
```  
Подключаемся с хостовой машины  
```  
admin@LAPTOP-**** MINGW64 ~/.ssh
$ ssh vagrant@localhost -p 2222
The authenticity of host '[localhost]:2222 ([127.0.0.1]:2222)' can't be established.
ED25519 key fingerprint is SHA256:90paTAT5cVlEPHPiY3djy4VxfnJZcyTkjPtK9IgZrGo.
This key is not known by any other names
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[localhost]:2222' (ED25519) to the list of known hosts.
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 15 Dec 2021 01:54:21 PM UTC

  System load:  0.51              Processes:               247
  Usage of /:   8.1% of 61.31GB   Users logged in:         1
  Memory usage: 68%               IPv4 address for dummy0: 10.2.2.2
  Swap usage:   6%                IPv4 address for eth0:   10.0.2.15

87 updates can be applied immediately.
42 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable



This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Wed Dec 15 13:50:42 2021 from ::1
vagrant@vagrant:~$
```

 
6. **Переименуйте файлы ключей из задания 5. Настройте файл конфигурации SSH клиента, так чтобы вход на удаленный сервер осуществлялся по имени сервера.**  
  
Переименовал  
```  
$ ls
id_rsa_1  id_rsa_1.pub  known_hosts  known_hosts.old  old  
```  
Подключился  
```  
$ ssh -i id_rsa_1 vagrant@localhost -p 2222
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 15 Dec 2021 03:00:07 PM UTC

  System load:  0.15              Processes:               249
  Usage of /:   8.1% of 61.31GB   Users logged in:         1
  Memory usage: 69%               IPv4 address for dummy0: 10.2.2.2
  Swap usage:   6%                IPv4 address for eth0:   10.0.2.15

87 updates can be applied immediately.
42 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable



This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Wed Dec 15 14:58:07 2021 from 10.0.2.2
vagrant@vagrant:~$  
```  
Создал файл config  
```  
$ cat config
Host vagrant
 HostName localhost
 IdentityFile ~/.ssh/id_rsa_1
 User vagrant
 Port 2222
 #StrictHostKeyChecking no
Host *
 User default_username
 IdentityFile ~/.ssh/id_rsa
 Protocol 2  
 ```  
Подключился  
```  
$ ssh vagrant
Welcome to Ubuntu 20.04.2 LTS (GNU/Linux 5.4.0-80-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Wed 15 Dec 2021 03:08:14 PM UTC

  System load:  0.03              Processes:               242
  Usage of /:   8.1% of 61.31GB   Users logged in:         1
  Memory usage: 69%               IPv4 address for dummy0: 10.2.2.2
  Swap usage:   6%                IPv4 address for eth0:   10.0.2.15

87 updates can be applied immediately.
42 of these updates are standard security updates.
To see these additional updates run: apt list --upgradable



This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Wed Dec 15 15:00:07 2021 from 10.0.2.2
vagrant@vagrant:~$  
```

7. **Соберите дамп трафика утилитой tcpdump в формате pcap, 100 пакетов. Откройте файл pcap в Wireshark.**  
  
https://github.com/NetVasiliy/Netology/blob/main/3.9.7.png  


