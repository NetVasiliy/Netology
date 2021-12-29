#!/usr/bin/env python3

import os
import socket
import time

host_list2 = {'google.com': 'null', 'ya.ru':'null', 'mail.google.com': 'null', 'drive.google.com':'null'}
while (1==1):
    for i in host_list2.keys():
            print(i + ' - ' + socket.gethostbyname(i))
            current_ip = socket.gethostbyname(i)
            if current_ip != host_list2[i]:
                    old_ip = host_list2[i]
                    host_list2[i] = current_ip
                    print('[ERROR]: ' + i + ' IP mismatch ' + old_ip + ' ' + current_ip)
    time.sleep(2)