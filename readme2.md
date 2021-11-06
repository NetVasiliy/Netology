#В виде результата напишите текстом ответы на вопросы и каким образом эти ответы были получены. 


##1. **Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.**  

    $ git show aefea
    хеш: aefead2207ef7e2aa5dc81a34aedf0cad4c32545
    Комментарий: Update CHANGELOG.md  

##2. Какому тегу соответствует коммит 85024d3?  

    $ git show 85024d3
    tag: v0.12.23  

##3. Сколько родителей у коммита b8d720? Напишите их хеши.<br/>

*У коммита b8d720 один родитель - 56cd7859e05c36c06b56d013b55a252d0bb7e158, образованный слиянием двух коммитов*  

    $ git show b8d720^
    commit 56cd7859e05c36c06b56d013b55a252d0bb7e158
    Merge: 58dcac4b7 ffbcf5581  

##4. Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.  

*Тут требуется помощь экcперта. Я не смог до конца разобраться, какой из вариантов правильный. **Склоняюсь к варианту 1**.* 

 ###4.1. Вариант 1. 9 коммитов  


    $ git log v0.12.23...v0.12.24 --oneline
    b14b74c49 [Website] vmc provider links
    3f235065b Update CHANGELOG.md
    6ae64e247 registry: Fix panic when server is unreachable
    5c619ca1b website: Remove links to the getting started guide's old location
    06275647e Update CHANGELOG.md
    d5f9411f5 command: Fix bug when using terraform login on Windows
    4b6d06cc5 Update CHANGELOG.md
    dd01a3507 Update CHANGELOG.md
    225466bc3 Cleanup after v0.12.23 release
Итого 9 коммитов (самый верхний я убрал, т.к это тег v0.12.24)  

 ###4.2. Вариант 2. 4 revisions.  

    $ git show v0.12.23
    tag v0.12.23
    commit 85024d3100126de36331c6982bfaac02cdab9e76 (tag: v0.12.23)
    $ git show v0.12.24
    tag v0.12.24
    commit 33ff1c03bb960b332be3af2e333462dde88b279e (tag: v0.12.24)
    admin@LAPTOP-V19MIJQS MINGW64 ~/PycharmProjects/pythonProject/Netology/terraform (main)
    $ git checkout 33ff1c03bb960b332be3af2e333462dde88b279e
    admin@LAPTOP-V19MIJQS MINGW64 ~/PycharmProjects/pythonProject/Netology/terraform ((v0.12.24))
    $ git bisect start
    admin@LAPTOP-V19MIJQS MINGW64 ~/PycharmProjects/pythonProject/Netology/terraform ((v0.12.24)|BISECTING)
    $ git bisect bad
    admin@LAPTOP-V19MIJQS MINGW64 ~/PycharmProjects/pythonProject/Netology/terraform ((v0.12.24)|BISECTING)
    $ git bisect good 85024d3100126de36331c6982bfaac02cdab9e76
    Bisecting: 4 revisions left to test after this (roughly 2 steps) 
    [06275647e2b53d97d4f0a19a0fec11f6d69820b5] Update CHANGELOG.md  
Итого: Bisecting пишет, что было 4 измененния.  
Я правильно понимаю, что меня закинуло в середину и я должен сам определить вниз мне двигаться по коммитам или вверх?

##5. Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).  

*Ответ:commit 8c928e83589d90a031f811fae52a81be7153e82f* 

    $ git log -S 'func providerSource' --oneline
    5af1e6234 main: Honor explicit provider_installation CLI config when present
    8c928e835 main: Consult local directories as potential mirrors of providers
    
    $ git log 8c928e835 -p -1
    commit 8c928e83589d90a031f811fae52a81be7153e82f
    ...
    ...
    +func providerSource(services *disco.Disco)  

##6. Найдите все коммиты в которых была изменена функция globalPluginDirs.  
  
    $ git log -S 'globalPluginDirs' --oneline
    35a058fb3 main: configure credentials from the CLI config file
*Просто использовали в другой функции*

    c0b176109 prevent log output during init
*Функцию не трогали* 

    8364383c3 Push plugin discovery down into command package
*Создание функции*  

##7. Кто автор функции synchronizedWriters?
    
Ответ: **Martin Atkins**  

    $ git log -S 'synchronizedWriters' --oneline
    bdfea50cc remove unused
    fd4f7eb0b remove prefixed io
    5ac311e2a main: synchronize writes to VT100-faker on Windows  

    $ git log 5ac311e2a -p -1
    commit 5ac311e2a91e381e2f52234668b49ba670aa0fe5
    Author: Martin Atkins <mart@degeneration.co.uk>
    Date:   Wed May 3 16:25:41 2017 -0700