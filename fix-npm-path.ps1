# fix-npm-path.ps1
# 修复npm路径优先级

Write-Host "正在修复npm路径优先级..." -ForegroundColor Yellow

# 1. 获取当前所有npm路径
Write-Host "`n查找所有npm路径:" -ForegroundColor Cyan
$npmPaths = @()
where.exe npm 2>$null | ForEach-Object {
    $npmPaths += $_
    Write-Host "  $_" -ForegroundColor White
}

# 2. 查找正确的npm路径（从AppData\Roaming\npm）
$correctNpmPath = "C:\Users\Administrator\AppData\Roaming\npm"
if (Test-Path $correctNpmPath) {
    Write-Host "`n找到正确的npm路径: $correctNpmPath" -ForegroundColor Green
} else {
    Write-Host "`n未找到正确的npm路径，尝试其他位置..." -ForegroundColor Yellow
    # 尝试其他可能的npm路径
    $possiblePaths = @(
        "$env:USERPROFILE\AppData\Roaming\npm",
        "$env:LOCALAPPDATA\npm",
        "C:\Program Files\nodejs"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $correctNpmPath = $path
            Write-Host "找到备选npm路径: $correctNpmPath" -ForegroundColor Green
            break
        }
    }
}

# 3. 重新构建PATH，让正确的路径优先
if ($correctNpmPath) {
    Write-Host "`n重新构建PATH环境变量..." -ForegroundColor Cyan
    
    # 获取当前PATH
    $paths = $env:PATH -split ';'
    $newPaths = @()
    
    # 首先添加正确的npm路径
    $newPaths += $correctNpmPath
    
    # 添加其他路径，但排除有问题的路径
    foreach ($path in $paths) {
        if ($path -and $path.Trim() -ne '' -and $path -ne $correctNpmPath) {
            # 排除 D:\Documents\01_Projects\ 相关路径
            if ($path -notlike '*01_Projects*') {
                $newPaths += $path
            }
        }
    }
    
    # 更新PATH
    $env:PATH = $newPaths -join ';'
    Write-Host "PATH已更新，正确的npm路径现在优先" -ForegroundColor Green
    
    # 4. 验证修复
    Write-Host "`n验证修复结果:" -ForegroundColor Cyan
    Write-Host "第一个找到的npm路径:" -ForegroundColor White
    where.exe npm 2>$null | Select-Object -First 1
    
    Write-Host "`n尝试运行npm --version:" -ForegroundColor White
    try {
        npm --version 2>$null
    } catch {
        Write-Host "npm命令仍然失败" -ForegroundColor Red
        Write-Host "可能需要重新安装Node.js" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n未找到正确的npm路径，建议重新安装Node.js" -ForegroundColor Red
    Write-Host "下载地址: https://nodejs.org/" -ForegroundColor Blue
}

Write-Host "`n修复完成！" -ForegroundColor Green