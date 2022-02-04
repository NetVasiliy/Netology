
run = True
#count = []
word_list = []
letter = "d"

def count_letter(word_list, letter):
  result = 0
  for word in word_list:
    if letter in word:
      result += 1
  return result

print(count_letter(['python', 'c++', 'c', 'scala', 'java'], 'c'))


while run :
  l = input("Введите слово: ")
  if l != "stop" :
    word_list.append(l)
  else :
    letter = input("Введите символ: ")
    run = False   

print(count_letter(word_list, letter))
print(word_list)
print(letter)
