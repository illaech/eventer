import os
import sys
from math import floor
import json
import datetime as dt
import base64 as b64
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from lang import RU, EN
import icons

""" Language. """

langs = {'RU': RU, 'EN': EN} # avaliable languages

def langSelect(config, lang):
    """ Change selected language. """
    config.lang = langs[lang]
    reload()

""" Timedelta formatting. """

def getFormattedStrTime(time, t_, td, tf, ts):
    """ Format 'time' to string with t_, td, tf and ts. """
    if time == 0:
        return 0
    t_dec, t_uni = int(time / 10) % 10, time % 10
    if t_dec == 0 and t_uni == 1:
        frmtd = '{} {}'.format(time, t_) # 1
    elif t_dec > 1 and t_uni == 1:
        frmtd = '{} {}'.format(time, td) # 21, 31, ...
    elif t_uni > 1 and t_uni < 5 and t_dec != 1:
        frmtd = '{} {}'.format(time, tf) # 2, 3, 4, 22, 23, 24, 32, 33, ...
    else:
        frmtd = '{} {}'.format(time, ts) # 5 to 20, 25 to 30, 35 to 40, ...
    return frmtd

def parseSeconds(num, dic=False):
    """ Format seconds to string includes days, hours, minutes and seconds. """
    days = floor(num / 86400)
    hours = floor(num % 86400 / 3600)
    minutes = floor(num % 86400 % 3600 / 60)
    seconds = floor(num % 86400 % 3600 % 60)

    if dic:
        return {'days': days, 'hours': hours,
                'minutes': minutes, 'seconds': seconds}

    days = getFormattedStrTime(days, conf.lang.DAY_, conf.lang.DAYD,
                               conf.lang.DAYF, conf.lang.DAYS)
    hours = getFormattedStrTime(hours, conf.lang.HOUR_, conf.lang.HOURD,
                                conf.lang.HOURF, conf.lang.HOURS)
    minutes = getFormattedStrTime(minutes, conf.lang.MINUTE_, conf.lang.MINUTED,
                                  conf.lang.MINUTEF, conf.lang.MINUTES)
    seconds = getFormattedStrTime(seconds, conf.lang.SECOND_, conf.lang.SECONDD,
                                  conf.lang.SECONDF, conf.lang.SECONDS)

    text = ''
    text += days if days != 0 else ''
    text += ', ' if (days != 0 and hours != 0 and minutes != 0
           and seconds != 0) else ''
    text += hours if hours != 0 else ''
    text += ', ' if (hours != 0 and minutes != 0 and seconds != 0) else ''
    text += minutes if minutes != 0 else ''
    text += ', ' if (minutes != 0 and seconds != 0) else ''
    text += seconds if seconds != 0 else ''

    if text == '':
        text = '{} {}'.format(seconds, conf.lang.SECONDS)
    return text

""" Icons. """

class Icon():
    """ Icon.

    Parameters
    ----------
    byte : base64-encoded byte string
        Set attribute 'base64' to 'byte'.
    icon : QIcon
        Set attribute 'icon' to 'icon'.

    Attributes
    ----------
    base64 : base64-encoded byte string
        Encoded pixmap of icon.
    icon : QIcon
        Icon itself.

    """
    def __init__(self, byte=b'', icon=None):
        self.base64 = byte
        self.icon = icon

    def setBytes(self, byte):
        """ Set attribute 'base64' to 'byte'. """
        self.base64 = byte
        return self

    def setIcon(self, icon):
        """ Set attribute 'icon' to 'icon'. """
        self.icon = icon
        return self

    def convertToIcon(self):
        """ Set 'icon' by converting 'base64' to QIcon. """
        byte = QByteArray().fromBase64(self.base64)
        image = QImage().fromData(byte, "ico");
        self.icon = QIcon(QPixmap().fromImage(image))
        return self

    def getIcon(self):
        """ Return 'icon'. """
        return self.icon

    def getBytes(self):
        """ Return 'base64'. """
        return self.base64

    def convertToBytes(self):
        """ Set 'base64' by converting 'icon' to bytes. """
        pass # work in progress

""" Config class. """

