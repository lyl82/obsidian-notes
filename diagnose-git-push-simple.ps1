Write-Host "=== Diagnosing git push connection issue ===" -ForegroundColor Cyan

# 1. Check git configuration
Write-Host "`n1. Checking git configuration:" -ForegroundColor Yellow
git config --list | Select-String -Pattern "proxy|http|url|remote" | ForEach-Object {
    Write-Host "   $_" -ForegroundColor Gray
}

# 2. Check remote repository URL
Write-Host "`n2. Checking remote repository URL:" -ForegroundColor Yellow
git remote -v

# 3. Test github.com connection
Write-Host "`n3. Testing github.com connection:" -ForegroundColor Yellow
try {
    $pingResult = Test-Connection github.com -Count 2 -ErrorAction Stop
    Write-Host "   Ping github.com successful" -ForegroundColor Green
} catch {
    Write-Host "   Ping github.com failed: $_" -ForegroundColor Red
}

# 4. Test HTTPS port 443
Write-Host "`n4. Testing HTTPS port 443:" -ForegroundColor Yellow
try {
    $tcpTest = New-Object System.Net.Sockets.TcpClient
    $tcpTest.Connect("github.com", 443)
    Write-Host "   Port 443 connection successful" -ForegroundColor Green
    $tcpTest.Close()
} catch {
    Write-Host "   Port 443 connection failed: $_" -ForegroundColor Red
}

# 5. Check system proxy settings
Write-Host "`n5. Checking system proxy settings:" -ForegroundColor Yellow
$proxyVars = @("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY")
foreach ($var in $proxyVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        Write-Host "   $var = $value" -ForegroundColor Yellow
    }
}

# 6. Check git proxy configuration
Write-Host "`n6. Checking git proxy configuration:" -ForegroundColor Yellow
$gitProxyConfig = @("http.proxy", "https.proxy", "http.sslVerify")
foreach ($config in $gitProxyConfig) {
    $value = git config --global $config
    if ($value) {
        Write-Host "   $config = $value" -ForegroundColor Yellow
    }
}

# 7. Check hosts file
Write-Host "`n7. Checking hosts file for github.com entries:" -ForegroundColor Yellow
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
if (Test-Path $hostsPath) {
    $hostsContent = Get-Content $hostsPath -ErrorAction SilentlyContinue
    $githubEntries = $hostsContent | Where-Object { $_ -match "github\.com" }
    if ($githubEntries) {
        Write-Host "   Found github.com entries:" -ForegroundColor Red
        $githubEntries | ForEach-Object { Write-Host "   $_" -ForegroundColor Red }
    } else {
        Write-Host "   No github.com entries found" -ForegroundColor Green
    }
}

# 8. Check SSH key configuration
Write-Host "`n8. Checking SSH key configuration:" -ForegroundColor Yellow
if (Test-Path "$env:USERPROFILE\.ssh\id_rsa.pub") {
    Write-Host "   SSH public key exists" -ForegroundColor Green
    Write-Host "   Consider using SSH URL: git@github.com:lyl82/obsidian-notes.git" -ForegroundColor Gray
} else {
    Write-Host "   SSH public key does not exist" -ForegroundColor Yellow
}

Write-Host "`n=== Recommended fixes ===" -ForegroundColor Cyan
Write-Host "1. Clear git proxy configuration:" -ForegroundColor Yellow
Write-Host "   git config --global --unset http.proxy" -ForegroundColor Gray
Write-Host "   git config --global --unset https.proxy" -ForegroundColor Gray
Write-Host "`n2. If using proxy, configure correctly:" -ForegroundColor Yellow
Write-Host "   git config --global http.proxy http://your-proxy-server:port" -ForegroundColor Gray
Write-Host "`n3. Try using SSH instead of HTTPS:" -ForegroundColor Yellow
Write-Host "   git remote set-url origin git@github.com:lyl82/obsidian-notes.git" -ForegroundColor Gray
Write-Host "`n4. Disable SSL verification (temporary):" -ForegroundColor Yellow
Write-Host "   git config --global http.sslVerify false" -ForegroundColor Gray
Write-Host "`n5. Check firewall or antivirus settings" -ForegroundColor Yellow