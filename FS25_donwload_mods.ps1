$ErrorActionPreference = "Stop"

# Define potential download folders
$folders = @(
    "C:\Users\$env:UserName\OneDrive\Documents\My Games\FarmingSimulator2025\mods",
    "C:\Users\$env:UserName\Documents\My Games\FarmingSimulator2025\mods"
)

# Check if folders exist
$existingFolders = @()
foreach ($folder in $folders) {
    if (Test-Path -Path $folder) {
        $existingFolders += $folder
    }
}

# If no folders exist, exit the script
if (-not $existingFolders) {
    Write-Host "None of the specified folders exist. Exiting the script." -ForegroundColor Red
    exit
}

Write-Host "Using the following download folders: $($existingFolders -join ', ')"

# Define the URLs to download
$urls = @(
    "https://github.com/Stephan-S/FS25_AutoDrive/releases/latest/download/FS25_AutoDrive.zip",
    "https://github.com/Williwillswisse/AD_xCrossing/releases/latest/download/FS25_AutoDrive_xCrossing.zip",
    "https://github.com/Courseplay/Courseplay_FS25/releases/latest/download/FS25_Courseplay.zip",
    "https://github.com/urbanswelt/FS25_SiloKing/releases/latest/download/FS25_SiloKing.zip"
)

# Download each file to all existing folders
foreach ($url in $urls) {
    # Extract the file name from the URL
    $fileName = ($url -split '/')[-1]
    foreach ($folder in $existingFolders) {
        $destinationPath = Join-Path -Path $folder -ChildPath $fileName

        # Download the file
        Write-Host "Downloading $url to $destinationPath"
        Invoke-WebRequest -Uri $url -OutFile $destinationPath -UseBasicParsing
    }
}

Write-Host "Download completed! Files saved to: $($existingFolders -join ', ')"
