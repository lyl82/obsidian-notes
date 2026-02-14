# OpenCode Superpowers Install — Completed

## Summary
- Cloned superpowers to D:\Documents\04_GitRepos\superpowers
- Linked plugin and skills into %USERPROFILE%\.config\opencode
- Ready to use after restarting OpenCode

## Paths
- Repo: D:\Documents\04_GitRepos\superpowers
- Plugin link: %USERPROFILE%\.config\opencode\plugins\superpowers.js → D:\Documents\04_GitRepos\superpowers\.opencode\plugins\superpowers.js
- Skills link: %USERPROFILE%\.config\opencode\skills\superpowers → D:\Documents\04_GitRepos\superpowers\skills

## Actions Executed (PowerShell)
```powershell
# Clone (in D:\Documents\04_GitRepos)
git clone https://github.com/obra/superpowers.git superpowers

# Ensure OpenCode config directories
$configRoot = Join-Path $env:USERPROFILE ".config\opencode"
New-Item -ItemType Directory -Path $configRoot -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $configRoot "plugins") -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $configRoot "skills") -Force | Out-Null

# Plugin symlink (fallback copies if symlink not permitted)
$pluginLink = Join-Path $configRoot "plugins\superpowers.js"
$pluginTarget = "D:\Documents\04_GitRepos\superpowers\.opencode\plugins\superpowers.js"
if (Test-Path $pluginLink) { Remove-Item $pluginLink -Force }
try { New-Item -ItemType SymbolicLink -Path $pluginLink -Target $pluginTarget -Force | Out-Null }
catch { Copy-Item $pluginTarget $pluginLink -Force }

# Skills symlink (fallback junction/copy)
$skillsLink = Join-Path $configRoot "skills\superpowers"
$skillsTarget = "D:\Documents\04_GitRepos\superpowers\skills"
if (Test-Path $skillsLink) { Remove-Item $skillsLink -Force -Recurse }
try { New-Item -ItemType SymbolicLink -Path $skillsLink -Target $skillsTarget -Force | Out-Null }
catch {
  try { New-Item -ItemType Junction -Path $skillsLink -Target $skillsTarget -Force | Out-Null }
  catch { Copy-Item $skillsTarget $skillsLink -Recurse -Force }
}
```

## Next Steps
- Restart OpenCode
- Ask: “do you have superpowers?”
- Use the native skill tool:
  - List skills: use skill tool to list skills
  - Load a skill: use skill tool to load superpowers/brainstorming

## Updating
```powershell
cd D:\Documents\04_GitRepos\superpowers
git pull
```

## Troubleshooting
- Plugin not loading
  1. Check link: ls -l %USERPROFILE%\.config\opencode\plugins\superpowers.js
  2. Check source: D:\Documents\04_GitRepos\superpowers\.opencode\plugins\superpowers.js
  3. Inspect OpenCode logs
- Skills not found
  1. Check link: ls -l %USERPROFILE%\.config\opencode\skills\superpowers
  2. Verify it points to D:\Documents\04_GitRepos\superpowers\skills
  3. Use the skill tool to list discovered skills

## References
- INSTALL.md: https://github.com/obra/superpowers/blob/main/.opencode/INSTALL.md
- Issues: https://github.com/obra/superpowers/issues
- Docs: https://github.com/obra/superpowers/blob/main/docs/README.opencode.md
