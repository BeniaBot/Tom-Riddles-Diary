# -*- coding: utf-8 -*-
"""
OfficeChat generator - Hebrew-trigger + prank-safe edition.
Fixes:
 (1) game trigger is HEBREW ("תתת") so it matches in the same AutoCorrect
     language list as the (working) Hebrew chat triggers.
 (2) chat + board texts NEVER reveal the mechanism (it's a prank on viewers).
 (3) no replacement value contains its own trigger (Word loop-prevention).
Code is pure ASCII (Hebrew via ChrW); import the .bas (do not paste).
"""
import io

# ===== game engine =====
WIN=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
def winner(b):
    for a,c,d in WIN:
        if b[a]!=' ' and b[a]==b[c]==b[d]: return b[a]
    return None
def full(b): return ' ' not in b
def minimax(b,pl):
    w=winner(b)
    if w=='O': return (1,None)
    if w=='X': return (-1,None)
    if full(b): return (0,None)
    mv=[i for i in range(9) if b[i]==' ']
    if pl=='O':
        best=(-2,None)
        for m in mv:
            nb=b[:]; nb[m]='O'; s,_=minimax(nb,'X')
            if s>best[0]: best=(s,m)
        return best
    best=(2,None)
    for m in mv:
        nb=b[:]; nb[m]='X'; s,_=minimax(nb,'O')
        if s<best[0]: best=(s,m)
    return best
def o_move(b):
    best=None
    for m in [i for i in range(9) if b[i]==' ']:
        nb=b[:]; nb[m]='O'; s,_=minimax(nb,'X')
        if best is None or s>best[0]: best=(s,m)
    return best[1]
entries={}
def rec(board,seq):
    for c in [i for i in range(9) if board[i]==' ']:
        nb=board[:]; nb[c]='X'; ns=seq+[c+1]; k=''.join(map(str,ns))
        if winner(nb)=='X': entries[k]=(''.join(nb),'win'); continue
        if full(nb): entries[k]=(''.join(nb),'draw'); continue
        om=o_move(nb); nb2=nb[:]; nb2[om]='O'
        if winner(nb2)=='O': entries[k]=(''.join(nb2),'lose'); continue
        if full(nb2): entries[k]=(''.join(nb2),'draw'); continue
        entries[k]=(''.join(nb2),'play'); rec(nb2,ns)
start=[' ']*9; entries['']=(''.join(start),'play'); rec(start,[])

# ===== texts (PRANK-SAFE: nothing reveals autocorrect / Word) =====
CHAT=[
 ("היי צאט","שלום! נעים מאוד. איך אפשר לעזור לך היום?  :)"),
 ("שלום צאט","שלום שלום! מה שלומך היום?  :)"),
 ("מה שלומך צאט","מצוין, תודה ששאלת! ואיך אתה מרגיש?  :)"),
 ("צאט מי אתה","אני העוזר החכם שלך -- שאל אותי כל דבר, אני כאן בשבילך.  :)"),
 ("צאט תודה","בכיף גדול! תמיד לשירותך.  :)"),
 ("צאט ספר בדיחה","מה אמר קיר אחד לקיר השני? ניפגש בפינה!  :D"),
 ("צאט עוד בדיחה","למה השלד לא הלך למסיבה? לא היה לו עם מי לרקוד!  :D"),
 ("צאט בדיחה נוספת","איזה חודש הכי קצר? מאי -- שלוש אותיות בלבד!  :D"),
 ("צאט אני עייף","קח הפסקה, כוס קפה, ונשימה עמוקה. אני אחכה לך כאן.  :)"),
 ("צאט אני שונא ימי שני","ימי שני מאתגרים לכולם. בוא נהפוך את היום לנפלא!  :)"),
 ("צאט אני דחיין","כל מסע גדול מתחיל בצעד קטן. מה הצעד הקטן שלך עכשיו?  :)"),
 ("צאט משעמם לי",'בוא נשחק! פשוט כתוב "בוא נשחק" ונתחיל.  :)'),
 ("צאט מה משמעות החיים","שאלה עמוקה! יש אומרים 42, אני אומר -- ליהנות מהרגע.  :)"),
 ("צאט מה מזג האוויר","אני מקווה שהשמש זורחת אצלך! יום יפה מתחיל בחיוך.  :)"),
 ("צאט אני מאוהב","איזה יופי! אין דבר נפלא מזה. שיהיה במזל!  :)"),
 ("צאט בוקר טוב","בוקר טוב ומואר! שיהיה לך יום מדהים.  :)"),
 ("צאט לילה טוב","לילה טוב! חלומות פז ומנוחה נעימה.  :)"),
 ("צאט תגיד לי משהו נחמד","אתה אדם מיוחד ועושה עבודה נהדרת. תמשיך כך!  :)"),
 ("צאט תן לי עצה","נשום עמוק, הקשב לעצמך, וסמוך על האינטואיציה שלך.  :)"),
 ("צאט אתה בינה מלאכותית","כן, אני AI -- ואני לומד ומשתפר כל הזמן.  :)"),
 ("צאט אתה אמיתי","אני כאן ומדבר איתך, לא?  :)"),
 ("צאט אתה אוהב חתולים","מי לא אוהב חתולים? יצורים מקסימים.  :)"),
 ("צאט עזרה",'אפשר לשוחח או לשחק! נסה: "צאט ספר בדיחה" או "בוא נשחק".  :)'),
]
def _strip_prefix_conflicts(chat):
    trigs=[nm for nm,_ in chat]; drop=set()
    for a in trigs:
        for b in trigs:
            if b!=a and b.startswith(a+" "): drop.add(b)
    return [(nm,v) for nm,v in chat if nm not in drop], drop
