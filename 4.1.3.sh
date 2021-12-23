#!/usr/bin/env bash
i=0
  while (($i<5))
  do
    echo 'ya.ru' >> 413.log
curl http://ya.ru
  if (($? == 0))
  then

    date >> 413.log
    echo 'OK' >> 413.log
  else

    date >> 413.log
    echo 'NOT OK' >> 413.log
    fi

    echo 'mail.ru' >> 413.log
curl http://mail.ru
  if (($? == 0))
  then

    date >> 413.log
    echo 'OK' >> 413.log
  else

    date >> 413.log
    echo 'NOT OK' >> 413.log
    fi

    echo 'localhost' >> 413.log
curl http://localhost
  if (($? == 0))
  then

    date >> 413.log
    echo 'OK' >> 413.log
  else

    date >> 413.log
    echo 'NOT OK' >> 413.log
    fi
echo 'Connecting...'
let "i+=1"

  done
