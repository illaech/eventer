import os
import sys
from math import floor
import datetime as dt
import base64 as b64
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


# pre-exec definitions

errors = []  # see line XXX (will be specified later)

# select directory where 'calendar.txt' will be placed
if sys.platform == 'win32':
    if os.getenv('APPDATA') is not None:
        directory = '{}\\eventer'.format(os.getenv('APPDATA'))
        filename = '{}{}calendar.txt'.format(directory, '\\')
    else:
        errors.append(['Не найдена директория %appdata%',
                       'IOError: Can\'t find directory'])
elif sys.platform == 'linux' or sys.platform == 'linux2':
    if os.getenv('HOME') is not None:
        directory = '{}/.eventer'.format(os.getenv('HOME'))
        filename = '{}{}calendar.txt'.format(directory, '/')
    else:
        errors.append(['Не найдена директория /home/user',
                       'IOError: Can\'t find directory'])
else:  # what directory use in 'darwin'?
   errors.append(['Неподдерживаемая система', 'OSError: Unsupported system'])

if len(errors) == 0:
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            errors.append(['Не могу создать директорию "{}"'.format(directory),
                           'PermissionError: Can\'t create directory!' \
                           'First launch requires superuser privelegies'])

tasks = []


# global functions

def rewrite():
    """Update tasks file"""
    try:
       global tasks
       tasks = sorted(tasks, key=lambda x: strToDate('{} {}'.format(x.date,
                                                                    x.time)))
       with open(filename, 'w') as f:
           f.write('\n'.join([str(x) for x in tasks]))
    except IOError:
        errors.append(['Не могу открыть файл "{}"'.format(filename),
                       'IOError: Can\'t open file!'])

def dateToStr(datetime):
    """Convert datetime object to strings and return a dictionary"""
    time = datetime.strftime('%H:%M:%S')
    date = datetime.strftime('%d.%m.%Y')
    return {'time': time, 'date': date}

def strToDate(string):
    """Convert string to datetime object and return it"""
    datetime = dt.datetime.strptime(string, '%d.%m.%Y %H:%M:%S')
    return datetime

def error(widget, text, textconsole):
    """Show error message"""
    QMessageBox.critical(widget, 'Ошибка', text, QMessageBox.Ok,
                         QMessageBox.Ok)
    # Here "raise Exception(textconsole)" can be used to close
    # the application immediately after the first error.
    # Also, logging to text file can be used here.
    print(textconsole)


# main class definitions

class Entry:
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


# QT class definitions

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.tray = QSystemTrayIcon(QIcon('add.ico'), self)

        menu = QMenu()
        addAction = menu.addAction('Добавить задачу',
                    lambda: self.showWindow(QSystemTrayIcon.Trigger))
        editAction = menu.addAction('Изменить задачи',
                     lambda: self.showWindow('editAction'))
        menu.addSeparator()
        exitAction = menu.addAction('Выход', self.quit)

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
                msgBox.setWindowTitle('Задача {}'.format(date))
                msgBox.setWindowIcon(QIcon('alert.ico'))
                msgBox.setIcon(QMessageBox.Information)
                # msgBox.setTextFormat(Qt.RichText)
                msgBox.addButton(QPushButton('Закрыть'), QMessageBox.YesRole)
                msgBox.addButton(QPushButton('Повторить через 10м'),
                                             QMessageBox.NoRole)
                msgBox.setWindowFlags(Qt.WindowStaysOnTopHint);
                reply = msgBox.exec_();
                msgBox.raise_();

                if reply == 1:
                    date = dateToStr(dt.datetime.now() + dt.timedelta(0, 600))
                    tasks.append(Entry(date['date'], date['time'], entry.text))
                    rewrite()
                if self.editActive:
                    self.editWindow.fill()

    def showWindow(self, event):

        if event == QSystemTrayIcon.Trigger and not (self.addActive or
                    self.editActive) or event == 'addAction':
            self.addWindow = AddWindow(self)
            self.addWindow.show()
            self.addWindow.setFocus(True)
            self.addWindow.activateWindow()
        elif self.addActive:
            QApplication.alert(self.addWindow)
        elif self.editActive:
            QApplication.alert(self.editWindow)
        elif event == 'editAction' and not self.editActive:
            self.editWindow = EditWindow(self)
            self.editWindow.show()
            self.editWindow.setFocus(True)
            self.editWindow.activateWindow()

    def quit(self):
        self.tray.hide()
        QCoreApplication.instance().quit()


class AddWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.index = None
        self.initUI()
        self.parent = parent
        self.parent.addActive = True

    def initUI(self):
        self.setWindowTitle('Добавление задачи')
        self.setWindowIcon(QIcon('add.ico'))

        self.resize(350, 350)
        self.move(QApplication.desktop().screen().rect().center() -
                  self.rect().center())

        grid = QGridLayout()
        self.setLayout(grid)

        dateLbl = QLabel('Дата')
        timeLbl = QLabel('Время')
        self.dateEdit = QLineEdit()
        self.timeEdit = QLineEdit()
        self.textEdit = QTextEdit()
        self.saveButt = QPushButton('Сохранить')
        self.closeBut = QPushButton('Закрыть')

        dateLbl.setAlignment(Qt.AlignCenter)
        timeLbl.setAlignment(Qt.AlignCenter)

        dateToolTipText = 'Формат даты: дд.мм.гггг<br/>Можно использовать' \
                          ' сокращенные варианты: дд.мм.гг и дд.мм'
        timeToolTipText = 'Формат времени: чч:мм:сс<br/>Можно использовать' \
                          ' сокращенные варианты: чч:мм и ч:мм'

        self.dateEdit.setToolTip(dateToolTipText)
        self.timeEdit.setToolTip(timeToolTipText)
        dateLbl.setToolTip(dateToolTipText)
        timeLbl.setToolTip(timeToolTipText)
        self.textEdit.setToolTip('Текст напоминания')
        self.saveButt.setToolTip('Сохранить напоминания')
        self.closeBut = QPushButton('Закрыть окно')

        grid.addWidget(dateLbl, 0, 0)
        grid.addWidget(timeLbl, 0, 1)
        grid.addWidget(self.dateEdit, 1, 0)
        grid.addWidget(self.timeEdit, 1, 1)
        grid.addWidget(self.textEdit, 2, 0, 14, 2)
        grid.addWidget(self.saveButt, 16, 0)
        grid.addWidget(self.closeBut, 16, 1)

        dateRegExp = QRegExp(
            '^((0[1-9]|[1-2]\d|3[01])\.(01|03|05|07|08|10|12)|' \
            '(0[1-9]|[1-2]\d)\.02|' \
            '(0[1-9]|[1-2]\d|30)\.(04|06|09|11))(\.\d\d|\.\d\d\d[1-9])?$'
        )
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

        self.closeBut.clicked.connect(lambda: self.closeEvent(QCloseEvent()))
        self.saveButt.clicked.connect(self.save)

        self.checkButton()

    def checkState(self, sender):
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
        self.checkButton()

    def checkButton(self):
        self.saveButt.setEnabled(self.dateEdit.valid and self.timeEdit.valid)

    def save(self):
        date = self.dateEdit.text()
        try:
            d, m, y = date.split('.')
        except ValueError:
            d, m = date.split('.')
            y = ''
        if y == '':
            y = dt.datetime.today().year
        d, m, y = map(int, [d, m, y])
        if y < 100:
            y = floor(dt.datetime.today().year / 100) * 100 + y
        if y % 4 != 0 and m == 2 and d > 28:
            d = 28
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
        if self.index != None:
            self.parent.window().show()
            self.parent.fill()
        self.closeEvent(QCloseEvent())

    def closeEvent(self, event):
        event.ignore()
        if self.index != None:
            self.parent.window().show()
            self.parent.fill()
            self.parent.parent.addActive = False
        else:
            self.parent.addActive = False
        self.hide()


class EditWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
        self.parent = parent
        self.parent.editActive = True

    def initUI(self):
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
        self.scroll.setWindowTitle('Изменение задач')
        self.scroll.setWindowIcon(QIcon('edit.ico'))
        self.scroll.closeEvent = self.closeEvent;
        self.scroll.mousePressEvent = self.mousePressEvent;

    def fill(self):
        for i in range(self.grid.count()):
            self.grid.itemAt(i).widget().close()
        self.rows = [{} for i in range(len(tasks))]
        for i in range(len(tasks)):
           #datetime = ' '.join(dateToStr(tasks[i].getDateTime()).values())
           datetime = ' '.join((dateToStr(tasks[i].getDateTime())['date'],
                                dateToStr(tasks[i].getDateTime())['time']))
           text = tasks[i].text.replace('\n', ' ')
           text = text[:25] + '...' if len(text) > 25 else text
           row = {}
           row['date'] = QLabel(datetime)
           row['text'] = QLabel(text)
           row['edit'] = QPushButton('Изменить')
           row['del'] = QPushButton('Удалить')
           row['edit'].clicked.connect(lambda checked, i=i: self.edit(i))
           row['del'].clicked.connect(lambda checked, i=i: self.delete(i))
           self.rows[i] = row

           self.grid.addWidget(self.rows[i]['date'], i, 0)
           self.grid.addWidget(self.rows[i]['text'], i, 1, 1, 2)
           self.grid.addWidget(self.rows[i]['edit'], i, 3)
           self.grid.addWidget(self.rows[i]['del'], i, 4)

    def edit(self, index):
        self.parent.addActive = True
        self.parent.showWindow('addAction')
        addWindow = self.parent.addWindow
        addWindow.dateEdit.setText(dateToStr(tasks[index].
                                   getDateTime())['date'])
        addWindow.timeEdit.setText(dateToStr(tasks[index].
                                   getDateTime())['time'])
        addWindow.textEdit.setText(tasks[index].text)
        addWindow.parent = self
        addWindow.index = index
        self.window().hide()

    def delete(self, index):
        entry = tasks[index]
        tasks.remove(entry)
        rewrite()
        self.fill()

    def closeEvent(self, event):
        self.parent.editActive = False
        event.ignore()
        self.scroll.hide()
        self.hide()

app = QApplication(sys.argv)
# Do not exit app if there're no opened windows
app.setQuitOnLastWindowClosed(False);
w = Window()

# Because of qt needs a widget to show message, errors are stored
# in list. When the main widget is created, every error in list
# is shown. After that, app is closed.
# If there're no errors it just pass that loop.
if len(errors) > 0:
    for err in errors:
        error(w, err[0], err[1])
    exit()

try:
    with open(filename, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            try:
                date, time, text = line.split('|')
                text = text.split('\'')[1]
                entry = Entry(date, time,
                              b64.b64decode(text).decode('utf-8'))
                tasks.append(entry)
            except:
                pass
except IOError:
    tasks = []

sys.exit(app.exec_())
