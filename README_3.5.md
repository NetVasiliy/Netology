# Домашнее задание к занятию "3.5. Файловые системы"

1. **Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.**  
Прочитал.  
***Разрежённый файл*** (англ. sparse file) — файл, в котором последовательности нулевых байтов[1] заменены на информацию об этих последовательностях (список дыр).  
2. **Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?**  
Не могут, потому что `inode+device` – однозначный идентификатор объекта в системе, А `inode` у них один.
3. **Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:**

    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ```

    **Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.**  
Сделал

4. **Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.**
  
      
    root@vagrant:~# fdisk /dev/sdb  
    Welcome to fdisk (util-linux 2.34).  
    Changes will remain in memory only, until you decide to write them.  
    Be careful before using the write command.  
      
    Device does not contain a recognized partition table.  
    Created a new DOS disklabel with disk identifier 0x308d1de2.  
     
    Command (m for help): g  
    Created a new GPT disklabel (GUID: 07ED6678-3875-254C-B0A4-A1A570CDE8ED).  
  
    Command (m for help): n  
    Partition number (1-128, default 1):  
    First sector (2048-5242846, default 2048):  
    Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242846, default 5242846): +2500M  
  
    Created a new partition 1 of type 'Linux filesystem' and of size 2.5 GiB.
6. **Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.**  
  


8. Соберите `mdadm` RAID1 на паре разделов 2 Гб.

9. Соберите `mdadm` RAID0 на второй паре маленьких разделов.

10. Создайте 2 независимых PV на получившихся md-устройствах.

11. Создайте общую volume-group на этих двух PV.

12. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

13. Создайте `mkfs.ext4` ФС на получившемся LV.

14. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.

15. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.

16. Прикрепите вывод `lsblk`.

17. Протестируйте целостность файла:

     ```bash
     root@vagrant:~# gzip -t /tmp/new/test.gz
     root@vagrant:~# echo $?
     0
     ```

18. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.

19. Сделайте `--fail` на устройство в вашем RAID1 md.

20. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.

21. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

     ```bash
     root@vagrant:~# gzip -t /tmp/new/test.gz
     root@vagrant:~# echo $?
     0
     ```

22. Погасите тестовый хост, `vagrant destroy`.

 
 ---

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Название файла Google Docs должно содержать номер лекции и фамилию студента. Пример названия: "1.1. Введение в DevOps — Сусанна Алиева".

Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. Чтобы это проверить, откройте ссылку в браузере в режиме инкогнито.

[Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop)

[Как запустить chrome в режиме инкогнито ](https://support.google.com/chrome/answer/95464?co=GENIE.Platform%3DDesktop&hl=ru)

[Как запустить  Safari в режиме инкогнито ](https://support.apple.com/ru-ru/guide/safari/ibrw1069/mac)

Любые вопросы по решению задач задавайте в чате Slack.

---
