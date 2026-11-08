& (Join-Path $PSScriptRoot 'run.ps1') 'check-postgres' @args
exit $LASTEXITCODE
