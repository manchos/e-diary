# Скрипты для правки базы данных электронного дневника

[Репозиторий электронного дневника](https://github.com/devmanorg/e-diary)

## Как пользоваться
Переместите файл schoolkid_script.py в корневую директорию проекта Django, рядом с manage.py.
Далее запустите скрипт из командной строки c указанием имени ученика 
и с имеющимися подкомандами:

```bash
python schoolkid_script.py --help
usage: schoolkid_script.py [-h] child_name {new-comm,rm-chast,fix-marks} ...

The hack script for repo: https://github.com/devmanorg/e-diary

positional arguments:
  child_name            schoolkid name (default: Фролов Иван)

optional arguments:
  -h, --help            show this help message and exit

subcommands:
  subcommands for fix schollkid diary

  {new-comm,rm-chast,fix-marks}
                        function description
    new-comm            create commendation
    rm-chast            remove chastisements
    fix-marks           remove bad marks and replace them by 5

```
## Подкоманда `new-comm`  
Создает новую похвалу для указанного ученика. 
Дата похвалы совпадет с датой последнего указанного по названию (-lesson) урока.
Похвала выбирается из
 [списка](https://pedsovet.org/beta/article/30-sposobov-pohvalit-ucenika) 
 через random.choice. 

```bash
python schoolkid_script.py '' new-comm --help
usage: schoolkid_script.py new-comm [-h] [-lesson LESSON_NAME]
                                    
optional arguments:
  -h, --help           show this help message and exit
  -lesson LESSON_NAME  lesson name
```
## Подкоманда `rm-chast` 
Удаляет замечания для указанного ученика.

```bash
python schoolkid_script.py rm-chast --help
usage: schoolkid_script.py rm-chast [-h]

optional arguments:
  -h, --help         show this help message and exit

```

## Подкоманда `fix_marks` 
Правит плохие оценки, двойки или тройки на пятерки для указанного ученика.

```bash
python schoolkid_script.py fix-marks --help
usage: schoolkid_script.py fix-marks [-h]

optional arguments:
  -h, --help         show this help message and exit

```
