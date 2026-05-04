Write-Host "=== Fixing git push connection ===" -ForegroundColor Cyan

# 1. Check current git configuration
Write-Host "`n1. Current git configuration:" -ForegroundColor Yellow
git config --list | Select-String -Pattern "http|https|ssl|proxy" | ForEach-Object {
    Write-Host "   $_" -ForegroundColor Gray
}

# 2. Remove any remaining proxy settings
Write-Host "`n2. Removing any proxy settings:" -ForegroundColor Yellow
$proxySettings = @("http.proxy", "https.proxy", "http.proxyAuthMethod", "https.proxyAuthMethod")
foreach ($setting in $proxySettings) {
    git config --global --unset $setting
    Write-Host "   Removed: $setting" -ForegroundColor Gray
}

# 3. Try different http versions
Write-Host "`n3. Trying different HTTP versions:" -ForegroundColor Yellow
Write-Host "   Setting http.version to HTTP/1.1" -ForegroundColor Gray
git config --global http.version HTTP/1.1

Write-Host "   Setting http.version to HTTP/2" -ForegroundColor Gray
git config --global http.version HTTP/2

# 4. Try with lower postBuffer size
Write-Host "`n4. Adjusting git buffer sizes:" -ForegroundColor Yellow
git config --global http.postBuffer 524288000  # 500MB
Write-Host "   Set http.postBuffer to 500MB" -ForegroundColor Gray

# 5. Try with different SSL backend
Write-Host "`n5. Checking SSL backend:" -ForegroundColor Yellow
$currentSSLBackend = git config --global http.sslbackend
Write-Host "   Current SSL backend: $currentSSLBackend" -ForegroundColor Gray

# Try with schannel (Windows native)
Write-Host "   Setting SSL backend to schannel" -ForegroundColor Gray
git config --global http.sslbackend schannel

# 6. Test connection with curl
Write-Host "`n6. Testing connection with curl:" -ForegroundColor Yellow
try {
    $curlOutput = curl -I https://github.com --max-time 10 2>&1
    Write-Host "   Curl test: $curlOutput" -ForegroundColor Gray
} catch {
    Write-Host "   Curl test failed: $_" -ForegroundColor Red
}

# 7. Try git fetch first (sometimes fetch works when push doesn't)
Write-Host "`n7. Trying git fetch:" -ForegroundColor Yellow
try {
    $fetchOutput = git fetch --verbose 2>&1
    Write-Host "   Git fetch output: $fetchOutput" -ForegroundColor Gray
} catch {
    Write-Host "   Git fetch failed: $_" -ForegroundColor Red
}

# 8. Try with increased timeout
Write-Host "`n8. Setting longer timeout:" -ForegroundColor Yellow
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 99999
Write-Host "   Set low speed limit and time" -ForegroundColor Gray

# 9. Try push with increased verbosity
Write-Host "`n9. Attempting git push with verbose output:" -ForegroundColor Yellow
Write-Host "   Running: git push -v --progress" -ForegroundColor Gray
$pushOutput = git push -v --progress 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Git push successful!" -ForegroundColor Green
    Write-Host "   Output: $pushOutput" -ForegroundColor Gray
} else {
    Write-Host "   Git push failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    Write-Host "   Error output: $pushOutput" -ForegroundColor Red
}

Write-Host "`n=== Fix attempts complete ===" -ForegroundColor Cyan