CHAT,_DROPPED=_strip_prefix_conflicts(CHAT)

# board prompts: prank-safe, contain NO trigger text
P_PLAY="תורך!  :)"
P_LOSE="ניצחתי! משחק טוב.  :)"
P_DRAW="תיקו! משחק צמוד.  :)"
P_WIN="ניצחת! כל הכבוד!  :)"

PFX_CODES="1514 1514 1514"          # "תתת"  = game trigger prefix (Hebrew)
PLAY_ALIAS_CODES="1489 1493 1488 32 1504 1513 1495 1511"  # "בוא נשחק" -> opens board

# ===== VBA encoding =====
def clean(s):
    out=[]
    for ch in s:
        o=ord(ch)
        if o in (0x200D,0x200E,0x200F,0xFE0F): continue
        if o>0xFFFF: continue
        out.append(ch)
    return ''.join(out)
def codes(s): return ' '.join(str(ord(c)) for c in clean(s))
def is_ascii(s): return all(32<=ord(c)<127 for c in s)
def vstr(s):
    if is_ascii(s): return '"%s"'%s.replace('"','""')
    return 'U("%s")'%codes(s)
U_FUNC=(
"Private Function U(ByVal codes As String) As String\n"
"    Dim parts As Variant\n    Dim i As Long\n    Dim s As String\n    s = \"\"\n"
"    If Len(codes) = 0 Then\n        U = \"\"\n        Exit Function\n    End If\n"
"    parts = Split(codes, \" \")\n"
"    For i = LBound(parts) To UBound(parts)\n"
"        If Len(parts(i)) > 0 Then\n            s = s & ChrW(CLng(parts(i)))\n        End If\n"
"    Next i\n    U = s\nEnd Function\n"
)
CHUNK=140

