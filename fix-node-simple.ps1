# fix-node-simple.ps1
# 简单修复Node.js路径

Write-Host "正在修复Node.js路径..." -ForegroundColor Yellow

# 1. 清理PATH中的问题路径
$paths = $env:PATH -split ';'
$cleanPaths = @()

foreach ($path in $paths) {
    if ($path -and $path.Trim() -ne '') {
        # 移除 D:\Documents\01_Projects\ 相关路径
        if ($path -notlike '*01_Projects*') {
            $cleanPaths += $path
        } else {
            Write-Host "移除有问题的路径: $path" -ForegroundColor Red
        }
    }
}

# 2. 更新PATH
$env:PATH = $cleanPaths -join ';'

# 3. 测试命令
Write-Host "`n测试基本命令..." -ForegroundColor Cyan

# 测试where命令
Write-Host "查找node.exe:" -ForegroundColor White
where.exe node 2>$null

Write-Host "`n查找npm.cmd:" -ForegroundColor White
where.exe npm 2>$null

# 4. 建议
Write-Host "`n建议:" -ForegroundColor Yellow
Write-Host "1. 如果Node.js未安装，请从 https://nodejs.org/ 下载安装"
Write-Host "2. 安装时选择'Add to PATH'选项"
Write-Host "3. 安装完成后重启终端"

Write-Host "`n修复完成！当前PATH已清理。" -ForegroundColor Green