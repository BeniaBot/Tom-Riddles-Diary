# -*- coding: utf-8 -*-
"""
Tom Riddle generator - carry-token edition.

INPUT MECHANISM (user-verified by real typing, Word 16.0):
The player never types move codes.  Every "play" board ends with a visible
line "המהלך שלך הוא- " followed by a HIDDEN carry token that encodes the
game history.  The player types just the cell digit + space; Word's
AutoCorrect matches the document text before the delimiter - hidden runs
included - so [hidden token][typed digit] forms the full trigger.  From move
2 on, the space left by the previous fire sits between token and digit, so
those entry names contain a space ("phrase" entries) - also verified live.

Token scheme (loop-prevention safe):
  TS = final tsadi (U+05E5) - a char that never precedes digits naturally.
  opener token (empty history)      = TS TS
  token embedded in board h         = TS + reversed(h)
  entry name for move d from ""     = TS TS d          (no space - opener
                                       value ends at its token)
  entry name for move d from h      = TS + reversed(h) + " " + d
  Reversal guarantees the fired name never appears inside the new value
  (cell digits are all distinct), so Word's loop prevention stays quiet.

Every board value STARTS with a paragraph mark: without it, inserting a
table mid-paragraph absorbs the preceding text into the first cell
(observed live).  "play" values END at the token (final paragraph mark
excluded) so typing continues on the same line; terminal values keep it.

All entries are FORMATTED (AddRichText -> Normal.dotm + real Save); boards
are real 3x3 tables.  Plain entries added via automation do not persist and
land in per-language lists - measured, see CLAUDE.md.
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

# display name for user-facing Hebrew messages (NOT for code identifiers)
NAME_HE="היומן של תום רידל"
# MsgBox flags: vbMsgBoxRtlReading (1048576) + vbMsgBoxRight (524288) make the
# Hebrew message render RTL with correct punctuation order.
MB_RTL=1048576+524288
MB_INFO=64+MB_RTL

# board prompts: prank-safe, contain NO trigger text
P_MOVE="המהלך שלך הוא- "          # ends every live board; token follows hidden
P_LOSE="ניצחתי! משחק טוב.  :)"
P_DRAW="תיקו! משחק צמוד.  :)"
P_WIN="ניצחת! כל הכבוד!  :)"

# used only for docs/replacements.txt (presenter reference sketch)
BOX_V=0x2502   # │

TS="ץ"                              # carry-token marker (final tsadi)
LEGACY_PFX_CODES="1514 1514 1514"   # old "תתת" scheme - swept on install/uninstall
PLAY_ALIAS_CODES="1489 1493 1488 32 1504 1513 1495 1511"  # "בוא נשחק" -> opens board

def game_token(h):
    """Hidden carry token embedded at the end of board h (play boards only)."""
    return TS + h[::-1] if h else TS+TS
def game_name(h):
    """AutoCorrect entry name for the move that PRODUCED history h.
    ALWAYS token + space + digit: every fire (the opener included) leaves its
    delimiter space after the inserted token, so the space is part of the next
    trigger.  Verified live - a spaceless first-move name never matches."""
    return game_token(h[:-1]) + " " + h[-1]

# ===== board table styling (wdColor = R + G*256 + B*65536) =====
def _rgb(r,g,b): return r + g*256 + b*65536
C_X=_rgb(192,0,0)        # X: bold dark red
C_O=_rgb(0,80,192)       # O: bold blue
C_D=_rgb(150,150,150)    # free-cell digit hints: gray
# CRASH RULE (measured, Word 16.0): on a WINDOWLESS document, ANY paragraph-
# alignment write - Range.ParagraphFormat or Styles(...).ParagraphFormat -
# kills the Word process (RPC 0x800706BE).  Text, Font, table geometry,
# Cells.VerticalAlignment and TableDirection are all safe.  Therefore the
# board uses NO horizontal paragraph alignment; instead the cells are made
# narrow (CELL_W + small padding) so a single glyph sits visually centered.
# ScreenUpdating=False on a windowless doc also crashes - never use it.
CELL_H=26                # row height in points
CELL_W=20                # column width in points (narrow = pseudo-centering)
CELL_PAD=2               # left+right cell padding in points
CELL_FONT=16
STATUS_FONT=12

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

GAME_KEYS=sorted([k for k in entries if k], key=lambda k:(len(k),k))

def _status_cases(w,indent,fn):
    for st,txt in (("play",P_MOVE),("lose",P_LOSE),("draw",P_DRAW),("win",P_WIN)):
        w('%sCase "%s"\n%s    %s = U("%s")\n'%(indent,st,indent,fn,codes(txt)))

# game-name recognizer emitted into VBA and VBS (shared logic):
# tsadi-scheme names (tsadi first, then only tsadi/digits/space) OR legacy
# taf-taf-taf prefix.  Used by the install pre-sweep, the uninstall safety
# net and the post-install count.
def _is_game_fn(w,vba):
    d=w
    if vba:
        d("Private Function IsGameName(ByVal nm As String) As Boolean\n")
        d("    Dim j As Long, c As String\n")
    else:
        d("Function IsGameName(nm)\n")
        d("    Dim j, c\n")
        d("    IsGameName = False\n")
    d("    If Len(nm) < 2 Then Exit Function\n")
    d('    If Left(nm, 3) = U("%s") Then\n'%LEGACY_PFX_CODES)
    d("        IsGameName = True\n")
    d("        Exit Function\n")
    d("    End If\n")
    d('    If Left(nm, 1) <> U("%s") Then Exit Function\n'%codes(TS))
    d("    For j = 2 To Len(nm)\n")
    d("        c = Mid(nm, j, 1)\n")
    d('        If Not (c = " " Or c = U("%s") Or (c >= "0" And c <= "9")) Then Exit Function\n'%codes(TS))
    d("    Next%s\n"%(" j" if vba else ""))
    d("    IsGameName = True\n")
    d("End Function\n")

def build_setup():
    o=io.StringIO(); w=o.write
    w('Attribute VB_Name = "TomRiddle_Setup"\n')
    w("' ===================================================================\n")
    w("'  Tom Riddle - Setup.  IMPORT this file (File > Import File), then F5\n")
    w("'  -> TomRiddle_Install.  Do NOT copy-paste into the code window.\n")
    w("'  All entries are FORMATTED AutoCorrect entries (AddRichText): boards\n")
    w("'  are real tables ending with a HIDDEN carry token; the player types\n")
    w("'  only the cell digit.  Entries live in Normal.dotm - the installer\n")
    w("'  performs a REAL NormalTemplate.Save at the end; without it NOTHING\n")
    w("'  persists after Word closes.\n")
    w("' ===================================================================\n")
    w("Option Explicit\n\n")
    w("Private tDoc As Document\n")
    w("Private tTbl As Table\n\n")
    w(U_FUNC); w("\n")
    _is_game_fn(w,vba=True); w("\n")
    w("Private Sub AddRich(ByVal nm As String, ByVal rng As Range)\n")
    w("    ' delete in a loop: a plain and a rich entry can share the same name\n")
    w("    Dim t As Long\n")
    w("    On Error Resume Next\n")
    w("    For t = 1 To 8\n")
    w("        Err.Clear\n")
    w("        Application.AutoCorrect.Entries(nm).Delete\n")
    w("        If Err.Number <> 0 Then Exit For\n")
    w("    Next t\n")
    w("    Err.Clear\n")
    w("    Application.AutoCorrect.Entries.AddRichText nm, rng\n")
    w("    On Error GoTo 0\n")
    w("End Sub\n\n")
    w("Private Function StatusText(ByVal status As String) As String\n")
    w("    Select Case status\n")
    _status_cases(w,"        ","StatusText")
    w("    End Select\n")
    w("End Function\n\n")
    w("Private Sub AddChat(ByVal nm As String, ByVal val As String)\n")
    w("    Dim r As Range\n")
    w("    Set r = tDoc.Content\n")
    w("    r.End = r.End - 1\n")
    w("    r.Text = val\n")
    w("    AddRich nm, tDoc.Content\n")
    w("End Sub\n\n")
    w("Private Sub BoardDoc()\n")
    w("    ' NO ParagraphFormat calls here: on a windowless document they\n")
    w("    ' crash the Word process (see the CRASH RULE in the generator).\n")
    w("    ' Layout: [paragraph mark][3x3 table][status/move paragraph].\n")
    w("    ' The LEADING paragraph mark is required: without it, inserting\n")
    w("    ' the value mid-line absorbs the preceding text into the table.\n")
    w("    tDoc.Content.Delete\n")
    w("    Dim r As Range\n")
    w("    Set r = tDoc.Range(0, 0)\n")
    w("    r.Text = vbCr\n")
    w("    Set tTbl = tDoc.Tables.Add(tDoc.Range(1, 1), 3, 3)\n")
    w("    tTbl.Borders.InsideLineStyle = 1\n")
    w("    tTbl.Borders.OutsideLineStyle = 1\n")
    w("    tTbl.Rows.Alignment = 1\n")
    w("    tTbl.Rows.HeightRule = 2\n")
    w("    tTbl.Rows.Height = %d\n"%CELL_H)
    w("    tTbl.Columns.Width = %d\n"%CELL_W)
    w("    On Error Resume Next\n")
    w("    tTbl.LeftPadding = %d\n"%CELL_PAD)
    w("    tTbl.RightPadding = %d\n"%CELL_PAD)
    w("    On Error GoTo 0\n")
    w("    tTbl.Range.Cells.VerticalAlignment = 1\n")
    w("    tTbl.Range.Font.Size = %d\n"%CELL_FONT)
    w("    tTbl.TableDirection = 1\n")
    w("    Dim sr As Range\n")
    w("    Set sr = tDoc.Paragraphs.Last.Range\n")
    w("    sr.Font.Bold = True\n")
    w("    sr.Font.Size = %d\n"%STATUS_FONT)
    w("End Sub\n\n")
    w("Private Sub SetCell(ByVal i As Long, ByVal ch As String)\n")
    w("    Dim r As Range\n")
    w("    Set r = tTbl.Cell((i - 1) \\ 3 + 1, (i - 1) Mod 3 + 1).Range\n")
    w("    r.End = r.End - 1\n")
    w("    r.Text = ch\n")
    w("    Set r = tTbl.Cell((i - 1) \\ 3 + 1, (i - 1) Mod 3 + 1).Range\n")
    w('    If ch = "X" Then\n')
    w("        r.Font.Bold = True\n")
    w("        r.Font.Color = %d\n"%C_X)
    w('    ElseIf ch = "O" Then\n')
    w("        r.Font.Bold = True\n")
    w("        r.Font.Color = %d\n"%C_O)
    w("    Else\n")
    w("        r.Font.Bold = False\n")
    w("        r.Font.Color = %d\n"%C_D)
    w("    End If\n")
    w("End Sub\n\n")
    w("Private Sub SetBoard(ByVal raw As String, ByVal status As String, ByVal tok As String)\n")
    w("    Dim i As Long, ch As String, sr As Range, tk As Range\n")
    w("    Set tTbl = tDoc.Tables(1)   ' re-fetch: table pointers can go stale\n")
    w("    For i = 1 To 9\n")
    w("        ch = Mid(raw, i, 1)\n")
    w('        If ch = " " Then ch = CStr(i)\n')
    w("        SetCell i, ch\n")
    w("    Next i\n")
    w("    Set sr = tDoc.Paragraphs.Last.Range\n")
    w("    sr.End = sr.End - 1\n")
    w("    If Len(tok) > 0 Then\n")
    w("        sr.Text = StatusText(\"play\") & tok\n")
    w("    Else\n")
    w("        sr.Text = StatusText(status)\n")
    w("    End If\n")
    w("    ' reset the line, then make ONLY the carry token invisible.\n")
    w("    ' Triple defense - real firing was seen stripping Hidden alone:\n")
    w("    ' Hidden + 1pt + white + no spellcheck squiggle.\n")
    w("    Set sr = tDoc.Paragraphs.Last.Range\n")
    w("    sr.Font.Hidden = False\n")
    w("    sr.Font.Size = %d\n"%STATUS_FONT)
    w("    sr.Font.Color = 0\n")
    w("    If Len(tok) > 0 Then\n")
    w("        Set tk = tDoc.Range(sr.End - 1 - Len(tok), sr.End - 1)\n")
    w("        tk.Font.Hidden = True\n")
    w("        tk.Font.Size = 1\n")
    w("        tk.Font.Color = 16777215\n")
    w("        On Error Resume Next\n")
    w("        tk.NoProofing = True\n")
    w("        On Error GoTo 0\n")
    w("    End If\n")
    w("End Sub\n\n")
    w("Private Sub G(ByVal nm As String, ByVal raw As String, ByVal status As String, ByVal tok As String)\n")
    w("    SetBoard raw, status, tok\n")
    w("    If Len(tok) > 0 Then\n")
    w("        ' play boards end AT the token so typing continues on the line\n")
    w("        AddRich nm, tDoc.Range(0, tDoc.Content.End - 1)\n")
    w("    Else\n")
    w("        AddRich nm, tDoc.Content\n")
    w("    End If\n")
    w("End Sub\n\n")

    chunks=[GAME_KEYS[i:i+CHUNK] for i in range(0,len(GAME_KEYS),CHUNK)]

    w("Public Sub TomRiddle_Install()\n")
    w('    MsgBox U("%s"), %d, U("%s")\n'
      %(codes("מתקין את "+NAME_HE+"... ההתקנה אורכת 2-3 דקות. לא לסגור את וורד עד הודעת הסיום."),MB_INFO,codes(NAME_HE)))
    w("    SweepGame   ' clear any previous version (old scheme included)\n")
    w("    ' NOTE: do NOT set ScreenUpdating = False - combined with an\n")
    w("    ' invisible document it reproducibly crashes Word (RPC failure).\n")
    w("    Set tDoc = Documents.Add(Visible:=False)\n")
    w("    InstallChat\n")
    w("    BoardDoc\n")
    for idx in range(len(chunks)): w("    InstallGame%d\n"%(idx+1))
    w("    InstallOpener\n")
    w("    tDoc.Saved = True\n")
    w("    tDoc.Close 0\n")
    w("    Set tDoc = Nothing\n")
    w("    Dim n As Long\n")
    w("    n = CountGame()\n")
    w("    ' REAL save - this is what makes the install survive Word closing\n")
    w("    On Error Resume Next\n")
    w("    NormalTemplate.Save\n")
    w("    On Error GoTo 0\n")
    w('    MsgBox U("%s") & n & U("%s") & vbCr & U("%s"), %d, U("%s")\n'
      %(codes(NAME_HE+" מוכן! נשמרו "),codes(" לוחות משחק.  :)"),codes("נסה בוורד:  היי צאט"),MB_INFO,codes(NAME_HE)))
    w("End Sub\n\n")
    w("Private Sub SweepGame()\n")
    w("    Dim i As Long\n")
    w("    For i = Application.AutoCorrect.Entries.Count To 1 Step -1\n")
    w("        If IsGameName(Application.AutoCorrect.Entries(i).Name) Then\n")
    w("            Application.AutoCorrect.Entries(i).Delete\n")
    w("        End If\n")
    w("    Next i\n")
    w("End Sub\n\n")
    w("Private Function CountGame() As Long\n")
    w("    Dim i As Long, n As Long\n")
    w("    For i = 1 To Application.AutoCorrect.Entries.Count\n")
    w("        If IsGameName(Application.AutoCorrect.Entries(i).Name) Then n = n + 1\n")
    w("    Next i\n")
    w("    CountGame = n\n")
    w("End Function\n\n")
    w("Private Sub InstallChat()\n")
    w("    ' no alignment set: the template default paragraph (RTL Hebrew\n")
    w("    ' profile) is already right-aligned, and ParagraphFormat writes\n")
    w("    ' crash a windowless document anyway\n")
    for nm,val in CHAT:
        w("    AddChat %s, %s\n"%(vstr(nm),vstr(val)))
    w("End Sub\n\n")
    w("Private Sub InstallOpener()\n")
    w('    SetBoard "         ", "play", U("%s")\n'%codes(game_token("")))
    w('    AddRich U("%s"), tDoc.Range(0, tDoc.Content.End - 1)\n'%PLAY_ALIAS_CODES)
    w("End Sub\n\n")
    for idx,ch in enumerate(chunks):
        w("Private Sub InstallGame%d()\n"%(idx+1))
        for key in ch:
            raw,status=entries[key]
            tok=game_token(key) if status=="play" else ""
            w('    G U("%s"), "%s", "%s", U("%s")\n'%(codes(game_name(key)),raw,status,codes(tok)))
        w("End Sub\n\n")
    return o.getvalue()

def build_remove():
    o=io.StringIO(); w=o.write
    w('Attribute VB_Name = "TomRiddle_Remove"\n')
    w("' IMPORT this file, then F5 -> TomRiddle_Uninstall.\n")
    w("Option Explicit\n\n")
    w(U_FUNC); w("\n")
    _is_game_fn(w,vba=True); w("\n")
    w("Private Sub DelE(ByVal nm As String)\n")
    w("    ' delete in a loop: a plain and a rich entry can share the same name\n")
    w("    Dim t As Long\n")
    w("    On Error Resume Next\n")
    w("    For t = 1 To 8\n")
    w("        Err.Clear\n")
    w("        Application.AutoCorrect.Entries(nm).Delete\n")
    w("        If Err.Number <> 0 Then Exit For\n")
    w("    Next t\n")
    w("    On Error GoTo 0\n")
    w("End Sub\n\n")
    chunks=[GAME_KEYS[i:i+CHUNK] for i in range(0,len(GAME_KEYS),CHUNK)]
    w("Public Sub TomRiddle_Uninstall()\n")
    w("    Dim before As Long, after As Long\n    before = Application.AutoCorrect.Entries.Count\n")
    w("    RemoveChat\n")
    for idx in range(len(chunks)): w("    RemoveGame%d\n"%(idx+1))
    w("    ' safety net: remove anything that looks like a game entry,\n")
    w("    ' current scheme or legacy\n")
    w("    Dim i As Long\n")
    w("    For i = Application.AutoCorrect.Entries.Count To 1 Step -1\n")
    w("        If IsGameName(Application.AutoCorrect.Entries(i).Name) Then\n")
    w("            Application.AutoCorrect.Entries(i).Delete\n")
    w("        End If\n")
    w("    Next i\n")
    w("    after = Application.AutoCorrect.Entries.Count\n")
    w("    ' REAL save - deletions of formatted entries live in Normal.dotm\n")
    w("    On Error Resume Next\n")
    w("    NormalTemplate.Save\n")
    w("    On Error GoTo 0\n")
    w('    MsgBox U("%s") & vbCr & U("%s") & (before - after) & U("%s"), %d, U("%s")\n'
      %(codes(NAME_HE+" הוסר."),codes("נמחקו "),codes(" החלפות. וורד חזר לקדמותו."),MB_INFO,codes(NAME_HE)))
    w("End Sub\n\n")
    w("Private Sub RemoveChat()\n")
    for nm,_ in CHAT: w("    DelE %s\n"%vstr(nm))
    w('    DelE U("%s")\n'%PLAY_ALIAS_CODES)  # "בוא נשחק" opener
    w("End Sub\n\n")
    for idx,ch in enumerate(chunks):
        w("Private Sub RemoveGame%d()\n"%(idx+1))
        for key in ch:
            w('    DelE U("%s")\n'%codes(game_name(key)))
        w("End Sub\n\n")
    return o.getvalue()

def build_diag():
    o=io.StringIO(); w=o.write
    w('Attribute VB_Name = "TomRiddle_Diag"\nOption Explicit\n\n')
    w(U_FUNC); w("\n")
    _is_game_fn(w,vba=True); w("\n")
    w("Public Sub TomRiddle_Diag()\n")
    w("    Dim n As Long, g As Long, i As Long, msg As String, v As String, e As Object\n")
    w("    n = Application.AutoCorrect.Entries.Count\n")
    w("    For i = 1 To n\n")
    w("        If IsGameName(Application.AutoCorrect.Entries(i).Name) Then g = g + 1\n")
    w("    Next i\n")
    w('    msg = "Total AutoCorrect entries: " & n & vbCrLf\n')
    w('    msg = msg & "Game entries: " & g & vbCrLf & vbCrLf\n')
    w('    v = "(NOT FOUND)"\n    On Error Resume Next\n')
    w('    Set e = Application.AutoCorrect.Entries(U("%s"))\n'%PLAY_ALIAS_CODES)
    w("    On Error GoTo 0\n")
    w('    If Not e Is Nothing Then v = "exists, RichText=" & e.RichText\n')
    w('    msg = msg & "Opener entry: " & v\n')
    w('    MsgBox msg, vbInformation, "Tom Riddle Diagnostics"\n')
    w("End Sub\n")
    return o.getvalue()

def build_vbs(install=True):
    o=io.StringIO(); w=o.write
    name = "Install" if install else "Uninstall"
    w("' %s-TomRiddle.vbs  -  double-click to %s (no VBA editor needed).\n"%(name, name.lower()))
    if install:
        w("' Boards are REAL Word tables stored as formatted AutoCorrect entries\n")
        w("' (AddRichText -> Normal.dotm).  Expect the install to take a couple of\n")
        w("' minutes; a completion popup reports how many boards were saved.\n")
    w("Option Explicit\n")
    w("Dim word, createdWord, tDoc, tTbl\n")
    w("Function U(codes)\n    Dim parts, i, s\n    s = \"\"\n")
    w("    If Len(codes) = 0 Then\n        U = \"\"\n        Exit Function\n    End If\n")
    w("    parts = Split(codes, \" \")\n    For i = 0 To UBound(parts)\n")
    w("        If Len(parts(i)) > 0 Then s = s & ChrW(CLng(parts(i)))\n    Next\n    U = s\nEnd Function\n")
    _is_game_fn(w,vba=False)
    w("Sub Announce(msg)\n")
    w("    If InStr(1, LCase(WScript.FullName), \"cscript\") > 0 Then\n")
    w("        WScript.Echo msg\n")
    w("    Else\n")
    w("        ' %d = vbInformation + vbMsgBoxRtlReading + vbMsgBoxRight\n"%MB_INFO)
    w('        MsgBox msg, %d, U("%s")\n'%(MB_INFO,codes(NAME_HE)))
    w("    End If\n")
    w("End Sub\n")
    w("On Error Resume Next\nSet word = GetObject(, \"Word.Application\")\n")
    w("If word Is Nothing Then\n    Set word = CreateObject(\"Word.Application\")\n    createdWord = True\nEnd If\n")
    w("On Error GoTo 0\n")
    w("If word Is Nothing Then\n    MsgBox \"Microsoft Word not found.\", 16, \"Tom Riddle\"\n    WScript.Quit\nEnd If\n")
    w("If createdWord Then word.Visible = False\n")
    if install:
        w("Sub AddRich(nm, rng)\n")
        w("    ' delete in a loop: a plain and a rich entry can share the same name\n")
        w("    Dim t\n")
        w("    On Error Resume Next\n")
        w("    For t = 1 To 8\n")
        w("        Err.Clear\n")
        w("        word.AutoCorrect.Entries(nm).Delete\n")
        w("        If Err.Number <> 0 Then Exit For\n")
        w("    Next\n")
        w("    Err.Clear\n")
        w("    word.AutoCorrect.Entries.AddRichText nm, rng\n")
        w("    On Error GoTo 0\n")
        w("End Sub\n")
        w("Function StatusText(status)\n")
        w("    Select Case status\n")
        for st,txt in (("play",P_MOVE),("lose",P_LOSE),("draw",P_DRAW),("win",P_WIN)):
            w('        Case "%s"\n            StatusText = U("%s")\n'%(st,codes(txt)))
        w("    End Select\n")
        w("End Function\n")
        w("Sub AddChat(nm, val)\n")
        w("    Dim r\n")
        w("    Set r = tDoc.Content\n")
        w("    r.End = r.End - 1\n")
        w("    r.Text = val\n")
        w("    AddRich nm, tDoc.Content\n")
        w("End Sub\n")
        w("Sub BoardDoc()\n")
        w("    ' NO ParagraphFormat calls: they crash Word on a windowless doc.\n")
        w("    ' Layout: [paragraph mark][3x3 table][status/move paragraph];\n")
        w("    ' the leading paragraph mark keeps the insertion off the line\n")
        w("    ' the player typed on (mid-line tables absorb preceding text).\n")
        w("    tDoc.Content.Delete\n")
        w("    Dim r\n")
        w("    Set r = tDoc.Range(0, 0)\n")
        w("    r.Text = vbCr\n")
        w("    Set tTbl = tDoc.Tables.Add(tDoc.Range(1, 1), 3, 3)\n")
        w("    tTbl.Borders.InsideLineStyle = 1\n")
        w("    tTbl.Borders.OutsideLineStyle = 1\n")
        w("    tTbl.Rows.Alignment = 1\n")
        w("    tTbl.Rows.HeightRule = 2\n")
        w("    tTbl.Rows.Height = %d\n"%CELL_H)
        w("    tTbl.Columns.Width = %d\n"%CELL_W)
        w("    On Error Resume Next\n")
        w("    tTbl.LeftPadding = %d\n"%CELL_PAD)
        w("    tTbl.RightPadding = %d\n"%CELL_PAD)
        w("    On Error GoTo 0\n")
        w("    tTbl.Range.Cells.VerticalAlignment = 1\n")
        w("    tTbl.Range.Font.Size = %d\n"%CELL_FONT)
        w("    tTbl.TableDirection = 1\n")
        w("    Dim sr\n")
        w("    Set sr = tDoc.Paragraphs.Last.Range\n")
        w("    sr.Font.Bold = True\n")
        w("    sr.Font.Size = %d\n"%STATUS_FONT)
        w("End Sub\n")
        w("Sub SetCell(i, ch)\n")
        w("    Dim r\n")
        w("    Set r = tTbl.Cell((i - 1) \\ 3 + 1, (i - 1) Mod 3 + 1).Range\n")
        w("    r.End = r.End - 1\n")
        w("    r.Text = ch\n")
        w("    Set r = tTbl.Cell((i - 1) \\ 3 + 1, (i - 1) Mod 3 + 1).Range\n")
        w('    If ch = "X" Then\n')
        w("        r.Font.Bold = True\n")
        w("        r.Font.Color = %d\n"%C_X)
        w('    ElseIf ch = "O" Then\n')
        w("        r.Font.Bold = True\n")
        w("        r.Font.Color = %d\n"%C_O)
        w("    Else\n")
        w("        r.Font.Bold = False\n")
        w("        r.Font.Color = %d\n"%C_D)
        w("    End If\n")
        w("End Sub\n")
        w("Sub SetBoard(raw, status, tok)\n")
        w("    Dim i, ch, sr, tk\n")
        w("    Set tTbl = tDoc.Tables(1)   ' re-fetch: table pointers can go stale\n")
        w("    For i = 1 To 9\n")
        w("        ch = Mid(raw, i, 1)\n")
        w('        If ch = " " Then ch = CStr(i)\n')
        w("        SetCell i, ch\n")
        w("    Next\n")
        w("    Set sr = tDoc.Paragraphs.Last.Range\n")
        w("    sr.End = sr.End - 1\n")
        w("    If Len(tok) > 0 Then\n")
        w('        sr.Text = StatusText("play") & tok\n')
        w("    Else\n")
        w("        sr.Text = StatusText(status)\n")
        w("    End If\n")
        w("    ' triple invisibility for the token: Hidden + 1pt + white + NoProofing\n")
        w("    Set sr = tDoc.Paragraphs.Last.Range\n")
        w("    sr.Font.Hidden = False\n")
        w("    sr.Font.Size = %d\n"%STATUS_FONT)
        w("    sr.Font.Color = 0\n")
        w("    If Len(tok) > 0 Then\n")
        w("        Set tk = tDoc.Range(sr.End - 1 - Len(tok), sr.End - 1)\n")
        w("        tk.Font.Hidden = True\n")
        w("        tk.Font.Size = 1\n")
        w("        tk.Font.Color = 16777215\n")
        w("        On Error Resume Next\n")
        w("        tk.NoProofing = True\n")
        w("        On Error GoTo 0\n")
        w("    End If\n")
        w("End Sub\n")
        w("Sub AddG(nm, raw, status, tok)\n")
        w("    SetBoard raw, status, tok\n")
        w("    If Len(tok) > 0 Then\n")
        w("        AddRich nm, tDoc.Range(0, tDoc.Content.End - 1)\n")
        w("    Else\n")
        w("        AddRich nm, tDoc.Content\n")
        w("    End If\n")
        w("End Sub\n")
        w("Sub SweepGame()\n")
        w("    Dim i\n")
        w("    For i = word.AutoCorrect.Entries.Count To 1 Step -1\n")
        w("        If IsGameName(word.AutoCorrect.Entries(i).Name) Then\n")
        w("            word.AutoCorrect.Entries(i).Delete\n")
        w("        End If\n")
        w("    Next\n")
        w("End Sub\n")
        w('Announce U("%s")\n'%codes("מתקין את "+NAME_HE+"... ההתקנה אורכת 2-3 דקות. אם וורד פתוח - אל תסגור אותו עד הודעת הסיום."))
        w("SweepGame\n")
        w("' invisible work document (Visible:=False): the user cannot close it\n")
        w("' mid-install even when we attach to their open Word instance.\n")
        w("' NOTE: no ScreenUpdating=False here - combined with a windowless\n")
        w("' document it reproducibly CRASHES Word (RPC 0x800706BE).\n")
        w("Set tDoc = word.Documents.Add(word.NormalTemplate.FullName, False, 0, False)\n")
        w("' no alignment set: template default (RTL profile) is already right-\n")
        w("' aligned, and ParagraphFormat writes crash a windowless document\n")
        for nm,val in CHAT: w("AddChat %s, %s\n"%(vstr(nm),vstr(val)))
        w("BoardDoc\n")
        for key in GAME_KEYS:
            raw,status=entries[key]
            tok=game_token(key) if status=="play" else ""
            w('AddG U("%s"), "%s", "%s", U("%s")\n'%(codes(game_name(key)),raw,status,codes(tok)))
        w('SetBoard "         ", "play", U("%s")\n'%codes(game_token("")))
        w('AddRich U("%s"), tDoc.Range(0, tDoc.Content.End - 1)\n'%PLAY_ALIAS_CODES)
        w("tDoc.Saved = True\ntDoc.Close 0\nSet tDoc = Nothing\n")
        w("Dim i2, n\nn = 0\n")
        w("For i2 = 1 To word.AutoCorrect.Entries.Count\n")
        w("    If IsGameName(word.AutoCorrect.Entries(i2).Name) Then n = n + 1\nNext\n")
        w("' REAL save - without it the whole install vanishes when Word closes\n")
        w("Dim saveNote\nsaveNote = \"\"\nOn Error Resume Next\nword.NormalTemplate.Save\n")
        w("If Err.Number <> 0 Then saveNote = \" [!] \" & Err.Description\nErr.Clear\nOn Error GoTo 0\n")
        w("If createdWord Then word.Quit\n")
        w('Announce U("%s") & n & U("%s") & saveNote\n'
          %(codes(NAME_HE+" מוכן! נשמרו "),codes(" לוחות. נסה בוורד:  היי צאט")))
    else:
        w("Sub DelE(nm)\n")
        w("    ' delete in a loop: a plain and a rich entry can share the same name\n")
        w("    Dim t\n")
        w("    On Error Resume Next\n")
        w("    For t = 1 To 8\n")
        w("        Err.Clear\n")
        w("        word.AutoCorrect.Entries(nm).Delete\n")
        w("        If Err.Number <> 0 Then Exit For\n")
        w("    Next\n")
        w("    On Error GoTo 0\n")
        w("End Sub\n")
        w('Announce U("%s")\n'%codes("מסיר את "+NAME_HE+"... זה לוקח פחות מדקה."))
        for nm,_ in CHAT: w("DelE %s\n"%vstr(nm))
        w('DelE U("%s")\n'%PLAY_ALIAS_CODES)
        for key in GAME_KEYS:
            w('DelE U("%s")\n'%codes(game_name(key)))
        w("' safety net: current scheme + legacy prefixes\n")
        w("Dim i\n")
        w("For i = word.AutoCorrect.Entries.Count To 1 Step -1\n")
        w("    If IsGameName(word.AutoCorrect.Entries(i).Name) Then\n")
        w("        word.AutoCorrect.Entries(i).Delete\n")
        w("    End If\nNext\n")
        w("' REAL save - deletions of formatted entries live in Normal.dotm\n")
        w("On Error Resume Next\nword.NormalTemplate.Save\nOn Error GoTo 0\n")
        w("If createdWord Then word.Quit\n")
        w('Announce U("%s")\n'%codes(NAME_HE+" הוסר. וורד חזר לקדמותו."))
    return o.getvalue()

setup=build_setup(); remove=build_remove(); diag=build_diag()
open("TomRiddle_Setup.bas","w",encoding="ascii").write(setup)
open("TomRiddle_Remove.bas","w",encoding="ascii").write(remove)
open("TomRiddle_Diag.bas","w",encoding="ascii").write(diag)
open("Install-TomRiddle.vbs","w",encoding="ascii").write(build_vbs(True))
open("Uninstall-TomRiddle.vbs","w",encoding="ascii").write(build_vbs(False))

# replacement list (UTF-8) - presenter reference only
def cell(raw,i):
    ch=raw[i-1]; return str(i) if ch==' ' else ch
def bl(raw,status):
    v=chr(BOX_V)
    b=" / ".join("%s%s%s%s%s%s%s"%(v,cell(raw,i),v,cell(raw,i+1),v,cell(raw,i+2),v)
                 for i in (1,4,7))
    s={'play':P_MOVE+"...",'lose':P_LOSE,'draw':P_DRAW,'win':P_WIN}[status]
    return "%s  %s"%(b,s)
with open("tomriddle_all_replacements.txt","w",encoding="utf-8") as f:
    f.write("תום רידל - רשימת החלפות (לעיני המפעיל בלבד!)\n"+"="*56+"\n")
    f.write('המשחק: "בוא נשחק" פותח לוח. בכל תור מקלידים את ספרת המשבצת\n')
    f.write('ואז רווח, בהמשך שורת "המהלך שלך הוא- " - הלוח הבא מופיע לבד\n')
    f.write('(את המצב נושא טוקן נסתר בסוף השורה; אין צורך בקודים).\n')
    f.write('טעית בספרה? Backspace והקלד שוב. בוורד כל לוח הוא טבלה אמיתית;\n')
    f.write('כאן "/" מפריד בין שורות הלוח לצורך תמצות בלבד.\n'+"="*56+"\n\n")
    f.write("--- א. שיחה ---\n\n")
    for nm,val in CHAT: f.write('"%s"  ->  %s\n\n'%(nm,val))
    f.write('"בוא נשחק"  ->  [לוח ריק]\n\n')
    f.write("\n--- ב. משחק (לפי רצף המהלכים שלך עד כה) ---\n\n")
    for key in GAME_KEYS:
        raw,status=entries[key]
        f.write("%-10s ->  %s\n"%(",".join(key),bl(raw,status)))

print("game states:",len(entries),"| game entries:",len(GAME_KEYS),"| chat:",len(CHAT),"| dropped:",_DROPPED)
for fn in ("TomRiddle_Setup.bas","TomRiddle_Remove.bas","TomRiddle_Diag.bas"):
    open(fn,encoding="ascii").read(); print("  %-24s %6d bytes ASCII-OK"%(fn,len(open(fn,encoding='ascii').read().encode('ascii'))))