class Config:
    """ Config element.

    Parameters and attributes
    -------------------------
    lang : Language object
        Defines language of application.
    tdelta : int
        Defines time delta for repeating tasks, seconds.
    filter: bool
        If True filter in EditWindow will be shown.

    Attribute
    ---------
    supported : tuple
        Defines appropriate input parameters.

    """
    supported = ('lang', 'tdelta', 'filter', 'backup')

    def __init__(self, lang=RU, tdelta=600, filter=True, backup=300):
        self.lang = lang
        self.tdelta = tdelta
        self.filter = filter
        self.backup = backup

    def __str__(self):
        """ Represent current configuration. """
        dic = {}
        for i in self.supported:
            dic[i] = str(getattr(self, i)) if \
                     hasattr(getattr(self, i), '__dict__') else \
                     getattr(self, i)
        return json.dumps(dic)

    def load(self, dic):
        """ Load attributes from given dictionary. """
        for i in dic:
            if i not in self.supported:
                pass
            else:
                setattr(self, i, dic[i])

    def dump(self, f):
        """ Write current configuration to config file. """
        try:
            with open(f, 'w') as f_:
                f_.write(str(self))
        except IOError:
            errors.append(['{} "{}"'.format(self.lang['CANT_OPEN_FILE'], f),
                           'IOError: Can\'t open file!'])

conf = Config() # Config object

""" Preliminary definitions. """

errors = []  # see line 997

# select directory where 'calendar.txt' will be placed
if sys.platform == 'win32': # if platform is windows, choose %appdata%
    if os.getenv('APPDATA') is not None:
        directory = '{}\\eventer'.format(os.getenv('APPDATA'))
        filename = '{}{}calendar.txt'.format(directory, '\\')
        config = '{}{}config.txt'.format(directory, '\\')
        backup = '{}{}backup.txt'.format(directory, '\\')
    else:
        errors.append(['{} %appdata%'.format(conf.lang.CANT_FIND_DIR),
                       'IOError: Can\'t find directory'])
elif sys.platform == 'linux' or sys.platform == 'linux2':
    # if platform is linux, choose '~/.eventer'
    if os.getenv('HOME') is not None:
        directory = '{}/.eventer'.format(os.getenv('HOME'))
        filename = '{}{}calendar.txt'.format(directory, '/')
        config = '{}{}config.txt'.format(directory, '/')
        backup = '{}{}backup.txt'.format(directory, '/')
    else:
        errors.append(['{} /home/user'.format(conf.lang.CANT_FIND_DIR),
                       'IOError: Can\'t find directory'])
else:
   errors.append(['{}'.format(conf.lang.UNSUPPORT_SYS),
                  'OSError: Unsupported system'])

if len(errors) == 0: # if there're no errors, create directory
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except:
            errors.append(['{} "{}"'.
                           format(conf.lang.CANT_CREATE_DIR, directory),
                           'PermissionError: Can\'t create directory!'])

tasks = [] # array for reminders

""" Some common global definitions. """

def rewrite():
    """ Update tasks file. """
    try:
        global tasks
        tasks = sorted(tasks, key=lambda x: strToDate('{} {}'.format(x.date,
                                                                     x.time)))
        with open(filename, 'w') as f:
            f.write('\n'.join([str(x) for x in tasks]))
    except IOError:
        errors.append(['{} "{}"'.format(conf.lang.CANT_OPEN_FILE, filename),
                       'IOError: Can\'t open file!'])

def rewriteConfig():
    """ Update config file. """
    try:
        conf.dump(config)
    except IOError:
        errors.append(['{} "{}"'.format(conf.lang.CANT_OPEN_FILE, config),
                       'IOError: Can\'t open file!'])

def dateToStr(datetime):
    """Convert datetime object to strings and return a dictionary"""
    time = datetime.strftime('%H{d}%M{d}%S'.format(d=conf.lang.TIME_DELIM))
    date = datetime.strftime('%d{d}%m{d}%Y'.format(d=conf.lang.DATE_DELIM))
    return {'time': time, 'date': date}

def strToDate(string):
    """Convert string to datetime object and return it"""
    datetime = dt.datetime.strptime(string, '%d.%m.%Y %H:%M:%S')
    return datetime

