while ((1==1))
do
curl http://localhost:9100
if (($? != 0))
then
date > curl.log
else exit
fi
done