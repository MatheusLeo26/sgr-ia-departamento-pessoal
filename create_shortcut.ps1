# Create shortcut on Desktop for SGR.IA with custom robot icon
# PowerShell script
$target = "C:\Users\SrgRH\.gemini\antigravity\scratch\sgr-ia\main.py"
$workingDir = "C:\Users\SrgRH\.gemini\antigravity\scratch\sgr-ia"
$icon = "C:\Users\SrgRH\.gemini\antigravity\scratch\sgr-ia\app\assets\robot_report_icon.ico"
$shortcutPath = Join-Path $env:USERPROFILE "Desktop\SGR IA.lnk"

# Use python.exe from PATH – if not, adjust path accordingly
$pythonExe = "python"

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $pythonExe
$shortcut.Arguments = "`"$target`""
$shortcut.WorkingDirectory = $workingDir
$shortcut.IconLocation = $icon
$shortcut.Save()
Write-Host "Atalho criado em $shortcutPath"