def error(widget, text, textconsole):
    """Show error message"""
    QMessageBox.critical(widget, conf.lang.ERROR, text, QMessageBox.Ok,
                         QMessageBox.Ok)
    # Here "raise Exception(textconsole)" can be used to close
    # the application immediately after the first error.
    # Also, logging to text file can be used here.
    print(textconsole)

def clearLayout(layout):
    """ Removes all widgets from specific layout. """
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)
        if not isinstance(item, QSpacerItem):
            item.widget().close()
        layout.removeItem(item)


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


""" QT class definitions. """

class MainWindow(QWidget):
    """ Main window of application. It is represented by icon in
    taskbar.

    Useful attributes
    -----------------
    addWindow : AddWindow object
    addActive : boolean
        If user wants to add new task, 'addWindow' becomes the QWidget for
        it, and while it is active 'addActive' remains True.
    editWindow : EditWindow object
    editActive : boolean
        If user wants to edit tasks, 'editWindow' becomes the QWidget for
        it, and while it is active 'editActive' remains True.
    tray : QSystemTrayIcon object
        Tray icon and all its attributes like context menu and
        activated action.
    timer : QTimer object
        Timer that fires every second. If one reminder's time is up,
        shows message.
    backupTimer : QTimer object
        Timer that fires every 5 minutes. Saves current state of
        tasks file to backup file.

    """
    def __init__(self):
        """ Init GUI and all required things. """
        super().__init__()

        iconAdd = Icon(byte=icons.add).convertToIcon().getIcon()
        self.tray = QSystemTrayIcon(iconAdd, self)

        menu = QMenu()
        menu.addAction(conf.lang.ADD_ACTION,
                       lambda: self.showWindow(QSystemTrayIcon.Trigger))
        menu.addAction(conf.lang.EDIT_ACTION,
                       lambda: self.showWindow('editAction'))
        menu.addSeparator()
        menu.addAction(conf.lang.OPT_ACTION,
                       lambda: self.showWindow('optAction'))

        menu.addAction(conf.lang.RESTORE, self.restore)
        menu.addAction(conf.lang.QUIT, self.quit)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.showWindow)

        self.tray.show()
        self.addWindow = None
        self.addActive = False
        self.editWindow = None
        self.editActive = False
        self.optWindow = None
        self.optActive = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.timerTick)
        self.timer.start(1000)

        self.backup()
        self.backupTimer = QTimer()
        self.backupTimer.timeout.connect(self.backup)
        self.backupTimer.start(conf.backup * 1000)

    def timerTick(self):
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
                msgBox = QMessageBox()
                msgBox.setText(entry.text)
                msgBox.setWindowTitle('{} {}'.format(conf.lang.TASK, date))
                iconAlert = Icon(byte=icons.alert).convertToIcon().getIcon()
                msgBox.setWindowIcon(iconAlert)
                msgBox.setIcon(QMessageBox.Information)
                # msgBox.setTextFormat(Qt.RichText)
                msgBox.addButton(QPushButton(conf.lang.REPEAT.format(
                                             parseSeconds(conf.tdelta))),
                                 QMessageBox.YesRole)
                msgBox.addButton(QPushButton(conf.lang.CLOSE),
                                 QMessageBox.NoRole)
                msgBox.setWindowFlags(Qt.WindowStaysOnTopHint)
                reply = msgBox.exec_()
                msgBox.raise_()

                if reply == 0:
                    date = dateToStr(dt.datetime.now() + dt.timedelta(0,
                                                                conf.tdelta))
                    date['date'] = date['date'].replace('/', '.')
                    date['time'] = date['time'].replace('.', ':')
                    tasks.append(Entry(date['date'], date['time'], entry.text))
                rewrite()
                if self.editActive:
                    self.editWindow.filterApply()

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
        if event == 'editAction':
            if self.editActive:
                QApplication.alert(self.editWindow)
            else:
                self.editWindow = EditWindow(self)
                self.editWindow.show()
                self.editWindow.setFocus(True)
                self.editWindow.activateWindow()
            return self.editWindow
        elif event == 'addAction':
            self.addWindow = AddWindow(self)
            self.addWindow.show()
            self.addWindow.setFocus(True)
            self.addWindow.activateWindow()
            return self.addWindow
        elif event == QSystemTrayIcon.Trigger:
            if self.addActive:
                QApplication.alert(self.addWindow)
            else:
                self.addWindow = AddWindow(self)
                self.addWindow.show()
                self.addWindow.setFocus(True)
                self.addWindow.activateWindow()
            return self.addWindow
        elif event == 'optAction':
            if self.addActive:
                self.addWindow.hide()
            if self.editActive:
                self.editWindow.hide()
            self.optWindow = OptionsWindow(self)
            self.optWindow.show()
            self.optWindow.setFocus(True)
            self.optWindow.activateWindow()

    def backup(self):
        """ Copies content of tasks file to backup file. """
        with open(backup, 'w') as to_, open(filename, 'r') as from_:
            to_.write(from_.read())

    def restore(self):
        """ Restores content of tasks file from backup file after
        user confirmation.

        """
        global tasks
        shure = QMessageBox.question(self, conf.lang.RESTORE,
                                     conf.lang.RESTORE_TEXT,
                                     QMessageBox.No | QMessageBox.Yes,
                                     QMessageBox.No)

        if shure == QMessageBox.No:
            pass
        else:
            temp = open(backup).read() # don't forget to read backup
            self.backup()
            with open(filename, 'w') as to_:
                to_.write(temp)
            tasks = []
            readTasks()
            if self.editActive:
                self.editWindow.filterApply()

    def quit(self, really=True):
        """ Quits application. Hides tray icon firstly.
        If really is not True, do not quits the application.
        It is used to re-launch the application.

        """
        self.tray.hide()
        self.timer.stop()
        self.backupTimer.stop()
        if really:
            QCoreApplication.instance().quit()


