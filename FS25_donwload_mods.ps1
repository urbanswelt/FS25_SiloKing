$ErrorActionPreference = "Stop"

# Define the download folder
$downloadFolder = "C:\Users\$env:UserName\OneDrive\Documents\My Games\FarmingSimulator2025\mods_dev"

# Create the folder if it does not exist
if (-not (Test-Path -Path $downloadFolder)) {
    New-Item -ItemType Directory -Path $downloadFolder -Force | Out-Null
}

# Define the URLs to download
$urls = @(
    "https://github.com/Stephan-S/FS25_AutoDrive/releases/latest/download/FS25_AutoDrive.zip",
    "https://github.com/Williwillswisse/AD_xCrossing/releases/latest/download/FS25_AutoDrive_xCrossing.zip",
    "https://github.com/Courseplay/Courseplay_FS25/releases/latest/download/FS25_Courseplay.zip",
    "https://github.com/urbanswelt/FS25_SiloKing/releases/latest/download/FS25_SiloKing.zip"
)

# Download each file
foreach ($url in $urls) {
    # Extract the file name from the URL
    $fileName = ($url -split '/')[-1]
    $destinationPath = Join-Path -Path $downloadFolder -ChildPath $fileName

    # Download the file
    Write-Host "Downloading $url to $destinationPath"
    Invoke-WebRequest -Uri $url -OutFile $destinationPath -UseBasicParsing
}

Write-Host "Download completed! Files saved to $downloadFolder."
