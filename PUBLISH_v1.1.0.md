# Publishing Serial Monitor v1.1.0

## Summary of Changes

### Features Implemented
1. **Toggle Autoscroll** - Checkbox to enable/disable automatic scrolling
2. **Autoconnect** - Automatically reconnects to previously connected device when replugged
3. **Improved Disconnection Handling** - Removed popup alert; shows "(COMX) Device Disconnected" in footer

### Files Modified
- `serial_monitor.pyw` - Added new features and updated to v1.1.0
- `README.md` - Updated feature list
- `RELEASE_NOTES.md` - Added v1.1.0 release notes
- All winget manifest files updated to v1.1.0

### Build Complete
- New executable built: `dist\SerialMonitor.exe`
- SHA256: `B8FC75DC8B8A824061D89612C48ABEB15228D130F0CBEC5823E7BA4DDA9A37AA`

## Steps to Publish

### 1. Create GitHub Release

```bash
# Create and push a new tag
git add .
git commit -m "Release v1.1.0 - Add autoscroll toggle, autoconnect, and improve disconnection handling"
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin main
git push origin v1.1.0
```

### 2. Upload Release to GitHub

1. Go to https://github.com/LouisHitchcock/serialMonitor/releases/new
2. Select tag: `v1.1.0`
3. Release title: `Serial Monitor v1.1.0`
4. Description: Copy from RELEASE_NOTES.md (v1.1.0 section)
5. Upload file: `dist\SerialMonitor.exe`
6. Click "Publish release"

### 3. Update Winget Package

After the GitHub release is published:

1. Fork the winget-pkgs repository if you haven't already:
   https://github.com/microsoft/winget-pkgs

2. Create a new branch for the update:
   ```bash
   git checkout -b LouisHitchcock.SerialMonitor-1.1.0
   ```

3. Copy the manifest files from `manifests/` directory to:
   ```
   winget-pkgs/manifests/l/LouisHitchcock/SerialMonitor/1.1.0/
   ```

4. Commit and push:
   ```bash
   git add .
   git commit -m "LouisHitchcock.SerialMonitor version 1.1.0"
   git push origin LouisHitchcock.SerialMonitor-1.1.0
   ```

5. Create a Pull Request to microsoft/winget-pkgs

6. Wait for the automated validation to pass and for the PR to be merged

## Testing the Release

After publishing to GitHub, test the download:
1. Download the EXE from the release page
2. Run it and verify all new features work:
   - Autoscroll checkbox appears and functions correctly
   - Autoconnect checkbox appears and functions correctly
   - Disconnection shows in footer without popup

## Manifest Files Updated

All three manifest files have been updated with:
- Version number: 1.1.0
- Release date: 2026-01-18
- InstallerUrl: https://github.com/LouisHitchcock/serialMonitor/releases/download/v1.1.0/SerialMonitor.exe
- InstallerSha256: B8FC75DC8B8A824061D89612C48ABEB15228D130F0CBEC5823E7BA4DDA9A37AA
- Updated description with new features

## Notes

- The executable is already built in `dist\SerialMonitor.exe`
- All manifest files are ready in the `manifests/` directory
- The SHA256 hash is already in the installer manifest
- Make sure to upload the exact file from `dist\SerialMonitor.exe` to match the SHA256 hash
