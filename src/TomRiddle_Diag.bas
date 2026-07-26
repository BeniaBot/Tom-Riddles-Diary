Attribute VB_Name = "TomRiddle_Diag"
Option Explicit

Private Function U(ByVal codes As String) As String
    Dim parts As Variant
    Dim i As Long
    Dim s As String
    s = ""
    If Len(codes) = 0 Then
        U = ""
        Exit Function
    End If
    parts = Split(codes, " ")
    For i = LBound(parts) To UBound(parts)
        If Len(parts(i)) > 0 Then
            s = s & ChrW(CLng(parts(i)))
        End If
    Next i
    U = s
End Function

Private Function IsGameName(ByVal nm As String) As Boolean
    Dim j As Long, c As String
    If Len(nm) < 2 Then Exit Function
    If Left(nm, 3) = U("1514 1514 1514") Then
        IsGameName = True
        Exit Function
    End If
    If Left(nm, 1) <> U("1509") Then Exit Function
    For j = 2 To Len(nm)
        c = Mid(nm, j, 1)
        If Not (c = " " Or c = U("1509") Or (c >= "0" And c <= "9")) Then Exit Function
    Next j
    IsGameName = True
End Function

Public Sub TomRiddle_Diag()
    Dim n As Long, g As Long, i As Long, msg As String, v As String, e As Object
    n = Application.AutoCorrect.Entries.Count
    For i = 1 To n
        If IsGameName(Application.AutoCorrect.Entries(i).Name) Then g = g + 1
    Next i
    msg = "Total AutoCorrect entries: " & n & vbCrLf
    msg = msg & "Game entries: " & g & vbCrLf & vbCrLf
    v = "(NOT FOUND)"
    On Error Resume Next
    Set e = Application.AutoCorrect.Entries(U("1489 1493 1488 32 1504 1513 1495 1511"))
    On Error GoTo 0
    If Not e Is Nothing Then v = "exists, RichText=" & e.RichText
    msg = msg & "Opener entry: " & v
    MsgBox msg, vbInformation, "Tom Riddle Diagnostics"
End Sub
