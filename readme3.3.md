#В виде результата напишите текстом ответы на вопросы и каким образом эти ответы были получены. 

1. **Какой системный вызов делает команда `cd`? В прошлом ДЗ мы выяснили, что `cd` не является самостоятельной  программой, это `shell builtin`, поэтому запустить `strace` непосредственно на `cd` не получится. Тем не менее, вы можете запустить `strace` на `/bin/bash -c 'cd /tmp'`. В этом случае вы увидите полный список системных вызовов, которые делает сам `bash` при старте. Вам нужно найти тот единственный, который относится именно к `cd`.**   
  

    chdir("/tmp")  

2. **Попробуйте использовать команду `file` на объекты разных типов на файловой системе. Например:**
    ```bash
    vagrant@netology1:~$ file /dev/tty
    /dev/tty: character special (5/0)
    vagrant@netology1:~$ file /dev/sda
    /dev/sda: block special (8/0)
    vagrant@netology1:~$ file /bin/bash
    /bin/bash: ELF 64-bit LSB shared object, x86-64
    ```
    **Используя `strace` выясните, где находится база данных `file` на основании которой она делает свои догадки.**  
     

 
        strace /bin/bash -c 'file /dev/tty'  
        read(3, "# Magic local data for file(1) c"..., 4096) = 111  
        openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3  

   /usr/share/misc/magic.mgc


3. **Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).**  
  
Создадим файл do_not_delete  
Наполним с помощью vim и закроем  
Откроем его во второй консоли через F3 в mc  
С помощью lsof ищем процесс в первой консоли:  
  
    sudo lsof | grep do_not_delete  
    mc        1296                          root   10r      REG              253,0      334     131137 /home/vagrant/do_not_delete  
Запомним его PID. 1296. И удалим  
  
    rm do_not_delete  
Опять ищем с помощью lsof:  
  
    sudo lsof | grep do_not_delete  
    mc        1296                          root   10r      REG              253,0      334     131137 /home/vagrant/do_not_delete (deleted)  
Файл помечен как "deleted"  
Запустим BASH как root: `sudo bash`. и запишем поверх содержимого пустоту:  
  
    echo '' >/proc/1296/fd/3

Теперь команда  

	sudo lsof | grep do_not_delete
ничего не выдаст. PROFIT!

4. **Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?**    
Зомби не занимают памяти (как процессы-сироты), но блокируют записи в таблице процессов, размер которой ограничен для каждого пользователя и системы в целом.  

5. **В iovisor BCC есть утилита `opensnoop`:**
    ```bash
    root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
    /usr/sbin/opensnoop-bpfcc
    ```
    **На какие файлы вы увидели вызовы группы `open` за первую секунду работы утилиты? Воспользуйтесь пакетом `bpfcc-tools` для Ubuntu 20.04. Дополнительные [сведения по установке](https://github.com/iovisor/bcc/blob/master/INSTALL.md).**  
Запустил: sudo opensnoop-bpfcc  
  

        vagrant@vagrant:~$ sudo opensnoop-bpfcc
        PID    COMM               FD ERR PATH
        591    irqbalance          6   0 /proc/interrupts
        591    irqbalance          6   0 /proc/stat
        591    irqbalance          6   0 /proc/irq/20/smp_affinity
        591    irqbalance          6   0 /proc/irq/0/smp_affinity
        591    irqbalance          6   0 /proc/irq/1/smp_affinity
        591    irqbalance          6   0 /proc/irq/8/smp_affinity
        591    irqbalance          6   0 /proc/irq/12/smp_affinity
        591    irqbalance          6   0 /proc/irq/14/smp_affinity
        591    irqbalance          6   0 /proc/irq/15/smp_affinity
        811    vminfo              4   0 /var/run/utmp
        574    dbus-daemon        -1   2 /usr/local/share/dbus-1/system-services
        574    dbus-daemon        18   0 /usr/share/dbus-1/system-services
        574    dbus-daemon        -1   2 /lib/dbus-1/system-services
        574    dbus-daemon        18   0 /var/lib/snapd/dbus-1/system-services/  

     

6. **Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.**  
  
  
        uname()  

Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version,
       domainname}.
  


7. **Чем отличается последовательность команд через `;` и через `&&` в bash? Например:**
    ```bash
    root@netology1:~# test -d /tmp/some_dir; echo Hi
    Hi
    root@netology1:~# test -d /tmp/some_dir && echo Hi
    root@netology1:~#
    ```
    **Есть ли смысл использовать в bash `&&`, если применить `set -e`?**  
`;`  - позволяет запускать несколько команд за один раз, и выполнение команды происходит последовательно.  
`&&` -  Оператор AND (&&) будет выполнять вторую команду только в том случае, если при выполнении первой состояние выхода первой команды равно “0”  
Смысла использовать `&&` нет, т.к.`set -e` тоже прекратит дальнейшее выполнение скрипта при ошибке.  
  

8.**Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?** 
  
`-e` - прекращает выполнение скрипта если команда завершилась ошибкой, выводит в stderr строку с ошибкой  
`-u` - прекращает выполнение скрипта, если встретилась несуществующая переменная  
`-x` - выводит выполняемые команды в stdout перед выполненинем  
`-o` pipefail возвращает код возврата набора/последовательности команд, ненулевой при последней команды или 0 для успешного выполнения команд.  
  
Это поможет при проверке скриптов.  
`-x` покажет, как скрипт работал  
`-u` покажет, если не задана какая-то переменная  
`-e` прекратит выполнение скрипта при ошибке  
`-o` pipefail покажет на какой команде скрипт упал  


  
9. **Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps` ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).**  
  

    	ps -ax -o stat >ps_stat  

    	root@vagrant:/home/vagrant# grep S ps_stat -c  
    	59  
    	root@vagrant:/home/vagrant# grep I ps_stat -c  
    	49

`S` - спящий процесс  
`I` - фоновый процесс  
`s` - is a session leader  
`l` - is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)  

 