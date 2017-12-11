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
            if currentChar == flag:
                offset = 1
                nextChar = self.__readCharAt(offset)
                while nextChar == ' ' or nextChar == '\n' or nextChar == '\t':
                    offset += 1
                    nextChar = self.__readCharAt(offset)
                if nextChar == ',' or nextChar == '}' or nextChar == ']':
                    currentChar = nextChar
                    self.__moveIndex(offset)
                    break
                elif nextChar == '.' and self.__readCharAt(offset+1) == '.':
                    offset += 2
                    nextChar = self.__readCharAt(offset)
                    while nextChar == ' ' or nextChar == '\n' or nextChar == '\t':
                        offset += 1
                        nextChar = self.__readCharAt(offset)
                    if nextChar == '"' or nextChar == "'":
                        currentChar = nextChar
                        self.__moveIndex(offset)
                        string += self.__stringHandle()
                        break
                    elif nextChar == '[' and self.__readCharAt(offset+1) == '[':
                        currentChar = self.__readCharAt(offset+1)
                        self.__moveIndex(offset+1)
                        string += self.__stringBracketHandle()
                        break
                    else:
                        raise Exception("Error : 字符串格式错误； ‘..' 之后应当接字符串； index： " + str(self.index + offset) + "； char: " + nextChar)

            elif currentChar == '\\':
                number = ''
                offset = 1
                nextChar = self.__readCharAt(offset)
                while nextChar.isdigit() == True and nextChar != ' ':
                    number += nextChar
                    offset += 1
                    nextChar = self.__readCharAt(offset)
                if number != '':
                    if int(number) > 255:
                        raise Exception("Error : 字符串格式错误；字符串 \\'" + number + "'  大于预留值； index： " + str(self.index))
                    else:
                        currentChar = chr(int(number))
                        self.__moveIndex(offset-1)

            string += currentChar
            currentChar = self.__readNextChar()

        if currentChar == '':
            raise Exception("Error : 字符串格式错误；字符串 '" + string + "' 缺少结束符； index： " + str(self.index))

        return string

    # 处理 [[ 开头的字符串
    def __stringBracketHandle(self):
        string = ''
        currentChar = self.__readNextChar()
        while currentChar != '':
            if currentChar == ']' and self.__readCharAt(1) == ']':
                offset = 2
                nextChar = self.__readCharAt(offset)
                while nextChar == ' ' or nextChar == '\n' or nextChar == '\t':
                    offset += 1
                    nextChar = self.__readCharAt(offset)
                if nextChar == ',' or nextChar == '}':
                    currentChar = nextChar
                    self.__moveIndex(offset)
                    break
                elif nextChar == '.' and self.__readCharAt(offset+1) == '.':
                    offset += 2
                    nextChar = self.__readCharAt(offset)
                    while nextChar == ' ' or nextChar == '\n' or nextChar == '\t':
                        offset += 1
                        nextChar = self.__readCharAt(offset)
                    if nextChar == '"' or nextChar == "'":
                        currentChar = nextChar
                        self.__moveIndex(offset)
                        string += self.__stringHandle()
                        break
                    elif nextChar == '[' and self.__readCharAt(offset+1) == '[':
                        currentChar = self.__readCharAt(offset+1)
                        self.__moveIndex(offset+1)
                        string += self.__stringBracketHandle()
                        break
                    else:
                        raise Exception("Error : 字符串格式错误； ‘..' 之后应当接字符串； index： " + str(self.index + offset) + "； char: " + nextChar)

            elif currentChar == '\\':
                number = ''
                offset = 1
                nextChar = self.__readCharAt(offset)
                while nextChar.isdigit() == True and nextChar != ' ':
                    number += nextChar
                    offset += 1
                    nextChar = self.__readCharAt(offset)
                if number != '':
                    if int(number) > 255:
                        raise Exception("Error : 字符串格式错误；字符串 \\'" + number + "'  大于预留值； index： " + str(self.index))
                    else:
                        currentChar = chr(int(number))
                        self.__moveIndex(offset-1)

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


        return string

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

            if self.__readCharUntil(2) == '--':
                self.__moveIndex(2)
                self.__commentSingleHandle()
                currentChar = self.__readNextChar()
                continue
            elif self.__readCharUntil(4) == '--[[':
                self.__moveIndex(4)
                self.__commentHandle()
                currentChar = self.__readNextChar()
                continue

            elif currentChar.isalnum() == False and currentChar != '-' and currentChar != '+' and currentChar != '.':
                break
            number += currentChar
            currentChar = self.__readNextChar()

        while currentChar == ' ' and currentChar == '\t' and currentChar == '\n':
            currentChar = self.__readNextChar()

        if currentChar != ',' and currentChar != ']' and currentChar != '}':
            raise Exception("Error : 数字 " + number + " 后缺少 , ] } ；index：" + str(self.index))

        self.__moveIndex(-1)

        number = self.__str2num(number)

        if positive == False:
            number *= -1

        return number

    # 处理表,left表示递归深度
    def __tableHandle(self, left):
        table = {}
        localLeft = left
        currentChar = self.__readChar()
        while currentChar == ' ' or currentChar == '\n' or currentChar == '\t':
            currentChar = self.__readNextChar()
        if currentChar != '{':
            raise Exception("Error : Lua table格式错误，table 需要以 { 开头; index: " + str(self.index))
        i = 1
        key = ''
        value = ''
        isList = True
        currentChar = self.__readNextChar()
        while currentChar != '':

            # 处理空字符
            while currentChar == ' ' or currentChar == '\n' or currentChar == '\t':
                currentChar = self.__readNextChar()

            # 处理table的情况，table只能作为value值
            if currentChar == '{':
                localLeft += 1
                value = self.__tableHandle(localLeft)
            elif currentChar == '}':
                localLeft -= 1
                if localLeft < left:
                    break

            # 处理 ' 和 " 开头的字符串的情况，该情况下的字符串必为value
            elif currentChar == '"' or currentChar == "'":
                value = self.__stringHandle()

            # 处理单行注释
            elif self.__readCharUntil(2) == '--':
                self.__moveIndex(2)
                self.__commentSingleHandle()

            # 处理多行注释
            elif self.__readCharUntil(4) == '--[[':
                self.__moveIndex(4)
                self.__commentHandle()

            # 处理 [] 包围的内容
            elif currentChar == '[':
                currentChar = self.__readNextChar()
                # 处理 [[ 开头的字符串的情况
                if currentChar == '[':
                    value = self.__stringBracketHandle()
                # 处理数字
                elif currentChar == '.' or currentChar.isdigit() == True or currentChar == '-':
                    key = self.__numberHandle()
                # 处理 ' 和 " 开头的字符串的情况，该情况下的字符串必为key
                elif currentChar == '"' or currentChar == "'":
                    key = self.__stringHandle()
                # 必须以 ] 结尾，符号匹配
                if self.__readChar() != ']':
                    raise Exception("Error : Lua table格式错误，缺少 ]; index: " + str(self.index))

            # 完成一个key-value的读取
            elif currentChar == ',':
                # 值为空，兼容{64,}的情况，空值不作处理，直接跳过
                if value == '':
                    currentChar = self.__readNextChar()
                    continue
                # 当key值不存在的时候，按顺序从1开始作为key值
                elif key == '':
                    if table.has_key(i) == False:
                        table.setdefault(i, value)
                        i += 1
                    value = ''
                else:
                    if table.has_key(key) == False:
                        table.setdefault(key, value)
                    key = ''
                    value = ''

            elif self.__readCharUntil(3) == 'nil':
                value = 'nil'
                self.__moveIndex(2)
            elif self.__readCharUntil(4) == 'true':
                value = 'true'
                self.__moveIndex(3)
            elif self.__readCharUntil(5) == 'false':
                value = 'false'
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
                if key == '':
                    raise Exception("Error : Lua table格式错误，在[key]=value对中，key不能为空; index: " + str(self.index))
                isList = False

            currentChar = self.__readNextChar()

        if currentChar != '}' and currentChar != '':
            raise Exception("Error : Lua table格式错误，table 需要以 } 结束; index: " + str(self.index))

        if value != '':
            if key == '':
                table.setdefault(i, value)
            else:
                table.setdefault(key, value)

        if isList == True:
            list = []
            for key,value in table.iteritems():
                list.append(value)
            return list

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

    # 将python字典转换为Lua table字符串
    def __py2lua(self):
        print self.myDict


    # 公有方法
    # 读取Lua table字符串
    def load(self, s):
        self.luaStr = s
        self.lenStr = len(self.luaStr)
        self.myDict = self.__tableHandle(1)
        print "Info PyLuaTblParser.load(): 完成Lua table字符串的读取"

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
        self.myDict.clear()
        for key,value in d.iteritems():
            if (type(key) == int or type(key) == str):
                dict.setdefault(key, value)
        print "Info PyLuaTblParser.loadDict(): 完成dict的读取"

    # 返回Lua table字符串
    def dump(self):
        return self.__py2lua()

    # 返回Lua table字符串
    def dumpLuaTable(self, f):
        s = self.__py2lua()
        output = open(f, 'w')
        output.write(s)
        output.close()

    # 返回一个dict
    def dumpDict(self):
        newDict = self.myDict
        return newDict