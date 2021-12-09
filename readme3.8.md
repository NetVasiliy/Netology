# Домашнее задание к занятию "3.8. Компьютерные сети, лекция 3"

1. **Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP**
```
telnet route-views.routeviews.org
Username: rviews
show ip route x.x.x.x/32
show bgp x.x.x.x/32
```  
Подключился, команды попробовал. Опытным путем выяснил, что маску писать не нужно.  

2. **Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации.**  
  
Создал `dummy0`:  
```root@vagrant:/etc/network# ifconfig
dummy0: flags=195<UP,BROADCAST,RUNNING,NOARP>  mtu 1500
        inet 10.2.2.2  netmask 255.255.255.255  broadcast 10.2.2.2
        inet6 fe80::e44c:28ff:fe06:d3a  prefixlen 64  scopeid 0x20<link>
        ether e6:4c:28:06:0d:3a  txqueuelen 1000  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2  bytes 289 (289.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.2.15  netmask 255.255.255.0  broadcast 10.0.2.255
        inet6 fe80::a00:27ff:fe73:60cf  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:73:60:cf  txqueuelen 1000  (Ethernet)
        RX packets 2435  bytes 227993 (227.9 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 2198  bytes 285215 (285.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 3557  bytes 4850999 (4.8 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3557  bytes 4850999 (4.8 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0  
```  
Добавил временный статический маршрут через `ip route add 172.16.0.0/16 dev dummy0`:  
```  
root@vagrant:~# ip -br route
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100
169.254.0.0/16 dev dummy0 scope link metric 1000  

root@vagrant:~# ip route add 172.16.0.0/16 dev dummy0  

root@vagrant:~# ip -br route
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100
169.254.0.0/16 dev dummy0 scope link metric 1000
172.16.0.0/16 dev dummy0 scope link  
```  
Вот он: `172.16.0.0/16 dev dummy0 scope link`  


3. **Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров.**  
  
```  
root@vagrant:/etc/bird# ss -tpnl4
State      Recv-Q     Send-Q          Local Address:Port            Peer Address:Port     Process
LISTEN     0          4096                  0.0.0.0:111                  0.0.0.0:*         users:(("rpcbind",pid=588,fd=4),("systemd",pid=1,fd=52))
LISTEN     0          511                   0.0.0.0:80                   0.0.0.0:*         users:(("nginx",pid=821,fd=6),("nginx",pid=820,fd=6),("nginx",pid=819,fd=6))
LISTEN     0          4096            127.0.0.53%lo:53                   0.0.0.0:*         users:(("systemd-resolve",pid=591,fd=13))
LISTEN     0          128                   0.0.0.0:22                   0.0.0.0:*         users:(("sshd",pid=879,fd=3))
LISTEN     0          5                   127.0.0.1:631                  0.0.0.0:*         users:(("cupsd",pid=3741,fd=7))
LISTEN     0          4096                127.0.0.1:8125                 0.0.0.0:*         users:(("netdata",pid=866,fd=27))
LISTEN     0          4096                  0.0.0.0:19999                0.0.0.0:*         users:(("netdata",pid=866,fd=4))  
```  
80 - HTTP  
53 - DNS
22 -SSH


4. **Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?**  
  
```  
root@vagrant:/etc/bird# ss -upnl4
State         Recv-Q        Send-Q                Local Address:Port                Peer Address:Port       Process
UNCONN        0             0                           0.0.0.0:631                      0.0.0.0:*           users:(("cups-browsed",pid=3744,fd=7))
UNCONN        0             0                           0.0.0.0:39826                    0.0.0.0:*           users:(("avahi-daemon",pid=633,fd=14))
UNCONN        0             0                         127.0.0.1:8125                     0.0.0.0:*           users:(("netdata",pid=866,fd=23))
UNCONN        0             0                     127.0.0.53%lo:53                       0.0.0.0:*           users:(("systemd-resolve",pid=591,fd=12))
UNCONN        0             0                    10.0.2.15%eth0:68                       0.0.0.0:*           users:(("systemd-network",pid=394,fd=20))
UNCONN        0             0                           0.0.0.0:111                      0.0.0.0:*           users:(("rpcbind",pid=588,fd=5),("systemd",pid=1,fd=53))
UNCONN        0             0                           0.0.0.0:5353                     0.0.0.0:*           users:(("avahi-daemon",pid=633,fd=12))
UNCONN        0             0                         127.0.0.1:323                      0.0.0.0:*           users:(("chronyd",pid=792,fd=5))  
```  
53 - DNS  
68 - DHCP  
631 - PRINT  



5. **Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали.**  
  


