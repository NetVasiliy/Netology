#!/usr/bin/env python3

import os

home_dir = '/home/vagrant/dz4.2/'
bash_command = ["cd " + home_dir, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
for result in result_os.split('\n'):
        if result.find('modified') != -1:
                prepare_result = result.replace('\tmodified:   ', '')
                print(home_dir + prepare_result)
