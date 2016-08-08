import os
import sys
from math import floor
import json
import datetime as dt
import base64 as b64
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

""" language definitions """
RU = {
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
    'SMTH_WRONG': 'Упс. Что-то пошло не так'
}

EN = {
    'NAME': 'EN',
    'CANT_FIND_DIR': 'Can\'t find directory',
    'UNSUPPORT_SYS': 'Unsupported system',
    'CANT_CREATE_DIR': 'Can\'t create directory',
    'CANT_OPEN_FILE': 'Can\'t open file',
    'ERROR': 'Error',
    'ADD_ACTION': 'Add new reminder',
    'EDIT_ACTION': 'Edit reminders',
    'CHANGE_LANGUAGE': 'Change language',
    'QUIT': 'Quit',
    'TASK': 'Reminder',
    'CLOSE': 'Close',
    'REPEAT': 'Repeat after 10 min',
    'ADD_TITLE': 'Add new reminder',
    'SAVE': 'Save',
    'DATE': 'Date',
    'TIME': 'Time',
    'DATE_DELIM': '/',
    'TIME_DELIM': '.',
    'DATE_TOOLTIP_TEXT': 'Date format: dd/mm/yyyy<br/>You also can use' \
                         ' short forms: dd/mm/yy and dd/mm,' \
                         ' and dots instead of slashes',
    'TIME_TOOLTIP_TEXT': 'Time format: hh.mm.ss<br/>You also can use' \
                         ' short forms: hh.mm and h.mm,' \
                         ' and colons instead of dots',
    'TEXT_TOOLTIP_TEXT': 'Text of reminder',
    'SAVE_TOOLTIP_TEXT': 'Save reminder',
    'CLOSE_TOOLTIP_TEXT': 'Close the window and don\'t add new reminder',
    'EDIT_TITLE': 'Edit reminders',
    'EDIT': 'Edit',
    'DELETE': 'Delete',
    'EDIT_TOOLTIP_TEXT': 'Edit this reminder',
    'DELETE_TOOLTIP_TEXT': 'Delete this reminder',
    'NO_TASKS': 'No entries to show',
    'SMTH_WRONG': 'Oops. Something goes wrong'
}

langs = {'RU': RU, 'EN': EN}

def langSelect(lang):
    conf.lang = langs[lang]
    reload()

""" Config class """

class Config:
    supported = ('lang', 'tdelta')
    lang = None
    tdelta = None

    def __init__(self, lang=RU, tdelta=600):
        self.lang = lang
        self.tdelta = tdelta

    def __str__(self):
        dic = {'lang': self.lang['NAME'], 'tdelta': self.tdelta}
        return json.dumps(dic)

    def load(self, dic):
        for i in dic:
            if i not in self.supported:
                pass
            else:
                setattr(self, i, dic[i])

    def dump(self, f):
        try:
            with open(f, 'w') as f_:
                f_.write(str(self))
        except IOError:
            errors.append(['{} "{}"'.format(conf.lang['CANT_OPEN_FILE'], f),
                           'IOError: Can\'t open file!'])

conf = Config(RU, 600)

""" preliminary definitions """

errors = []  # see line 738

# select directory where 'calendar.txt' will be placed
if sys.platform == 'win32': # if platform is windows, choose %appdata%
    if os.getenv('APPDATA') is not None:
        directory = '{}\\eventer'.format(os.getenv('APPDATA'))
        filename = '{}{}calendar.txt'.format(directory, '\\')
        config = '{}{}config.txt'.format(directory, '\\')
    else:
        errors.append(['{} %appdata%'.format(conf.lang['CANT_FIND_DIR']),
                       'IOError: Can\'t find directory'])
elif sys.platform == 'linux' or sys.platform == 'linux2':
    # if platform is linux, choose '~/.eventer'
    if os.getenv('HOME') is not None:
        directory = '{}/.eventer'.format(os.getenv('HOME'))
        filename = '{}{}calendar.txt'.format(directory, '/')
        config = '{}{}config.txt'.format(directory, '/')
    else:
        errors.append(['{} /home/user'.format(conf.lang['CANT_FIND_DIR']),
                       'IOError: Can\'t find directory'])
