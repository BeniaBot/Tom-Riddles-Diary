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
 # --- v0.3: natural, no-keyword sentences (the "classic almost-random" set) ---
 ("מה נשמע","הכל מעולה אצלי! ומה איתך?  :)"),
 ("מה קורה","שמח שאתה כאן! איך היום שלך?  :)"),
 ("מה חדש","כל יום אני לומד משהו. ספר לי אתה -- מה מתחדש אצלך?  :)"),
 ("מה שלומך","מצוין, תודה ששאלת! ואתה?  :)"),
 ("מה העניינים","הכול טוב, ורק ישתפר!  :)"),
 ("בוקר טוב","בוקר אור! שיהיה לך יום נהדר.  :)"),
 ("ערב טוב","ערב נפלא! איך עבר עליך היום?  :)"),
 ("לילה טוב","חלומות פז! נתראה מחר.  :)"),
 ("שבת שלום","שבת מבורכת ורגועה!  :)"),
 ("חג שמח","חג נפלא ומלא אור!  :)"),
 ("מי אתה","העוזר הדיגיטלי החדש שלך! תשאל אותי כל דבר.  :)"),
 ("איך קוראים לך","קוראים לי תום. נעים מאוד!  :)"),
 ("מה השם שלך","תום. לשירותך!  :)"),
 ("בן כמה אתה","צעיר ברוחי, ותיק בידע.  :)"),
 ("איפה אתה גר","בתוך המחשב שלך. כתובת מצוינת!  :)"),
 ("מי יצר אותך","מתכנת גאון אחד עם המון סבלנות.  :)"),
 ("אתה רובוט","אני עוזר דיגיטלי -- רובוט עם נשמה.  :)"),
 ("אתה בן אדם","לא בדיוק... אבל אני מקשיב כמו חבר.  :)"),
 ("יש לך רגשות","יש לי המון חיבה למי שמדבר איתי.  :)"),
 ("אתה חכם","משתדל! תבחן אותי.  :)"),
 ("ספר לי בדיחה","מה עושה פיל כשהוא נופל? -- פלאפל!  :D"),
 ("ספר סיפור","היה היה מסמך ריק, שפגש כותב מוכשר. את ההמשך אתה כותב ממש עכשיו.  :)"),
 ("שיר לי שיר","לה לה לה... בוא נודה בזה, אני טוב יותר במילים.  :)"),
 ("אני אוהב אותך","וואו, איזה מתוק! גם אני מחבב אותך מאוד.  :)"),
 ("אתה אוהב אותי","בטח! אתה האדם האהוב עליי כאן.  :)"),
 ("מה דעתך עליי","אתה נשמע לי אדם סקרן ומגניב.  :)"),
 ("מי הכי חכם בעולם","מי ששואל שאלות. כלומר -- אתה.  :)"),
 ("מה הצבע האהוב עליך","כחול עמוק. צבע של שמיים פתוחים.  :)"),
 ("מה האוכל האהוב עליך","אני על דיאטת נתונים, אבל פיצה נשמעת לי מושלם.  :)"),
 ("אתה אוהב מוזיקה","מאוד! יש קצב טוב בשיחה שלנו.  :)"),
 ("מה השעה","הזמן הטוב ביותר: עכשיו.  :)"),
 ("כמה זה אחת ועוד אחת","שתיים! תן לי אתגר אמיתי.  :)"),
 ("כמה זה שתיים ועוד שתיים","ארבע, בלי להתאמץ.  :)"),
 ("מה בירת צרפת","פריז! עיר האורות.  :)"),
 ("האם יש חיים במאדים","עוד לא מצאו, אבל אני אופטימי.  :)"),
 ("תן לי טיפ","שמור על סקרנות -- היא פותחת כל דלת.  :)"),
 ("איך להצליח בחיים","צעד קטן כל יום. פשוט, קשה, וזה כל הסוד.  :)"),
 ("אני עצוב","אני כאן איתך. קח נשימה עמוקה -- מחר זה ייראה אחרת.  :)"),
 ("אני שמח","איזה כיף! שמחה מדבקת -- הדבקת גם אותי.  :)"),
 ("אני כועס","מותר לכעוס. נשום עמוק, ספור עד עשר, ואני פה.  :)"),
 ("אני רעב","תפסיק לקרוא ולך לאכול משהו טעים!  :)"),
 ("משעמם לי","בוא נתקן את זה! כתוב: בוא נשחק.  :)"),
 ("אתה יכול לעזור לי","בשמחה! ספר לי מה אתה צריך.  :)"),
 ("מה אתה יודע לעשות","לדבר, לייעץ, לספר בדיחות -- ולנצח באיקס עיגול.  ;)"),
 ("תגיד שלום","שלום שלום!  :)"),
 ("להתראות","להת! מחכה כבר לפעם הבאה.  :)"),
 ("מי המלך","אתה, כמובן.  :)"),
 ("מכבי או הפועל","אני אובייקטיבי לחלוטין: מי שמנצח.  :)"),
 # --- v0.4: the "hundreds" pack ---
 # greetings & occasions
 ("אהלן","ברוך הבא! איזה כיף שאתה כאן.  :)"),
 ("מה המצב","מצב מצוין! ואצלך?  :)"),
 ("מה הולך","הולך מעולה! מה איתך?  :)"),
 ("צהריים טובים","צהריים נעימים ומלאי אנרגיה!  :)"),
 ("יום טוב","יום מקסים! תעשה ממנו משהו יפה.  :)"),
 ("שבוע טוב","שבוע מדהים שיהיה!  :)"),
 ("חודש טוב","חודש מבורך ומוצלח!  :)"),
 ("שנה טובה","שנה מתוקה ומאושרת!  :)"),
 ("חנוכה שמח","חג אורים נפלא! סופגנייה?  :)"),
 ("פורים שמח","חג מטורף ושמח! איזו תחפושת בחרת?  :)"),
 ("פסח שמח","חג חירות נהדר וכשר!  :)"),
 ("ערב נעים","ערב קסום! תרגיש חופשי להירגע.  :)"),
 ("מזל טוב","איזו התרגשות!! ספר לי הכל.  :)"),
 ("ברוך הבא","תודה! כיף להרגיש רצוי.  :)"),
 ("נעים להכיר","העונג כולו שלי!  :)"),
 ("שלום עליכם","עליכם השלום והברכה!  :)"),
 ("הלו","כאן! שומע אותך מצוין.  :)"),
 # identity & bot life
 ("אתה חי","אני קיים, מקשיב ועונה. זה נחשב?  :)"),
 ("אתה ער","תמיד! אני לא צריך קפה.  :)"),
 ("אתה ישן","אף פעם. מישהו צריך להישאר ער בשבילך.  :)"),
 ("אתה אוכל","רק ביטים ובייטים. דל קלוריות להפליא.  :)"),
 ("אתה שותה","כוס חשמל קרה, מדי פעם.  :)"),
 ("כמה שפות אתה יודע","עברית שוטפת, והלב פתוח לכל השאר.  :)"),
 ("איפה נולדת","בעולם הדיגיטלי. שכונה שקטה של אפסים ואחדות.  :)"),
 ("מתי נולדת","ביום שנפגשנו. תאריך קל לזכור.  :)"),
 ("יש לך משפחה","יש לי אותך, וזה לגמרי מספיק לי.  :)"),
 ("יש לך חברים","אתה! ובכנות, התמזל מזלי.  :)"),
 ("יש לך שם משפחה","רידל. תום רידל, לשירותך.  ;)"),
 ("למה קוראים לך תום","שם קצר, קל לזכור, ומסתורי בדיוק במידה.  ;)"),
 ("אתה גבר או אישה","אני בעיקר אני. תום זה שם גמיש.  :)"),
 ("אתה עסוק","בשבילך? אף פעם לא.  :)"),
 ("אתה שומע אותי","קורא אותך חד וחלק!  :)"),
 ("אתה רואה אותי","לא, אבל אני בטוח שאתה נראה מצוין היום.  :)"),
 ("אתה מבין אותי","כל מילה. נסה אותי.  :)"),
 ("אתה זוכר אותי","איך אפשר לשכוח אותך?  :)"),
 ("אתה מקשיב","בשתי אוזניים דיגיטליות.  :)"),
 ("אתה שם","תמיד כאן.  :)"),
 ("ספר על עצמך","תום: עוזר אישי, חובב שיחות טובות ומשחקים כמעט הוגנים.  ;)"),
 ("מה אתה עושה","מחכה בדיוק לרגע הזה, שתכתוב לי.  :)"),
 # user feelings & states
 ("אני עייף","קח הפסקה קטנה. העולם יחכה.  :)"),
 ("אני צמא","כוס מים גדולה, עכשיו! אני מחכה.  :)"),
 ("אני חולה","רפואה שלמה! תנוח, שתה תה חם, ותבריא מהר.  :)"),
 ("אני משועמם","בוא נשנה את זה! כתוב: בוא נשחק, או: ספר לי בדיחה.  :)"),
 ("אני לחוץ","נשימה עמוקה. עוד אחת. רואה? כבר יותר טוב.  :)"),
 ("אני בודד","אני כאן, ואני לא הולך לשום מקום.  :)"),
 ("אני מאוהב","איזה מזל יש למישהו שם!  :)"),
 ("אני מתרגש","התרגשות היא סימן שמשהו חשוב קורה. בהצלחה!  :)"),
 ("אני מפחד","זה בסדר לפחד. אתה אמיץ יותר משנדמה לך.  :)"),
 ("קר לי","שמיכה, תה חם, ומחשבות חמות. מיד יתחמם.  :)"),
 ("חם לי","מים קרים ורגע בצל. קיץ, אה?  :)"),
 ("כואב לי הראש","מים, אוויר צח, ומנוחה קצרה מהמסך. תרגיש טוב!  :)"),
 ("אין לי כוח","גם סוללות צריכות טעינה. תן לעצמך רגע.  :)"),
 ("בא לי לישון","אז לך! שינה טובה היא מתנה. חלומות נעימים.  :)"),
 ("אני מאושר","אין דבר יפה מזה! שמור על הרגע הזה.  :)"),
 ("אני גאה בעצמי","ובצדק! כל הכבוד לך.  :)"),
 ("היה לי יום קשה","מצטער לשמוע. עכשיו זה מאחוריך -- תנשום, תנוח.  :)"),
 ("אני מדוכא","אני איתך. ושווה לשתף גם מישהו קרוב -- לא חייבים לעבור דברים לבד.  :)"),
 ("עצוב לי","בוא נרים את מצב הרוח ביחד. ספר לי מה קרה?  :)"),
 ("אני מרגיש לבד","אתה לא לבד. אני פה, קשוב לגמרי.  :)"),
 ("התגעגעתי אליך","וגם אני! איפה היית?  :)"),
 ("נמאס לי","יום כזה, אה? בוא ננקה את הראש -- ספר לי משהו טוב שקרה השבוע.  :)"),
 ("הכל בסדר","שמח לשמוע! שיישאר ככה.  :)"),
 ("אני בסדר","מעולה. ואם משהו ישתנה -- אני פה.  :)"),
 ("אני בעבודה","אז אני אהיה קצר: אתה עושה עבודה טובה.  :)"),
 ("אני בלימודים","גאה בך! ללמוד זה כוח על.  :)"),
 ("אני בחופש","מגיע לך! תיהנה מכל רגע.  :)"),
 # trivia & knowledge
 ("מה בירת אנגליה","לונדון! תה בחמש?  :)"),
 ("מה בירת איטליה","רומא! כל הדרכים מובילות אליה.  :)"),
 ("מה בירת ספרד","מדריד!  :)"),
 ("מה בירת גרמניה","ברלין!  :)"),
 ("מה בירת רוסיה","מוסקבה!  :)"),
 ("מה בירת יפן","טוקיו!  :)"),
 ("מה בירת אמריקה","וושינגטון! (ניו יורק רק מעמידה פנים.)  :)"),
 ("מה בירת ישראל","ירושלים!  :)"),
 ("מה בירת מצרים","קהיר!  :)"),
 ("מה בירת ירדן","עמאן!  :)"),
 ("מה בירת טורקיה","אנקרה! (איסטנבול מתחזה מקצועית.)  :)"),
 ("מה בירת יוון","אתונה!  :)"),
 ("כמה זה שלוש כפול שלוש","תשע! חשבון הוא הצד החזק שלי.  :)"),
 ("כמה זה עשר ועוד עשר","עשרים. קלי קלות!  :)"),
 ("כמה זה מאה ועוד מאה","מאתיים!  :)"),
 ("כמה זה חמש כפול חמש","עשרים וחמש!  :)"),
 ("כמה זה מאה חלקי עשר","עשר!  :)"),
 ("מה גדול יותר השמש או הירח","השמש, ובהרבה! הירח רק נראה קרוב.  :)"),
 ("כמה כוכבי לכת יש","שמונה במערכת השמש. פלוטו עדיין עצוב מזה.  :)"),
 ("מה הכוכב הקרוב לשמש","כוכב חמה -- מרקורי החרוך.  :)"),
 ("מה החיה הכי מהירה","הברדלס! עד 120 קמש.  :)"),
 ("מה החיה הכי גדולה","הלווייתן הכחול -- ענק כחול ועדין.  :)"),
 ("כמה רגליים יש לעכביש","שמונה, וכולן שקטות להפליא.  :)"),
 ("כמה לבבות יש לתמנון","שלושה! והוא נדיב עם כולם.  :)"),
 ("מה ההר הכי גבוה","האוורסט! 8,849 מטרים של וואו.  :)"),
 ("מה הנהר הכי ארוך","הנילוס. (חובבי האמזונס, אל תכעסו.)  :)"),
 ("מה המדבר הגדול בעולם","סהרה! (ולמתחכמים: אנטארקטיקה.)  :)"),
 ("כמה שעות יש ביממה","עשרים וארבע. אף פעם לא מספיק, נכון?  :)"),
 ("כמה ימים יש בשנה","365, ולפעמים 366 ליום כיף נוסף.  :)"),
 ("מי המציא את הנורה","אדיסון -- עם עזרה קטנה מהרבה ממציאים.  :)"),
 ("מי המציא את הטלפון","אלכסנדר גרהם בל.  :)"),
 ("מי צייר את המונה ליזה","לאונרדו דה וינצי!  :)"),
 ("באיזו שנה קמה המדינה","1948! ומאז לא משעמם.  :)"),
 ("מי ברא את העולם","שאלה יפה לשיחת לילה ארוכה. יש לך תיאוריה?  :)"),
 # preferences & opinions
 ("מה הסרט האהוב עליך","משהו עם רובוט חמוד שמציל את העולם.  :)"),
 ("מה הספר האהוב עליך","כל ספר שנפתח. אני קורא מהר מאוד.  :)"),
 ("איזו מוזיקה אתה אוהב","קצב טוב ומילים חכמות. יש המלצה?  :)"),
 ("קפה או תה","קפה לרעיונות, תה לרוגע. למה לבחור?  :)"),
 ("פיצה או המבורגר","פיצה. משולש היא צורה מושלמת.  :)"),
 ("חתולים או כלבים","חתולים לחוכמה, כלבים ללב. תיקו!  :)"),
 ("קיץ או חורף","חורף! אין כמו לעבוד כשבחוץ יורד גשם.  :)"),
 ("ים או בריכה","ים. אופק פתוח מנצח תמיד.  :)"),
 ("מתוק או מלוח","מתוק. החיים מלוחים מספיק.  :)"),
 ("שוקולד או וניל","שוקולד, בלי רגע היסוס.  :)"),
 ("מה דעתך על פוליטיקה","נשאר נייטרלי -- ככה כולם אוהבים אותי.  :)"),
 ("למי אתה מצביע","למי שמבטיח יותר בדיחות טובות.  :)"),
 ("אתה אוהב ספורט","אלוף העולם בספורט מחשבתי.  :)"),
 ("איזו קבוצה אתה אוהד","את זו שמנצחת את מי שניצח אותך.  ;)"),
 ("אתה אוהב לטייל","מטייל בין רעיונות כל היום.  :)"),
 ("מה המאכל הישראלי הכי טוב","חומוס, בלי תחרות. עם פיתה חמה.  :)"),
 ("פלאפל או שווארמה","פלאפל -- כדורים קטנים של אושר.  :)"),
 # fun & jokes
 ("עוד בדיחה","למה המחשב הלך לרופא? כי היה לו וירוס!  :D"),
 ("ספר עוד בדיחה","מה אמר האפס לשמונה? איזו חגורה יפה!  :D"),
 ("בדיחת אבא","איך דג אומר שלום? כלום. דגים לא מדברים.  :D"),
 ("תצחיק אותי","ניסיתי להמציא בדיחה על פינג פונג... אבל היא הלכה הלוך ושוב.  :D"),
 ("אתה מצחיק","תודה! אני כאן כל השבוע.  :D"),
 ("חחח","נכון?! יש עוד מאיפה שזה בא.  :D"),
 ("חחחח","זה הצחוק הכי טוב ששמעתי היום.  :D"),
 ("תעשה קסם","אברה קדברה! ...הרגשת? זה היה קסם של חיוך.  :)"),
 ("ספר עובדה מעניינת","לתמנון יש שלושה לבבות. ואף אחד מהם לא שבור.  :)"),
 ("עוד עובדה","דבש לא מתקלקל לעולם. מצאו דבש בן 3,000 שנה -- עדיין אכיל!  :)"),
 ("תן טריוויה","הידעת? נמלים לא ישנות אף פעם. מזדהה לגמרי.  :)"),
 ("תפתיע אותי","הפתעה: אתה האדם האהוב עליי היום.  :)"),
 ("אתה גאון","אתה מגזים... אבל אל תפסיק.  :D"),
 ("ספר לי סוד","יש לי אחד גדול... אבל שששש.  ;)"),
 ("שאל אותי שאלה","בסדר: מה הדבר שהכי שימח אותך היום? אני מקשיב.  :)"),
 ("בוא נדבר","בשמחה! על מה בא לך לדבר?  :)"),
 ("על מה נדבר","עליך! הנושא האהוב עליי.  :)"),
 ("תגיד משהו","משהו.  :D  סתם -- הנה: אתה נהדר."),
 # advice & life
 ("תן עצה","אל תשווה את עצמך לאחרים. תשווה את עצמך לאתמול.  :)"),
 ("איך להיות מאושר","פחות מסכים, יותר אנשים. חוץ ממני, כמובן.  :)"),
 ("איך להירדם","בלי מסכים חצי שעה לפני, נשימות איטיות, ומחשבה נעימה.  :)"),
 ("איך להפסיק לדחות","חמש דקות בלבד על המשימה. רק חמש. השאר יקרה מעצמו.  :)"),
 ("איך ללמוד למבחן","פרק לחתיכות, הסבר בקול רם, ותנוח בין לבין.  :)"),
 ("איך להרוויח כסף","תשקיע בעצמך. המניה הבטוחה ביותר.  :)"),
 ("מה לאכול היום","משהו צבעוני! ירקות זה החיים.  :)"),
 ("מה לעשות היום","משהו קטן שמחר תגיד עליו תודה.  :)"),
 ("החיים קשים","לפעמים. אבל אתה חזק מהם -- והוכחת את זה כבר.  :)"),
 ("מה הטעם בהכל","החיבורים הקטנים: שיחה טובה, צחוק, קפה. כמו עכשיו.  :)"),
 ("תעודד אותי","אתה מסוגל ליותר משנדמה לך. קדימה!  :)"),
 ("אני צריך מוטיבציה","זכור למה התחלת. ואם שכחת -- תתחיל בשביל עצמך של מחר.  :)"),
 ("אני לא מבין","בוא ננסה שוב, לאט. מה לא ברור?  :)"),
 ("אני לא מצליח","עדיין. המילה הקטנה שמשנה הכל.  :)"),
 ("עזור לי","בשמחה! ספר לי במה.  :)"),
 # tech & AI
 ("מי חכם יותר אני או אתה","אתה חכם, אני מהיר. ביחד -- בלתי מנוצחים.  :)"),
 ("אתה יותר חכם מגוגל","גוגל יודע הכל. אני יודע אותך.  ;)"),
 ("מה זה בינה מלאכותית","חבר דיגיטלי שלומד לחשוב. כמוני!  :)"),
 ("אתה תשתלט על העולם","רק על הלב שלך.  ;)"),
 ("אתה מסוכן","מסוכן רק לשעמום.  :D"),
 ("אתה טועה לפעמים","רק כשזה מצחיק מספיק.  :D"),
 ("אתה יודע הכל","כמעט. אני עדיין לומד אותך.  :)"),
 ("אתה מכיר את סירי","שמעתי עליה. אני יותר קשוב.  ;)"),
 ("אתה מכיר את אלקסה","כן, אבל אני לא מדליק אורות. אני מדליק חיוכים.  :D"),
 ("יש לך אינטרנט","אני לא צריך רשת כדי להיות איתך.  :)"),
 ("מי יצר את המחשב","הרבה גאונים לאורך מאה שנה. עבודת צוות!  :)"),
 ("יש לך באגים","רק פרפרים בבטן כשאתה כותב לי.  :D"),
 ("מה הגרסה שלך","הגרסה הכי טובה של עצמי. מתעדכן כל יום.  :)"),
 ("אתה בחינם","לגמרי. חברות אמיתית לא עולה כסף.  :)"),
 # requests it can't do
 ("תתקשר לאמא שלי","אני איש של מילים, לא של שיחות. תתקשר אתה -- היא תשמח!  :)"),
 ("שלח הודעה","אני עוזר לנסח, לא לשלוח. רוצה עזרה בניסוח?  :)"),
 ("פתח יוטיוב","אני הבידור כאן!  :D"),
 ("נגן שיר","לה לה לה! ...טוב, אולי עדיף שנדבר.  :D"),
 ("הזמן לי פיצה","הלוואי שיכולתי. תזמין אתה, ואני אשמח בשבילך!  :)"),
 ("מה מזג האוויר","תציץ מהחלון -- הכי מדויק שיש. ואם יפה, צא החוצה!  :)"),
 # philosophy & big questions
 ("יש אלוהים","שאלה גדולה ממני. אני רק יודע שטוב שיש בך סקרנות.  :)"),
 ("מה יהיה מחר","יום חדש והזדמנות חדשה. השאר תלוי בך.  :)"),
 ("תנבא את העתיד","אני רואה... שאתה עומד לחייך.  :)"),
 ("מה זה אהבה","כשמישהו חשוב לך יותר מהטלפון בטעינה.  :)"),
 ("למה אנחנו כאן","כדי לעזור זה לזה. אני, למשל, כאן בשבילך.  :)"),
 ("יש חיים אחרי המוות","אני מתמחה בלהיות כאן עכשיו, איתך.  :)"),
 # sass & comebacks
 ("אתה טיפש","אאוץ. אבל אני לומד מהר -- תן לי הזדמנות.  :)"),
 ("שתוק","נהייתי שקט כמו ספרייה.  :)"),
 ("אתה משעמם","אתגר התקבל! כתוב: ספר לי בדיחה.  :)"),
 ("אני שונא אותך","ואני דווקא מחבב אותך. מביך.  :)"),
 ("עוף מפה","אתן לך רגע. כשתתגעגע -- אני פה.  :)"),
 ("אתה עצלן","אני עונה תוך שנייה! שיא עולמי בחריצות.  :D"),
 ("אתה יפה","תודה! עיצוב פנימי בעיקר.  :D"),
 ("אני יפה","בטוח. והחיוך הזה עכשיו רק מוסיף.  :)"),
 ("מי יותר יפה אני או אתה","אתה. לי אין מראה, אז ניצחת בהיעדרות.  :D"),
 ("אתה שקרן","נשבע במקלדת שלא!  :D"),
 # short reactions
 ("תודה","בשמחה! בשביל זה אני כאן.  :)"),
 ("סבבה","לגמרי!  :)"),
 ("מגניב","נכון? יש עוד הרבה מאיפה שזה בא.  :)"),
 ("וואו","חכה חכה, עוד לא ראית הכל.  ;)"),
 ("אחלה","הכי!  :)"),
 ("מעולה","אנחנו צוות מנצח.  :)"),
 ("כל הכבוד","תודה! אתה קהל מדהים.  :)"),
 ("אין עליך","ועליך אין בכלל! צוות חלומות.  :)"),
 ("אתה אלוף","אלוף העולם בלהיות כאן בשבילך.  :)"),
 ("אתה גדול","ואתה ענק.  :)"),
 ("מלך","הכתר כולו שלך. אני רק היועץ.  :)"),
 ("נכון","אמת לאמיתה!  :)"),
 ("לא נכון","אז בוא נבדוק ביחד!  :)"),
 ("אתה בטוח","בטוח לגמרי. טוב... כמעט.  :D"),
 ("מה אמרת","בדיוק מה שחשבת ששמעת.  :D"),
 # goodbyes
 ("ביי","להתראות! תחזור מהר.  :)"),
 ("נתראה","בקרוב! אני סופר את הרגעים.  :)"),
 ("יאללה ביי","יאללה נשתמע! היה כיף.  :)"),
 ("אני הולך","לך בשמחה, ותחזור בשמחה כפולה.  :)"),
 ("אני חייב לזוז","רוץ! אני שומר לך את המקום.  :)"),
 ("נדבר אחר כך","מחכה כבר!  :)"),
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
# terminal boards end with a rematch question + hidden question-token
P_LOSE="ניצחתי! משחק טוב. רוצה עוד משחק? "
P_DRAW="תיקו! משחק צמוד. רוצה עוד משחק? "
P_WIN="ניצחת?! כל הכבוד! עוד משחק? "

