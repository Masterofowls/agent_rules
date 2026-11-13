& (Join-Path $PSScriptRoot 'run.ps1') 'check-disk' @args
exit $LASTEXITCODE