class AddWindow(QWidget):
    """ Window for adding reminders.

    Useful attributes
    -----------------
    parentWindow : MainWindow object
        Parent of the window.
    (date|time)Edit : QLineEdit object
    textEdit : QTextEdit object
    (save|close)Btn : QPushButton object
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
        self.setWindowTitle(conf.lang.ADD_TITLE)
        iconAdd = Icon(byte=icons.add).convertToIcon().getIcon()
        self.setWindowIcon(iconAdd)

        self.resize(350, 350)
        self.move(QApplication.desktop().screen().rect().center() -
                  self.rect().center()) # center window on screen

        grid = QGridLayout()
        self.setLayout(grid)

        dateLbl = QLabel(conf.lang.DATE)
        timeLbl = QLabel(conf.lang.TIME)
        self.dateEdit = QLineEdit()
        self.timeEdit = QLineEdit()
        self.textEdit = QTextEdit()
        self.saveBtn = QPushButton(conf.lang.SAVE)
        self.closeBtn = QPushButton(conf.lang.CLOSE)

        dateLbl.setAlignment(Qt.AlignCenter)
        timeLbl.setAlignment(Qt.AlignCenter)

        dateToolTipText = conf.lang.DATE_TOOLTIP_TEXT
        timeToolTipText = conf.lang.TIME_TOOLTIP_TEXT

        self.dateEdit.setToolTip(dateToolTipText)
        self.timeEdit.setToolTip(timeToolTipText)
        dateLbl.setToolTip(dateToolTipText)
        timeLbl.setToolTip(timeToolTipText)
        self.textEdit.setToolTip(conf.lang.TEXT_TOOLTIP_TEXT)
        self.saveBtn.setToolTip(conf.lang.SAVE_TOOLTIP_TEXT)
        self.closeBtn.setToolTip(conf.lang.CLOSE_TOOLTIP_TEXT)

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
            '^(((0[1-9]|[1-9])|[1-2]\d|3[01])(/|\.)' \
            '((0)?1|(0)?3|(0)?5|(0)?7|(0)?8|10|12)|' \
            '((0[1-9]|[1-9])|[1-2]\d)(/|\.)(0)?2|' \
            '((0[1-9]|[1-9])|[1-2]\d|30)(/|\.)' \
            '((0)?4|(0)?6|(0)?9|11))' \
            '((/|\.)\d\d|(/|\.)' \
            '(\d\d\d[1-9]|\d\d[1-9]\d|\d[1-9]\d\d|[1-9]\d\d\d))?$'
        )
        """ regexp for time:
        23 hours, 59 minutes, 59 seconds;
        : or . as delimiter.
        """
        timeRegExp = QRegExp(
            '^([0-9]|[01]\d|2[0-3])(:|\.)(\d|[0-5]\d)((:|\.)(\d|[0-5]\d))?$'
        )
        dateValid = QRegExpValidator(dateRegExp)
        timeValid = QRegExpValidator(timeRegExp)
        self.dateEdit.validator = dateValid
        # if there's no text in lineEdits, pressing 'Return' button will
        # insert today's date and time in them, else it will return 0
        self.dateEdit.returnPressed.connect(lambda: \
            self.dateEdit.setText(dateToStr(dt.datetime.today())['date']) if
                self.dateEdit.text() is '' else 0)
        self.dateEdit.textChanged.connect(self.checkState)
        self.dateEdit.textChanged.emit(self.timeEdit.text())
        self.timeEdit.validator = timeValid
        self.timeEdit.returnPressed.connect(lambda: \
            self.timeEdit.setText(dateToStr(dt.datetime.today())['time']) if
                self.timeEdit.text() is '' else 0)
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
        """ Saves reminder. """
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
        self.closeEvent(QCloseEvent())

    def closeEvent(self, event):
        """ Closes window. """
        event.ignore()
        if self.index != None:
            self.parentWindow.parentWindow.addActive = False
            self.parentWindow.show()
            self.parentWindow.filterApply()
        else:
            if self.parentWindow.editActive:
                self.parentWindow.editWindow.filterApply()
            self.parentWindow.addActive = False
        self.hide()


class EditWindow(QWidget):
    """ Window for adding reminders.

    Useful attributes
    -----------------
    parentWindow : MainWindow object
        Parent of the window.
    taskArea : QScrollArea object
        Scroll area of window.
    rows : list of dictionaries
        Element of rows is a dictionary:
            {'date', 'text', 'edit', 'del'}.
        'date' and 'text' are QLabels,
        'edit' and 'del' are QPushButtons.
        Such dictionary represents one element from tasks list.
    grid : QGridLayout object
        Layout of objects in QScrollArea.
    activeTasks : list
        List of visible tasks in grid.
    filter : QHBoxLayout object
        Layout of filter widgets.
    (date|text)Field : QLineEdit object
        Filter widgets.

    """
    def __init__(self, parent=None):
        super().__init__()
        self.parentWindow = parent
        self.parentWindow.editActive = True
        self.activeTasks = tasks
        self.dateFieldText = ''
        self.textFieldText = ''
        self.initUI()

    def initUI(self):
        """ Init user interface. """
        # use QVBoxLayout to store two layouts vertically
        self.vl = QVBoxLayout()

        # widget for scrollArea
        self.topWidget = QWidget()
        self.grid = QGridLayout()
        self.topWidget.setLayout(self.grid)
        self.vl.addWidget(self.topWidget)

        # layout for filter
        self.filter = QHBoxLayout()
        # draw filter widgets
        self.drawFilter()
        spacer = QSpacerItem(10, 0, vPolicy=QSizePolicy.MinimumExpanding)
        self.vl.addItem(spacer)
        self.vl.addLayout(self.filter)

        self.setLayout(self.vl)
        self.rows = []

        self.taskArea = QScrollArea(self)
        self.taskArea.setWidget(self.topWidget)
        self.taskArea.setWidgetResizable(True)
        self.taskArea.resize(500, 350)
        self.resize(500, 395)
        self.setMinimumSize(460, 90)
        self.filterApply()
        self.show()
        self.move(QApplication.desktop().screen().rect().center() -
                  self.rect().center())
        self.setWindowTitle(conf.lang.EDIT_TITLE)
        iconEdit = Icon(byte=icons.edit).convertToIcon().getIcon()
        self.setWindowIcon(iconEdit)

    def drawFilter(self):
        """ Draws filter widgets. """
        clearLayout(self.filter)

        self.hideBtn = QPushButton()
        if conf.filter:
            self.hideBtn.setText(conf.lang.VISIBLE_F)
            self.hideBtn.setFixedSize(23, 23)
            self.vl.setContentsMargins(11, 11, 11, 11)
        else:
            self.hideBtn.setText(conf.lang.HIDDEN_F)
            self.hideBtn.setFixedSize(23, 15)
            self.vl.setContentsMargins(0, 0, 0, 0)
        self.hideBtn.clicked.connect(self.inverseFilter)
        self.filter.addWidget(self.hideBtn)
        if conf.filter:
            filterLbl = QLabel(conf.lang.FILTER)
            filterLbl.setStyleSheet('QLabel {' \
                                            'border-width: 0 1px 0 0;' \
                                            'border-style: solid;' \
                                            'border-color: black;' \
                                            'margin: 0 5px 0 0;' \
                                           '}')
            self.filter.addWidget(filterLbl)

            dateLbl = QLabel(conf.lang.DATE_F)
            self.filter.addWidget(dateLbl)
            self.dateField = QLineEdit()
            self.dateField.setText(self.dateFieldText)
            self.filter.addWidget(self.dateField)

            textLbl = QLabel(conf.lang.TEXT_F)
            self.filter.addWidget(textLbl)
            self.textField = QLineEdit()
            self.textField.setText(self.textFieldText)
            self.filter.addWidget(self.textField)

            self.dateField.textChanged.connect(self.filterApply)
            self.textField.textChanged.connect(self.filterApply)

    def inverseFilter(self):
        """ Change state of filter. """
        conf.filter = not conf.filter
        rewriteConfig()
        if not conf.filter:
            self.dateFieldText = self.dateField.text()
            self.textFieldText = self.textField.text()
        self.drawFilter()
        self.resizeEvent(QResizeEvent(QSize(self.width(), self.height()),
                                      QSize(self.width(), self.height())))

    def fill(self):
        """ Fill self.taskArea by items that represens tasks. """
        # delete items from self.grid
        clearLayout(self.grid)

        aTasks = self.activeTasks
        self.rows = [{} for i in range(len(aTasks))]
        if len(aTasks) == 0:
            noLbl = QLabel(conf.lang.NO_TASKS)
            noLbl.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(noLbl, 0, 0, 1, 5)
        else:
            for i in range(len(aTasks)):
                datetime = ' '.join((dateToStr(aTasks[i].getDateTime())['date'],
                                     dateToStr(aTasks[i].getDateTime())['time']))
                # replace newlines and tabs in text
                text = aTasks[i].text.replace('\n', ' ').replace('\t', '   ')
                row = {}
                row['date'] = QLabel(datetime)
                row['text'] = QLabel()
                # change label's resizeEvent
                # with passing QLabel and text
                row['text'].resizeEvent = \
                            lambda evt, lbl=row['text'], txt=text: \
                                   self.labelResize(lbl, evt, txt)
                row['edit'] = QPushButton(conf.lang.EDIT)
                row['del'] = QPushButton(conf.lang.DELETE)
                row['edit'].setToolTip(conf.lang.EDIT_TOOLTIP_TEXT)
                row['del'].setToolTip(conf.lang.DELETE_TOOLTIP_TEXT)
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
        self.grid.addItem(spacer, len(aTasks), 0, 1, 5)
        self.grid.setColumnMinimumWidth(0, 100)
        self.grid.setColumnMinimumWidth(3, 80)
        self.grid.setColumnMinimumWidth(4, 80)
        for i in range(self.grid.columnCount()):
            self.grid.setColumnStretch(i, 0)
        self.grid.setColumnStretch(1, 1)

    def labelResize(self, label, event, text):
        """ Change label's text due to its size. """
        width = self.taskArea.width() - 320
        # if get width from event: width = event.size().width()
        # resizing will stop when full text is shown in label
        metrics = QFontMetrics(label.font())
        ellipsis = metrics.elidedText(text, Qt.ElideRight, width)
        label.setText(ellipsis)

    def filterApply(self):
        """ Selects tasks to be shown. """
        date = self.dateField.text()
        text = self.textField.text().replace('\n', ' ').replace('\t', '   ')
        text = text.lower()

        aTasks = []
        for i in tasks:
            datetime = ' '.join((dateToStr(i.getDateTime())['date'],
                                 dateToStr(i.getDateTime())['time']))
            tasktext = i.text.replace('\n', ' ').replace('\t', '   ')
            tasktext = tasktext.lower()
            if datetime.find(date) > -1 and tasktext.find(text) > -1:
                aTasks.append(i)

        self.activeTasks = aTasks
        self.fill()

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
        self.hide()

    def delete(self, index):
        """ Delete selected reminder from tasks list. """
        entry = tasks[index]
        tasks.remove(entry)
        rewrite()
        self.filterApply()

    def resizeEvent(self, event):
        """ Resize taskArea due to size of window. """
        width = event.size().width()
        height = self.size().height()
        if conf.filter:
            self.taskArea.resize(width, height - 45)
        else:
            self.taskArea.resize(width, height - 15)

    def closeEvent(self, event):
        """ Closes window. """
        self.parentWindow.editActive = False
        event.ignore()
        self.hide()


