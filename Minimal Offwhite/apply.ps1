# Installs and applies this cursor scheme for the current user (no admin needed).
# Usage: powershell -ExecutionPolicy Bypass -File apply.ps1
$ErrorActionPreference = 'Stop'
$name = Split-Path $PSScriptRoot -Leaf
$dest = Join-Path $env:LOCALAPPDATA "Cursors\$name"

$roles = [ordered]@{
    Arrow = 'pointer.cur'; Help = 'help.cur'; AppStarting = 'working.ani'; Wait = 'busy.ani'
    Crosshair = 'precision.cur'; IBeam = 'text.cur'; NWPen = 'handwriting.cur'; No = 'unavailable.cur'
    SizeNS = 'vert.cur'; SizeWE = 'horz.cur'; SizeNWSE = 'dgn1.cur'; SizeNESW = 'dgn2.cur'
    SizeAll = 'move.cur'; UpArrow = 'alternate.cur'; Hand = 'link.cur'; Pin = 'pin.cur'; Person = 'person.cur'
}

New-Item -ItemType Directory -Force $dest | Out-Null
foreach ($f in $roles.Values) { Copy-Item (Join-Path $PSScriptRoot $f) $dest -Force }

$key = 'HKCU:\Control Panel\Cursors'
$paths = foreach ($r in $roles.Keys) { Join-Path $dest $roles[$r] }
Set-ItemProperty "$key\Schemes" -Name $name -Value ($paths -join ',')
Set-ItemProperty $key -Name '(default)' -Value $name
foreach ($r in $roles.Keys) { Set-ItemProperty $key -Name $r -Value (Join-Path $dest $roles[$r]) }

Add-Type -Namespace Win32 -Name Native -MemberDefinition @'
[DllImport("user32.dll", SetLastError = true)]
public static extern bool SystemParametersInfo(uint action, uint param, System.IntPtr vparam, uint winIni);
'@
[Win32.Native]::SystemParametersInfo(0x57, 0, [IntPtr]::Zero, 0x03) | Out-Null  # SPI_SETCURSORS
Write-Host "Applied '$name' cursors from $dest"
