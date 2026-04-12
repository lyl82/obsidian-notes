# check-nodejs-simple.ps1
# 简单检查F:odejs目录

Write-Host "Checking F:odejs directory..." -ForegroundColor Yellow

$nodejsPath = "F:\Nodejs"

if (Test-Path $nodejsPath) {
    Write-Host "Directory exists: $nodejsPath" -ForegroundColor Green
    
    # 检查关键文件
    $nodeExe = "$nodejsPath\node.exe"
    $npmCmd = "$nodejsPath\npm.cmd"
    
    if (Test-Path $nodeExe) {
        Write-Host "Found node.exe" -ForegroundColor Green
    } else {
        Write-Host "NOT found node.exe" -ForegroundColor Red
    }
    
    if (Test-Path $npmCmd) {
        Write-Host "Found npm.cmd" -ForegroundColor Green
    } else {
        Write-Host "NOT found npm.cmd" -ForegroundColor Yellow
    }
    
    # 列出目录内容
    Write-Host "`nDirectory contents:" -ForegroundColor Cyan
    dir $nodejsPath
    
} else {
    Write-Host "Directory NOT found: $nodejsPath" -ForegroundColor Red
}

Write-Host "`nCheck completed!" -ForegroundColor Green