else:
   errors.append(['{}'.format(conf.lang['UNSUPPORT_SYS']),
                  'OSError: Unsupported system'])

if len(errors) == 0:
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            errors.append(['{} "{}"'.
                           format(conf.lang['CANT_CREATE_DIR'], directory),
                           'PermissionError: Can\'t create directory!'])

tasks = []

""" global functions """

def rewrite():
    """ Update tasks file """
    try:
        global tasks
        tasks = sorted(tasks, key=lambda x: strToDate('{} {}'.format(x.date,
                                                                     x.time)))
        with open(filename, 'w') as f:
            f.write('\n'.join([str(x) for x in tasks]))
    except IOError:
        errors.append(['{} "{}"'.format(conf.lang['CANT_OPEN_FILE'], filename),
                       'IOError: Can\'t open file!'])

def rewriteConfig():
    """ Update config file """
    try:
        conf.dump(config)
    except IOError:
        errors.append(['{} "{}"'.format(conf.lang['CANT_OPEN_FILE'], config),
                       'IOError: Can\'t open file!'])

def dateToStr(datetime):
    """Convert datetime object to strings and return a dictionary"""
    time = datetime.strftime('%H{d}%M{d}%S'.format(d=conf.lang['TIME_DELIM']))
    date = datetime.strftime('%d{d}%m{d}%Y'.format(d=conf.lang['DATE_DELIM']))
    return {'time': time, 'date': date}

def strToDate(string):
    """Convert string to datetime object and return it"""
    datetime = dt.datetime.strptime(string, '%d.%m.%Y %H:%M:%S')
    return datetime

def error(widget, text, textconsole):
    """Show error message"""
    QMessageBox.critical(widget, conf.lang['ERROR'], text, QMessageBox.Ok,
                         QMessageBox.Ok)
    # Here "raise Exception(textconsole)" can be used to close
    # the application immediately after the first error.
    # Also, logging to text file can be used here.
    print(textconsole)


""" main class definitions """

class Entry:
    """ Task entry.

    Parameters and attributes
    -------------------------
    date : string
        Date of task, dd.mm.yy.
    time : string
        Time of task, hh:mm:ss.
    text : string
        Text of task.

    """
    def __init__(self, date, time, text):
        self.date = date
        self.time = time
        self.text = text

    def __str__(self):
        """Return string, constits of date, time and text of entry,
        separated by '|'.

        The returned entry's text is base64-encoded.

        """
        return '{}|{}|{}'.format(self.date, self.time,
                                 b64.b64encode(self.text.encode('utf-8')))

    def getDateTime(self):
        """Return datetime object that stores entry's date and time"""
        return strToDate('{} {}'.format(self.date, self.time))


""" QT class definitions """

