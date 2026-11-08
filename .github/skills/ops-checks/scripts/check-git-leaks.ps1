& (Join-Path $PSScriptRoot 'run.ps1') 'check-git-leaks' @args
exit $LASTEXITCODE
