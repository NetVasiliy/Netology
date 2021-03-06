
# Домашнее задание к занятию "5.2. Применение принципов IaaC в работе с виртуальными машинами"

---

## Задача 1

- **Опишите своими словами основные преимущества применения на практике IaaC паттернов.**  
  
- Ускорение развертывания.  
- Снижение "человеческого фактора".
- Отслеживание версионности.  


- **Какой из принципов IaaC является основополагающим?**  
  
Иденпотентность - если настроил один раз правильно, то эта конфигурация у всех будет работать.  


## Задача 2

- **Чем Ansible выгодно отличается от других систем управление конфигурациями?**  
  
Тем, что Ansible использует существующую SSH структуру. Для меня дополнительным плюсом является еще и `Python`.  

- **Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?**  
  
На мой взгляд надежнее `Push`, т.к. мы сразу видим, что все получилось, но требуется кнопка. Если использовать `Pull`, то потребуется дополнительный мониторинг, чтобы периодически убеждаться "Конфигурация загрузилась".  


## Задача 3

**Установить на личный компьютер:**

- VirtualBox  
  
```  
C:\Program Files\Oracle\VirtualBox>vboxmanage --version
6.1.18r142142  
```  

- Vagrant  
```  
C:\HashiCorp\Virt_05>vagrant --version
Vagrant 2.2.19  
```
- Ansible
  
```  
ansible --version
ansible 2.9.6
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Jun  2 2021, 10:49:15) [GCC 9.4.0]  
  ```  

*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*  
  


## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

- Создать виртуальную машину.
- Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды  
 К сожалению связка Win+Virtualbox+Vagrant (ubuntu+ansible+vagrant), в которой я пытался запустить машину в вагранте с помощью файлов из лекции, не сработала. Надо позже попробовать сделать это на хостовой Linux. 
```
docker ps
```
