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

    test_str = '''{\r\nroot = {\r\n\t"Test Pattern String",\r\n\t-- {"object with 1 member" = {"array with 1 element",},},\r\n\t{["object with 1 member"] = {"array with 1 element",},},\r\n\t{},\r\n\t[99] = -42,\r\n\t[98] = {{}},\r\n\t[97] = {{},{}},\r\n\t[96] = {{}, 1, 2, nil},\r\n\t[95] = {1, 2, {["1"] = 1}},\r\n\t[94] = { {["1"]=1, ["2"]=2}, {1, ["2"]=2}, ["3"] = 3 },\r\n\ttrue,\r\n\tfalse,\r\n\tnil,\r\n\t{\r\n\t\t["integer"]= 1234567890,\r\n\t\treal=-9876.543210,\r\n\t\te= 0.123456789e-12,\r\n\t\tE= 1.234567890E+34,\r\n\t\tzero = 0,\r\n\t\tone = 1,\r\n\t\tspace = " ",\r\n\t\tquote = "\\"",\r\n\t\tbackslash = "\\\\",\r\n\t\tcontrols = "\\b\\f\\n\\r\\t",\r\n\t\tslash = "/ & \\\\",\r\n\t\talpha= "abcdefghijklmnopqrstuvwyz",\r\n\t\tALPHA = "ABCDEFGHIJKLMNOPQRSTUVWYZ",\r\n\t\tdigit = "0123456789",\r\n\t\tspecial = "`1~!@#$%^&*()_+-={\':[,]}|;.</>?",\r\n\t\thex = "0x01230x45670x89AB0xCDEF0xabcd0xef4A",\r\n\t\t["true"] = true,\r\n\t\t["false"] = false,\r\n\t\t["nil"] = nil,\r\n\t\tarray = {nil, nil,},\r\n\t\tobject = {  },\r\n\t\taddress = "50 St. James Street",\r\n\t\turl = "http://www.JSON.org/",\r\n\t\tcomment = "// /* <!-- --",\r\n\t\t["# -- --> */"] = " ",\r\n\t\t[" s p a c e d " ] = {1,2 , 3\r\n\r\n\t\t\t,\r\n\r\n\t\t\t4 , 5        ,          6           ,7        },\r\n\t\t--[[[][][]  Test multi-line comments\r\n\t\t\tcompact = {1,2,3,4,5,6,7},\r\n\t- -[luatext = "{\\"object with 1 member\\" = {\\"array with 1 element\\"}}",\r\n\t\tquotes = "&#34; (0x0022) %22 0x22 034 &#x22;",\r\n\t\t["\\\\\\"\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"]\r\n\t\t= "A key can be any string"]]\r\n\t--         ]]\r\n\t\tcompact = {1,2,3,4,5,6,7},\r\n\t\tluatext = "{\\"object with 1 member\\" = {\\"array with 1 element\\"}}",\r\n\t\tquotes = "&#34; (0x0022) %22 0x22 034 &#x22;",\r\n\t\t["\\\\\\"\\b\\f\\n\\r\\t`1~!@#$%^&*()_+-=[]{}|;:\',./<>?"]\r\n\t\t= "A key can be any string"\r\n\t},\r\n\t0.5 ,31415926535897932384626433832795028841971693993751058209749445923.\r\n\t,\r\n\t3.1415926535897932384626433832795028841971693993751058209749445923\r\n\t,\r\n\r\n\t1066\r\n\r\n\r\n\t,"rosebud"\r\n\r\n}}
    '''

    a1 = PyLuaTblParser()
    a2 = PyLuaTblParser()
    a3 = PyLuaTblParser()


    a1.load(test_str)
    print a1.dump()
    d1 = a1.dumpDict()

    a2.loadDict(d1)
    a2.dumpLuaTable('output.txt')
    a3.loadLuaTable('output.txt')

    d3 = a3.dumpDict()

    print d1 == d3
    print '\n'
    print d1
    print '\n'
    print d3