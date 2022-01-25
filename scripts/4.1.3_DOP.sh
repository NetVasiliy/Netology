#!/usr/bin/env bash
i=0
array_hosts=("ya.ru" "mail.ru" "localhost")

  while (($i<5))
  do

    for ah in ${array_hosts[@]}
      do
      echo $ah >> 413_DOP.log
      date >> 413_DOP.log
curl $ah
  if (($? == 0))
  then
      echo 'OK' >> 413_DOP.log
  else
      echo 'NOT OK' >> 413_DOP.log
    fi
      done

echo 'Connecting...'
let "i+=1"
  done