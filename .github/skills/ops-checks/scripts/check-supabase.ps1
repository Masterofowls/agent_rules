& (Join-Path $PSScriptRoot 'run.ps1') 'check-supabase' @args
exit $LASTEXITCODE