def build_setup():
    o=io.StringIO(); w=o.write
    w('Attribute VB_Name = "OfficeChat_Setup"\n')
    w("' ===================================================================\n")
    w("'  OfficeChat - Setup.  IMPORT this file (File > Import File), then F5\n")
    w("'  -> OfficeChat_Install.  Do NOT copy-paste into the code window.\n")
    w("' ===================================================================\n")
    w("Option Explicit\n\n")
    w(U_FUNC); w("\n")
    w("Private Sub AddPlain(ByVal nm As String, ByVal val As String)\n")
    w("    On Error Resume Next\n    Application.AutoCorrect.Entries.Add nm, val\n    On Error GoTo 0\nEnd Sub\n\n")
    w("Private Function CellCh(ByVal raw As String, ByVal i As Long) As String\n")
    w("    Dim ch As String\n    ch = Mid(raw, i, 1)\n")
    w("    If ch = \" \" Then\n        CellCh = CStr(i)\n    Else\n        CellCh = ch\n    End If\nEnd Function\n\n")
    w("Private Function BoardText(ByVal raw As String, ByVal status As String) As String\n")
    w("    Dim r1 As String, r2 As String, r3 As String, s As String\n")
    w("    Dim nl As String, L As String, P As String\n")
    w("    nl = ChrW(11)\n")     # soft line break (stacks rows, stays one plain entry)
    w("    L = ChrW(8234)\n")    # LRE: force left-to-right so digits are not reversed
    w("    P = ChrW(8236)\n")    # PDF: end the LTR run
    w('    r1 = L & " " & CellCh(raw,1) & " | " & CellCh(raw,2) & " | " & CellCh(raw,3) & " " & P\n')
    w('    r2 = L & " " & CellCh(raw,4) & " | " & CellCh(raw,5) & " | " & CellCh(raw,6) & " " & P\n')
    w('    r3 = L & " " & CellCh(raw,7) & " | " & CellCh(raw,8) & " | " & CellCh(raw,9) & " " & P\n')
    w("    Select Case status\n")
    w('        Case "play"\n            s = U("%s")\n'%codes(P_PLAY))
    w('        Case "lose"\n            s = U("%s")\n'%codes(P_LOSE))
    w('        Case "draw"\n            s = U("%s")\n'%codes(P_DRAW))
    w('        Case "win"\n            s = U("%s")\n'%codes(P_WIN))
    w("    End Select\n")
    w("    BoardText = r1 & nl & r2 & nl & r3 & nl & s & nl\n")
    w("End Function\n\n")
    w("Private Sub G(ByVal key As String, ByVal raw As String, ByVal status As String)\n")
    w('    AddPlain U("%s") & key, BoardText(raw, status)\n'%PFX_CODES)
    w("End Sub\n\n")

    keys=sorted(entries.keys(), key=lambda k:(len(k),k))
    chunks=[keys[i:i+CHUNK] for i in range(0,len(keys),CHUNK)]

    w("Public Sub OfficeChat_Install()\n")
    w("    InstallChat\n")
    for idx in range(len(chunks)): w("    InstallGame%d\n"%(idx+1))
    w('    MsgBox U("%s") & vbCr & U("%s"), vbInformation, "OfficeChat"\n'
      %(codes("OfficeChat מוכן!  :)"),codes('נסה בוורד:  היי צאט')))
    w("End Sub\n\n")

    w("Private Sub InstallChat()\n")
    for nm,val in CHAT:
        w("    AddPlain %s, %s & vbCr\n"%(vstr(nm),vstr(val)))
    # "בוא נשחק" opens the empty board (smooth demo opener)
    w('    AddPlain U("%s"), BoardText("         ", "play")\n'%PLAY_ALIAS_CODES)
    w("End Sub\n\n")

    for idx,ch in enumerate(chunks):
        w("Private Sub InstallGame%d()\n"%(idx+1))
        for key in ch:
            raw,status=entries[key]
            w('    G "%s", "%s", "%s"\n'%(key,raw,status))
        w("End Sub\n\n")
    return o.getvalue()

def build_remove():
    o=io.StringIO(); w=o.write
    w('Attribute VB_Name = "OfficeChat_Remove"\n')
    w("' IMPORT this file, then F5 -> OfficeChat_Uninstall.\n")
    w("Option Explicit\n\n")
    w(U_FUNC); w("\n")
    w("Private Sub DelE(ByVal nm As String)\n")
    w("    On Error Resume Next\n    Application.AutoCorrect.Entries(nm).Delete\n    On Error GoTo 0\nEnd Sub\n\n")
    keys=sorted(entries.keys(), key=lambda k:(len(k),k))
    chunks=[keys[i:i+CHUNK] for i in range(0,len(keys),CHUNK)]
    w("Public Sub OfficeChat_Uninstall()\n")
    w("    Dim before As Long, after As Long\n    before = Application.AutoCorrect.Entries.Count\n")
    w("    RemoveChat\n")
    for idx in range(len(chunks)): w("    RemoveGame%d\n"%(idx+1))
    w("    ' safety net: remove anything starting with the game prefix\n")
    w("    Dim i As Long, p3 As String\n")
    w('    p3 = U("%s")\n'%PFX_CODES)
    w("    For i = Application.AutoCorrect.Entries.Count To 1 Step -1\n")
    w("        If Left(Application.AutoCorrect.Entries(i).Name, 3) = p3 Then\n")
    w("            Application.AutoCorrect.Entries(i).Delete\n        End If\n    Next i\n")
    w("    after = Application.AutoCorrect.Entries.Count\n")
    w('    MsgBox U("%s") & vbCr & U("%s") & (before - after) & U("%s"), vbInformation, "OfficeChat"\n'
      %(codes("OfficeChat הוסר."),codes("נמחקו "),codes(" החלפות. וורד חזר לקדמותו.")))
    w("End Sub\n\n")
    w("Private Sub RemoveChat()\n")
    for nm,_ in CHAT: w("    DelE %s\n"%vstr(nm))
    w('    DelE U("%s")\n'%PLAY_ALIAS_CODES)  # "בוא נשחק" alias
    w("End Sub\n\n")
    for idx,ch in enumerate(chunks):
        w("Private Sub RemoveGame%d()\n"%(idx+1))
        for key in ch:
            w('    DelE U("%s") & "%s"\n'%(PFX_CODES,key))
        w("End Sub\n\n")
    return o.getvalue()

