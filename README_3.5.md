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
  
      
    fdisk /dev/sdb  
    ...  
    lsblk  
    NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT  
    sda                    8:0    0   64G  0 disk  
    ├─sda1                 8:1    0  512M  0 part /boot/efi  
    ├─sda2                 8:2    0    1K  0 part  
    └─sda5                 8:5    0 63.5G  0 part  
      ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /  
      └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]  
    sdb                    8:16   0  2.5G  0 disk  
    ├─sdb1                 8:17   0    2G  0 part  
    └─sdb2                 8:18   0  511M  0 part  
    sdc                    8:32   0  2.5G  0 disk  

5. **Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.**  
     

    root@vagrant:~# root@vagrant:~# sfdisk -d /dev/sdb >sdb_table  
    root@vagrant:~# cat sdb_table  
    label: dos  
    label-id: 0x052a8287   
    device: /dev/sdb  
    unit: sectors  
  
    /dev/sdb1 : start=        2048, size=     4194304, type=83  
    /dev/sdb2 : start=     4196352, size=     1046528, type=83  
  
    root@vagrant:~# sfdisk /dev/sdc <sdb_table  
  
    lsblk  
    NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT  
    sda                    8:0    0   64G  0 disk  
    ├─sda1                 8:1    0  512M  0 part /boot/efi  
    ├─sda2                 8:2    0    1K  0 part  
    └─sda5                 8:5    0 63.5G  0 part  
      ├─vgvagrant-root   253:0    0 62.6G  0 lvm  /  
      └─vgvagrant-swap_1 253:1    0  980M  0 lvm  [SWAP]  
    sdb                    8:16   0  2.5G  0 disk  
    ├─sdb1                 8:17   0    2G  0 part  
    └─sdb2                 8:18   0  511M  0 part  
    sdc                    8:32   0  2.5G  0 disk  
    ├─sdc1                 8:33   0    2G  0 part  
    └─sdc2                 8:34   0  511M  0 part  

6. **Соберите `mdadm` RAID1 на паре разделов 2 Гб.**  
  
 
    mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1  
    root@vagrant:~# lsblk  
    NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT  
    sda                    8:0    0   64G  0 disk  
    ├─sda1                 8:1    0  512M  0 part  /boot/efi  
    ├─sda2                 8:2    0    1K  0 part  
    └─sda5                 8:5    0 63.5G  0 part  
      ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /  
      └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]  
    sdb                    8:16   0  2.5G  0 disk  
    ├─sdb1                 8:17   0    2G  0 part  
    │ └─md0                9:0    0    2G  0 raid1  
    └─sdb2                 8:18   0  511M  0 part  
    sdc                    8:32   0  2.5G  0 disk   
    ├─sdc1                 8:33   0    2G  0 part  
    │ └─md0                9:0    0    2G  0 raid1  
    └─sdc2                 8:34   0  511M  0 part  



7. **Соберите `mdadm` RAID0 на второй паре маленьких разделов.**  
    

    mdadm --create /dev/md1 --level=0 --raid-devices=2 /dev/sdb2 /dev/sdc2

8. **Создайте 2 независимых PV на получившихся md-устройствах.**  
  
    
    pvcreate -v /dev/md0  
    pvcreate -v /dev/md1  
      
    root@vagrant:~# pvs 
      PV         VG        Fmt  Attr PSize    PFree  
      /dev/md0             lvm2 ---    <2.00g   <2.00g  
      /dev/md1             lvm2 ---  1018.00m 1018.00m  
      /dev/sda5  vgvagrant lvm2 a--   <63.50g       0  


9. **Создайте общую volume-group на этих двух PV.**  
  
  
    root@vagrant:~# vgcreate vg_3_5 /dev/md0 /dev/md1  
      Volume group "vg_3_5" successfully created  
    root@vagrant:~# vgs  
      VG        #PV #LV #SN Attr   VSize   VFree  
      vg_3_5      2   0   0 wz--n-  <2.99g <2.99g  
      vgvagrant   1   2   0 wz--n- <63.50g     0   