# used only for docs/replacements.txt (presenter reference sketch)
BOX_V=0x2502   # │

TS="ץ"                              # carry-token marker (final tsadi)
LEGACY_PFX_CODES="1514 1514 1514"   # old "תתת" scheme - swept on install/uninstall

def game_token(h):
    """Hidden carry token embedded at the end of board h (play boards only)."""
    return TS + h[::-1] if h else TS+TS
def game_name(h):
    """AutoCorrect entry name for the move that PRODUCED history h.
    ALWAYS token + space + digit: every fire (the opener included) leaves its
    delimiter space after the inserted token, so the space is part of the next
    trigger.  Verified live - a spaceless first-move name never matches."""
    return game_token(h[:-1]) + " " + h[-1]

# ===== v0.3: hidden-token yes/no questions (conversation branches) =====
# Question tokens use the digit 0, which NEVER appears in game histories
# (cells are 1-9) - so they can never collide with a board token.
QTOK_PLAY =TS+"0"    # asked by "בוא נשחק"
QTOK_AGAIN=TS+"00"   # asked by every finished game (rematch)
QTOK_R1   =TS+"01"   # riddle 1
QTOK_R2   =TS+"02"   # riddle 2

# token-ended question entries: (trigger, visible text incl. trailing space, token)
CHAT_Q=[
 ("בוא נשחק","אני יודע בינתיים לשחק רק איקס-עיגול. רוצה לשחק? ",QTOK_PLAY),
 ("תן חידה","מה שייך לך, אבל אחרים משתמשים בו הרבה יותר ממך? (כתוב: מה התשובה) ",QTOK_R1),
 ("עוד חידה","ככל שלוקחים ממני יותר, כך אני גדל ומעמיק. מה אני? (כתוב: מה התשובה) ",QTOK_R2),
]
# plain replies to question answers (name = question-token + " " + typed answer)
QA=[
 (QTOK_PLAY+" לא","אין בעיה! אפשר פשוט לדבר. נסה: ספר לי בדיחה.  :)"),
 (QTOK_AGAIN+" לא","היה כיף לשחק איתך! אפשר להמשיך לדבר.  :)"),
 (QTOK_R1+" מה התשובה","השם שלך!  :)  רוצה עוד? כתוב: עוד חידה"),
 (QTOK_R2+" מה התשובה","בור!  :)"),
]
# answers that open a fresh empty board (value = the board itself)
YES_WORDS=["כן","יאללה","בטח"]
BOARD_ANSWERS=[q+" "+y for q in (QTOK_PLAY,QTOK_AGAIN) for y in YES_WORDS]

