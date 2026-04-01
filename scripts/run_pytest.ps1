[CmdletBinding(PositionalBinding = $false)]
param(
    [string]$PythonExe = "",
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PytestArgs
)

$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = (Resolve-Path (Join-Path $scriptRoot "..")).Path
if ([string]::IsNullOrWhiteSpace($PythonExe)) {
    $defaultCondaPython = "C:\ProgramData\anaconda3\envs\DLEnv\python.exe"
    if (Test-Path $defaultCondaPython) {
        $PythonExe = $defaultCondaPython
    }
    else {
        $PythonExe = "python"
    }
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$baseTemp = Join-Path $workspaceRoot "artifacts\manual_checks\pytest_runs\run_$timestamp"
New-Item -ItemType Directory -Force -Path $baseTemp | Out-Null

$env:PYTHONPATH = "src"
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = "1"
$env:TEMP = $baseTemp
$env:TMP = $baseTemp

$args = @(
    "-m",
    "pytest",
    "--basetemp",
    $baseTemp,
    "-p",
    "no:cacheprovider"
) + $PytestArgs

Write-Output "Using Python: $PythonExe"
Write-Output "Using base temp: $baseTemp"
Write-Output ("Pytest args: " + ($args -join " "))

Push-Location $workspaceRoot
try {
    & $PythonExe @args
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
