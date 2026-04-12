# install-mcp-direct.ps1
# 直接安装Trae MCP，绕过有问题的npm

Write-Host "准备安装Trae MCP..." -ForegroundColor Yellow

# 方法1：尝试使用npx（如果可用）
Write-Host "`n方法1：尝试使用npx安装" -ForegroundColor Cyan
try {
    npx --version 2>$null
    Write-Host "npx可用，尝试安装..." -ForegroundColor Green
    npx @modelcontextprotocol/server-trae install
} catch {
    Write-Host "npx不可用或安装失败" -ForegroundColor Yellow
    
    # 方法2：使用npm的完整路径
    Write-Host "`n方法2：查找正确的npm路径" -ForegroundColor Cyan
    
    # 查找npm.cmd文件（排除有问题的路径）
    $npmPaths = cmd /c where npm.cmd 2>$null
    $validNpmPath = $null
    
    foreach ($path in $npmPaths) {
        if ($path -notlike '*01_Projects*') {
            $validNpmPath = $path
            Write-Host "找到有效的npm路径: $validNpmPath" -ForegroundColor Green
            break
        }
    }
    
    if ($validNpmPath) {
        Write-Host "使用有效的npm安装..." -ForegroundColor Green
        & $validNpmPath install @modelcontextprotocol/server-trae -g
    } else {
        Write-Host "`n方法3：直接使用Node.js运行安装脚本" -ForegroundColor Cyan
        
        # 创建临时安装脚本
        $installScript = @"
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('正在安装Trae MCP服务器...');

// 方法1：尝试使用npm（如果可用）
try {
    const npm = require.resolve('npm/bin/npm-cli.js');
    const child = spawn('node', [npm, 'install', '@modelcontextprotocol/server-trae', '-g'], {
        stdio: 'inherit',
        shell: true
    });
    
    child.on('close', (code) => {
        if (code === 0) {
            console.log('安装成功！');
        } else {
            console.error('安装失败，退出码:', code);
        }
    });
} catch (error) {
    console.log('npm不可用，尝试其他方法...');
    
    // 方法2：直接下载并安装
    const installDir = path.join(process.env.APPDATA, 'npm', 'node_modules', '@modelcontextprotocol', 'server-trae');
    console.log('目标安装目录:', installDir);
    
    // 这里可以添加直接下载和安装的逻辑
    console.log('请手动安装: npm install @modelcontextprotocol/server-trae -g');
}
"@
        
        $tempFile = "temp-install.js"
        Set-Content -Path $tempFile -Value $installScript
        
        Write-Host "创建了临时安装脚本: $tempFile" -ForegroundColor Green
        Write-Host "请运行: node $tempFile" -ForegroundColor Yellow
    }
}

Write-Host "`n安装尝试完成！" -ForegroundColor Green
Write-Host "如果上述方法都失败，建议：" -ForegroundColor Yellow
Write-Host "1. 重新安装Node.js（从 https://nodejs.org/）" -ForegroundColor White
Write-Host "2. 安装时选择'Add to PATH'选项" -ForegroundColor White
Write-Host "3. 安装完成后运行: npm install @modelcontextprotocol/server-trae -g" -ForegroundColor White