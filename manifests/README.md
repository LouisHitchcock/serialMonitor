# Windows Package Manager (winget) Manifests

These manifest files are for submitting Serial Monitor to the Windows Package Manager (winget).

## Files

- `LouisHitchcock.SerialMonitor.yaml` - Version manifest
- `LouisHitchcock.SerialMonitor.installer.yaml` - Installer details
- `LouisHitchcock.SerialMonitor.locale.en-US.yaml` - Package metadata

## How to Submit

See `WINGET_SUBMISSION.md` in the root directory for complete instructions.

## Quick Start

1. Upload `SerialMonitor.exe` to GitHub releases
2. Submit PR to https://github.com/microsoft/winget-pkgs
3. Wait for approval (~1-3 days)

## Package Identifier

`LouisHitchcock.SerialMonitor`

## After Submission

Users will be able to install with:

```powershell
winget install LouisHitchcock.SerialMonitor
```
