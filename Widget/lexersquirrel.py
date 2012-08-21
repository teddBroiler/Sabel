from PyQt4.Qsci import QsciLexerCustom,QsciStyle,QsciScintilla
from PyQt4.QtCore import QString
from PyQt4.QtGui import QFont, QColor
from globals import fontName, fontSize

class LexerSquirrel(QsciLexerCustom):
    words1 = [
         'base','break','case','catch','class','clone',
         'continue','const','default','delete','else','enum',
         'extends','for','foreach','function','if','in',
         'local','null','resume','return','switch','this',
         'throw','try','typeof','while','yield','constructor',
         'instanceof','true','false','static'
        ]
        
    words2 = [
         'init', 'dest', 'onLoad', 'onDispose', 'onGainedFocus','onMotionEvent',
         'onLostFocus','onUpdate','onFps','onKeyEvent','onSensorEvent',
         'onControlEvent','onDrawFrame','onError','onLowMemory','onNetCallBack'
        ]

    words3 = [
        'rawdelete', 'rawin', 'array', 'seterrorhandler', 'setdebughook',
        'enabledebuginfo', 'getroottable', 'setroottable', 'getconsttable',
        'setconsttable', 'assert', 'print', 'compilestring', 'collectgarbage',
        'type', 'getstackinfos', 'newthread', 'tofloat', 'tostring',
        'tointeger', 'tochar', 'weakref', 'slice', 'find', 'tolower',
        'toupper', 'len', 'rawget', 'rawset', 'clear', 'append', 'push',
        'extend', 'pop', 'top', 'insert', 'remove', 'resize', 'sort',
        'reverse', 'call', 'pcall', 'acall', 'pacall', 'bindenv', 'instance',
        'getattributes', 'getclass', 'getstatus', 'ref'
        ]
        
    words4 = [
         ]
    def __init__(self,colorStyle, parent = None):
        QsciLexerCustom.__init__(self, parent)
        self.parent = parent
        self.sci = self.parent
        self.colorStyle = colorStyle
        self.plainFont = QFont()
        self.plainFont.setFamily(fontName)
        self.plainFont.setFixedPitch(True)
        self.plainFont.setPointSize(fontSize)
        self.marginFont = QFont()
        self.marginFont.setPointSize(10)
        self.marginFont.setFamily("MS Dlg")
        self.boldFont = QFont()
        self.boldFont.setPointSize(10)
        self.boldFont.setFamily("Courier New")
        self.boldFont.setBold(True)
        self.styles = [
          #index description color paper font eol
          QsciStyle(0, QString("base"), self.colorStyle.color, self.colorStyle.paper, self.plainFont, True),
          QsciStyle(1, QString("comment"), QColor("#008000"), QColor("#eeffee"), self.marginFont, True),
          QsciStyle(2, QString("keyword"), QColor("#000080"), QColor("#ffffff"), self.boldFont, False),
          QsciStyle(3, QString("string"), QColor("#800000"), QColor("#ffffff"), self.marginFont, True),
          QsciStyle(4, QString("atom"), QColor("#008080"), QColor("#ffffff"), self.plainFont, True),
          QsciStyle(5, QString("macro"), QColor("#808000"), QColor("#ffffff"), self.boldFont, True),
          QsciStyle(6, QString("error"), QColor("#000000"), QColor("#ffd0d0"), self.plainFont, True),
        ]
        #print("LexerErlang created")
        
    def setColorStyle(self,cs):
        self.colorStyle = cs
        self.styles[0].setColor(self.colorStyle.color)
        self.styles[0].setPaper(self.colorStyle.paper)
        
    def language(self):
        return 'Squirrel'
    
    def foldCompact(self):
        return self._foldcompact

    def setFoldCompact(self, enable):
        self._foldcompact = bool(enable)

    def description(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.description()
        return QString("")
    
    def defaultColor(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.color()
        return QsciLexerCustom.defaultColor(self, ix)

    def defaultFont(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.font()
        return QsciLexerCustom.defaultFont(self, ix)

    def defaultPaper(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.paper()
        return QsciLexerCustom.defaultPaper(self, ix)

    def defaultEolFill(self, ix):
        for i in self.styles:
          if i.style() == ix:
            return i.eolFill()
        return QsciLexerCustom.defaultEolFill(self, ix)
    
    def styleText(self, start, end):
        editor = self.editor()
        if editor is None:
            return

        SCI = editor.SendScintilla
        set_style = self.setStyling

        source = ''
        if end > editor.length():
            end = editor.length()
        if end > start:
            source = bytearray(end - start)
            SCI(QsciScintilla.SCI_GETTEXTRANGE, start, end, source)
        if not source:
            return

        self.startStyling(start, 0x1f)

        index = SCI(QsciScintilla.SCI_LINEFROMPOSITION, start)

        for line in source.splitlines(True):
# Try to uncomment the following line to see in the console
# how Scintiallla works. You have to think in terms of isolated
# lines rather than globally on the whole text.
          #  print line

            length = len(line)

            if line.startswith('#'):
                newState = self.styles[3]
            elif line.startswith('\t+') or line.startswith('    +'):
                newState = self.styles[3]
            else:
                pos = SCI(QsciScintilla.SCI_GETLINEENDPOSITION, index) - length + 1
                i = 0
                while i < length:
                    wordLength = 1

                    self.startStyling(i + pos, 0x1f)
                    newState = self.styles[0]
                    """
                    for word in self.words1:
                        if line[i:].startswith(word):
                                newState = self.styles[3]
                                wordLength = len(word)
                        
                    """
                    if chr(line[i]) in '0123456789':
                        newState = self.styles[4]
                    else:
                        if line[i:].startswith("class"):
                                newState = self.styles[2]
                                wordLength = len('class')
                        elif line[i:].startswith('function'):
                                newState = self.styles[3]
                                wordLength = len('function')
                        elif line[i:].startswith('if'):
                                newState = self.styles[4]
                                wordLength = len('if')
                        elif line[i:].startswith('#'):
                                newState = self.styles[4]
                                wordLength = length
                        elif line[i:].startswith('//'):
                                newState = self.styles[4]
                                wordLength = length
                        else:
                            newState = self.styles[0]
                         
                    i += wordLength
                    set_style(wordLength, newState)
                newState = None
            if newState:
                set_style(length, newState)

            index += 1


import sys
from PyQt4 import QtCore, QtGui, Qsci

class MainWindow(QtGui.QMainWindow):
     def __init__(self):
         QtGui.QMainWindow.__init__(self)
         self.setWindowTitle('Custom Lexer Example')
         self.setGeometry(QtCore.QRect(50,200,400,400))
         self.editor = Qsci.QsciScintilla(self)
         self.editor.setUtf8(True)
         self.editor.setMarginWidth(2, 15)
         self.editor.setFolding(True)
         self.setCentralWidget(self.editor)
         self.lexer = CustomLexer(self.editor)
         self.editor.setLexer(self.lexer)
         self.editor.setText('\n# sample source\n\nfoo = 1\nbar = 2\n')

class CustomLexer(Qsci.QsciLexerCustom):
     def __init__(self, parent):
         Qsci.QsciLexerCustom.__init__(self, parent)
         self._styles = {
             0: 'Default',
             1: 'Comment',
             2: 'Key',
             3: 'Assignment',
             4: 'Value',
             }
         for key,value in self._styles.iteritems():
             setattr(self, value, key)

     def description(self, style):
         return self._styles.get(style, '')

     def defaultColor(self, style):
         if style == self.Default:
             return QtGui.QColor('#000000')
         elif style == self.Comment:
             return QtGui.QColor('#C0C0C0')
         elif style == self.Key:
             return QtGui.QColor('#0000CC')
         elif style == self.Assignment:
             return QtGui.QColor('#CC0000')
         elif style == self.Value:
             return QtGui.QColor('#00CC00')
         return Qsci.QsciLexerCustom.defaultColor(self, style)

     def styleText(self, start, end):
         editor = self.editor()
         if editor is None:
             return

         # scintilla works with encoded bytes, not decoded characters.
         # this matters if the source contains non-ascii characters and
         # a multi-byte encoding is used (e.g. utf-8)
         source = ''
         if end > editor.length():
             end = editor.length()
         if end > start:
             if sys.hexversion >= 0x02060000:
                 # faster when styling big files, but needs python 2.6
                 source = bytearray(end - start)
                 editor.SendScintilla(
                     editor.SCI_GETTEXTRANGE, start, end, source)
             else:
                 source = unicode(editor.text()
                                 ).encode('utf-8')[start:end]
         if not source:
             return

         # the line index will also be needed to implement folding
         index = editor.SendScintilla(editor.SCI_LINEFROMPOSITION, start)
         if index > 0:
             # the previous state may be needed for multi-line styling
             pos = editor.SendScintilla(
                       editor.SCI_GETLINEENDPOSITION, index - 1)
             state = editor.SendScintilla(editor.SCI_GETSTYLEAT, pos)
         else:
             state = self.Default

         set_style = self.setStyling
         self.startStyling(start, 0x1f)

         # scintilla always asks to style whole lines
         for line in source.splitlines(True):
             length = len(line)
             if line.startswith('#'):
                 state = self.Comment
             else:
                 # the following will style lines like "x = 0"
                 pos = line.find('=')
                 if pos > 0:
                     set_style(pos, self.Key)
                     set_style(1, self.Assignment)
                     length = length - pos - 1
                     state = self.Value
                 else:
                     state = self.Default
             set_style(length, state)
             # folding implementation goes here
             levelFolder = editor.SendScintilla(editor.SCI_GETFOLDLEVEL, index-1)
             if line.startswith('+ '):
                 editor.SendScintilla(editor.SCI_SETFOLDLEVEL, index, levelFolder + 1)
             index += 1

if __name__ == "__main__":
     app = QtGui.QApplication(sys.argv)
     app.connect(app, QtCore.SIGNAL('lastWindowClosed()'),
                 QtCore.SLOT('quit()'))
     win = MainWindow()
     win.show()
     sys.exit(app.exec_())
