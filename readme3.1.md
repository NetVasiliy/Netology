#В виде результата напишите текстом ответы на вопросы и каким образом эти ответы были получены. 

**5. Ознакомьтесь с графическим интерфейсом VirtualBox, посмотрите как выглядит виртуальная машина, которую создал для вас Vagrant, какие аппаратные ресурсы ей выделены. Какие ресурсы выделены по-умолчанию?**  

 Оператива 1024  
 HDD 64Гб

**6. Ознакомьтесь с возможностями конфигурации VirtualBox через Vagrantfile: документация. Как добавить оперативной памяти или ресурсов процессора виртуальной машине?**     
  2 способа:

   1. через файл Vagrantfile
   2. Через VirtualBox  
  
**8. Ознакомиться с разделами man bash, почитать о настройках самого bash:**  

***какой переменной можно задать длину журнала history, и на какой строчке manual это описывается?***  

Line 687  
HISTFILESIZE
              The  maximum number of lines contained in the history file.  When this variable is assigned a value, the history file is truncated, if necessary, to con‐
              tain no more than that number of lines by removing the oldest entries.  The history file is also truncated to this size after writing it when a shell ex‐
              its.  If the value is 0, the history file is truncated to zero size.  Non-numeric values and numeric values less than zero inhibit truncation.  The shell
              sets the default value to the value of HISTSIZE after reading any startup files.  
  
***что делает директива ignoreboth в bash?***  
ignoreboth - не сохраняет строки, начинающиеся с пробела и строки, совпадающие с последней выполненой командой.  
  
**9. В каких сценариях использования применимы скобки {} и на какой строчке man bash это описано?**  
***В составных командах***  
Line 221

{ list; }
              list is simply executed in the current shell environment.  list must be terminated with a newline or semicolon.  This is known as a group  command.   The
              return  status  is the exit status of list.  Note that unlike the metacharacters ( and ), { and } are reserved words and must occur where a reserved word
              is permitted to be recognized.  Since they do not cause a word break, they must be separated from list by whitespace or another shell metacharacter.  
  
**10. Основываясь на предыдущем вопросе, как создать однократным вызовом touch 100000 файлов? А получилось ли создать 300000? Если нет, то почему?**  
  
***touch {1..100000}***  
***touch {1..300000} имеем Argument list too long ARG_MAX - Слишком длинный список аргументов***  
  
**11. В man bash поищите по /\[\[. Что делает конструкция [[ -d /tmp ]]**  
***Проверяет наличие каталога /tmp***  
  
**12. Основываясь на знаниях о просмотре текущих (например, PATH) и установке новых переменных; командах, которые мы рассматривали, добейтесь в выводе type -a bash в виртуальной машине наличия первым пунктом в списке**  
  
    ln -s /usr/bin /tmp/new_path_dir
    PATH=/tmp/new_path_dir:$PATH   

    bash is /tmp/new_path_dir/bash  
    bash is /usr/bin/bash  
    bash is /bin/bash  

**13. Чем отличается планирование команд с помощью batch и at?**  
  
***at***      executes commands at a specified time.  
***Выполняет команды в определенное время***  

***batch***   executes commands when system load levels permit; in other words, when the load  average  drops  below
               1.5, or the value specified in the invocation of atd.  
***Выполняет команды когда позволяет уровень нагрузки системы.***  