class MainWindow(QWidget):
    """ Main window of application. It is represented by icon in
    taskbar.

    Useful attributes
    -----------------
    addWindow : AddWindow object
    addActive : boolean
        If user wants to add new task, addWindow becomes the QWidget for
        it, and while it is active addActive remains True.
    editWindow : EditWindow object
    editActive : boolean
        If user wants to edit tasks, editWindow becomes the QWidget for
        it, and while it is active editActive remains True.
    tray : QSystemTrayIcon object
        Tray icon and all its attributes like context menu and
        activated action.
    timer : QBasicTimer
        Timer that fires every second. If one reminder's time is up,
        shows message.

    """
    def __init__(self):
        super().__init__()

        self.tray = QSystemTrayIcon(QIcon('add.ico'), self)

        menu = QMenu()
        menu.addAction(conf.lang['ADD_ACTION'],
                       lambda: self.showWindow(QSystemTrayIcon.Trigger))
        menu.addAction(conf.lang['EDIT_ACTION'],
                       lambda: self.showWindow('editAction'))
        menu.addSeparator()

        langlist = QActionGroup(self, exclusive=True)
        act_ru = QAction('Русский', self, checkable=True)
        act_ru.triggered.connect(lambda evt: langSelect('RU'))
        act_en = QAction('English', self, checkable=True)
        act_en.triggered.connect(lambda evt: langSelect('EN'))
        langlist.addAction(act_ru)
        langlist.addAction(act_en)

        langmenu = menu.addMenu(conf.lang['CHANGE_LANGUAGE'])
        langmenu.addAction(act_ru)
        langmenu.addAction(act_en)
        act_ru.setChecked(True)
        self.lang = {'RU': act_ru, 'EN': act_en}

        menu.addAction(conf.lang['QUIT'], self.quit)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.showWindow)

        self.tray.show()
        self.addWindow = None
        self.addActive = False
        self.editWindow = None
        self.editActive = False

        self.timer = QBasicTimer()
        self.timer.start(1000, self)

    def timerEvent(self, event):
        """ Checks tasks entry's time if it is up. Shows message with
        entry's text if its time's up.

        """
        global tasks
        global rewrite
        for entry in tasks:
            date = entry.getDateTime()
            today = dt.datetime.today()
            if (date - today).days < 0:
                tasks.remove(entry)
                rewrite()
                msgBox = QMessageBox()
                msgBox.setText(entry.text)
                msgBox.setWindowTitle('{} {}'.format(conf.lang['TASK'], date))
                msgBox.setWindowIcon(QIcon('alert.ico'))
                msgBox.setIcon(QMessageBox.Information)
                # msgBox.setTextFormat(Qt.RichText)
                msgBox.addButton(QPushButton(conf.lang['REPEAT']),
                                             QMessageBox.YesRole)
                msgBox.addButton(QPushButton(conf.lang['CLOSE']),
                                             QMessageBox.NoRole)
                msgBox.setWindowFlags(Qt.WindowStaysOnTopHint)
                reply = msgBox.exec_()
                msgBox.raise_()

                if reply == 0:
                    date = dateToStr(dt.datetime.now() + dt.timedelta(0, 600))
                    tasks.append(Entry(date['date'], date['time'], entry.text))
                    rewrite()
                if self.editActive:
                    self.editWindow.fill()

    def showWindow(self, event):
        """ Show child windows.
        If event is QSystemTrayIcon.Trigger then it checks if
        all windows are not open and show addWindow.

        If event is 'addAction' it means that user from editWindow
        want to edit reminder, so it opens addWindow.

        Then it checks if addAction or editAction is True, and alert
        appropriate window.

        Then if event is 'editAction' then it opens editWindow.

        """
        if event == QSystemTrayIcon.Trigger and not (self.addActive or
                    self.editActive) or event == 'addAction':
            self.addWindow = AddWindow(self)
            self.addWindow.show()
            self.addWindow.setFocus(True)
            self.addWindow.activateWindow()
            return self.addWindow
        elif self.addActive:
            QApplication.alert(self.addWindow)
            return self.addWindow
        elif self.editActive:
            QApplication.alert(self.editWindow)
            return self.editWindow
        elif event == 'editAction':
            self.editWindow = EditWindow(self)
            self.editWindow.show()
            self.editWindow.setFocus(True)
            self.editWindow.activateWindow()
            return self.editWindow

    def quit(self, really=True):
        """ Quits application. Hides tray icon firstly. """
        self.tray.hide()
        if really:
            QCoreApplication.instance().quit()


