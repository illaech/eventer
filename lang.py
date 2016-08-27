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
         'backup_timer', 'opt_action', 'full_name', 'message_timer')

ru_dict = {
    'NAME': 'RU',
    'FULL_NAME': 'Русский',
    'DATE_DELIM': '.',
    'TIME_DELIM': ':',
    'ERROR': 'Ошибка',
    'SMTH_WRONG': 'Упс. Что-то пошло не так',
    'CANT_FIND_DIR': 'Не найдена директория',
    'UNSUPPORT_SYS': 'Неподдерживаемая система',
    'CANT_CREATE_DIR': 'Не могу создать директорию',
    'CANT_OPEN_FILE': 'Не могу открыть файл',
    'ADD_ACTION': 'Добавить напоминание',
    'EDIT_ACTION': 'Изменить напоминания',
    'OPT_ACTION': 'Изменить настройки',
    'RESTORE': 'Восстановить напоминания',
    'QUIT': 'Выход',
    'SAVE': 'Сохранить',
    'CLOSE': 'Закрыть',
    'EDIT': 'Изменить',
    'DELETE': 'Удалить',
    'TASK': 'Задача',
    'REPEAT': 'Повторить через {}',
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
    'RESTORE_TEXT': 'Вы уверены, что хотите загрузить сохраненные ранее ' \
                    'напоминания?\nВернуть текущие задачи можно выбрав ' \
                    'пункт меню "Восстановить напоминания" еще раз',
    'ADD_TITLE': 'Добавление напоминания',
    'DATE': 'Дата',
    'TIME': 'Время',
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
    'EDIT_TOOLTIP_TEXT': 'Изменить это напоминание',
    'DELETE_TOOLTIP_TEXT': 'Удалить это напоминание',
    'NO_TASKS': 'Нет задач для отображения',
    'FILTER': 'Фильтр',
    'TEXT_F': 'Текст:',
    'DATE_F': 'Дата:',
    'OPT_TITLE': 'Настройки',
    'CHANGE_LANGUAGE': 'Сменить язык',
    'CHANGE_TDELTA': 'Повторять напоминания через',
    'MESSAGE_TIMER': 'Автоматически скрывать сообщения после',
    'BACKUP_TIMER': 'Сохранять напоминания каждые'
}

class Language:
    # language definitions
    NAME = 'EN'
    FULL_NAME = 'English'
    DATE_DELIM = '/'
    TIME_DELIM = ':'
    # errors
    ERROR = 'Error'
    SMTH_WRONG = 'Oops. Something goes wrong'
    CANT_FIND_DIR = 'Can\'t find directory'
    UNSUPPORT_SYS = 'Unsupported system'
    CANT_CREATE_DIR = 'Can\'t create directory'
    CANT_OPEN_FILE = 'Can\'t open file'
    # menu items
    ADD_ACTION = 'Add new reminder'
    EDIT_ACTION = 'Edit reminders'
    OPT_ACTION = 'Change settings'
    RESTORE = 'Restore reminders'
    QUIT = 'Quit'
    # buttons
    SAVE = 'Save'
    CLOSE = 'Close'
    EDIT = 'Edit'
    DELETE = 'Delete'
    # messages
    TASK = 'Reminder'
    REPEAT = 'Repeat after {}'
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
    RESTORE_TEXT = 'Are you sure to load previously saved reminders?\n' \
                   'If you\'ll do so, you can roll back your reminders ' \
                   'by choosing that menu item again'
    # addWindow
    ADD_TITLE = 'Add new reminder'
    DATE = 'Date'
    TIME = 'Time'
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
    # editWindow
    EDIT_TITLE = 'Edit reminders'
    EDIT_TOOLTIP_TEXT = 'Edit this reminder'
    DELETE_TOOLTIP_TEXT = 'Delete this reminder'
    NO_TASKS = 'No entries to show'
    FILTER = 'Filter'
    DATE_F = 'Date:'
    TEXT_F = 'Text:'
    VISIBLE_F = '˅'
    HIDDEN_F = '˄'
    # optionsWindow
    OPT_TITLE = 'Settings'
    CHANGE_LANGUAGE = 'Change language'
    CHANGE_TDELTA = 'Repeat reminders after'
    MESSAGE_TIMER = 'Automatically close message after'
    BACKUP_TIMER = 'Save reminders every'
    
    def __init__(self, dic=None, **kwargs):
        if dic != None:
            for i in dic:
                if i.lower() not in allowed:
                    print('"{} : {}" not supported'.format(i, dic[i]))
                else:
                    setattr(self, i.upper(), dic[i])
        if kwargs != None:
            for i in kwargs:
                if i.lower() not in allowed:
                    print('"{} : {}" not supported'.format(i, dic[i]))
                    pass
                else:
                    setattr(self, i.upper(), kwargs[i])
    
    def __str__(self):
        return self.NAME
    
    def __repr__(self):
        return str(self)
        
EN = Language()
RU = Language(dic=ru_dict)
