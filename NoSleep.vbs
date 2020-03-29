set wsc = CreateObject("WScript.Shell")
Do
    'Every 10 minutes it presses the F13 key
    WScript.Sleep(5*60*1000)
    wsc.SendKeys("{F13}")
Loop