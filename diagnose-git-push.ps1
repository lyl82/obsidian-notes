Write-Host "=== 诊断 git push 连接问题 ===" -ForegroundColor Cyan

# 1. 检查 git 配置
Write-Host "`n1. 检查 git 配置:" -ForegroundColor Yellow
git config --list | Select-String -Pattern "proxy|http|url|remote" | ForEach-Object {
    Write-Host "   $_" -ForegroundColor Gray
}

# 2. 检查远程仓库 URL
Write-Host "`n2. 检查远程仓库 URL:" -ForegroundColor Yellow
git remote -v

# 3. 测试 github.com 连接
Write-Host "`n3. 测试 github.com 连接:" -ForegroundColor Yellow
try {
    $pingResult = Test-Connection github.com -Count 2 -ErrorAction Stop
    Write-Host "   Ping github.com 成功" -ForegroundColor Green
} catch {
    Write-Host "   Ping github.com 失败: $_" -ForegroundColor Red
}

# 4. 测试 HTTPS 端口 443
Write-Host "`n4. 测试 HTTPS 端口 443:" -ForegroundColor Yellow
try {
    $tcpTest = New-Object System.Net.Sockets.TcpClient
    $tcpTest.Connect("github.com", 443)
    Write-Host "   端口 443 连接成功" -ForegroundColor Green
    $tcpTest.Close()
} catch {
    Write-Host "   端口 443 连接失败: $_" -ForegroundColor Red
}

# 5. 检查系统代理设置
Write-Host "`n5. 检查系统代理设置:" -ForegroundColor Yellow
$proxyVars = @("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy", "ALL_PROXY")
foreach ($var in $proxyVars) {
    $value = [Environment]::GetEnvironmentVariable($var)
    if ($value) {
        Write-Host "   $var = $value" -ForegroundColor Yellow
    }
}

# 6. 检查 git 是否使用代理
Write-Host "`n6. 检查 git 代理配置:" -ForegroundColor Yellow
$gitProxyConfig = @("http.proxy", "https.proxy", "http.sslVerify")
foreach ($config in $gitProxyConfig) {
    $value = git config --global $config
    if ($value) {
        Write-Host "   $config = $value" -ForegroundColor Yellow
    }
}

# 7. 检查 hosts 文件
Write-Host "`n7. 检查 hosts 文件中的 github.com 条目:" -ForegroundColor Yellow
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
if (Test-Path $hostsPath) {
    $hostsContent = Get-Content $hostsPath -ErrorAction SilentlyContinue
    $githubEntries = $hostsContent | Where-Object { $_ -match "github\.com" }
    if ($githubEntries) {
        Write-Host "   发现 github.com 条目:" -ForegroundColor Red
        $githubEntries | ForEach-Object { Write-Host "   $_" -ForegroundColor Red }
    } else {
        Write-Host "   没有找到 github.com 相关条目" -ForegroundColor Green
    }
}

# 8. 尝试使用 git 协议 (ssh) 代替 https
Write-Host "`n8. 检查 SSH 密钥配置:" -ForegroundColor Yellow
if (Test-Path "$env:USERPROFILE\.ssh\id_rsa.pub") {
    Write-Host "   SSH 公钥存在" -ForegroundColor Green
    Write-Host "   可以考虑使用 SSH URL: git@github.com:lyl82/obsidian-notes.git" -ForegroundColor Gray
} else {
    Write-Host "   SSH 公钥不存在" -ForegroundColor Yellow
}

Write-Host "`n=== 建议的修复步骤 ===" -ForegroundColor Cyan
Write-Host "1. 清除 git 代理配置:" -ForegroundColor Yellow
Write-Host "   git config --global --unset http.proxy" -ForegroundColor Gray
Write-Host "   git config --global --unset https.proxy" -ForegroundColor Gray
Write-Host "`n2. 如果使用代理，请正确配置:" -ForegroundColor Yellow
Write-Host "   git config --global http.proxy http://你的代理服务器:端口" -ForegroundColor Gray
Write-Host "`n3. 尝试使用 SSH 协议代替 HTTPS:" -ForegroundColor Yellow
Write-Host "   git remote set-url origin git@github.com:lyl82/obsidian-notes.git" -ForegroundColor Gray
Write-Host "`n4. 禁用 SSL 验证 (临时):" -ForegroundColor Yellow
Write-Host "   git config --global http.sslVerify false" -ForegroundColor Gray
Write-Host "`n5. 检查防火墙或杀毒软件设置" -ForegroundColor Yellow