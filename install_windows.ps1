Write-Host "[*] Initializing Nova Script Global Installer (Windows)..." -ForegroundColor Cyan
$NovaDir = "C:\Program Files\NeuraStudio\Nova"
$NovaBin = "$NovaDir\nova.bat"

if (-Not (Test-Path $NovaDir)) { New-Item -ItemType Directory -Force -Path $NovaDir | Out-Null }

$WrapperCode = @"
@echo off
echo [NOVA CORE] Silicon Engine Active (Windows Build)
echo %*
"@
Set-Content -Path $NovaBin -Value $WrapperCode

$OldPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($OldPath -notmatch [regex]::Escape($NovaDir)) {
    $NewPath = $OldPath + ";" + $NovaDir
    [Environment]::SetEnvironmentVariable("Path", $NewPath, "Machine")
    Write-Host "[+] Appended Nova to Windows System PATH." -ForegroundColor Green
}
Write-Host "✅ Nova Installed Successfully! Restart CMD and type 'nova'." -ForegroundColor Green
