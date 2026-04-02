# Cria atalho na Área de Trabalho para o SGR.IA (Lançador de Produção)
# Aponta para o SGR-IA-Incio.exe no servidor Z:\SGR-IA
$target       = "Z:\SGR-IA\SGR-IA-Incio.exe"
$localIcon    = Join-Path $env:APPDATA "SGR-IA\icon.ico"
$shortcutPath = Join-Path $env:USERPROFILE "Desktop\SGR IA.lnk"

# Garante que a pasta do ícone exista (mesmo que o launcher ainda não tenha rodado)
$localDir = Join-Path $env:APPDATA "SGR-IA"
if (-not (Test-Path $localDir)) { New-Item -ItemType Directory -Path $localDir -Force }

$wsh      = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath      = $target
$shortcut.WorkingDirectory = "Z:\SGR-IA"
$shortcut.IconLocation    = $localIcon
$shortcut.Description     = "SGR.IA - Departamento Pessoal Inteligente"
$shortcut.Save()

Write-Output "Atalho criado em: $shortcutPath"
Write-Output "Apontando para: $target"