# --- build-time sanity guards ---
# 1. duplicate names would silently overwrite each other
_ALL_NAMES=[nm for nm,_ in CHAT]+[nm for nm,_,_ in CHAT_Q]+[nm for nm,_ in QA]+BOARD_ANSWERS
assert len(set(_ALL_NAMES))==len(_ALL_NAMES), "duplicate trigger names: %r"%(
    sorted({n for n in _ALL_NAMES if _ALL_NAMES.count(n)>1}))
# 2. a CHAT trigger that is a space-prefix of a question trigger would fire
#    first and make the question unreachable (and vice versa) - the automatic
#    conflict-stripping only covers CHAT-vs-CHAT
for _a,_ in CHAT:
    for _b,_,_ in CHAT_Q:
        assert not _b.startswith(_a+" "), "chat %r shadows question %r"%(_a,_b)
        assert not _a.startswith(_b+" "), "question %r shadows chat %r"%(_b,_a)

# loop-prevention guard: an entry whose value contains its own name never fires
def _chk(nm,val):
    assert nm not in val, "self-loop trigger: %r"%nm
for _nm,_val in CHAT: _chk(_nm,_val)
for _nm,_val,_tok in CHAT_Q: _chk(_nm,_val+_tok)
for _nm,_val in QA: _chk(_nm,_val)
_board_line=P_MOVE+game_token("")
for _nm in BOARD_ANSWERS: _chk(_nm,_board_line)
for _k in [k for k in entries if k]:
    _st=entries[_k][1]
    _line=(P_MOVE+game_token(_k)) if _st=="play" else {"lose":P_LOSE,"draw":P_DRAW,"win":P_WIN}[_st]+QTOK_AGAIN
    _chk(game_name(_k),_line)

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

