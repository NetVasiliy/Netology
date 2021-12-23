while ((1==1))
do
curl http://localhost:9101
if (($? != 0))
then
date > curl.log
echo 'Connecting...'
sleep 5
else
  echo '!!!OK!!!'
  break
fi
done