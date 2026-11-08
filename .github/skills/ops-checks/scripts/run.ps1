$ErrorActionPreference = 'Stop'
$python = if ($env:OPS_CHECKS_PYTHON) { $env:OPS_CHECKS_PYTHON } else { 'python' }
if (-not (Get-Command $python -ErrorAction SilentlyContinue)) {
    [Console]::Error.WriteLine('Python 3.10+ is required')
    exit 2
}
& $python (Join-Path $PSScriptRoot 'checks.py') @args
exit $LASTEXITCODE
