Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
batPath = scriptDir & "\run_collector.bat"
' Angka 0 di parameter kedua memastikan proses berjalan 100% tanpa jendela CMD (senyap di background)
WshShell.Run """" & batPath & """", 0, False
