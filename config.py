TOKEN = "8513692458:AAE4mnkOb4B6EpvyUBpBYeqDuwaQXhKnuGM"
GIGACHAT_TOKEN = "MDE5YjFkNDgtNWI4Mi03NTkyLTk5MDMtOGU5N2VmYjU4YjA3OmJiOWUzZjliLThjMDUtNDJlZi1hNmVkLTc2MjdlMTJmOTcyMg=="
YANDEX_API_KEY = "AQVN2cpZmCtPuIaqTRxmJkqyM1xAl4t28CEh-60i"
YANDEX_FOLDER_ID = "b1gvd1p1vf5vib0oko06"
##Идентификатор API-ключа ajepp9cpgaqfn23akj8s

##CHANNEL_ID = -1003754848653
##При нажатии в главном меню на кнопку Отложка ничего не происходит, а при нажатии на кнопку График появляется вот такая ошибка
##2026-03-17 00:35:22,333 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8513692458:AAE4mnkOb4B6EpvyUBpBYeqDuwaQXhKnuGM/answerCallbackQuery "HTTP/1.1 200 OK"
##2026-03-17 00:35:22,337 - telegram.ext.Application - ERROR - No error handlers are registered, logging exception.
##Traceback (most recent call last):
##  File "C:\Users\пк\PycharmProjects\Textbot\.venv\Lib\site-packages\telegram\ext\_application.py", line 1315, in process_update
##    await coroutine
##  File "C:\Users\пк\PycharmProjects\Textbot\.venv\Lib\site-packages\telegram\ext\_handlers\basehandler.py", line 159, in handle_update
##    return await self.callback(update, context)
##           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
##  File "C:\Users\пк\PycharmProjects\Textbot\handlers.py", line 269, in button_callback
##    context.user_data["scheduled_time"]=t
##                                        ^
##UnboundLocalError: cannot access local variable 't' where it is not associated with a value
##2026-03-17 00:35:32,418 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8513692458:AAE4mnkOb4B6EpvyUBpBYeqDuwaQXhKnuGM/getUpdates "HTTP/1.1 200 OK"
## Также при перезапуске и заранее отложенному сообщению, слетело подключение к каналу и ничего не выложилось
##2026-03-17 00:39:40,155 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8513692458:AAE4mnkOb4B6EpvyUBpBYeqDuwaQXhKnuGM/getUpdates "HTTP/1.1 200 OK"
##2026-03-17 00:39:50,248 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8513692458:AAE4mnkOb4B6EpvyUBpBYeqDuwaQXhKnuGM/getUpdates "HTTP/1.1 200 OK"
##2026-03-17 00:40:00,003 - apscheduler.scheduler - INFO - Removed job 12f73cb413e74035bfc0bb3cc4d358b2
##2026-03-17 00:40:00,004 - apscheduler.executors.default - INFO - Running job "publish_post_job (trigger: date[2026-03-16 21:40:00 UTC], next run at: 2026-03-16 21:40:00 UTC)" (scheduled at 2026-03-16 21:40:00+00:00)
##2026-03-17 00:40:00,005 - root - ERROR - Канал не подключён
##2026-03-17 00:40:00,005 - apscheduler.executors.default - INFO - Job "publish_post_job (trigger: date[2026-03-16 21:40:00 UTC], next run at: 2026-03-16 21:40:00 UTC)" executed successfully
##2026-03-17 00:40:00,340 - httpx - INFO - HTTP Request: POST https://api.telegram.org/bot8513692458:AAE4mnkOb4B6EpvyUBpBYeqDuwaQXhKnuGM/getUpdates "HTTP/1.1 200 OK"
