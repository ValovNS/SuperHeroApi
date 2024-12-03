В данном репозитории предсталвелы две версии кода для нахождения персонажа с самым высоким ростом на superhero-api c учетом ввода пользователем пола персонажа и наличия у него работы.
В первой версии кода (ver1) использован более времязатратный подход, при котором программа запрашиват json кажого персонажа по очереди и проверяет выполнение заданных пользователем условий.
Во второй версии кода (ver2) программа запрашиват один json со всеми персонажами и уже в нем анализирует заданные пользователем условия, что существенно ускоряет выполнение программы.
Стоит отметить, что обе версии выдают одинаковых персонажей при одинаковых запросах.
Также в репозитории представлены варианты тестирования: 
• первой версии кода, в котором попарно тестируется несколько вариантов заданных пользователем условий;
• второй версии кода, в котором попарно тестируется большее количество вариантов заданных пользователем условий.