class AddWindow(QWidget):
    """ Window for adding reminders.

    Useful attributes
    -----------------
    parentWindow : MainWindow object
        Parent of the window.
    (date|time)Edit : QLineEdit
    textEdit : QTextEdit
    (save|close)Btn : QPushButton
        Widgets in the window.

    """
    def __init__(self, parent=None):
        super().__init__()
        self.index = None
        self.initUI()
        self.parentWindow = parent
        self.parentWindow.addActive = True

    def initUI(self):
        """ Init user interface. """
        self.setWindowTitle(conf.lang['ADD_TITLE'])
        self.setWindowIcon(QIcon('add.ico'))

        self.resize(350, 350)
        self.move(QApplication.desktop().screen().rect().center() -
                  self.rect().center()) # center window on screen

        grid = QGridLayout()
        self.setLayout(grid)

        dateLbl = QLabel(conf.lang['DATE'])
        timeLbl = QLabel(conf.lang['TIME'])
        self.dateEdit = QLineEdit()
        self.timeEdit = QLineEdit()
        self.textEdit = QTextEdit()
        self.saveBtn = QPushButton(conf.lang['SAVE'])
        self.closeBtn = QPushButton(conf.lang['CLOSE'])

        dateLbl.setAlignment(Qt.AlignCenter)
        timeLbl.setAlignment(Qt.AlignCenter)

        dateToolTipText = conf.lang['DATE_TOOLTIP_TEXT']
        timeToolTipText = conf.lang['TIME_TOOLTIP_TEXT']

        self.dateEdit.setToolTip(dateToolTipText)
        self.timeEdit.setToolTip(timeToolTipText)
        dateLbl.setToolTip(dateToolTipText)
        timeLbl.setToolTip(timeToolTipText)
        self.textEdit.setToolTip(conf.lang['TEXT_TOOLTIP_TEXT'])
        self.saveBtn.setToolTip(conf.lang['SAVE_TOOLTIP_TEXT'])
        self.closeBtn.setToolTip(conf.lang['CLOSE_TOOLTIP_TEXT'])

        grid.addWidget(dateLbl, 0, 0)
        grid.addWidget(timeLbl, 0, 1)
        grid.addWidget(self.dateEdit, 1, 0)
        grid.addWidget(self.timeEdit, 1, 1)
        grid.addWidget(self.textEdit, 2, 0, 14, 2)
        grid.addWidget(self.saveBtn, 16, 0)
        grid.addWidget(self.closeBtn, 16, 1)

        """ regexp for date:
        31 days in january, march, may, july, august, october and december;
        30 days in april, june, september and november;
        29 days in february (year validate is in save function);
        2 or 4 decimal year (no 0000 year);
        / or . as delimiter.
        """
        dateRegExp = QRegExp(
            '^((0[1-9]|[1-2]\d|3[01])(/|\.)(01|03|05|07|08|10|12)|' \
            '(0[1-9]|[1-2]\d)(/|\.)02|' \
            '(0[1-9]|[1-2]\d|30)(/|\.)(04|06|09|11))((/|\.)\d\d|(/|\.)'\
            '(\d\d\d[1-9]|\d\d[1-9]\d|\d[1-9]\d\d|[1-9]\d\d\d))?$'
        )
        # regexp for time: 23 hours, 59 minutes, : or . as delimiter
        timeRegExp = QRegExp(
            '^([0-9]|[01]\d|2[0-3])(:|\.)[0-5]\d((:|\.)[0-5]\d)?$'
        )
        dateValid = QRegExpValidator(dateRegExp)
        timeValid = QRegExpValidator(timeRegExp)
        self.dateEdit.validator = dateValid
        self.dateEdit.textChanged.connect(self.checkState)
        self.dateEdit.textChanged.emit(self.timeEdit.text())
        self.timeEdit.validator = timeValid
        self.timeEdit.textChanged.connect(self.checkState)
        self.timeEdit.textChanged.emit(self.timeEdit.text())

        self.dateEdit.valid = False
        self.timeEdit.valid = False

        self.closeBtn.clicked.connect(lambda: self.closeEvent(QCloseEvent()))
        self.saveBtn.clicked.connect(self.save)

        # disable saveBtn
        self.saveBtn.setEnabled(False)

    def checkState(self, sender):
        """ Checks if date and time are in appropriate forms.
        Colors background of (date|time)Edit depending of their text.

        """
        sender = self.sender()
        validator = sender.validator
        state = validator.validate(sender.text(), 0)[0]
        if state == QValidator.Acceptable:
            color = '#5df375' # green
            self.sender().valid = True
        elif state == QValidator.Intermediate:
            color = '#fffa76' # yellow
            self.sender().valid = False
        else:
            color = '#ff8d93' # red
            self.sender().valid = False
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)

        # If date and time are in appropriate forms, enable saveBtn
        self.saveBtn.setEnabled(self.dateEdit.valid and self.timeEdit.valid)

    def save(self):
        """ Saves reminder """
        date = self.dateEdit.text().replace('/', '.')
        try:
            d, m, y = date.split('.')
        except ValueError:
            d, m = date.split('.')
            y = ''
        if y == '':
            y = dt.datetime.today().year
        elif len(y) < 4:
            y = floor(dt.datetime.today().year / 100) * 100 + int(y)
        else:
            y = int(y)
        d, m = map(int, [d, m])
        if y % 4 != 0 and m == 2 and d > 28:
            d = 28 # if date if 29.02 but year is not leap
        y = '{:04d}'.format(y)
        m = '{:02d}'.format(m)
        d = '{:02d}'.format(d)
        date = '.'.join([d, m, y])

        time = self.timeEdit.text().replace('.', ':')
        try:
            h, m, s = time.split(':')
        except ValueError:
            h, m = time.split(':')
            s = ''
        if s == '':
            s = '00'
        h, m, s = map(int, [h, m, s])
        h = '{:02d}'.format(h)
        m = '{:02d}'.format(m)
        s = '{:02d}'.format(s)
        time = ':'.join([h, m, s])

        if self.index != None:
            entry = tasks[self.index]
            tasks.remove(entry)
        text = self.textEdit.toPlainText()
        entry = Entry(date, time, text)
        tasks.append(entry)
        rewrite()
        if self.index != None: # if addWindow is called from editWindow
            self.parentWindow.show()
            self.parentWindow.window().show()
            self.parentWindow.scroll.show()
            self.parentWindow.fill()
        self.closeEvent(QCloseEvent())

    def closeEvent(self, event):
        """ Closes window. """
        event.ignore()
        if self.index != None:
            self.parentWindow.window().show()
            self.parentWindow.fill()
            self.parentWindow.parentWindow.addActive = False
        else:
            self.parentWindow.addActive = False
        self.hide()


