### Как сдавать задания

Привет! 

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы.

---


# Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

## Обязательные задания

1. **Есть скрипт**:
	```bash
	a=1
	b=2
	c=a+b
	d=$a+$b
	e=$(($a+$b))
	```
    * Какие значения переменным c,d,e будут присвоены и почему?  
   c: `a+b` потому, что это строка состоящая из единой записи.  
   d: `1+2` потому, что это строка, где подставлены переменные a=1 и b=2.  
   e: `3` потому, что это выражение за счет ((...)) воспринимается как арифметическое действие.
    

2. **На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным. В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:**
	```bash
	while ((1==1)
	do
	curl https://localhost:4757
	if (($? != 0))
	then
	date >> curl.log
	fi
	done
	```  
   
Первое надо закрыть скобку `)` в цикле, второе убрать дозапись в файл `>` и наконец предусмотреть выход `else break` , если сервис станет доступен. При этом в файле `curl.log` останется последний момент, когда сервис недоступен.  
```bash  
    while ((1==1))
    do
curl http://localhost:9100
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
```

3. **Необходимо написать скрипт, который проверяет доступность трёх IP: 192.168.0.1, 173.194.222.113, 87.250.250.242 по 80 порту и записывает результат в файл log. Проверять доступность необходимо пять раз для каждого узла.** 
  
Использовал хосты не из задания, а реальные. ya.ru, mail.ru, localhost.
  
```bash  
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
  
  ```  


4. **Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается**  
  
```bash  
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
      break 2 #break N прерывает цикл, стоящий на N уровней выше -это было познавательно.
  fi
     done
    sleep 1
echo 'Connecting...'
  done
 
  ```  


