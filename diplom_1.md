# Курсовая работа по итогам модуля "DevOps и системное администрирование"

Курсовая работа необходима для проверки практических навыков, полученных в ходе прохождения курса "DevOps и системное администрирование".

Мы создадим и настроим виртуальное рабочее место. Позже вы сможете использовать эту систему для выполнения домашних заданий по курсу

## Задание

1. **Создайте виртуальную машину Linux.**  
  
![avatar](https://github.com/NetVasiliy/Netology/blob/main/media/D_1.PNG)  

2. **Установите ufw и разрешите к этой машине сессии на порты 22 и 443, при этом трафик на интерфейсе localhost (lo) должен ходить свободно на все порты.**  
  
```  
vagrant@vagrant:~$ sudo ufw enable
Command may disrupt existing ssh connections. Proceed with operation (y|n)? y
Firewall is active and enabled on system startup
vagrant@vagrant:~$ sudo ufw show added
Added user rules (see 'ufw status' for running firewall):
ufw allow 22
ufw allow 443
ufw allow in on lo0
ufw allow out on lo0  
```  

3. **Установите hashicorp vault ([инструкция по ссылке](https://learn.hashicorp.com/tutorials/vault/getting-started-install?in=vault/getting-started#install-vault)).**  
  
```  
vagrant@vagrant:~$ curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
OK  
vagrant@vagrant:~$ sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"  
...  
Reading package lists... Done  
vagrant@vagrant:~$ sudo apt-get update && sudo apt-get install vault  
...  
writing new private key to 'tls.key'
-----
Vault TLS key and self-signed certificate have been generated in '/opt/vault/tls'.  
  ```  
Проверяем:  
```  
vagrant@vagrant:~$ vault
Usage: vault <command> [args]

Common commands:
    read        Read data and retrieves secrets  
    ...    
   ```

4. **Cоздайте центр сертификации по инструкции ([ссылка](https://learn.hashicorp.com/tutorials/vault/pki-engine?in=vault/secrets-management)) и выпустите сертификат для использования его в настройке веб-сервера nginx (срок жизни сертификата - месяц).**  
  
Стартуем vault в другом терминале от root:  
```  
root@vagrant:~# vault server -dev -dev-root-token-id root
==> Vault server configuration:

             Api Address: http://127.0.0.1:8200
                     Cgo: disabled
         Cluster Address: https://127.0.0.1:8201
              Go Version: go1.17.5
              Listener 1: tcp (addr: "127.0.0.1:8200", cluster address: "127.0.0.1:8201", max_request_duration: "1m30s", max_request_size: "33554432", tls: "disabled")
               Log Level: info
                   Mlock: supported: true, enabled: false
           Recovery Mode: false
                 Storage: inmem
                 Version: Vault v1.9.2
             Version Sha: f4c6d873e2767c0d6853b5d9ffc77b0d297bfbdf

==> Vault server started! Log data will stream in below  
```
  
Настраиваем по инструкции для сайта example.com, но меняем время действия на 744 часа:  
```  
root@vagrant:~# export VAULT_ADDR=http://127.0.0.1:8200
root@vagrant:~# export VAULT_TOKEN=root  
root@vagrant:~# vault secrets enable pki
Success! Enabled the pki secrets engine at: pki/  
root@vagrant:~# vault secrets tune -max-lease-ttl=744h pki
Success! Tuned the secrets engine at: pki/  
root@vagrant:~# vault write -field=certificate pki/root/generate/internal \
> common_name="example.com" \
> ttl=744h > CA_cert.crt  
root@vagrant:~# vault write pki/config/urls \
> issuing_certificates="$VAULT_ADDR/v1/pki/ca" \
> crl_distribution_points="$VAULT_ADDR/v1/pki/crl"
Success! Data written to: pki/config/urls  
root@vagrant:~# vault secrets enable -path=pki_int pki
Success! Enabled the pki secrets engine at: pki_int/
root@vagrant:~# vault secrets tune -max-lease-ttl=744h pki_int
Success! Tuned the secrets engine at: pki_int/  
root@vagrant:~# vault write -format=json pki_int/intermediate/generate/internal \
> common_name="example.com Intermediate Authority" \
> | jq -r '.data.csr' > pki_intermediate.csr  
root@vagrant:~# vault write -format=json pki/root/sign-intermediate csr=@pki_intermediate.csr \
> format=pem_bundle ttl="744h" \
> | jq -r '.data.certificate' > intermediate.cert.pem  
root@vagrant:~# vault write pki_int/intermediate/set-signed certificate=@intermediate.cert.pem
Success! Data written to: pki_int/intermediate/set-signed  
root@vagrant:~# vault write pki_int/roles/example-dot-com \
> allowed_domains="example.com" \
> allow_subdomains=true \
> max_ttl="744h"
Success! Data written to: pki_int/roles/example-dot-com  
```  
Создание сертификатов для test.example.com  
```  
root@vagrant:~# vault write -format=json pki_int/issue/example-dot-com common_name="test.example.com" ttl="720h" > test.
example.com.crt  
root@vagrant:~# cat test.example.com.crt | jq -r .data.certificate > test.example.com.crt.pem
root@vagrant:~# cat test.example.com.crt | jq -r .data.issuing_ca >> test.example.com.crt.pem
root@vagrant:~# cat test.example.com.crt | jq -r .data.private_key > test.example.com.crt.key  
  
  ```
  
  

5. **Установите корневой сертификат созданного центра сертификации в доверенные в хостовой системе.**  
  
![avatar](https://github.com/NetVasiliy/Netology/blob/main/media/D_5.png)  

6. **Установите nginx.**  
  
Установка и проверка статуса:  
```  
vagrant@vagrant:~$ sudo apt install nginx  
...   
vagrant@vagrant:~$ systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2022-01-26 12:20:28 UTC; 1min 11s ago
       Docs: man:nginx(8)
   Main PID: 4908 (nginx)
      Tasks: 3 (limit: 1071)
     Memory: 4.7M
     CGroup: /system.slice/nginx.service
             ├─4908 nginx: master process /usr/sbin/nginx -g daemon on; master_process on;
             ├─4909 nginx: worker process
             └─4910 nginx: worker process

Jan 26 12:20:28 vagrant systemd[1]: Starting A high performance web server and a reverse proxy server...
Jan 26 12:20:28 vagrant systemd[1]: Started A high performance web server and a reverse proxy server.  
```

7. **По инструкции ([ссылка](https://nginx.org/en/docs/http/configuring_https_servers.html)) настройте nginx на https, используя ранее подготовленный сертификат:**
  - **можно использовать стандартную стартовую страницу nginx для демонстрации работы сервера;**
  - **можно использовать и другой html файл, сделанный вами;**  
  
Перекинул фалы ключа и сертификата в папку /tmp.  
Создал файл /var/www/html/index.html.
В файл /etc/nginx/sites-available/default добавил секцию:  
```  
server {
    listen              443 ssl;
    server_name         www.example.com;
    ssl_certificate     /tmp/test.example.com.crt.pem;
    ssl_certificate_key /tmp/test.example.com.crt.key;
    ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers         HIGH:!aNULL:!MD5;
    root /var/www/html;
    index index.html;
}  
```

8. **Откройте в браузере на хосте https адрес страницы, которую обслуживает сервер nginx.**  
  
На локальной машине прописал в файле `hosts`  
`127.0.0.1	test.example.com`  
и открыл сайт
![avatar](https://github.com/NetVasiliy/Netology/blob/main/media/D_8.png)  

9. **Создайте скрипт, который будет генерировать новый сертификат в vault:**
  - **генерируем новый сертификат так, чтобы не переписывать конфиг nginx;**
  - **перезапускаем nginx для применения нового сертификата.**  
  
Скрипт такой:  
```  
#!/usr/bin/env bash  
export VAULT_ADDR=http://127.0.0.1:8200
export VAULT_TOKEN=root  
  
vault write -format=json pki_int/issue/example-dot-com common_name="test.example.com" ttl="720h" > /tmp/test.example.com.crt  
cat /tmp/test.example.com.crt | jq -r .data.certificate > /tmp/test.example.com.crt.pem
cat /tmp/test.example.com.crt | jq -r .data.issuing_ca >> /tmp/test.example.com.crt.pem
cat /tmp/test.example.com.crt | jq -r .data.private_key > /tmp/test.example.com.crt.key  
systemctl restart nginx  
```
После запуска скрипта сайт продолжает работать, но меняется дата сертификата:  
  
![avatar](https://github.com/NetVasiliy/Netology/blob/main/media/D_9.png)  

10. **Поместите скрипт в crontab, чтобы сертификат обновлялся какого-то числа каждого месяца в удобное для вас время.**  
  
`root@vagrant:/tmp# crontab -e`  
Добавил строку:  
`1 1 1 * * /tmp/vault.sh`  
Сертификат будет обновлятся 1 числа каждого месяца в 1:01  
Для проверки заменил на запуск каждую минуту:  
`* * * * * /tmp/vault.sh`  
Результат есть:  
  
![avatar](https://github.com/NetVasiliy/Netology/blob/main/media/D_10.png)



## Результат

Результатом курсовой работы должны быть снимки экрана или текст:

- Процесс установки и настройки ufw
- Процесс установки и выпуска сертификата с помощью hashicorp vault
- Процесс установки и настройки сервера nginx
- Страница сервера nginx в браузере хоста не содержит предупреждений 
- Скрипт генерации нового сертификата работает (сертификат сервера ngnix должен быть "зеленым")
- Crontab работает (выберите число и время так, чтобы показать что crontab запускается и делает что надо)

## Как сдавать курсовую работу

Курсовую работу выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. 
Ссылка на инструкцию [Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop).
