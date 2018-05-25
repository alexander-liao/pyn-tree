import sys

codepage  = """¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?"""
codepage += """@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶"""
codepage += """°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂ"""
codepage += """ĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭ§Äẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”"""

getters = {}

def Getter(name):
	def wrapper(function):
		getters[name] = function
		return function
	return wrapper

def getstr(code):
	c = code.pop(0)
	if c not in getters:
		return ""
	return getters[c](code)

def transpile(code):
	output = """# Python code transpiled from %d bytes of PynTree code

global_register = {}

def assign(name, val):
	global_register[name] = val
	return val

def getval(name):
	return global_register.get(name, 0)

def fallthrough(obj):
	return print(obj) or obj

""" % len(code)
	code = list(code)
	while code:
		output += getstr(code) + "\n"
	return output

@Getter("C")
def oneArgFuncCall(code):
	return "(%s)(%s)" % (getstr(code), getstr(code))

@Getter("c")
def splatFuncCall(code):
	return "(%s)(*%s)" % (getstr(code), getstr(code))

@Getter("D")
def declare(code):
	return "assign('%s', %s)" % (code.pop(0), getstr(code))

@Getter("P")
def declare(code):
	return "fallthrough(%s)" % getstr(code)

@Getter("x")
def varX(code):
	return "getval('x')"

@Getter("1")
def num1(code):
	return "1" + consumeNum(code)

@Getter("2")
def num2(code):
	return "2" + consumeNum(code)

@Getter("3")
def num2(code):
	return "3" + consumeNum(code)

@Getter("4")
def num2(code):
	return "4" + consumeNum(code)

@Getter("5")
def num2(code):
	return "5" + consumeNum(code)

@Getter("6")
def num2(code):
	return "6" + consumeNum(code)

@Getter("7")
def num2(code):
	return "7" + consumeNum(code)

@Getter("8")
def num2(code):
	return "8" + consumeNum(code)

@Getter("9")
def num2(code):
	return "9" + consumeNum(code)

@Getter("0")
def num2(code):
	return "0" + consumeNum(code)

@Getter("-")
def negnum(code):
	return "-" + consumeNum(code, neg = False)

@Getter(".")
def decnum(code):
	return "." + consumeNum(code, decimal = False)

@Getter("'")
def schar(code):
	return "'%s'" % code.pop(0) if code[0] != "\\" else "'%s'" % (code.pop(0) + code.pop(0))

@Getter('"')
def gstr(code):
	output = '"'
	while code:
		c = code.pop(0)
		if c == '"':
			break
		elif c == "\\":
			output += "\\" + code.pop(0)
		else:
			output += c
	return output + '"'

@Getter(" ")
def empty(code):
	return getstr(code)

@Getter("+")
def add(code):
	return "(%s + %s)" % (getstr(code), getstr(code))

@Getter("_")
def sub(code):
	return "(%s - %s)" % (getstr(code), getstr(code))

@Getter("×")
def mul(code):
	return "(%s * %s)" % (getstr(code), getstr(code))

@Getter(":")
def floordiv(code):
	return "(%s // %s)" % (getstr(code), getstr(code))

@Getter("÷")
def div(code):
	return "(%s / %s)" % (getstr(code), getstr(code))

@Getter("*")
def exp(code):
	return "(%s ** %s)" % (getstr(code), getstr(code))

def consumeNum(code, digits = "0123456789", neg = True, decimal = True):
	output = ""
	while code and (code[0] in digits or code[0] == "-" and neg or code[0] == "." and decimal):
		if code[0] == "-": neg = False
		if code[0] == ".": decimal = False
		output += code.pop(0)
	return output

import os

with open("__compiled.py", "w") as f:
	with open(os.sys.argv[1], "r") as g:
    f.write(transpile(g.read()))

os.system("python3 __compiled.py")
