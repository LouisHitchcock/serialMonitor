# Submitting Serial Monitor to Windows Package Manager (winget)

## Prerequisites

Before submitting to winget, you need to:

1. **Upload the release to GitHub**
   - Go to https://github.com/LouisHitchcock/serialMonitor/releases
   - Create a new release for v1.0.0
   - Upload `SerialMonitor.exe` as a release asset

2. **Get the SHA256 hash** of the uploaded EXE

## Step 1: Calculate SHA256 Hash

After uploading to GitHub, download the release and calculate its hash:

```powershell
# Download from GitHub release
$url = "https://github.com/LouisHitchcock/serialMonitor/releases/download/v1.0.0/SerialMonitor.exe"
Invoke-WebRequest -Uri $url -OutFile "SerialMonitor-download.exe"

# Calculate SHA256
Get-FileHash -Algorithm SHA256 "SerialMonitor-download.exe" | Select-Object Hash
```

Or calculate it now before uploading:

```powershell
Get-FileHash -Algorithm SHA256 "dist\SerialMonitor.exe" | Select-Object Hash
```

## Step 2: Update Manifest

1. Copy the SHA256 hash
2. Edit `manifests\LouisHitchcock.SerialMonitor.installer.yaml`
3. Replace `TO_BE_REPLACED_AFTER_UPLOAD` with the actual hash

## Step 3: Fork winget-pkgs Repository

1. Go to https://github.com/microsoft/winget-pkgs
2. Click "Fork" to create your own copy

## Step 4: Clone Your Fork

```powershell
git clone https://github.com/YOUR_USERNAME/winget-pkgs.git
cd winget-pkgs
```

## Step 5: Create Package Directory

```powershell
# Create directory structure
New-Item -ItemType Directory -Path "manifests\l\LouisHitchcock\SerialMonitor\1.0.0" -Force

# Copy manifest files
Copy-Item "C:\Users\Louis\Desktop\Code\SerialMonitor\manifests\*" `
          "manifests\l\LouisHitchcock\SerialMonitor\1.0.0\"
```

## Step 6: Test the Manifest Locally

```powershell
# Install winget manifest testing tool
winget install wingetcreate

# Validate manifest
winget validate manifests\l\LouisHitchcock\SerialMonitor\1.0.0
```

## Step 7: Commit and Push

```powershell
git checkout -b serialmonitor-1.0.0
git add manifests/l/LouisHitchcock/SerialMonitor/1.0.0/
git commit -m "New package: LouisHitchcock.SerialMonitor version 1.0.0"
git push origin serialmonitor-1.0.0
```

## Step 8: Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull requests" → "New pull request"
3. Base repository: `microsoft/winget-pkgs`
4. Base branch: `master`
5. Head repository: `YOUR_USERNAME/winget-pkgs`
6. Compare branch: `serialmonitor-1.0.0`
7. Click "Create pull request"
8. Fill in the template and submit

## Step 9: Wait for Review

- Microsoft reviewers will check your submission
- Automated tests will run
- Address any feedback if needed
- Usually takes 1-3 days

## After Approval

Once merged, users can install your app with:

```powershell
winget install LouisHitchcock.SerialMonitor
```

Or just:

```powershell
winget install "Serial Monitor"
```

## Updating in the Future

For future versions:
1. Create new release on GitHub
2. Calculate new SHA256
3. Create new manifest version directory
4. Submit new PR to winget-pkgs

## Alternative: Use WingetCreate Tool

Microsoft provides a tool to automate this:

```powershell
# Install tool
winget install wingetcreate

# Create manifest automatically
wingetcreate new https://github.com/LouisHitchcock/serialMonitor/releases/download/v1.0.0/SerialMonitor.exe
```

## Resources

- **winget-pkgs repo**: https://github.com/microsoft/winget-pkgs
- **Contribution guide**: https://github.com/microsoft/winget-pkgs/blob/master/CONTRIBUTING.md
- **Manifest schema**: https://github.com/microsoft/winget-cli/tree/master/schemas/JSON/manifests
- **WingetCreate**: https://github.com/microsoft/winget-create
