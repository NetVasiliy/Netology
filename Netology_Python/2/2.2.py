HELP = """
help - напечатать справку по программе.
add - добавить задачу в список (название задачи запрашиваем у пользователя).
show - напечатать все добавленные задачи.
exit - выход"""

#tasks = {[]}
today = []
tomorrow = []
other =[]


run = True
date = True

while run:
  command = input("Введите команду: ")
   
  if command == "help":
    print(HELP)    
  elif command == "show":
    print("Сегодня: ",today,";","Завтра: ",tomorrow,";","Похуй: ",other,".")
  elif command == "add":
    task = input("Введите название задачи: ")
    #addtasks.append(task)
    print("Задача добавлена")
    
    while date:  
     time = input("Введите дату: ")
  
     if time == "today" :
      today.append(task)
      break
     elif time == "tomorrow" :
      tomorrow.append(task)
      break
     else :
      other.append(task)
      break
    #break
      #  date=False
  elif command == "exit":
    print("Спасибо за использование")
    run= False
  else: 
    print("Неизвестная команда")
  #  run=False
    break



print("До свидания!")
