Netology
First change
Second change

#Comments for ./Terraform/.gitignore
**/.terraform/*#Все содержимое любого вложенного каталога с именем ".terraform"
*.tfstate #Все файлы с расширением "tfstate" 
*.tfstate.* #Все файлы в которых встречается ".tfstate."
crash.log #Только этот файл
*.tfvars #Все файлы с расширением "tfvars"
override.tf #Только этот файл
override.tf.json #Только этот файл
*_override.tf #Все файлы с окончанием "_override.tf"
*_override.tf.json #Все файлы с окончанием "_override.tf.json"
.terraformrc #Все файлы с расширением "terraformrc"
terraform.rc #Только этот файл