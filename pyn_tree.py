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
	if not code: return "tryinput()"
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

import builtins, ast, functools

def getval(name):
	if name in global_register: return global_register[name]
	if name in globals(): return globals()[name]
	if name in dir(builtins): return getattr(builtins, name)
	return 0

def tryinput():
	val = input()
	try: return ast.literal_eval(val)
	except: return val

def deduplicate(array):
	output = []
	seen = {}
	for obj in array:
		if obj not in seen:
			output.append(obj)
			seen.add(obj)
	return output

def getintable(obj):
	if type(obj) == str:
		return obj
	else:
		try:
			return "".join("0123456789abcdefghijklmnopqrstuvwxyz"[y] for y in obj)
		except:
			return "0"

def concat(left, right):
	if hasattr(left, "__iter__"): left = list(left)
	else: left = [left]
	if hasattr(right, "__iter__"): right = list(right)
	else: right = [right]
	return left + right

def wloop(cond, iter):
	output = 0
	while cond():
		output = iter()
	return output

def numerify(obj):
	try:
		return int(obj)
	except:
		try:
			return float(obj)
		except:
			try:
				return complex(obj)
			except:
				return obj

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

@Getter("E")
def evalinput(code):
	return "eval(input())"

@Getter("D")
def declare(code):
	return "assign('%s', %s)" % (code.pop(0), getstr(code))

@Getter("€")
def listcompx(code):
	return "[[assign('x', x)] and %s for x in %s]" % (getstr(code), getstr(code))

@Getter("F")
def repeatloop(code):
	times = getstr(code)
	return "[%s for _ in range(%s)]" % (getstr(code), times)

@Getter("Ḟ")
def listcomp(code):
	return "[[assign('%s', x)] and %s for x in %s]" % (code.pop(0), getstr(code), getstr(code))

@Getter("G")
def getvarname(code):
	return "getval(%s)" % getstr(code)

@Getter("I")
def getint(code):
	return "int(input())"

@Getter("J")
def joiner(code):
	return "''.join(map(str, %s))" % getstr(code)

@Getter("L")
def getlength(code):
	return "len(%s)" % getstr(code)

@Getter("Ŀ")
def getlist(code):
	return "list(input())"

@Getter("Ḷ")
def lowerrange(code):
	return "list(range(int(%s)))" % getstr(code)

@Getter("Ṁ")
def maxgetter(code):
	return "max(%s)" % getstr(code)

@Getter("Ṃ")
def mingetter(code):
	return "min(%s)" % getstr(code)

@Getter("N")
def getnumber(code):
	return "numerify(input())"

@Getter("P")
def declare(code):
	return "fallthrough(%s)" % getstr(code)

@Getter("Q")
def deduplicate(code):
	return "deduplicate(%s)" % getstr(code)

@Getter("R")
def upperrange(code):
	return "list(range(1, 1 + int(%s)))" % getstr(code)

@Getter("S")
def getstring(code):
	return "input()"

@Getter("Ṡ")
def sorter(code):
	return "sorted(%s)" % getstr(code)

@Getter("c")
def splatFuncCall(code):
	return "(%s)(*%s)" % (getstr(code), getstr(code))

@Getter("ċ")
def multiFuncCall(code):
	func = getstr(code)
	arglist = []
	while code and code[0] != "}":
		arglist.append(getstr(code))
	if code: code.pop(0)
	return "(%s)(%s)" % (func, ", ".join(arglist))

@Getter("d")
def setlongvar(code):
	return "assign(%s, %s)" % (getstr(code), getstr(code))

@Getter("e")
def evaler(code):
	return "eval(%s)" % getstr(code)

@Getter("f")
def listcompxcond(code):
	return "[[assign('x', x)] and %s for x in %s if %s]" % (getstr(code), getstr(code), getstr(code))

@Getter("ḟ")
def listcompcond(code):
	return "[[assign('%s', x)] and %s for x in %s if %s]" % (code.pop(0), getstr(code), getstr(code), getstr(code))

