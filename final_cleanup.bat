@echo off
echo ========================================
echo    Final Cleanup - Remove Unnecessary Files
echo ========================================
echo.

echo Removing unnecessary files while keeping essential agent system...
echo.

REM Remove cleanup scripts (already used)
if exist "cleanup_script.ps1" (
    echo Removing: cleanup_script.ps1
    del "cleanup_script.ps1"
    echo ✓ Deleted: cleanup_script.ps1
)

if exist "cleanup_script.bat" (
    echo Removing: cleanup_script.bat  
    del "cleanup_script.bat"
    echo ✓ Deleted: cleanup_script.bat
)

if exist "cleanup_agent_folder.bat" (
    echo Removing: cleanup_agent_folder.bat
    del "cleanup_agent_folder.bat" 
    echo ✓ Deleted: cleanup_agent_folder.bat
)

REM Remove old config-based crew file
if exist "crew_with_config.py" (
    echo Removing: crew_with_config.py (old version)
    del "crew_with_config.py"
    echo ✓ Deleted: crew_with_config.py
)

REM Remove testing and status files
if exist "system_status.py" (
    echo Removing: system_status.py
    del "system_status.py"
    echo ✓ Deleted: system_status.py
)

if exist "test_models.py" (
    echo Removing: test_models.py
    del "test_models.py"
    echo ✓ Deleted: test_models.py
)

echo.
echo ========================================
echo Final cleanup completed!
echo.
echo Your AI News Agents system now contains only essential files:
echo - src/ai_news_agents/ (main agent system)
echo - pyproject.toml (dependencies)
echo - uv.lock (lock file)
echo - README.md (documentation)
echo - news/ (output folder)
echo - knowledge/ (user preferences)
echo - Documentation guides
echo ========================================
pause
