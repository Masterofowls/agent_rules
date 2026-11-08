& (Join-Path $PSScriptRoot 'run.ps1') 'check-ssh' @args
exit $LASTEXITCODE
