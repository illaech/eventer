""" language definitions """
names = ('name', 'cant_find_dir', 'unsupport_sys', 'cant_create_dir',
         'cant_open_file', 'error', 'add_action', 'edit_action', 'restore',
         'change_language', 'quit', 'task', 'close', 'repeat', 'add_title',
         'save', 'date', 'time', 'date_delim', 'time_delim', 'smth_wrong',
         'date_tooltip_text', 'time_tooltip_text', 'text_tooltip_text',
         'save_tooltip_text', 'close_tooltip_text', 'edit_title', 'edit',
         'delete', 'edit_tooltip_text', 'delete_tooltip_text', 'no_tasks')

ru_dict = {
    'NAME': 'RU',
    'CANT_FIND_DIR': 'Не найдена директория',
    'UNSUPPORT_SYS': 'Неподдерживаемая система',
    'CANT_CREATE_DIR': 'Не могу создать директорию',
    'CANT_OPEN_FILE': 'Не могу открыть файл',
    'ERROR': 'Ошибка',
    'ADD_ACTION': 'Добавить задачу',
    'EDIT_ACTION': 'Изменить задачи',
    'CHANGE_LANGUAGE': 'Сменить язык',
    'QUIT': 'Выход',
    'TASK': 'Задача',
    'CLOSE': 'Закрыть',
    'REPEAT': 'Повторить через 10 мин',
    'ADD_TITLE': 'Добавление задачи',
    'SAVE': 'Сохранить',
    'DATE': 'Дата',
    'TIME': 'Время',
    'DATE_DELIM': '.',
    'TIME_DELIM': ':',
    'DATE_TOOLTIP_TEXT': 'Формат даты: дд.мм.гггг<br/>Можно использовать' \
                         ' сокращенные варианты: дд.мм.гг и дд.мм' \
                         ' и "/" вместо точек',
    'TIME_TOOLTIP_TEXT': 'Формат времени: чч:мм:сс<br/>Можно использовать' \
                         ' сокращенные варианты: чч:мм и ч:мм' \
                         ' и точки вместо двоеточий',
    'TEXT_TOOLTIP_TEXT': 'Текст напоминания',
    'SAVE_TOOLTIP_TEXT': 'Сохранить напоминания',
    'CLOSE_TOOLTIP_TEXT': 'Закрыть окно без добавления задачи',
    'EDIT_TITLE': 'Изменение задач',
    'EDIT': 'Изменить',
    'DELETE': 'Удалить',
    'EDIT_TOOLTIP_TEXT': 'Изменить эту задачу',
    'DELETE_TOOLTIP_TEXT': 'Удалить эту задачу',
    'NO_TASKS': 'Нет задач для отображения',
    'SMTH_WRONG': 'Упс. Что-то пошло не так',
    'RESTORE': 'Восстановить напоминания',
    'RESTORE_TEXT': 'Вы уверены, что хотите загрузить сохраненные ранее ' \
                    'напоминания?\nВернуть текущие задачи можно выбрав ' \
                    'пункт меню "Восстановить напоминания" еще раз'
}

class Language:
    NAME = 'EN'
    CANT_FIND_DIR = 'Can\'t find directory'
    UNSUPPORT_SYS = 'Unsupported system'
    CANT_CREATE_DIR = 'Can\'t create directory'
    CANT_OPEN_FILE = 'Can\'t open file'
    ERROR = 'Error'
    ADD_ACTION = 'Add new reminder'
    EDIT_ACTION = 'Edit reminders'
    CHANGE_LANGUAGE = 'Change language'
    QUIT = 'Quit'
    TASK = 'Reminder'
    CLOSE = 'Close'
    REPEAT = 'Repeat after 10 min'
    ADD_TITLE = 'Add new reminder'
    SAVE = 'Save'
    DATE = 'Date'
    TIME = 'Time'
    DATE_DELIM = '/'
    TIME_DELIM = '.'
    DATE_TOOLTIP_TEXT = 'Date format: dd/mm/yyyy<br/>You also can use' \
                         ' short forms: dd/mm/yy and dd/mm,' \
                         ' and dots instead of slashes'
    TIME_TOOLTIP_TEXT = 'Time format: hh.mm.ss<br/>You also can use' \
                         ' short forms: hh.mm and h.mm,' \
                         ' and colons instead of dots'
    TEXT_TOOLTIP_TEXT = 'Text of reminder'
    SAVE_TOOLTIP_TEXT = 'Save reminder'
    CLOSE_TOOLTIP_TEXT = 'Close the window and don\'t add new reminder'
    EDIT_TITLE = 'Edit reminders'
    EDIT = 'Edit'
    DELETE = 'Delete'
    EDIT_TOOLTIP_TEXT = 'Edit this reminder'
    DELETE_TOOLTIP_TEXT = 'Delete this reminder'
    NO_TASKS = 'No entries to show'
    SMTH_WRONG = 'Oops. Something goes wrong'
    RESTORE = 'Restore reminders'
    RESTORE_TEXT = 'Are you sure to load previously saved reminders?\n' \
                   'If you\'ll do so, you can roll back your reminders ' \
                   'by choosing that menu item again'
    
    def __init__(self, dic=None, **kwargs):
        if dic != None:
            for i in dic:
                if i.lower() not in names:
                    pass
                else:
                    setattr(self, i.upper(), dic[i])
        if kwargs != None:
            for i in kwargs:
                if i.lower() not in names:
                    pass
                else:
                    setattr(self, i.upper(), kwargs[i])
    
    def __str__(self):
        return self.NAME
    
    def __repr__(self):
        return str(self)
        
EN = Language()
RU = Language(dic=ru_dict)
