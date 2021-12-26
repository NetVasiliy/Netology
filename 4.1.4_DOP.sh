#!/usr/bin/env bash

array_hosts=("ya.ru" "mail.ru" "localhost")
  while ((1==1))
  do
    for ah in ${array_hosts[@]}
      do
      echo $ah >> 414_DOP.log
      date >> 414_DOP.log
curl $ah
  if (($? == 0))
    then
      echo 'OK' >> 414_DOP.log
    else
    echo $ah >> ERROR414_DOP.log
    date >> ERROR414_DOP.log
    break 2
    #’очу знать почему break не срабатывает, а 2 срабатывает...
    fi
     done
    sleep 1
echo 'Connecting...'
  done
