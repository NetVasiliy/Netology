# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

1. **На лекции мы познакомились с [node_exporter](https://github.com/prometheus/node_exporter/releases). В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой [unit-файл](https://www.freedesktop.org/software/systemd/man/systemd.service.html) для node_exporter:**  

    * поместите его в автозагрузку,
    * предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на `systemctl cat cron`),
    * удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.  
     
    Поьзовалься инструкцией отсюда: https://www.dmosk.ru/instruktions.php?object=prometheus-linux   
    Ставил последнюю версию 1.3.0


         wget https://github.com/prometheus/node_exporter/releases/download/v1.3.0/node_exporter-1.3.0.linux-amd64.tar.gz  
 ***unit-файл***  node_exporter.service  
  
  
  
         root@vagrant:~/node_exporter-1.3.0.linux-amd64# cat /etc/systemd/system/node_exporter.service  
         [Unit]  
         Description=Node Exporter Service  
         After=network.target  
  
         [Service]  
         User=nodeusr  
         Group=nodeusr  
         Type=simple  
         ExecStart=/usr/local/bin/node_exporter $EXTRA_OPTS  
         ExecReload=/bin/kill -HUP $MAINPID  
         Restart=on-failure  
  
         [Install]  
         WantedBy=multi-user.target  
  
После перезагрузки сервис поднялся PID=736  
После команды `systemctl stop node_exporter` сервис пропал из процессов.  
После команды `systemctl start node_exporter` сервис поднялся PID=2283.  

      

2. **Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.**  
  
  
Я бы выбрал:  
* ***node_cpu_seconds_total*** - Seconds the CPUs spent in each mode.  
* ***node_memory_MemAvailable_bytes*** - Memory information field MemAvailable_bytes.  
* ***node_memory_MemFree_bytes*** - Memory information field MemFree_bytes.  
* ***node_filesystem_avail_bytes*** - Filesystem space available to non-root users in bytes.  
* ***node_disk_io_now*** - The number of I/Os currently in progress.  
* ***node_network_receive_errs_total*** -  Network device statistic receive_errs.  
* ***node_network_transmit_errs_total*** -  Network device statistic transmit_errs.  
* 

3. ***Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`). После успешной установки:***
    * в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0`,
    * добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

    ```bash
    config.vm.network "forwarded_port", guest: 19999, host: 19999
    ```

    После успешной перезагрузки в браузере *на своем ПК* (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.  
  
  
Выполнено:    

            http://localhost:19999/#menu_system_submenu_cpu;theme=slate

4. ***Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?***  
  
Можно:    

            dmesg |grep virtua  
        [    0.003858] CPU MTRRs all blank - virtualized system.  
        [    0.046170] Booting paravirtualized kernel on KVM  
        [    3.175935] systemd[1]: Detected virtualization oracle.  


5. ***Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?***  
  
Системное ограничение - это максимальное количество файловых дескрипторов.    

            /sbin/sysctl -n fs.nr_open  
            1048576  
  
Другое ограниечение в системе - это "жесткое" ограничение `ulimit`:   

            ulimit -Hn  
            1048576

6. **Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.**  
  
  
        Первый терминал:  
        unshare -f --pid --mount-proc sleep 60m  
        Другой терминал:  
        ps aux |grep sleep  
        root        3275  0.0  0.0   8080   592 pts/1    S+   15:13   0:00 unshare -f --pid --mount-proc sleep 60m  
        root        3276  0.0  0.0   8076   528 pts/1    S+   15:13   0:00 sleep 60m  
  
        nsenter --target 3276 --pid --mount  
        ps aux  
        USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND  
        root           1  0.0  0.0   8076   528 pts/1    S+   15:13   0:00 sleep 60m  
        root           2  0.0  0.1   9836  4064 pts/3    S    15:18   0:00 -bash  
        root          11  0.0  0.1  11492  3504 pts/3    R+   15:18   0:00 ps aux  
  
Видно, что `sleep` работает под PID=1
        

7. **Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?**  
  
`:(){ :|:& };:` - Логическая бомба (известная также как fork bomb), забивающая память системы, что в итоге приводит к её зависанию.  
Этот Bash код создаёт функцию, которая запускает ещё два своих экземпляра, которые, в свою очередь снова запускают эту функцию и так до тех пор, пока этот процесс не займёт всю физическую память компьютера, и он просто не зависнет.  
  
  
        dmesg |grep fork  
        [ 8057.269666] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-7.scope  
        [ 8066.742284] cgroup: fork rejected by pids controller in /user.slice/user-1000.slice/session-4.scope  
  
`cgroup` - обеспечивают механизм для агрегирования множества
задач и их будущих потомков в иерархические группы с определенным поведением.  
По умолчанию `ulimit -u` покажет число 7714.  
Для изменения в сессии можно задать вручную `ulimit- u [число]`, для постоянного надо редактировать файл `/etc/security/limits.conf`    


 
