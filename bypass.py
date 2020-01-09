import sys, os, shlex, string, math

os.system("color")

var = {}
gotos = []
commentsymbol = ";"
abc = string.printable[:62]+"_"+"."

try: filename = sys.argv[1]
except: filename = "code.txt"

def error(txt):
    global c
    print("[ERROR] "+txt)
    print("[LINE] "+str(c))
    sys.exit()

########################################################################################

LOG_COUNT = 0
def log(text):
    global LOG_COUNT
    LOG_COUNT += 1
    file = open("log.log","a+")
    file.write(str(LOG_COUNT)+" | "+str(text)+"\n")
    file.close()

def checkvn(vn):
    try:
        int(vn[0])
        error("Illegal variable name")
    except: pass
    if vn[0] == "." or vn[-1] == ".": error("Illegal variable name")
    return vn

def cut(y):
    read = False
    end = []
    e = ""
    y += " NONE"
    for x in y:
        e += x
        if read == True and x == '"':
            read = False
            end.append("S#"+e.strip())
            e = ""
        elif read == False and x == '"':
            read = True
        if read == False and x == ' ':
            issymbol = False
            if e.strip() == "": continue
            for E in e.strip():
                if not E in abc: issymbol = True; break
            if issymbol == True:
                if e.strip() != ",": end.append("X#"+e.strip())
            else:
                try:
                    int(e.strip())
                    end.append("I#"+e.strip())
                except:
                    end.append("V#"+e.strip())
            e = ""
    END = []
    for e in end:
        if e != "": END.append(e)
    return END

########################################################################################

def getval(V):
    if V[0] == "S":
        return V[3:-1]
    elif V[0] == "V":
        return var[V[2:]]
    elif V[0] == "I":
        return int(V[2:])



functions = [
"get",
"log",
"lognb", # log, no break
"cls",
"times",
"cut",
"split",
"math.add",
"math.sub",
"math.mul",
"math.div",
"math.sqrt",
"math.square",
"math.killfloat",
"replace",
"combine",
"scombine",
"exit",
#"conv.int",
#"conv.str",
#"",
#"",
#"",
#"",
#"",
]
def runfunc(cutted):
    if cutted[0][2] == "/":
        func = cutted[0][3:]
        args = []
        if "V#with" in cutted:
            for ca in cutted[2:]: args.append(getval(ca))
    else:
        func = cutted[2][2:]
        args = []
        if "V#with" in cutted:
            for ca in cutted[4:]: args.append(getval(ca))

    log("FUNCTION: "+str(func))
    log("\tARGS: "+str(args))
    ret = "none"

    if func == "log":
        for a in args: print(str(a),end="") # "".join DOESNT WORK!
        print()
    if func == "lognb":
        for a in args: print(str(a),end="") # "".join DOESNT WORK!

    if func == "get":
        ret = input()
    if func == "cls":
        os.system("cls")
    if func == "times":
        ret = args[0] * int(args[1])
    if func == "cut":
        ret = args[0][int(args[1]):int(args[1])]

    if func == "split":
        ret = args[0].split()[int(args[1])]
        
    if func == "math.add":
        end = 0
        for a in args: end += float(a)
        ret = end
    if func == "math.sub":
        end = 0
        for a in args: end -= float(a)
        ret = end
    if func == "math.mul":
        end = 0
        for a in args: end *= float(a)
        ret = end
    if func == "math.div":
        end = 0
        for a in args: end /= float(a)
        ret = end
    if func == "math.sqrt":
        ret = math.sqrt(float(args[0]))
    if func == "math.square":
        try: ret = float(args[0]) ** float(args[1])
        except IndexError: ret = float(args[0]) ** 2
    if func == "math.killfloat":
        F = str(args[0])
        if "." in F: ret = int(F.split(".")[0])
        else: ret = float(F)
    """
    if func == "conv.int":
        ret = "I#"+args[0]
    if func == "conv.str":
        ret = "S#"+args[0]
    """

    if func == "combine":
        end = ""
        for a in args: end += str(a)
        ret = end

    if func == "scombine":
        end = ""
        for a in args: end += str(a+" ")
        ret = end[:-1]

    if func == "replace":
        ret = args[0].replace(args[1],args[2])

    if func == "exit":
        sys.exit()


    log("\tRETURNING: "+str(ret))
    #print(func,"===",ret)
    return ret


def parser(line):
    cutted = cut(line)
    #print(cutted)
    if cutted[0] == "X#bypass:" and cutted[2] == "X#=":
        a = getval(cutted[1])
        b = getval(cutted[3])
        if a == b:
            return "bypass"
        return

    if cutted[0] == "X#goto:":
        log("GOTO? -> "+str(gotos))
        gotopoint = ""
        try:
            g = int(cutted[1][2:])
            gotopoint = "goto "+str(g)
        except:
            g = cutted[1][2:]
            #print(g,gotos)
            if g in gotos: gotopoint = "goto "+str(g)
            else: error("GotoError")

        if "X#=" in cutted and cutted[3] == "X#=":
            log("\t>>>"+getval(cutted[2]))
            log("\t>>>"+getval(cutted[4]))
            
            if not getval(cutted[2]) == getval(cutted[4]):
                return
            else: log("\t(GOTO/IF) -> ["+getval(cutted[2])+"/"+getval(cutted[4])+"], now goto.")
        else:
            log("->GOTO without IF.")
        log("GOTO: "+str(gotopoint))
        return gotopoint

################################################
    try:
        if cutted[1] == "V#is" and cutted[0][:2] == "V#":
            vn = checkvn(cutted[0][2:])
            var[vn] = getval(cutted[2])
            return
    except IndexError: pass
################################################
    try:
        if cutted[1] == "V#add" and cutted[0][:2] == "V#":
            vn = checkvn(cutted[0][2:])
            var[vn] += getval(cutted[2])
            return
    except IndexError: pass
################################################
    try:
        if cutted[1] == "V#as" and cutted[0][:2] == "V#" and cutted[2][:2] == "V#" or cutted[2][:2] == "X#":
            if cutted[2][2:] in functions:
                ret = runfunc(cutted)
                var[cutted[0][2:]] = ret
            else:
                error("Undefined Function '"+cutted[2][2:]+"'")
            return
    except IndexError: pass
################################################
    try:
        if cutted[0][:3] == "X#/" and cutted[0][3:] in functions:
            runfunc(cutted)
            return

    except IndexError:
        pass

    

ffile = open(filename)
file = ffile.read().split("\n")
ffile.close()

for f in file:
    if not f == "" and not f[0] == ";":
        cutted = cut(f)
        if cutted[0][:3] == "X#\\" and cutted[0][-1] == "\\":
            if not cutted[0][3:-1] in gotos: gotos.append(cutted[0][3:-1])
        


file.insert(0,"")

L = len(file)
c = 0
run = 0
while c != L:
    log("{%s}" % str(c))
    run += 1
    var["bypass.counter"] = run
    line = file[c]
    if line != "" and line[0] != commentsymbol:
        out = parser(line)
        try:
            if out == "bypass":
                c += file[c:].index("<*>")
            elif out[:5] == "goto ":
                try:
                    int(out[5:])
                    c = int(out[5:])-1
                except:
                    if out[5:] in gotos: c = file.index("\\"+out[5:]+"\\")
                    else: error("Undefined goto statement")
        except TypeError:
            pass # out = None

        c += 1

    else:
        c += 1
        continue

#print(var)
#print(gotos)

"""
Error - Troubleshooting
- Is function in [functions]?
- Does variable exist?
"""