@Getter("g")
def getlongvar(code):
	output = ""
	while code and code[0].isidentifier():
		output += code.pop(0)
	if code: code.pop(0)
	return "getval('%s')" % output

@Getter("i")
def toint(code):
	return "int(%s)" % getstr(code)

@Getter("ị")
def tointbase(code):
	return "int(getintable(%s), %s)" % (getstr(code), getstr(code))

@Getter("j")
def customjoiner(code):
	return "(%s).join(map(str, %s))" % (getstr(code), getstr(code))

@Getter("l")
def tolist(code):
	return "list(%s)" % getstr(code)

@Getter("ḷ")
def toset(code):
	return "set(%s)" % getstr(code)

@Getter("ṁ")
def maxkey(code):
	return "max(%s, key = lambda x: %s)" % (getstr(code), getstr(code))

@Getter("ṃ")
def minkey(code):
	return "min(%s, key = lambda x: %s)" % (getstr(code), getstr(code))

@Getter("n")
def tonumber(code):
	return "numerify(%s)" % getstr(code)

@Getter("s")
def tostring(code):
	return "str(%s)" % getstr(code)

@Getter("ṡ")
def keysorter(code):
	return "sorted(%s, key = lambda x: [assign('x', x)] and %s)" % (getstr(code), getstr(code))

@Getter("w")
def varW(code):
	return "getval('w')"

@Getter("x")
def varX(code):
	return "getval('x')"

@Getter("y")
def varY(code):
	return "getval('y')"

@Getter("z")
def varZ(code):
	return "getval('z')"

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

@Getter("\n")
@Getter(" ")
def empty(code):
	return getstr(code)

@Getter("ø")
def subgetraw(code):
	attrname = ""
	while code and code[0].isidentifier():
		attrname += code.pop(0)
	if code: code.pop(0)
	return "getattr(%s, %r)" % (getstr(code), attrname)

binfunc = {}

binfunc["Ø"] = "getattr({L}, {R})"
@Getter("Ø")
def subgetter(code):
	return "getattr(%s, %s)" % (getstr(code), getstr(code))

binfunc["+"] = "{L} + {R}"
@Getter("+")
def add(code):
	return "(%s + %s)" % (getstr(code), getstr(code))

binfunc["_"] = "{L} - {R}"
@Getter("_")
def sub(code):
	return "(%s - %s)" % (getstr(code), getstr(code))

binfunc["×"] = "{L} * {R}"
@Getter("×")
def mul(code):
	return "(%s * %s)" % (getstr(code), getstr(code))

binfunc[":"] = "{L} // {R}"
@Getter(":")
def floordiv(code):
	return "(%s // %s)" % (getstr(code), getstr(code))

binfunc["÷"] = "{L} / {R}"
@Getter("÷")
def div(code):
	return "(%s / %s)" % (getstr(code), getstr(code))

binfunc["*"] = "{L} ** {R}"
@Getter("*")
def exp(code):
	return "(%s ** %s)" % (getstr(code), getstr(code))

binfunc["&"] = "{L} & {R}"
@Getter("&")
def _and(code):
	return "(%s & %s)" % (getstr(code), getstr(code))

binfunc["|"] = "{L} | {R}"
@Getter("|")
def _or(code):
	return "(%s | %s)" % (getstr(code), getstr(code))

binfunc["^"] = "{L} ^ {R}"
@Getter("^")
def _xor(code):
	return "(%s ^ %s)" % (getstr(code), getstr(code))

binfunc[">"] = "{L} > {R}"
@Getter(">")
def gt(code):
	return "(%s > %s)" % (getstr(code), getstr(code))

binfunc["<"] = "{L} < {R}"
@Getter("<")
def lt(code):
	return "(%s < %s)" % (getstr(code), getstr(code))

@Getter("¬")
def logical_not(code):
	return "(not %s)" % getstr(code)

binfunc[";"] = "concat({L}, {R})"
@Getter(";")
def concat(code):
	return "concat(%s, %s)" % (getstr(code), getstr(code))