class OptionsWindow(QWidget):
    """ Window for changing settings.

    Useful attributes
    -----------------

    """
    def __init__(self, parent=None):
        super().__init__()
        self.parentWindow = parent
        self.parentWindow.optActive = True
        self.initUI()

    def initUI(self):
        """ Init user interface. """
        self.setWindowTitle(conf.lang.OPT_TITLE)
        iconOpt = Icon(byte=icons.options).convertToIcon().getIcon()
        self.setWindowIcon(iconOpt)

        self.resize(500, 150)
        self.move(QApplication.desktop().screen().rect().center() -
                  self.rect().center()) # center window on screen

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.fill()

    def fill(self):
        """ Fills windows with widgets. """
        clearLayout(self.grid)
        tdeltaDict = parseSeconds(conf.tdelta, dic=True)

        self.grid.addWidget(QLabel(conf.lang.CHANGE_LANGUAGE), 0, 0)
        self.langCombo = QComboBox()
        langList = []
        for i in langs.values():
            if i.NAME == conf.lang.NAME:
                langList.insert(0, i.FULL_NAME)
            else:
                langList.append(i.FULL_NAME)

        self.langCombo.insertItems(0, langList)
        self.grid.addWidget(self.langCombo, 0, 1, 1, 4)

        self.grid.addWidget(QLabel(conf.lang.CHANGE_TDELTA), 1, 0)
        self.tdeltaDaysEdit = QLineEdit()
        self.tdeltaDaysEdit.setText(str(tdeltaDict['days']))
        self.tdeltaDaysEdit.setValidator(QIntValidator(0, 999))
        self.grid.addWidget(self.tdeltaDaysEdit, 1, 1)
        self.grid.addWidget(QLabel(conf.lang.DAYS), 1, 2)
        self.tdeltaHoursEdit = QLineEdit()
        self.tdeltaHoursEdit.setText(str(tdeltaDict['hours']))
        self.tdeltaHoursEdit.setValidator(QIntValidator(0, 23))
        self.grid.addWidget(self.tdeltaHoursEdit, 1, 3)
        self.grid.addWidget(QLabel(conf.lang.HOURS), 1, 4)
        self.tdeltaMinsEdit = QLineEdit()
        self.tdeltaMinsEdit.setText(str(tdeltaDict['minutes']))
        self.tdeltaMinsEdit.setValidator(QIntValidator(0, 59))
        self.grid.addWidget(self.tdeltaMinsEdit, 1, 5)
        self.grid.addWidget(QLabel(conf.lang.MINUTES), 1, 6)
        self.tdeltaSecsEdit = QLineEdit()
        self.tdeltaSecsEdit.setText(str(tdeltaDict['seconds']))
        self.tdeltaSecsEdit.setValidator(QIntValidator(0, 59))
        self.grid.addWidget(self.tdeltaSecsEdit, 1, 7)
        self.grid.addWidget(QLabel(conf.lang.SECONDS), 1, 8)

        self.grid.addWidget(QLabel(conf.lang.BACKUP_TIMER), 2, 0)
        self.backupMinsEdit = QLineEdit()
        self.backupMinsEdit.setText(str(int(conf.backup / 60)))
        self.backupMinsEdit.setValidator(QIntValidator(0, 999))
        self.grid.addWidget(self.backupMinsEdit, 2, 1)
        self.grid.addWidget(QLabel(conf.lang.MINUTES), 2, 2)

        spacer = QSpacerItem(10, 0, vPolicy=QSizePolicy.MinimumExpanding)
        self.grid.addItem(spacer, 3, 0)

        saveBtn = QPushButton(conf.lang.SAVE)
        saveBtn.clicked.connect(self.save)
        self.grid.addWidget(saveBtn, 4, 5, 1, 2)
        closeBtn = QPushButton(conf.lang.CLOSE)
        closeBtn.clicked.connect(lambda: self.closeEvent(QCloseEvent()))
        self.grid.addWidget(closeBtn, 4, 7, 1, 2)

    def save(self):
        tdelta = [self.tdeltaSecsEdit.text(), self.tdeltaMinsEdit.text(),
                  self.tdeltaHoursEdit.text(), self.tdeltaDaysEdit.text()]
        tdelta = list(map(lambda x: int(x) if x != '' else 0, tdelta))
        tdelta[1] *= 60
        tdelta[2] *= 3600
        tdelta[3] *= 86400
        tdelta = sum(tdelta)
        conf.tdelta = tdelta

        if self.backupMinsEdit.text() == '':
            self.backupMinsEdit.setText('0')
        backup = int(self.backupMinsEdit.text())
        if backup == 0:
            backup = 5
        conf.backup = backup * 60

        if self.langCombo.currentText() != conf.lang.FULL_NAME:
            for i in langs.values():
                if i.FULL_NAME == self.langCombo.currentText():
                    conf.lang = i

        self.closeEvent(QCloseEvent(), changed=True)

    def closeEvent(self, event, changed=False):
        """ Closes window. """
        self.parentWindow.optActive = False
        if self.parentWindow.addActive:
            self.parentWindow.addWindow.show()
            if self.parentWindow.addWindow.index == None:
                if self.parentWindow.editActive:
                    self.parentWindow.editWindow.show()
        else:
            if self.parentWindow.editActive:
                self.parentWindow.editWindow.show()

        event.ignore()

        if changed:
            reload()

        self.hide()