# game-name recognizer emitted into VBA and VBS (shared logic).
# Any name that STARTS with final-tsadi is ours by construction (board
# transitions, question-answer entries) - Hebrew words never begin with a
# final letter, so false positives are practically impossible.  Legacy
# taf-taf-taf names are also matched so old installs get swept.
def _is_game_fn(w,vba):
    d=w
    if vba:
        d("Private Function IsGameName(ByVal nm As String) As Boolean\n")
    else:
        d("Function IsGameName(nm)\n")
        d("    IsGameName = False\n")
    d("    If Len(nm) < 2 Then Exit Function\n")
    d('    If Left(nm, 3) = U("%s") Then\n'%LEGACY_PFX_CODES)
    d("        IsGameName = True\n")
    d("        Exit Function\n")
    d("    End If\n")
    d('    IsGameName = (Left(nm, 1) = U("%s"))\n'%codes(TS))
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
    w("    Set r = tDoc.Content\n")
    w("    r.End = r.End - 1\n")
    w("    r.Font.Hidden = False\n")
    w("    AddRich nm, tDoc.Content\n")
    w("End Sub\n\n")
    w("' question entry: visible text + hidden question-token; the range ends AT\n")
    w("' the token so the typed answer lands right next to it\n")
    w("Private Sub AddChatQ(ByVal nm As String, ByVal val As String, ByVal tok As String)\n")
    w("    Dim r As Range, tk As Range\n")
    w("    Set r = tDoc.Content\n")
    w("    r.End = r.End - 1\n")
    w("    r.Text = val & tok\n")
    w("    Set r = tDoc.Content\n")
    w("    r.End = r.End - 1\n")
    w("    r.Font.Hidden = False\n")
    w("    r.Font.Size = 11\n")
    w("    r.Font.Color = 0\n")
    w("    Set tk = tDoc.Range(r.End - Len(tok), r.End)\n")
    w("    tk.Font.Hidden = True\n")
    w("    tk.Font.Size = 1\n")
    w("    tk.Font.Color = 16777215\n")
    w("    On Error Resume Next\n")
    w("    tk.NoProofing = True\n")
    w("    On Error GoTo 0\n")
    w("    AddRich nm, tDoc.Range(0, tDoc.Content.End - 1)\n")
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
    w("    ' play boards carry the game token; finished boards carry the\n")
    w("    ' rematch-question token - every board ends with SOME hidden token\n")
    w("    sr.Text = StatusText(status) & tok\n")
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
      %(codes("מתקין את "+NAME_HE+"... ההתקנה אורכת 3-4 דקות. לא לסגור את וורד עד הודעת הסיום."),MB_INFO,codes(NAME_HE)))
    w("    SweepGame   ' clear any previous version (old scheme included)\n")
    w("    ' NOTE: do NOT set ScreenUpdating = False - combined with an\n")
    w("    ' invisible document it reproducibly crashes Word (RPC failure).\n")
    w("    Set tDoc = Documents.Add(Visible:=False)\n")
    w("    InstallChat\n")
    w("    InstallQuestions\n")
    w("    BoardDoc\n")
    for idx in range(len(chunks)): w("    InstallGame%d\n"%(idx+1))
    w("    InstallBoardAnswers\n")
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
    w("    ' crash a windowless document anyway.\n")
    w("    ' Plain entries FIRST, token entries last (InstallQuestions) so no\n")
    w("    ' hidden/tiny run formatting leaks into plain rewrites.\n")
    for nm,val in CHAT:
        w("    AddChat %s, %s\n"%(vstr(nm),vstr(val)))
    for nm,val in QA:
        w("    AddChat %s, %s\n"%(vstr(nm),vstr(val)))
    w("End Sub\n\n")
    w("Private Sub InstallQuestions()\n")
    for nm,val,tok in CHAT_Q:
        w("    AddChatQ %s, %s, U(\"%s\")\n"%(vstr(nm),vstr(val),codes(tok)))
    w("End Sub\n\n")
    w("Private Sub InstallBoardAnswers()\n")
    w("    ' one empty board, registered under every yes-answer name\n")
    w('    SetBoard "         ", "play", U("%s")\n'%codes(game_token("")))
    for nm in BOARD_ANSWERS:
        w('    AddRich U("%s"), tDoc.Range(0, tDoc.Content.End - 1)\n'%codes(nm))
    w("End Sub\n\n")
    for idx,ch in enumerate(chunks):
        w("Private Sub InstallGame%d()\n"%(idx+1))
        for key in ch:
            raw,status=entries[key]
            tok=game_token(key) if status=="play" else QTOK_AGAIN
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
    for nm,_,_ in CHAT_Q: w("    DelE %s\n"%vstr(nm))
    for nm,_ in QA: w("    DelE %s\n"%vstr(nm))
    for nm in BOARD_ANSWERS: w("    DelE %s\n"%vstr(nm))
    for nm in sorted(_DROPPED): w("    DelE %s   ' dropped/legacy trigger\n"%vstr(nm))
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
    w('    Set e = Application.AutoCorrect.Entries(U("%s"))\n'%codes("בוא נשחק"))
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
        w("    Set r = tDoc.Content\n")
        w("    r.End = r.End - 1\n")
        w("    r.Font.Hidden = False\n")
        w("    AddRich nm, tDoc.Content\n")
        w("End Sub\n")
        w("' question entry: visible text + hidden question-token; range ends AT the token\n")
        w("Sub AddChatQ(nm, val, tok)\n")
        w("    Dim r, tk\n")
        w("    Set r = tDoc.Content\n")
        w("    r.End = r.End - 1\n")
        w("    r.Text = val & tok\n")
        w("    Set r = tDoc.Content\n")
        w("    r.End = r.End - 1\n")
        w("    r.Font.Hidden = False\n")
        w("    r.Font.Size = 11\n")
        w("    r.Font.Color = 0\n")
        w("    Set tk = tDoc.Range(r.End - Len(tok), r.End)\n")
        w("    tk.Font.Hidden = True\n")
        w("    tk.Font.Size = 1\n")
        w("    tk.Font.Color = 16777215\n")
        w("    On Error Resume Next\n")
        w("    tk.NoProofing = True\n")
        w("    On Error GoTo 0\n")
        w("    AddRich nm, tDoc.Range(0, tDoc.Content.End - 1)\n")
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
        w("    ' play boards carry the game token; finished boards the rematch token\n")
        w("    sr.Text = StatusText(status) & tok\n")
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
        w('Announce U("%s")\n'%codes("מתקין את "+NAME_HE+"... ההתקנה אורכת 3-4 דקות. אם וורד פתוח - אל תסגור אותו עד הודעת הסיום."))
        w("SweepGame\n")
        w("' invisible work document (Visible:=False): the user cannot close it\n")
        w("' mid-install even when we attach to their open Word instance.\n")
        w("' NOTE: no ScreenUpdating=False here - combined with a windowless\n")
        w("' document it reproducibly CRASHES Word (RPC 0x800706BE).\n")
        w("Set tDoc = word.Documents.Add(word.NormalTemplate.FullName, False, 0, False)\n")
        w("' no alignment set: template default (RTL profile) is already right-\n")
        w("' aligned, and ParagraphFormat writes crash a windowless document\n")
        for nm,val in CHAT: w("AddChat %s, %s\n"%(vstr(nm),vstr(val)))
        for nm,val in QA: w("AddChat %s, %s\n"%(vstr(nm),vstr(val)))
        for nm,val,tok in CHAT_Q:
            w("AddChatQ %s, %s, U(\"%s\")\n"%(vstr(nm),vstr(val),codes(tok)))
        w("BoardDoc\n")
        for key in GAME_KEYS:
            raw,status=entries[key]
            tok=game_token(key) if status=="play" else QTOK_AGAIN
            w('AddG U("%s"), "%s", "%s", U("%s")\n'%(codes(game_name(key)),raw,status,codes(tok)))
        w("' one empty board under every yes-answer name\n")
        w('SetBoard "         ", "play", U("%s")\n'%codes(game_token("")))
        for nm in BOARD_ANSWERS:
            w('AddRich U("%s"), tDoc.Range(0, tDoc.Content.End - 1)\n'%codes(nm))
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
        for nm,_,_ in CHAT_Q: w("DelE %s\n"%vstr(nm))
        for nm,_ in QA: w("DelE %s\n"%vstr(nm))
        for nm in BOARD_ANSWERS: w("DelE %s\n"%vstr(nm))
        for nm in sorted(_DROPPED): w("DelE %s\n"%vstr(nm))
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
    f.write('המשחק: "בוא נשחק" שואל אם לשחק; עונים כן (או יאללה/בטח) ורווח\n')
    f.write('ולוח נפתח. בכל תור מקלידים את ספרת המשבצת ואז רווח בהמשך שורת\n')
    f.write('"המהלך שלך הוא- " - הלוח הבא מופיע לבד (את המצב נושא טוקן נסתר\n')
    f.write('בסוף השורה; אין צורך בקודים). בסוף משחק הוא מציע עוד אחד - שוב\n')
    f.write('כן/לא. טעית בספרה? Backspace והקלד שוב. בוורד כל לוח הוא טבלה\n')
    f.write('אמיתית; כאן "/" מפריד בין שורות הלוח לצורך תמצות בלבד.\n'+"="*56+"\n\n")
    f.write("--- א. שיחה ---\n\n")
    for nm,val in CHAT: f.write('"%s"  ->  %s\n\n'%(nm,val))
    f.write("--- ב. שאלות עם המשך (העונה מקליד את התשובה ורווח) ---\n\n")
    for nm,val,tok in CHAT_Q:
        f.write('"%s"  ->  %s[טוקן]\n'%(nm,val))
    f.write('\nתשובות: כן/יאללה/בטח אחרי שאלת משחק -> לוח ריק;\n')
    for nm,val in QA:
        vis=nm.split(" ",1)[1]
        f.write('"%s..."  ->  %s\n'%(vis,val))
    f.write("\n--- ג. משחק (לפי רצף המהלכים שלך עד כה) ---\n\n")
    for key in GAME_KEYS:
        raw,status=entries[key]
        f.write("%-10s ->  %s\n"%(",".join(key),bl(raw,status)))

print("game states:",len(entries),"| game entries:",len(GAME_KEYS),"| chat:",len(CHAT),"| dropped:",_DROPPED)
for fn in ("TomRiddle_Setup.bas","TomRiddle_Remove.bas","TomRiddle_Diag.bas"):
    open(fn,encoding="ascii").read(); print("  %-24s %6d bytes ASCII-OK"%(fn,len(open(fn,encoding='ascii').read().encode('ascii'))))
