# Триггер скриптов Home Assistant
# author: Timhok

from datetime import date
import os

from vacore import VACore

modname = os.path.basename(__file__)[:-3] # calculating modname

# функция на старте
def start(core:VACore):
    manifest = {
        "name": "Календарь Home Assistant",
        "version": "1.0",
        "require_online": True,

        "default_options": {
            "hassio_url": "http://hassio.lan:8123/",
            "hassio_calendar": "api/calendars/calendar.calendar", # название вашего календаря
            "hassio_key": "", # получить в /profile, "Долгосрочные токены доступа"
        },

        "commands": {
            "сегодня|события|календарь": hassio_calendar,
        }
    }
    return manifest

def start_with_options(core:VACore, manifest:dict):
    pass

def hassio_calendar(core:VACore, phrase: str):

    options = core.plugin_options(modname)

    if options["hassio_url"] == "" or options["hassio_key"] == "":
        print(options)
        core.play_voice_assistant_speech("Нужен ключ или ссылка для Хоум Ассистента")
        return

    try:
        import requests
        url = options["hassio_url"] + options["hassio_calendar"]
        headers = {"Authorization": "Bearer " + options["hassio_key"]}
        now = date.today()
        now_str = now.strftime("%Y-%m-%d")
        res = requests.get(url+"?start="+ now_str +"T00:00:00.000Z&end="+ now_str +"T00:00:00.000Z", headers=headers)
        hassio_calendar = res.json()
        hassio_events = ""
        for service in hassio_calendar:
            hassio_events = hassio_events + " "+service["summary"]
        if hassio_events == "":
            hassio_events = "Событий нет"
        text = "Сегодня" + hassio_events
        core.play_voice_assistant_speech(text)

    except:
        import traceback
        traceback.print_exc()
        core.play_voice_assistant_speech("Что то пошло не так")
        return
