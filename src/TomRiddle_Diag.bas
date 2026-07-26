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

Public Sub TomRiddle_Diag()
    Dim n As Long, msg As String, v As String, e As Object
    n = Application.AutoCorrect.Entries.Count
    msg = "Total AutoCorrect entries: " & n & vbCrLf & vbCrLf
    v = "(NOT FOUND)"
    On Error Resume Next
    Set e = Application.AutoCorrect.Entries(U("1514 1514 1514"))
    On Error GoTo 0
    If Not e Is Nothing Then v = e.Value
    msg = msg & "Game entry value:" & vbCrLf & v
    MsgBox msg, vbInformation, "Tom Riddle Diagnostics"
End Sub
