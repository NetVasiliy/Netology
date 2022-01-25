#!/usr/bin/env bash
while ((1==1))
do
curl http://localhost:9100
if (($? != 0))
then
date > curl.log
echo 'Connecting...'
sleep 5
else
break
fi
done
echo '!!!OK!!!'