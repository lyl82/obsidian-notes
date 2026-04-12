# check-nodejs.ps1
# 检查F:odejs目录

Write-Host "检查 F:odejs 目录..." -ForegroundColor Yellow

$nodejsPath = "F:\Nodejs"

if (Test-Path $nodejsPath) {
    Write-Host "目录存在: $nodejsPath" -ForegroundColor Green
    
    # 检查关键文件
    $nodeExe = Join-Path $nodejsPath "node.exe"
    $npmCmd = Join-Path $nodejsPath "npm.cmd"
    $npxCmd = Join-Path $nodejsPath "npx.cmd"
    
    if (Test-Path $nodeExe) {
        Write-Host "✓ 找到 node.exe" -ForegroundColor Green
        Write-Host "  路径: $nodeExe" -ForegroundColor Gray
        
        # 测试node版本
        try {
            $version = & $nodeExe --version 2>$null
            Write-Host "  Node.js版本: $version" -ForegroundColor Cyan
        } catch {
            Write-Host "  ✗ 无法运行node.exe" -ForegroundColor Red
        }
    } else {
        Write-Host "✗ 未找到 node.exe" -ForegroundColor Red
    }
    
    if (Test-Path $npmCmd) {
        Write-Host "✓ 找到 npm.cmd" -ForegroundColor Green
        Write-Host "  路径: $npmCmd" -ForegroundColor Gray
    } else {
        Write-Host "✗ 未找到 npm.cmd" -ForegroundColor Yellow
    }
    
    if (Test-Path $npxCmd) {
        Write-Host "✓ 找到 npx.cmd" -ForegroundColor Green
    } else {
        Write-Host "✗ 未找到 npx.cmd" -ForegroundColor Yellow
    }
    
    # 列出目录内容
    Write-Host "`n目录内容:" -ForegroundColor Cyan
    Get-ChildItem $nodejsPath | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize
    
} else {
    Write-Host "✗ 目录不存在: $nodejsPath" -ForegroundColor Red
    Write-Host "请确保Node.js已下载到该位置" -ForegroundColor Yellow
}

Write-Host "`n检查完成！" -ForegroundColor Green