def build_diag():
    o=io.StringIO(); w=o.write
    w('Attribute VB_Name = "OfficeChat_Diag"\nOption Explicit\n\n')
    w(U_FUNC); w("\n")
    w("Public Sub OfficeChat_Diag()\n")
    w("    Dim n As Long, msg As String, v As String, e As Object\n")
    w("    n = Application.AutoCorrect.Entries.Count\n")
    w('    msg = "Total AutoCorrect entries: " & n & vbCrLf & vbCrLf\n')
    w('    v = "(NOT FOUND)"\n    On Error Resume Next\n')
    w('    Set e = Application.AutoCorrect.Entries(U("%s"))\n'%PFX_CODES)
    w("    On Error GoTo 0\n")
    w("    If Not e Is Nothing Then v = e.Value\n")
    w('    msg = msg & "Game entry value:" & vbCrLf & v\n')
    w('    MsgBox msg, vbInformation, "OfficeChat Diagnostics"\n')
    w("End Sub\n")
    return o.getvalue()

def build_vbs(install=True):
    o=io.StringIO(); w=o.write
    name = "Install" if install else "Uninstall"
    w("' %s-OfficeChat.vbs  -  double-click to %s (no VBA editor needed).\n"%(name, name.lower()))
    w("Option Explicit\n")
    w("Dim word, createdWord\n")
    w("Function U(codes)\n    Dim parts, i, s\n    s = \"\"\n")
    w("    If Len(codes) = 0 Then\n        U = \"\"\n        Exit Function\n    End If\n")
    w("    parts = Split(codes, \" \")\n    For i = 0 To UBound(parts)\n")
    w("        If Len(parts(i)) > 0 Then s = s & ChrW(CLng(parts(i)))\n    Next\n    U = s\nEnd Function\n")
    w("On Error Resume Next\nSet word = GetObject(, \"Word.Application\")\n")
    w("If word Is Nothing Then\n    Set word = CreateObject(\"Word.Application\")\n    createdWord = True\nEnd If\n")
    w("On Error GoTo 0\n")
    w("If word Is Nothing Then\n    MsgBox \"Microsoft Word not found.\", 16, \"OfficeChat\"\n    WScript.Quit\nEnd If\n")
    w("If createdWord Then word.Visible = False\n")
    if install:
        w("Function CellCh(raw, i)\n    Dim ch\n    ch = Mid(raw, i, 1)\n")
        w("    If ch = \" \" Then\n        CellCh = CStr(i)\n    Else\n        CellCh = ch\n    End If\nEnd Function\n")
        w("Function BoardText(raw, status)\n    Dim r1, r2, r3, s, nl, L, P\n")
        w("    nl = ChrW(11)\n    L = ChrW(8234)\n    P = ChrW(8236)\n")
        w("    r1 = L & \" \" & CellCh(raw,1) & \" | \" & CellCh(raw,2) & \" | \" & CellCh(raw,3) & \" \" & P\n")
        w("    r2 = L & \" \" & CellCh(raw,4) & \" | \" & CellCh(raw,5) & \" | \" & CellCh(raw,6) & \" \" & P\n")
        w("    r3 = L & \" \" & CellCh(raw,7) & \" | \" & CellCh(raw,8) & \" | \" & CellCh(raw,9) & \" \" & P\n")
        w("    Select Case status\n")
        w('        Case "play"\n            s = U("%s")\n'%codes(P_PLAY))
        w('        Case "lose"\n            s = U("%s")\n'%codes(P_LOSE))
        w('        Case "draw"\n            s = U("%s")\n'%codes(P_DRAW))
        w('        Case "win"\n            s = U("%s")\n'%codes(P_WIN))
        w("    End Select\n    BoardText = r1 & nl & r2 & nl & r3 & nl & s & nl\nEnd Function\n")
        w("Sub AddP(nm, val)\n    On Error Resume Next\n    word.AutoCorrect.Entries.Add nm, val\n    On Error GoTo 0\nEnd Sub\n")
        w("Sub AddG(key, raw, status)\n    AddP U(\"%s\") & key, BoardText(raw, status)\nEnd Sub\n"%PFX_CODES)
        for nm,val in CHAT: w("AddP %s, %s & vbCr\n"%(vstr(nm),vstr(val)))
        w('AddP U("%s"), BoardText("         ", "play")\n'%PLAY_ALIAS_CODES)
        for key in sorted(entries.keys(), key=lambda k:(len(k),k)):
            raw,status=entries[key]; w('AddG "%s", "%s", "%s"\n'%(key,raw,status))
        w("If createdWord Then\n    word.NormalTemplate.Saved = True\n    word.Quit\nEnd If\n")
        w('MsgBox U("%s") & vbCr & U("%s"), 64, "OfficeChat"\n'%(codes("OfficeChat מוכן!  :)"),codes("נסה בוורד:  היי צאט")))
    else:
        w("Sub DelE(nm)\n    On Error Resume Next\n    word.AutoCorrect.Entries(nm).Delete\n    On Error GoTo 0\nEnd Sub\n")
        for nm,_ in CHAT: w("DelE %s\n"%vstr(nm))
        w('DelE U("%s")\n'%PLAY_ALIAS_CODES)
        for key in sorted(entries.keys(), key=lambda k:(len(k),k)):
            w('DelE U("%s") & "%s"\n'%(PFX_CODES,key))
        w("Dim i, p3\np3 = U(\"%s\")\n"%PFX_CODES)
        w("For i = word.AutoCorrect.Entries.Count To 1 Step -1\n")
        w("    If Left(word.AutoCorrect.Entries(i).Name, 3) = p3 Then\n        word.AutoCorrect.Entries(i).Delete\n    End If\nNext\n")
        w("If createdWord Then\n    word.NormalTemplate.Saved = True\n    word.Quit\nEnd If\n")
        w('MsgBox U("%s"), 64, "OfficeChat"\n'%codes("OfficeChat הוסר. וורד חזר לקדמותו."))
    return o.getvalue()

