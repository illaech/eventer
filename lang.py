""" language definitions """
allowed = ('name', 'cant_find_dir', 'unsupport_sys', 'cant_create_dir',
         'cant_open_file', 'error', 'add_action', 'edit_action', 'restore',
         'change_language', 'quit', 'task', 'close', 'repeat', 'add_title',
         'save', 'date', 'time', 'date_delim', 'time_delim', 'smth_wrong',
         'date_tooltip_text', 'time_tooltip_text', 'text_tooltip_text',
         'save_tooltip_text', 'close_tooltip_text', 'edit_title', 'edit',
         'delete', 'edit_tooltip_text', 'delete_tooltip_text', 'no_tasks',
         'restore_text', 'day_', 'dayd', 'days', 'dayf', 'hour_', 'hourd',
         'hours', 'hourf', 'minute_', 'minuted', 'minutes', 'minutef',
         'second_', 'secondd', 'seconds', 'secondf', 'filter', 'date_f',
         'text_f', 'hidden_f', 'visible_f', 'opt_title', 'change_tdelta',
         'backup_timer')

ru_dict = {
    'NAME': 'RU',
    'CANT_FIND_DIR': 'Не найдена директория',
    'UNSUPPORT_SYS': 'Неподдерживаемая система',
    'CANT_CREATE_DIR': 'Не могу создать директорию',
    'CANT_OPEN_FILE': 'Не могу открыть файл',
    'ERROR': 'Ошибка',
    'ADD_ACTION': 'Добавить напоминание',
    'EDIT_ACTION': 'Изменить напоминания',
    'CHANGE_LANGUAGE': 'Сменить язык',
    'QUIT': 'Выход',
    'TASK': 'Задача',
    'CLOSE': 'Закрыть',
    'REPEAT': 'Повторить через {}',
    'ADD_TITLE': 'Добавление напоминания',
    'SAVE': 'Сохранить',
    'DATE': 'Дата',
    'TIME': 'Время',
    'DATE_DELIM': '.',
    'TIME_DELIM': ':',
    'DATE_TOOLTIP_TEXT': 'Используемые форматы дат:<br/><i>дд.мм.гггг</i>, ' \
                         '<i>дд.мм.гг</i>, <i>дд.мм</i>.<br/>' \
                         'Вместо <i>дд</i> и <i>мм</i> можно использовать' \
                         ' <i>д</i> и <i>м</i>; а также "/" вместо точек',
    'TIME_TOOLTIP_TEXT': 'Используемые форматы времени:<br/><i>чч:мм:сс</i>,' \
                         ' <i>чч:мм</i>.<br/>Вместо <i>чч</i>, <i>мм</i> и ' \
                         '<i>сс</i> можно использовать <i>ч</i>, <i>м</i> и ' \
                         '<i>с</i>; а также точки вместо двоеточий',
    'TEXT_TOOLTIP_TEXT': 'Текст напоминания',
    'SAVE_TOOLTIP_TEXT': 'Сохранить напоминания',
    'CLOSE_TOOLTIP_TEXT': 'Закрыть окно без добавления напоминания',
    'EDIT_TITLE': 'Изменение напоминаний',
    'EDIT': 'Изменить',
    'DELETE': 'Удалить',
    'EDIT_TOOLTIP_TEXT': 'Изменить это напоминание',
    'DELETE_TOOLTIP_TEXT': 'Удалить это напоминание',
    'NO_TASKS': 'Нет задач для отображения',
    'SMTH_WRONG': 'Упс. Что-то пошло не так',
    'RESTORE': 'Восстановить напоминания',
    'RESTORE_TEXT': 'Вы уверены, что хотите загрузить сохраненные ранее ' \
                    'напоминания?\nВернуть текущие задачи можно выбрав ' \
                    'пункт меню "Восстановить напоминания" еще раз',
    'DAY_': 'день',
    'DAYD': 'день',
    'DAYS': 'дней',
    'DAYF': 'дня',
    'HOUR_': 'час',
    'HOURD': 'час',
    'HOURS': 'часов',
    'HOURF': 'часа',
    'MINUTE_': 'минуту',
    'MINUTED': 'минуту',
    'MINUTES': 'минут',
    'MINUTEF': 'минуты',
    'SECOND_': 'секунду',
    'SECONDD': 'секунду',
    'SECONDS': 'секунд',
    'SECONDF': 'секунды',
    'FILTER': 'Фильтр',
    'TEXT_F': 'Текст:',
    'DATE_F': 'Дата:',
    'OPT_TITLE': 'Настройки',
    'CHANGE_TDELTA': 'Повторять задачи через',
    'BACKUP_TIMER': 'Сохранять задачи каждые'
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
    REPEAT = 'Repeat after {}'
    ADD_TITLE = 'Add new reminder'
    SAVE = 'Save'
    DATE = 'Date'
    TIME = 'Time'
    DATE_DELIM = '/'
    TIME_DELIM = '.'
    DATE_TOOLTIP_TEXT = 'Appropriate date formats:<br/><i>dd/mm/yyyy</i>, ' \
                        '<i>dd/mm/yy/</i>, and <i>dd/mm</i>.<br/>You also ' \
                        'can use <i>d</i> and <i>m</i> instead of <i>dd</i>' \
                        ' and <i>mm</i>.<br/>Also, you can use dots ' \
                        'instead of slashes'
    TIME_TOOLTIP_TEXT = 'Appropriate time formats:<br/><i>hh.mm.ss</i>, ' \
                        '<i>hh.mm</i>.<br/>You also can use <i>h</i>, ' \
                        '<i>m</i> and <i>s</i> instead of <i>hh</i>, ' \
                        '<i>mm</i> and <i>ss</i>.<br/>Also, you can use ' \
                        'colons instead of dots'
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
    DAY_ = 'day'  # 1
    DAYD = 'days' # 21, 31, ...
    DAYS = 'days' # 5, 6, ...
    DAYF = 'days' # 2, 3, 4, 22, ...
    HOUR_ = 'hour'
    HOURD = 'hours'
    HOURS = 'hours'
    HOURF = 'hours'
    MINUTE_ = 'minute'
    MINUTED = 'minutes'
    MINUTES = 'minutes'
    MINUTEF = 'minutes'
    SECOND_ = 'second'
    SECONDD = 'seconds'
    SECONDS = 'seconds'
    SECONDF = 'seconds'
    FILTER = 'Filter'
    DATE_F = 'Date:'
    TEXT_F = 'Text:'
    VISIBLE_F = '˅'
    HIDDEN_F = '˄'
    OPT_TITLE = 'Settings'
    CHANGE_TDELTA = 'Repeat reminders after'
    BACKUP_TIMER = 'Save reminders every'
    
    def __init__(self, dic=None, **kwargs):
        if dic != None:
            for i in dic:
                if i.lower() not in allowed:
                    print(i.lower())
                else:
                    setattr(self, i.upper(), dic[i])
        if kwargs != None:
            for i in kwargs:
                if i.lower() not in allowed:
                    pass
                else:
                    setattr(self, i.upper(), kwargs[i])
    
    def __str__(self):
        return self.NAME
    
    def __repr__(self):
        return str(self)
        
EN = Language()
RU = Language(dic=ru_dict)