10. **Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.**  
  
  
    lvcreate -L 100M -n lv1_35 vg_3_5 /dev/md1  
    lvs  
      LV     VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert  
      lv1_35 vg_3_5    -wi-a----- 100.00m  
      root   vgvagrant -wi-ao---- <62.54g  
      swap_1 vgvagrant -wi-ao---- 980.00m  


11. **Создайте `mkfs.ext4` ФС на получившемся LV.**  
  
  
    mkfs.ext4 -L new35 /dev/vg_3_5/lv1_35  
    blkid  
    /dev/mapper/vg_3_5-lv1_35: LABEL="new35" UUID="e9b2bf8b-af82-4929-81a6-2662c35ff757" TYPE="ext4"  


12. **Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.**  
  
  
    mount /dev/vg_3_5/lv1_35 /tmp/new   

    root@vagrant:~# mount |grep lv1_35  
    /dev/mapper/vg_3_5-lv1_35 on /tmp/new type ext4 (rw,relatime,stripe=256)  


13. **Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.**  
    

    ls /tmp/new  
    lost+found  test.gz  


14. Прикрепите вывод `lsblk`.
  
  
      NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT  
  
    sda                    8:0    0   64G  0 disk  
    ├─sda1                 8:1    0  512M  0 part  /boot/efi  
    ├─sda2                 8:2    0    1K  0 part  
    └─sda5                 8:5    0 63.5G  0 part  
      ├─vgvagrant-root   253:0    0 62.6G  0 lvm   /  
      └─vgvagrant-swap_1 253:1    0  980M  0 lvm   [SWAP]  
    sdb                    8:16   0  2.5G  0 disk  
    ├─sdb1                 8:17   0    2G  0 part  
    │ └─md0                9:0    0    2G  0 raid1  
    └─sdb2                 8:18   0  511M  0 part  
      └─md1                9:1    0 1018M  0 raid0  
        └─vg_3_5-lv1_35  253:2    0  100M  0 lvm   /tmp/new  
    sdc                    8:32   0  2.5G  0 disk  
    ├─sdc1                 8:33   0    2G  0 part  
    │ └─md0                9:0    0    2G  0 raid1  
    └─sdc2                 8:34   0  511M  0 part  
      └─md1                9:1    0 1018M  0 raid0  
         └─vg_3_5-lv1_35  253:2    0  100M  0 lvm   /tmp/new  


15. **Протестируйте целостность файла:**  
  
  
    root@vagrant:~# gzip -t /tmp/new/test.gz  
    root@vagrant:~# echo $?  



16. **Используя pvmove, переместите содержимое PV с RAID0 на RAID1.**  
     
    
    root@vagrant:~# pvmove /dev/md1 /dev/md0
    /dev/md1: Moved: 20.00%
    /dev/md1: Moved: 100.00%  
    

17. **Сделайте `--fail` на устройство в вашем RAID1 md.**  
  
  
    root@vagrant:~# mdadm --fail /dev/md0 /dev/sdb1  
    mdadm: set /dev/sdb1 faulty in /dev/md0  


18. **Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.**  
  
  
    root@vagrant:~# dmesg |grep md0  

    [ 2308.856443] md/raid1:md0: not clean -- starting background reconstruction
    [ 2308.856445] md/raid1:md0: active with 2 out of 2 mirrors
    [ 2308.856458] md0: detected capacity change from 0 to 2144337920
    [ 2308.859153] md: resync of RAID array md0
    [ 2319.230942] md: md0: resync done.
    [10441.325402] md/raid1:md0: Disk failure on sdb1, disabling device.
               md/raid1:md0: Operation continuing on 1 devices.  
  
   

19. **Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:**  


     ```bash
     root@vagrant:~# gzip -t /tmp/new/test.gz
     root@vagrant:~# echo $?
     0
     ```
  
Протестировал  

21. Погасите тестовый хост, `vagrant destroy`.

 Убил.
 