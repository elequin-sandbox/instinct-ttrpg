# push-to-github.ps1
# Run this from the project folder to push index.html to GitHub.
# It reads your GitHub token from Claude's config automatically.

$ErrorActionPreference = "Stop"

# 1. Read token from Claude config
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$config = Get-Content $configPath -Raw | ConvertFrom-Json
$token = $config.mcpServers.github.env.GITHUB_PERSONAL_ACCESS_TOKEN

if (-not $token) {
    Write-Error "Could not find GITHUB_PERSONAL_ACCESS_TOKEN in $configPath"
    exit 1
}

# 2. Read local index.html
$filePath = "$PSScriptRoot\index.html"
$content = Get-Content $filePath -Raw -Encoding UTF8

# 3. Get current file SHA from GitHub (required for updates)
$headers = @{
    Authorization = "token $token"
    Accept        = "application/vnd.github.v3+json"
}
$apiUrl = "https://api.github.com/repos/Nathan-Elequin/act-tactics/contents/index.html"
Write-Host "Fetching current file SHA from GitHub..."
$existing = Invoke-RestMethod -Uri $apiUrl -Headers $headers -Method Get
$sha = $existing.sha

# 4. Base64-encode the content
$bytes  = [System.Text.Encoding]::UTF8.GetBytes($content)
$b64    = [Convert]::ToBase64String($bytes)

# 5. Push the update
$body = @{
    message = "Remove Instinct button from class filter chip row"
    content = $b64
    sha     = $sha
} | ConvertTo-Json

Write-Host "Pushing index.html to Nathan-Elequin/act-tactics..."
Invoke-RestMethod -Uri $apiUrl -Method Put -Headers $headers -Body $body -ContentType "application/json"

Write-Host ""
Write-Host "Done! index.html pushed successfully." -ForegroundColor Green
Write-Host "Your site will redeploy in ~30 seconds."
