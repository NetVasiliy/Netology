#!/usr/bin/env bash
i=0
  while ((1==1))
  do

    echo 'ya.ru' >> 414.log
curl http://ya.ru
  if (($? == 0))
  then
    date >> 414.log
    echo 'OK' >> 414.log
  else
    echo 'ya.ru' >> ERROR414.log
    break
    fi

    echo 'mail.ru' >> 413.log
curl http://mail.ru
  if (($? == 0))
  then
    date >> 413.log
    echo 'OK' >> 413.log
  else
    echo 'mail.ru' >> ERROR414.log
    break
    fi

    echo 'localhost' >> 413.log
curl http://localhost
  if (($? == 0))
  then
    date >> 413.log
    echo 'OK' >> 413.log
  else
    echo 'localhost' >> ERROR414.log
    break
    fi
sleep 1
echo 'Connecting...'
  done
