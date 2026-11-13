& (Join-Path $PSScriptRoot 'run.ps1') 'check-git-state' @args
exit $LASTEXITCODE
