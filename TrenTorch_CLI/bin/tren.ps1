$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Resolve Python executable: prefer active virtual environment, then local .venv, then system python
$pythonExe = "python"
if (-not $env:VIRTUAL_ENV) {
    $localVenv = Join-Path $ScriptDir "..\.venv\Scripts\python.exe"
    $rootVenv = Join-Path $ScriptDir "..\..\.venv\Scripts\python.exe"
    if (Test-Path $localVenv) {
        $pythonExe = (Resolve-Path $localVenv).Path
    } elseif (Test-Path $rootVenv) {
        $pythonExe = (Resolve-Path $rootVenv).Path
    }
}

$trenScript = Join-Path $ScriptDir "tren"
& $pythonExe $trenScript @args
$exitCode = if ($null -ne $LASTEXITCODE) { $LASTEXITCODE } else { 0 }
exit $exitCode
