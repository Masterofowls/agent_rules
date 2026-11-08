---
description: "Use when writing or running PowerShell or Windows CMD commands, .ps1, .bat, or .cmd scripts; covers quoting, exit codes, safe elevation with gsudo, and portability."
applyTo: ["**/*.{ps1,psm1,psd1,bat,cmd}", "**/{scripts,tools}/**"]
---

# PowerShell and CMD

- Identify the actual shell and PowerShell version before choosing syntax. Prefer PowerShell for Windows automation; use CMD only for batch compatibility or tools requiring it.
- Prefer explicit cmdlet names over aliases in reusable scripts. Use `Join-Path`, `$PSScriptRoot`, and `-LiteralPath` where appropriate; do not assume the caller's working directory.
- Use parameter blocks, validation, and explicit defaults. Pass arguments directly with the call operator instead of building command strings or using `Invoke-Expression`.
- Quote paths with spaces correctly. PowerShell escaping, CMD escaping, and Bash escaping are different; do not copy commands between shells unchanged.
- Use terminating errors for failures that must stop the script, with `try`/`catch` only for recovery or added context. Check native command exit codes explicitly; `$ErrorActionPreference` alone does not reliably catch them across versions.
- Preserve the child process exit code and send diagnostics separately from machine-readable output. Do not suppress failures with broad catches.
- Keep environment setup and commands that depend on it in the same process. For Visual Studio batch setup, invoke the batch file and compiler in one CMD process.
- In CMD, use `set "NAME=value"`, `pushd`/`popd`, and `exit /b` deliberately; account for expansion inside blocks and avoid delayed expansion corrupting arguments containing `!`.
- Prefer `gsudo` for an explicitly authorized operation requiring Windows elevation when it is installed. Elevate only the necessary command, never the whole workflow by default.
- Check for `gsudo` first; do not silently install it, bypass UAC, or change execution policy. If unavailable, report that and use an approved elevation method.
- Inspect resolved filesystem targets before mutations. Never use broad cleanup, name-based process termination, or shell redirection to bypass file-preservation rules.
- Use bounded timeouts for network/process work and clean up only owned resources. Keep credentials out of command lines and logs.
- Follow the paired `.ps1`/`.sh` contract in the reusable-patterns instructions. Validate syntax, run the existing linter and formatter, and test exit codes and quoted arguments.
