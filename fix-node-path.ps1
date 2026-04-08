# fix-node-path.ps1
# 修复Node.js和npm路径的脚本

Write-Host "正在修复Node.js和npm路径..." -ForegroundColor Yellow

# 1. 获取当前PATH
$currentPath = $env:PATH

# 2. 移除有问题的路径
$paths = $currentPath -split ';'
$cleanPaths = @()

foreach ($path in $paths) {
    # 保留有效的路径，移除有问题或无效的路径
    if ($path -and $path.Trim() -ne '') {
        # 移除 D:\Documents\01_Projects\ 相关路径
        if ($path -notlike '*01_Projects*') {
            # 检查路径是否存在
            if (Test-Path $path) {
                $cleanPaths += $path
            } else {
                Write-Host "移除无效路径: $path" -ForegroundColor Gray
            }
        } else {
            Write-Host "移除有问题的路径: $path" -ForegroundColor Red
        }
    }
}

# 3. 添加常见的Node.js安装路径（如果存在）
$possibleNodePaths = @(
    "C:\Program Files\nodejs",
    "E:\nodejs",
    "$env:USERPROFILE\AppData\Roaming\npm",
    "$env:LOCALAPPDATA\Programs\nodejs"
)

foreach ($nodePath in $possibleNodePaths) {
    if (Test-Path $nodePath) {
        if ($cleanPaths -notcontains $nodePath) {
            $cleanPaths = @($nodePath) + $cleanPaths
            Write-Host "添加Node.js路径: $nodePath" -ForegroundColor Green
        }
    }
}

# 4. 更新PATH环境变量
$newPath = $cleanPaths -join ';'
$env:PATH = $newPath

# 5. 保存到用户环境变量（可选）
Write-Host "`n是否要将修复后的PATH保存到用户环境变量？" -ForegroundColor Yellow
$saveToEnv = Read-Host "输入 'y' 保存，其他键跳过"
if ($saveToEnv -eq 'y') {
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "已保存到用户环境变量，需要重启终端生效" -ForegroundColor Green
}

# 6. 测试Node.js和npm
Write-Host "`n测试Node.js和npm..." -ForegroundColor Yellow

try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "✓ Node.js版本: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ Node.js未找到" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Node.js未找到" -ForegroundColor Red
}

try {
    $npmVersion = npm --version 2>$null
    if ($npmVersion) {
        Write-Host "✓ npm版本: $npmVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ npm未找到" -ForegroundColor Red
        Write-Host "建议重新安装Node.js" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ npm未找到" -ForegroundColor Red
    Write-Host "建议重新安装Node.js" -ForegroundColor Yellow
}

# 7. 显示修复后的PATH摘要
Write-Host "`n修复后的PATH摘要（Node.js相关）:" -ForegroundColor Cyan
$env:PATH -split ';' | Where-Object { $_ -match 'node|npm' } | ForEach-Object {
    Write-Host "  $_" -ForegroundColor White
}

Write-Host "`n修复完成！" -ForegroundColor Green
Write-Host "如果Node.js/npm仍然不可用，请重新安装Node.js。" -ForegroundColor Yellow
Write-Host "下载地址: https://nodejs.org/" -ForegroundColor Blue