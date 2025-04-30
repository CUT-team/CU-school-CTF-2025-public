# Решение задачи

## Вариант 1

1. Открыть файл с помощью [Adobe Acrobat Reader](https://get.adobe.com/ru/reader/) или [Foxit Reader](https://www.foxit.com/ru/pdf-reader/).
   
   _Для пользователей Linux для запуска Foxit Reader можно использовать Wine (тестировался запуск [Portable-версии](../public/FoxitReaderPortable.zip)). Либо можно использовать виртуальную машину с Windows._

2. Нажать кнопку «Печать».
3. Для Adobe Acrobat нужно выбрать какой-нибудь виртуальный принтер и отправить печать на него. Для Foxit можно сразу отменить печать.
4. Выполнить поиск в документе по строке `cuctf`, флаг будет написан белым текстом на случайной странице в документе.

## Вариант 2

1. Скачать утилиту `pdfinfo` из пакета [Poppler](https://poppler.freedesktop.org/).
2. С помощью команды `pdfinfo -js bookworm.pdf` получить [обфусцированный JavaScript код](../src/obfuscated.js).
3. Перейти на [деобфускатор JS кода](https://obf-io.deobfuscate.io/) и вставить полученный на предыдущем шаге код. Результат: [deobfuscated.js](deobfuscated.js).
4. На 35-ой строке есть HEX-строка `63756374667b5930755f3472335f763372795f673030645f34745f504446737d`. С помощью [CyberChef](https://gchq.github.io/CyberChef/) декодируем её и получаем флаг.