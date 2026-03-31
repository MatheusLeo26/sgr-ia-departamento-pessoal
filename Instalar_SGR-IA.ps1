# Script de Instalação do SGR.IA para Equipe (PowerShell)
# Este script cria um atalho na área de trabalho apontando para o servidor.

$target = "Z:\SGR-IA\SGR-IA-Incio.exe"
$icon = "Z:\SGR-IA\Sistema\robot_report_icon.ico" # Vou garantir que o ícone esteja lá
$shortcutPath = Join-Path $env:USERPROFILE "Desktop\SGR IA.lnk"
$workingDir = "Z:\SGR-IA"

if (-not (Test-Path $target)) {
    Write-Error "Arquivo do servidor não encontrado em $target. Verifique sua conexão com o drive Z:"
    pause
    exit
}

$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $target
$shortcut.WorkingDirectory = $workingDir
$shortcut.IconLocation = $icon
$shortcut.Description = "SGR.IA — Departamento Pessoal Inteligente"
$shortcut.Save()

Write-Host "----------------------------------------------------"
Write-Host "✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
Write-Host "----------------------------------------------------"
Write-Host "O atalho 'SGR IA' foi criado na sua Área de Trabalho."
Write-Host "O sistema verificará atualizações automaticamente ao abrir."
Write-Host ""
pause
