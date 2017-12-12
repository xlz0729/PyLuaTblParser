# coding=utf-8

from PyLuaTblParser import *


if __name__ == '__main__':
    test_str = '''{
        ['\\\\"\\x08\\x00c\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\\',./<>?']='foolish',
        ['\\097\\065bd']= {65,23,5},   --aAbd=[65,23,5]
        dict = {
            number = {43,43.21,43.21e-1,43.21e+1,0043.21,00043,.4321,-.4321,0x1.921FB54442D18P+1},
            subDict = {
                ['nil'] = {nil,false,true,'false'},
                string = {
                    one = [[value]],
                    two = " -- one line comment ",
                    three = 'Hello ' .. [[world]] .. " !!!",
                    ['fo' .. 'ur'] = 'say hi !!!',
                    ["this is a \\"comment\\" "] = " --[[comment--]]",
                    ["this is a 'one line comment'"] = "-- comment"
                },
                ['N'] = nil,
                other = {
                    1,
                    2,
                    3,
                    [45] = 11    --[[fdsaf--]],
                    [''] = '',
                    ''
                }
            }
        }
    ,,,}'''

    test_str = "{{1='Test Pattern String',99=-42,2={{'array with 1 element'}}}"
    a = PyLuaTblParser()
    a.load(test_str)
    print a.myDict
    dumpStr = a.dump()

    a1 = PyLuaTblParser()
    a1.loadLuaTable('input.txt')
    dumpTableStr = a1.dump()
    a1.dumpLuaTable('output.txt')

    testDict = {1:11, 2:12, False:'drop', 'newItem':4}
    a.loadDict(testDict)
    dumpDict = a.dumpDict()

    print dumpStr == dumpTableStr
    print "\n"
    print a.dumpDict()
    print "\n"
    print a1.dumpDict()
    print "\n"
    print dumpDict
