@echo off
chcp 65001 >nul
echo ========================================
echo ExifTool 视频元数据提取工具
echo ========================================
echo.

set EXIFTOOL=F:\downloadforsetup\exiftool-13.45_64\exiftool.exe

:menu
echo 请选择操作：
echo.
echo 1. 查看单个视频的完整元数据
echo 2. 提取单个视频的时间和GPS信息
echo 3. 批量导出所有视频元数据到CSV
echo 4. 查找包含GPS信息的视频
echo 5. 查找缺少时间戳的视频
echo 6. 导出JSON格式（便于程序处理）
echo 7. 退出
echo.
set /p choice=请输入选项 (1-7): 

if "%choice%"=="1" goto single_full
if "%choice%"=="2" goto single_gps
if "%choice%"=="3" goto batch_csv
if "%choice%"=="4" goto find_gps
if "%choice%"=="5" goto find_no_time
if "%choice%"=="6" goto export_json
if "%choice%"=="7" exit
goto menu

:single_full
echo.
set /p filepath=请输入视频文件完整路径: 
echo.
echo 正在读取元数据...
echo.
%EXIFTOOL% -G1 "%filepath%"
echo.
pause
goto menu

:single_gps
echo.
set /p filepath=请输入视频文件完整路径: 
echo.
echo 正在提取时间和GPS信息...
echo.
%EXIFTOOL% -CreateDate -ModifyDate -GPSLatitude -GPSLongitude -GPSPosition -Make -Model "%filepath%"
echo.
pause
goto menu

:batch_csv
echo.
set /p dirpath=请输入视频目录路径 (默认: D:\个人记录): 
if "%dirpath%"=="" set dirpath=D:\个人记录
set outputfile=%~dp0video_metadata_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.csv
set outputfile=%outputfile: =0%
echo.
echo 正在批量提取元数据...
echo 输出文件: %outputfile%
echo.
%EXIFTOOL% -csv -r -ext mp4 -ext mov -FileName -FileSize -CreateDate -ModifyDate -Duration -ImageWidth -ImageHeight -VideoFrameRate -GPSLatitude -GPSLongitude -Make -Model "%dirpath%" > "%outputfile%"
echo.
echo ✓ 完成！文件已保存到: %outputfile%
echo.
pause
goto menu

:find_gps
echo.
set /p dirpath=请输入视频目录路径 (默认: D:\个人记录): 
if "%dirpath%"=="" set dirpath=D:\个人记录
echo.
echo 正在查找包含GPS信息的视频...
echo.
%EXIFTOOL% -if "$GPSLatitude" -FileName -CreateDate -GPSPosition -r "%dirpath%"
echo.
pause
goto menu

:find_no_time
echo.
set /p dirpath=请输入视频目录路径 (默认: D:\个人记录): 
if "%dirpath%"=="" set dirpath=D:\个人记录
echo.
echo 正在查找缺少时间戳的视频...
echo.
%EXIFTOOL% -if "$CreateDate eq '0000:00:00 00:00:00' or not $CreateDate" -FileName -FileModifyDate -r "%dirpath%"
echo.
pause
goto menu

:export_json
echo.
set /p filepath=请输入视频文件完整路径: 
set outputfile=%filepath%.json
echo.
echo 正在导出JSON格式...
echo 输出文件: %outputfile%
echo.
%EXIFTOOL% -json -G "%filepath%" > "%outputfile%"
echo.
echo ✓ 完成！
echo.
pause
goto menu
