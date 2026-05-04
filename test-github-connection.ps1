Write-Host "=== Testing github.com connection ===" -ForegroundColor Cyan

# Test ping
Write-Host "`n1. Testing ping to github.com:" -ForegroundColor Yellow
try {
    $pingResult = Test-Connection github.com -Count 2 -ErrorAction Stop
    Write-Host "   Ping successful (response time: $($pingResult[0].ResponseTime)ms)" -ForegroundColor Green
} catch {
    Write-Host "   Ping failed: $_" -ForegroundColor Red
}

# Test TCP connection to port 443
Write-Host "`n2. Testing TCP connection to github.com:443:" -ForegroundColor Yellow
try {
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    $tcpClient.Connect("github.com", 443)
    Write-Host "   TCP connection successful" -ForegroundColor Green
    $tcpClient.Close()
} catch {
    Write-Host "   TCP connection failed: $_" -ForegroundColor Red
}

# Test HTTPS connection using Invoke-WebRequest
Write-Host "`n3. Testing HTTPS connection to github.com:" -ForegroundColor Yellow
try {
    # Try to get the main page (with short timeout)
    $response = Invoke-WebRequest -Uri "https://github.com" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "   HTTPS connection successful (Status: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "   HTTPS connection failed: $_" -ForegroundColor Red
}

# Test git-specific connection
Write-Host "`n4. Testing git protocol connection:" -ForegroundColor Yellow
try {
    # Test git's own connection
    $gitOutput = git ls-remote https://github.com/lyl82/obsidian-notes.git --quiet 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "   Git connection successful" -ForegroundColor Green
    } else {
        Write-Host "   Git connection failed" -ForegroundColor Red
        Write-Host "   Output: $gitOutput" -ForegroundColor Gray
    }
} catch {
    Write-Host "   Git connection test error: $_" -ForegroundColor Red
}

Write-Host "`n=== Connection test complete ===" -ForegroundColor Cyan