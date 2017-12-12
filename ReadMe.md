# Python: lua table parser

---

## 接口说明

1. **load(self, s)**：读取Lua table数据，输入s为一个符合Lua table定义的字符串，无返回值；若遇到Lua table格式错误的应该抛出异常；
2. **dump(self)**：根据类中数据返回Lua table字符串
3. **loadLuaTable(self, f)**：从文件中读取Lua table字符串，f为文件路径，异常处理同1，文件操作失败抛出异常；
4. **dumpLuaTable(self, f)**：将类中的内容以Lua table格式存入文件，f为文件路径，文件若存在则覆盖，文件操作失败抛出异常；
5. **loadDict(self, d)**：读取dict中的数据，存入类中，只处理数字和字符串两种类型的key，其他类型的key直接忽略；
6. **dumpDict(self)**：返回一个dict，包含类中的数据

## 功能简介

### string：
1. 支持三种字符串格式: 'xxx', "xxx", [[xxx]]
2. 支持反斜杠转义
3. 不支持[==[xxx]==]字符串表示形式

### number：
1. 支持所有符合lua规范的数字形式
2. 不支持表达式

### comment：
1. 支持单行注释 --xxx
2. 支持多行注释和行间注释 --[[xxx--]]
3. 不支持嵌套注释