class EditWindow(QWidget):
    """ Window for adding reminders.

    Useful attributes
    -----------------
    parentWindow : MainWindow object
        Parent of the window.
    scroll : QScrollArea object
        Scroll area of window.
    rows : list of dictionaries
        Element of rows is a dictionary:
            {'date', 'text', 'edit', 'del'}.
        'date' and 'text' are QLabels,
        'edit' and 'del' are QPushButtons.
        Such dictionary represents one element from tasks list.
    grid : QGridLayout object
        Layout of objects in QScrollArea.

    """
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
        self.parentWindow = parent
        self.parentWindow.editActive = True

    def initUI(self):
        """ Init user interface. """
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.rows = []
        self.fill()

        self.scroll = QScrollArea()
        self.scroll.setWidget(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.resize(500, 350)
        self.scroll.show()
        self.scroll.move(QApplication.desktop().screen().rect().center() -
                         self.rect().center())
        self.scroll.setWindowTitle(conf.lang['EDIT_TITLE'])
        self.scroll.setWindowIcon(QIcon('edit.ico'))
        self.scroll.closeEvent = self.closeEvent
        self.scroll.mousePressEvent = self.mousePressEvent

    def fill(self):
        """ Fill self.scroll by items that represens tasks """
        # delete items from self.grid
        for i in range(self.grid.count()):
            item = self.grid.itemAt(i)
            if isinstance(item, QSpacerItem):
                self.grid.removeItem(item)
            else:
                self.grid.itemAt(i).widget().close()

        self.rows = [{} for i in range(len(tasks))]
        if len(tasks) == 0:
            noLbl = QLabel(conf.lang['NO_TASKS'])
            noLbl.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(noLbl, 0, 0, 1, 5)
        else:
            for i in range(len(tasks)):
                datetime = ' '.join((dateToStr(tasks[i].getDateTime())['date'],
                                     dateToStr(tasks[i].getDateTime())['time']))
                # replace newlines and tabs in text, cut in on 25 symbols
                text = tasks[i].text.replace('\n', ' ').replace('\t', '   ')
                text = text[:25] + '...' if len(text) > 25 else text
                row = {}
                row['date'] = QLabel(datetime)
                row['text'] = QLabel(text)
                row['edit'] = QPushButton(conf.lang['EDIT'])
                row['del'] = QPushButton(conf.lang['DELETE'])
                row['edit'].setToolTip(conf.lang['EDIT_TOOLTIP_TEXT'])
                row['del'].setToolTip(conf.lang['DELETE_TOOLTIP_TEXT'])
                # pass k=i to lambda function to save value of i
                row['edit'].clicked.connect(lambda checked, k=i: self.edit(k))
                row['del'].clicked.connect(lambda checked, k=i: self.delete(k))

                self.rows[i] = row

                self.grid.addWidget(self.rows[i]['date'], i, 0)
                self.grid.addWidget(self.rows[i]['text'], i, 1, 1, 2)
                self.grid.addWidget(self.rows[i]['edit'], i, 3)
                self.grid.addWidget(self.rows[i]['del'], i, 4)
        # add spacer to pin rows to window's top side
        spacer = QSpacerItem(10, 0, vPolicy=QSizePolicy.MinimumExpanding)
        self.grid.addItem(spacer, len(tasks), 0, 1, 5)

    def edit(self, index):
        """ Open addWindow with selected task. """
        self.parentWindow.addActive = True
        self.parentWindow.showWindow('addAction')
        addWindow = self.parentWindow.addWindow
        addWindow.dateEdit.setText(dateToStr(tasks[index].
                                   getDateTime())['date'])
        addWindow.timeEdit.setText(dateToStr(tasks[index].
                                   getDateTime())['time'])
        addWindow.textEdit.setText(tasks[index].text)
        addWindow.parentWindow = self
        # pass index parameter to notice it in addWindow
        addWindow.index = index
        self.window().hide()

    def delete(self, index):
        """ Delete selected reminder from tasks list """
        entry = tasks[index]
        tasks.remove(entry)
        rewrite()
        self.fill()

    def closeEvent(self, event):
        """ Closes window. """
        self.parentWindow.editActive = False
        event.ignore()
        self.scroll.hide()
        self.hide()

""" main program part """

app = QApplication(sys.argv)
# Do not exit app if there're no opened windows
app.setQuitOnLastWindowClosed(False)
w = MainWindow()

def reload():
    global w
    params = (w.addActive, w.addWindow, w.editActive, w.editWindow)
    w.quit(False)
    w = MainWindow()
    for l in w.lang:
        w.lang[l].setChecked(False)
    w.lang[conf.lang['NAME']].setChecked(True)
    rewriteConfig()
    w.addActive, w.addWindow, w.editActive, w.editWindow = params
    if w.editWindow:
        w.editWindow.parentWindow = w
        w.editWindow.scroll.hide()
        w.editWindow.hide()
        w.editWindow = None
        if w.editActive:
            w.editActive = False
            w.showWindow('editAction')
    if w.addWindow:
        if w.addActive:
            index = w.addWindow.index
            date = w.addWindow.dateEdit.text()
            time = w.addWindow.timeEdit.text()
            text = w.addWindow.textEdit.toPlainText()
        w.addWindow.hide()
        if w.addActive:
            w.addActive = False
            if index != None:
            w.showWindow('addAction')
                w.addActive = False
                w.editActive = False
                w.showWindow('editAction')
                w.addActive = True
                w.editWindow.scroll.hide()
                w.editWindow.hide()
                w.addWindow.parentWindow = w.editWindow
            w.addWindow.dateEdit.setText(date)
            w.addWindow.timeEdit.setText(time)
            w.addWindow.textEdit.setText(text)
            w.addWindow.index = index

# Trying to read config file.
# If there's no config file, default config is loaded.
try:
    with open(config, 'r') as f:
        conf.load(json.loads(f.readlines()[0]))
    langSelect(conf.lang)
except IOError:
    pass
except Exception as e:
    errors.append(['{}\n{}'.format(conf.lang['SMTH_WRONG'], e),
                       '{}'.format(e)])

# Because of qt needs a widget to show message, errors are stored
# in list. When the main widget is created, every error in list
# is shown. After that, app is closed.
# If there're no errors script just passes the loop.
if len(errors) > 0:
    for err in errors:
        error(w, err[0], err[1])
    exit()

# Trying to read task list.
# If there's no tasks file, task list is empty.
try:
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            try:
                date, time, text = line.replace('\n', '').split('|')
                text = text.split('\'')[1]
                entry = Entry(date, time,
                              b64.b64decode(text).decode('utf-8'))
                tasks.append(entry)
            except:
                pass
except IOError:
    pass
except Exception as e:
    errors.append(['{}\n{}'.format(conf.lang['SMTH_WRONG'], e),
                       '{}'.format(e)])


# Execute application
sys.exit(app.exec_())