binfunc["="] = "{L} == {R}"
@Getter("=")
def equality(code):
	return "(%s == %s)" % (getstr(code), getstr(code))

binfunc["⁻"] = "{L} != {R}"
@Getter("⁻")
def inequality(code):
	return "(%s != %s)" % (getstr(code), getstr(code))

binfunc["ė"] = "{L} in {R}"
@Getter("ė")
def containcheck(code):
	return "(%s in %s)" % (getstr(code), getstr(code))

binfunc["ẹ"] = "{L} not in {R}"
@Getter("ẹ")
def uncontaincheck(code):
	return "(%s not in %s)" % (getstr(code), getstr(code))

@Getter("?")
def condif(code):
	condition = getstr(code)
	return "(%s if %s else None)" % (getstr(code), condition)

@Getter("¿")
def condifelse(code):
	condition = getstr(code)
	return "(%s if %s else %s)" % (getstr(code), condition, getstr(code))

@Getter("¤")
def block(code):
	output = []
	while code and code[0] != "}":
		output.append(getstr(code))
	if code: code.pop(0)
	return "(" + " and ".join("[%s]" % k for k in output[:-1]) + " and %s)" % output[-1]

@Getter("⁺")
def selfie(code):
	return ("(lambda a: %s)(%s)" % (binfunc[code.pop(0)], getstr(code))).format(L = "a", R = "a")

@Getter("¡")
def whileloop(code):
	return "wloop(lambda: (%s), lambda: (%s))" % (getstr(code), getstr(code))

@Getter("#")
def arrayaccess(code):
	return "(%s)[%s]" % (getstr(code), getstr(code))

@Getter("/")
def reducer(code):
	return ("functools.reduce(lambda a, b: %s, %s)" % (binfunc[code.pop(0)], getstr(code))).format(L = "a", R = "b")

@Getter("\\")
def insertraw(code):
	return code.pop(0)

@Getter("`")
def slicer(code):
	if code[0] == "`":
		code.pop(0)
		return "%s:%s:%s" % (getstr(code), getstr(code), getstr(code))
	else:
		return "%s:%s" % (getstr(code), getstr(code))

@Getter("§")
def funcdef(code):
	args = []
	splat = code[0] == "*"
	if splat: code.pop(0)
	while code and code[0] != ":":
		args.append(code.pop(0))
	if code: code.pop(0)
	return "lambda " + "*" * splat + ", ".join(args) + ": " + "[0, " + ", ".join("assign('%s', %s)" % (name, name) for name in args) + "] and " + getstr(code)

@Getter("[")
def formlist(code):
	output = []
	while code and code[0] != "]":
		output.append(getstr(code))
	if code: code.pop(0)
	return "[" + ", ".join(output) + "]"

@Getter("{")
def formlist(code):
	output = []
	while code and code[0] != "}":
		output.append(getstr(code))
	if code: code.pop(0)
	return "set([" + ", ".join(output) + "])"

@Getter("æ")
def specials(code):
	format = special_format.get(code.pop(0), "%s")
	return format % tuple(getstr(code) for _ in range(format.count("%s")))

special_format = {
	"f": "(%s).find",
	"c": "(%s).count",
	"i": "(%s).index",
	"r": "(%s).replace",
	"=": "%s = %s",
}

def consumeNum(code, digits = "0123456789", neg = True, decimal = True):
	output = ""
	while code and (code[0] in digits or code[0] == "-" and neg or code[0] == "." and decimal):
		if code[0] == "-": neg = False
		if code[0] == ".": decimal = False
		output += code.pop(0)
	return output

try:
	with open(sys.argv[1], "r") as f:
		trans = transpile(f.read())
except:
	trans = transpile(sys.argv[1])

if "--transpile" in sys.argv:
	print(trans)
else:
	with open("__transpiled.py", "w") as f:
		f.write(trans)
	import os
	os.system("python3 __transpiled.py")