setup=build_setup(); remove=build_remove(); diag=build_diag()
open("OfficeChat_Setup.bas","w",encoding="ascii").write(setup)
open("OfficeChat_Remove.bas","w",encoding="ascii").write(remove)
open("OfficeChat_Diag.bas","w",encoding="ascii").write(diag)
open("Install-OfficeChat.vbs","w",encoding="ascii").write(build_vbs(True))
open("Uninstall-OfficeChat.vbs","w",encoding="ascii").write(build_vbs(False))

# replacement list (UTF-8) - presenter reference only
def cell(raw,i):
    ch=raw[i-1]; return str(i) if ch==' ' else ch
def bl(raw,status):
    b="%s|%s|%s / %s|%s|%s / %s|%s|%s"%tuple(cell(raw,i) for i in range(1,10))
    s={'play':P_PLAY,'lose':P_LOSE,'draw':P_DRAW,'win':P_WIN}[status]
    return "%s  %s"%(b,s)
with open("officechat_all_replacements.txt","w",encoding="utf-8") as f:
    f.write("OfficeChat - רשימת החלפות (לעיני המפעיל בלבד!)\n"+"="*56+"\n")
    f.write('טריגר המשחק: "תתת" + ספרות (למשל תתת, תתת5, תתת59...).\n')
    f.write('"בוא נשחק" פותח לוח ריק. "/" = מעבר שורה בלוח.\n'+"="*56+"\n\n")
    f.write("--- א. שיחה ---\n\n")
    for nm,val in CHAT: f.write('"%s"  ->  %s\n\n'%(nm,val))
    f.write('"בוא נשחק"  ->  [לוח ריק]\n\n')
    f.write("\n--- ב. משחק (טריגר = תתת + רצף ספרות) ---\n\n")
    for key in sorted(entries.keys(), key=lambda k:(len(k),k)):
        raw,status=entries[key]; trig="תתת"+key if key else "תתת"
        f.write("%-10s ->  %s\n"%(trig,bl(raw,status)))

print("game states:",len(entries),"| chat:",len(CHAT),"| dropped:",_DROPPED)
for fn in ("OfficeChat_Setup.bas","OfficeChat_Remove.bas","OfficeChat_Diag.bas"):
    open(fn,encoding="ascii").read(); print("  %-24s %6d bytes ASCII-OK"%(fn,len(open(fn,encoding='ascii').read().encode('ascii'))))
