# coding=utf-8


class PyLuaTblParser():
    # 初始化方法
    def __init__(self):
        self.index = 0
        self.lenStr = 0
        self.luaStr = ''
        self.myDict = {}


    # 私有方法
    # 处理 ' 和 " 开头的字符串
    def __stringHandle(self):
        flag = self.__readChar()
        string = ''
        currentChar = self.__readNextChar()
        while currentChar != '':
            # 处理反斜杠的情况
            if currentChar == '\\':
                offset = 1
                nextChar = self.__readCharAt(offset)
                if nextChar == 'a':
                    string += '\a'
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == 'b':
                    string += '\b'
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == 'f':
                    string += '\f'
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == 'n':
                    string += '\n'
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == 'r':
                    string += '\r'
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == 't':
                    string += '\t'
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == 'v':
                    string += '\v'
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == '\\':
                    string += '\\'
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == '\"':
                    string += '\"'
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == '\'':
                    string += '\''
                    self.__moveIndex(offset)
                    currentChar = self.__readNextChar()
                elif nextChar == 'x':
                    self.__moveIndex(offset+1)
                    try:
                        string += chr(int(self.__readCharUntil(2), 16))
                    except:
                        raise Exception("Error : 字符串格式错误； index： " + str(self.index))
                    self.__moveIndex(2)
                    currentChar = self.__readChar()
                elif nextChar.isdigit() == True:
                    self.__moveIndex(offset)
                    try:
                        string += chr(int(self.__readCharUntil(3)))
                    except:
                        raise Exception("Error : 字符串格式错误； index： " + str(self.index))
                    self.__moveIndex(3)
                    currentChar = self.__readChar()
                else:
                    raise Exception("Error : 字符串格式错误； index： " + str(self.index))
                continue

            elif currentChar == flag:
                currentChar = self.__readNextChar()
                while currentChar == ' ' or currentChar == '\n' or currentChar == '\t':
                    currentChar = self.__readNextChar()

                if self.__readCharUntil(4) == '--[[':
                    self.__moveIndex(4)
                    self.__commentHandle()
                elif self.__readCharUntil(2) == '--':
                    self.__moveIndex(2)
                    self.__commentSingleHandle()
                elif self.__readCharUntil(2) == '..':
                    self.__moveIndex(2)
                    currentChar = self.__readChar()
                    while currentChar == ' ' or currentChar == '\n' or currentChar == '\t':
                        currentChar = self.__readNextChar()

                    if self.__readCharUntil(4) == '--[[':
                        self.__moveIndex(4)
                        self.__commentHandle()
                    elif self.__readCharUntil(2) == '--':
                        self.__moveIndex(2)
                        self.__commentSingleHandle()
                    elif currentChar == '"' or currentChar == "'":
                        string += self.__stringHandle()
                        currentChar = self.__readChar()
                        continue
                    elif self.__readCharUntil(2) == '[[':
                        self.__moveIndex(1)
                        string += self.__stringBracketHandle()
                        currentChar = flag
                        continue
                    else:
                        raise Exception("Error : 字符串格式错误； ‘..' 之后应当接字符串； index： " + str(self.index) + "； char: " + currentChar)
                elif currentChar == ',' or currentChar == '}' or currentChar == ']':
                    self.__moveIndex(-1)
                    break

            string += currentChar
            currentChar = self.__readNextChar()

        if currentChar == '':
            raise Exception("Error : 字符串格式错误；字符串 '" + string + "' 缺少结束符； index： " + str(self.index))

        return string

    # 处理 [[ 开头的字符串，[[]]包围的字符串不需要处理反斜杠问题
    def __stringBracketHandle(self):
        string = ''
        currentChar = self.__readNextChar()
        while currentChar != '':
            if self.__readCharUntil(2) == ']]':
                offset = 2
                nextChar = self.__readCharAt(offset)
                while nextChar == ' ' or nextChar == '\n' or nextChar == '\t':
                    offset += 1
                    nextChar = self.__readCharAt(offset)
                if nextChar == ',' or nextChar == '}':
                    self.__moveIndex(offset-1)
                    break
                elif nextChar == '.' and self.__readCharAt(offset+1) == '.':
                    offset += 2
                    nextChar = self.__readCharAt(offset)
                    while nextChar == ' ' or nextChar == '\n' or nextChar == '\t':
                        offset += 1
                        nextChar = self.__readCharAt(offset)
                    if nextChar == '"' or nextChar == "'":
                        self.__moveIndex(offset)
                        string += self.__stringHandle()
                        break
                    elif nextChar == '[' and self.__readCharAt(offset+1) == '[':
                        self.__moveIndex(offset+1)
                        string += self.__stringBracketHandle()
                        break
                    else:
                        raise Exception("Error : 字符串格式错误； ‘..' 之后应当接字符串； index： " + str(self.index + offset) + "； char: " + nextChar)

            string += currentChar
            currentChar = self.__readNextChar()

        if currentChar == '':
            raise Exception("Error : 字符串格式错误；字符串 '" + string + "' 缺少结束符； index： " + str(self.index))

        return string

    # 处理单行注释
    def __commentSingleHandle(self):
        currentChar = self.__readChar()
        while currentChar != '\n' and currentChar != '':
            currentChar = self.__readNextChar()

    # 处理多行注释，不考虑嵌套注释
    def __commentHandle(self):
        while self.__readCharUntil(4) != '--]]' and self.__readCharUntil(4) != '':
            self.__moveIndex(1)
        self.__moveIndex(3)

    # 将字符串转换为数字，同时检查数字合法性，
    # 输入的数字一定以数字开头，不存在 .123 和 -456 的情况
    def __str2num(self, string):
        # 去除开头的0
        number = 0
        # 处理16进制数
        if string[0:2] == '0x' or string[0:2] == '0X':
            hasPoint = False
            exp = 1
            i = 2
            while i < len(string) and string[i] == '0' and i + 1 < len(string) and string[i] != '.':
                i += 1
            while i < len(string):
                if string[i].isdigit() == True:
                    if hasPoint == False:
                        number = number * 16 + int(string[i])
                    else:
                        number += float(string[i]) / (exp * 16)
                        exp += 1
                elif ord(string[i]) >= 65 and ord(string[i]) <= 70:
                    currentBit = 10 + ord(string[i]) - 65
                    if hasPoint == False:
                        number = number * 16 + currentBit
                    else:
                        number += float(currentBit) / (exp * 16)
                        exp += 1
                elif ord(string[i]) >= 97 and ord(string[i]) <= 102:
                    currentBit = 10 + ord(string[i]) - 97
                    if hasPoint == False:
                        number = number * 16 + currentBit
                    else:
                        number += float(currentBit) / (exp * 16)
                        exp += 1
                elif string[i] == 'p' or string[i] == 'P':
                    if i + 1 >= len(string):
                        raise Exception("Error : 数字 " + string + " 非法")
                    else:
                        try:
                            p = int(string[i + 1:])
                        except:
                            raise Exception("Error : 数字 " + string + " 非法")
                        if p < 0:
                            number /= -1 * float(p) + 1
                        else:
                            number *= p + 1
                    break
                elif string[i] == '.':
                    if hasPoint == False:
                        hasPoint = True
                        number = float(number)
                    else:
                        raise Exception("Error : 数字 " + string + " 非法")
                else:
                    raise Exception("Error : 数字 " + string + " 非法")
                i += 1
        else:
            try:
                if '.' in string:
                    number = float(string)
                else:
                    number = int(string)
            except:
                raise Exception("Error : 数字 " + string + " 非法")

        return number

    # 处理数字
    def __numberHandle(self):
        number = ''
        positive = True
        currentChar = self.__readChar()
        if currentChar == '-':
            currentChar = self.__readNextChar()
            if currentChar == '.':
                number = '0.'
                currentChar = self.__readNextChar()
            positive = False
        elif currentChar == '.':
            number = '0.'
            currentChar = self.__readNextChar()

        while currentChar != '':

            if self.__readCharUntil(4) == '--[[':
                self.__moveIndex(4)
                self.__commentHandle()
                currentChar = self.__readNextChar()
                continue
            elif self.__readCharUntil(2) == '--':
                self.__moveIndex(2)
                self.__commentSingleHandle()
                currentChar = self.__readNextChar()
                continue

            elif currentChar.isalnum() == False and currentChar != '-' and currentChar != '+' and currentChar != '.':
                break
            number += currentChar
            currentChar = self.__readNextChar()

        while currentChar == ' ' or currentChar == '\t' or currentChar == '\n':
            currentChar = self.__readNextChar()

        if currentChar == '':
            raise Exception("Error : 数字 " + number + " 后缺少 , ] } ；index：" + str(self.index))

        self.__moveIndex(-1)

        number = self.__str2num(number)

        if positive == False:
            number *= -1

        return number

    # 处理表
    def __tableHandle(self, deep):
        table = {}
        localLeft = 1
        currentChar = self.__readChar()
        while currentChar == ' ' or currentChar == '\n' or currentChar == '\t':
            currentChar = self.__readNextChar()
        if currentChar != '{':
            raise Exception("Error : Lua table格式错误，table 需要以 { 开头; index: " + str(self.index))
        i = 1
        key = None
        value = None
        isList = True
        currentChar = self.__readNextChar()
        while currentChar != '':

            # 处理空字符
            while currentChar == ' ' or currentChar == '\n' or currentChar == '\t':
                currentChar = self.__readNextChar()

            # 处理table的情况，table只能作为value值
            if currentChar == '{':
                localLeft += 1
                value = self.__tableHandle(deep + 1)
            elif currentChar == '}':
                localLeft -= 1
                if localLeft < 1:
                    break

            # 处理 ' 和 " 开头的字符串的情况，该情况下的字符串必为value
            elif currentChar == '"' or currentChar == "'":
                value = self.__stringHandle()

            # 处理 [[ 开头的字符串的情况
            elif self.__readCharUntil(2) == '[[':
                self.__moveIndex(1)
                value = self.__stringBracketHandle()

            # 处理 ' 和 " 开头的字符串的情况，该情况下的字符串必为key
            elif self.__readCharUntil(2) == '[\'' or self.__readCharUntil(2) == '["':
                self.__moveIndex(1)
                key = self.__stringHandle()
                self.__moveIndex(1)

            # 处理多行注释
            elif self.__readCharUntil(4) == '--[[':
                self.__moveIndex(4)
                self.__commentHandle()

            # 处理单行注释
            elif self.__readCharUntil(2) == '--':
                self.__moveIndex(2)
                self.__commentSingleHandle()


            # 处理 [] 包围的内容
            elif currentChar == '[':
                currentChar = self.__readNextChar()
                # 处理数字作为key的情况
                if currentChar == '.' or currentChar.isdigit() == True or currentChar == '-':
                    key = self.__numberHandle()
                    self.__moveIndex(1)
                # 必须以 ] 结尾，符号匹配
                if self.__readChar() != ']':
                    raise Exception("Error : Lua table格式错误，缺少 ]; index: " + str(self.index))

            # 完成一个key-value的读取
            elif currentChar == ',':
                # 值为空，兼容{64,,}的情况，空值不作处理，直接跳过
                # 当{['']=''}的情况，需要插入
                if value != None:
                    # 当key值不存在的时候，按顺序从1开始作为key值
                    if key == None:
                        if table.has_key(i) == False:
                            table.setdefault(i, value)
                            i += 1
                        value = None
                    else:
                        if table.has_key(key) == False:
                            table.setdefault(key, value)
                        key = None
                        value = None

            elif self.__readCharUntil(3) == 'nil':
                value = 'nil'
                self.__moveIndex(2)
            elif self.__readCharUntil(4) == 'true':
                value = True
                self.__moveIndex(3)
            elif self.__readCharUntil(5) == 'false':
                value = False
                self.__moveIndex(4)

            # 处理数字作为value的情况，无key值，例如：{56,5,}
            elif currentChar == '.' or currentChar.isdigit() == True or currentChar == '-':
                value = self.__numberHandle()

            # 处理字符串作为key值的情况，此时的字符串只能由字母、数字和下划线组成，
            # 字符串不能以数字开头，123abc为非法字符串，abc123合法
            # 正确示例：{number=56,_string="lua"}
            elif currentChar.isalpha() == True or currentChar == '_':
                key = currentChar
                currentChar = self.__readNextChar()
                while currentChar.isalnum() == True or currentChar == '_':
                    key += currentChar
                    currentChar = self.__readNextChar()

            elif currentChar == '=':
                isList = False

            currentChar = self.__readNextChar()

        if currentChar != '}' and currentChar != '':
            raise Exception("Error : Lua table格式错误，table 需要以 } 结束; index: " + str(self.index))

        if value != None:
            if key == None:
                if table.has_key(i) == False:
                    table.setdefault(i, value)
                    i += 1
            else:
                if table.has_key(key) == False:
                    table.setdefault(key, value)

        if isList == True and deep > 1:
            list = []
            for key,value in table.iteritems():
                if value == 'nil':
                    value = 'None'
                list.append(value)
            return list
        else:
            delKeys = []
            for key,value in table.iteritems():
                if value == 'nil':
                    delKeys.append(key)
            for key in delKeys:
                del  table[key]

        return table

    # 读入当前字符
    def __readChar(self):
        if self.index >= self.lenStr:
            return ''
        else:
            return self.luaStr[self.index]

    # 移动index
    def __moveIndex(self, offset):
        self.index += offset

    # 读入下一个字符
    def __readNextChar(self):
        self.index += 1
        if self.index >= self.lenStr:
            return ''
        else:
            return self.luaStr[self.index]

    # 读入指定位置的字符
    def __readCharAt(self, offset):
        if self.index + offset >= self.lenStr:
            return ''
        else:
            return self.luaStr[self.index + offset]

    # 读入指定位置的字符
    def __readCharUntil(self, offset):
        if self.index + offset > self.lenStr:
            return ''
        else:
            return self.luaStr[self.index : self.index + offset]

    # 将python列表转换为lua table字符串
    def __listToStr(self, myList):
        string = '{'
        for item in myList:
            if isinstance(item, (int, float)) == True:
                string += str(item) + ','
            elif isinstance(item, str) == True:
                string += '"' + item + '",'
            elif isinstance(item, bool) == True:
                if item == True:
                    string += 'true,'
                else:
                    string += 'false,'
            elif isinstance(item, list) == True:
                string += self.__listToStr(item) + ','
            elif isinstance(item, dict) == True:
                string += self.__dictToStr(item) + ','
        string += '}'
        return string

    # 将python字典转换为Lua table字符串
    def __dictToStr(self, myDict):
        string = '{'
        for key,value in myDict.iteritems():
            if isinstance(key, (int, float)) == True:
                string += '["' + str(key) + '"]='
            else:
                string += key + '='

            if isinstance(value, (int, float)) == True:
                string += str(value) + ','
            elif isinstance(value, str) == True:
                string += '"' + value + '",'
            elif isinstance(value, bool) == True:
                if value == True:
                    string += 'true,'
                else:
                    string += 'false,'
            elif isinstance(value, list) == True:
                string += self.__listToStr(value) + ','
            elif isinstance(value, dict) == True:
                string += self.__dictToStr(value) + ','
        string += '}'
        return string


    # 公有方法
    # 读取Lua table字符串
    def load(self, s):
        self.luaStr = s
        self.lenStr = len(self.luaStr)
        self.myDict = self.__tableHandle(1)

    # 从文件中读取Lua table字符串
    def loadLuaTable(self, f):
        input = open(f)
        try:
            s = input .read()
        except:
            raise Exception("Error PyLuaTblParser.loadLuaTable(): 文件 " + f + " 不存在")
        finally:
            input.close()
        self.load(s)

    # 读取dict中的数据
    def loadDict(self, d):
        for key,value in d.iteritems():
            if isinstance(key, (int, float, str)) == True:
                if self.myDict.has_key(key):
                    self.myDict[key] = value
                else:
                    self.myDict.setdefault(key,value)

    # 返回Lua table字符串
    def dump(self):
        if isinstance(self.myDict, (list)) == True:
            return self.__listToStr(self.myDict)
        else:
            return self.__dictToStr(self.myDict)

    # 返回Lua table字符串
    def dumpLuaTable(self, f):
        s = self.dump()
        output = open(f, 'w')
        try:
            output.write(s)
        except:
            raise Exception("Error PyLuaTblParser.loadLuaTable(): 文件 " + f + " 写入失败")
        finally:
            output.close()

    # 返回一个dict
    def dumpDict(self):
        newDict = self.myDict
        return newDict