""" "Main" program part. """

app = QApplication(sys.argv)
# Do not exit app if there're no opened windows
app.setQuitOnLastWindowClosed(False)
w = MainWindow()

def reload():
    """ Restart the application. """
    global w
    params = (w.addActive, w.addWindow, w.editActive, w.editWindow)
    w.quit(False) # 'really' parameter is set to False
    w = MainWindow() # do it again
    rewriteConfig()
    # restore parameters
    w.addActive, w.addWindow, w.editActive, w.editWindow = params
    if w.editWindow:
        w.editWindow.parentWindow = w
        w.editWindow.hide()
        w.editWindow = None
        if w.editActive:
            w.editActive = False
            if w.addActive:
                if w.addWindow.index != None:
                    pass
                else:
                    w.showWindow('editAction')
            else:
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
            w.showWindow('addAction')
            if index != None:
                w.addActive = False
                w.editActive = False
                w.showWindow('editAction')
                w.addActive = True
                w.editWindow.hide()
                w.addWindow.parentWindow = w.editWindow
            w.addWindow.dateEdit.setText(date)
            w.addWindow.timeEdit.setText(time)
            w.addWindow.textEdit.setText(text)
            w.addWindow.index = index

def readConfig():
    """ Read config file and apply its parameters. """
    # Trying to read config file.
    # If there's no config file, default config is loaded.
    try:
        with open(config, 'r') as f:
            conf.load(json.loads(f.readlines()[0]))
        langSelect(conf, conf.lang)
    except IOError:
        pass
    except Exception as e:
        errors.append(['{}\n{}'.format(conf.lang.SMTH_WRONG, e),
                       '{}'.format(e)])

def readTasks():
    """ Read reminders list. """
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
        errors.append(['{}\n{}'.format(conf.lang.SMTH_WRONG, e),
                       '{}'.format(e)])

readConfig()
readTasks()

# Because of qt needs a widget to show message, errors are stored
# in list. When the main widget is created, every error in list
# is shown. After that, app is closed.
# If there're no errors script just passes the loop.
if len(errors) > 0:
    for err in errors:
        error(w, err[0], err[1])
    exit()

# Execute application
sys.exit(app.exec_())
