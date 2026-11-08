& (Join-Path $PSScriptRoot 'run.ps1') 'check-docker' @args
exit $LASTEXITCODE
