$ErrorActionPreference = 'Stop'

$path = 'd:\个人记录\obsidian-file\wjmber\LifeOS\6_Resources\2024-03工资核算_模拟数据.xlsx'
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
$wb = $excel.Workbooks.Add()
while ($wb.Worksheets.Count -lt 11) { $null = $wb.Worksheets.Add() }
$names = @(
  '员工基本信息表',
  '薪资基础表',
  '考勤原始数据表',
  '请假申请表',
  '加班申请表',
  '绩效考核表',
  '社保公积金基数表',
  '专项附加扣除表',
  '月度考勤汇总表',
  '工资计算明细表',
  '银行报盘表'
)
for ($i = 1; $i -le $names.Count; $i++) {
  $wb.Worksheets.Item($i).Name = $names[$i-1]
}

$employees = @(
  [pscustomobject]@{Id='E001';Name='张睿';Dept='技术部';Seq='技术序列';Grade=12000;Hire='2019-06-15';Card='6222021000000000011'},
  [pscustomobject]@{Id='E002';Name='李婧';Dept='产品部';Seq='技术序列';Grade=10000;Hire='2020-03-10';Card='6222021000000000028'},
  [pscustomobject]@{Id='E003';Name='王琪';Dept='销售部';Seq='营销序列';Grade=9000;Hire='2018-09-01';Card='6222021000000000035'},
  [pscustomobject]@{Id='E004';Name='赵敏';Dept='行政部';Seq='行政序列';Grade=8000;Hire='2021-01-20';Card='6222021000000000042'},
  [pscustomobject]@{Id='E005';Name='陈浩';Dept='技术部';Seq='技术序列';Grade=15000;Hire='2017-11-05';Card='6222021000000000059'},
  [pscustomobject]@{Id='E006';Name='周雅';Dept='产品部';Seq='技术序列';Grade=11000;Hire='2022-05-16';Card='6222021000000000066'},
  [pscustomobject]@{Id='E007';Name='孙航';Dept='销售部';Seq='营销序列';Grade=7000;Hire='2023-08-01';Card='6222021000000000073'},
  [pscustomobject]@{Id='E008';Name='胡琳';Dept='行政部';Seq='行政序列';Grade=6000;Hire='2020-12-12';Card='6222021000000000080'},
  [pscustomobject]@{Id='E009';Name='高峰';Dept='技术部';Seq='技术序列';Grade=14000;Hire='2018-03-25';Card='6222021000000000097'},
  [pscustomobject]@{Id='E010';Name='林雪';Dept='产品部';Seq='技术序列';Grade=9500;Hire='2019-02-18';Card='6222021000000000104'},
  [pscustomobject]@{Id='E011';Name='宋妍';Dept='行政部';Seq='行政序列';Grade=5000;Hire='2024-02-01';Card='6222021000000000111'},
  [pscustomobject]@{Id='E012';Name='徐哲';Dept='销售部';Seq='营销序列';Grade=8500;Hire='2020-07-07';Card='6222021000000000128'},
  [pscustomobject]@{Id='E013';Name='邓杰';Dept='技术部';Seq='技术序列';Grade=13000;Hire='2021-09-09';Card=''},
  [pscustomobject]@{Id='E014';Name='韩悦';Dept='产品部';Seq='技术序列';Grade=4000;Hire='2023-04-03';Card='6222021000000000142'},
  [pscustomobject]@{Id='E015';Name='罗楠';Dept='销售部';Seq='营销序列';Grade=16000;Hire='2016-10-30';Card='6222021000000000159'}
)

function Set-Table($ws, $header, $rows) {
  $rowCount = $rows.Count + 1
  $colCount = $header.Count
  $data = New-Object object[,] $rowCount, $colCount
  for ($c=0; $c -lt $colCount; $c++) { $data[0,$c] = $header[$c] }
  for ($r=0; $r -lt $rows.Count; $r++) {
    for ($c=0; $c -lt $colCount; $c++) { $data[$r+1,$c] = $rows[$r][$c] }
  }
  $ws.Range('A1').Resize($rowCount, $colCount).Value2 = $data
  $ws.Range('A1').EntireRow.Font.Bold = $true
  $ws.Columns.AutoFit() | Out-Null
}

$ws = $wb.Worksheets.Item('员工基本信息表')
$header = @('员工ID','姓名','部门','岗位序列','工资标准（薪级）','入职日期','银行卡号')
$rows = @()
foreach ($e in $employees) {
  $rows += ,@($e.Id, $e.Name, $e.Dept, $e.Seq, $e.Grade, [datetime]$e.Hire, $e.Card)
}
Set-Table $ws $header $rows
$ws.Columns.Item(6).NumberFormat = 'yyyy-mm-dd'

$ws = $wb.Worksheets.Item('薪资基础表')
$header = @('员工ID','基本工资系数','技能工资系数','住房补贴','医疗补贴','固定工资系数')
$rows = @()
$rand = New-Object System.Random(202403)
foreach ($e in $employees) {
  $base = [math]::Round(0.55 + $rand.NextDouble()*0.15, 2)
  $skill = [math]::Round(0.10 + $rand.NextDouble()*0.10, 2)
  $house = 600 + $rand.Next(0, 6)*100
  $medical = 200 + $rand.Next(0, 5)*50
  $rows += ,@($e.Id, $base, $skill, $house, $medical, 0.7)
}
Set-Table $ws $header $rows

$ws = $wb.Worksheets.Item('考勤原始数据表')
$header = @('日期','员工ID','上班打卡','下班打卡','迟到分钟','早退分钟','缺卡','补签')
$rows = New-Object System.Collections.Generic.List[object[]]
$start = Get-Date '2024-03-01'
$end = Get-Date '2024-03-31'
$workdays = @()
for ($d=$start; $d -le $end; $d=$d.AddDays(1)) {
  if ($d.DayOfWeek -ne 'Saturday' -and $d.DayOfWeek -ne 'Sunday') { $workdays += $d }
}
$rand = New-Object System.Random(20240315)
$lateOverrides = @{'E005|2024-03-12'=45; 'E009|2024-03-20'=35}
$missingOverrides = @{'E009|2024-03-18'=$true; 'E013|2024-03-08'=$true; 'E011|2024-03-22'=$true}
foreach ($e in $employees) {
  foreach ($day in $workdays) {
    $key = "{0}|{1}" -f $e.Id, $day.ToString('yyyy-MM-dd')
    $missing = $missingOverrides.ContainsKey($key) -or ($rand.NextDouble() -lt 0.015)
    if ($missing) {
      $rows.Add(@($day, $e.Id, $null, $null, 0, 0, 1, 0))
      continue
    }
    $startBase = $day.Date.AddHours(9.5)
    $endBase = $day.Date.AddHours(18.5)
    $startOffset = $rand.Next(-5, 41)
    if ($lateOverrides.ContainsKey($key)) { $startOffset = $lateOverrides[$key] }
    $endOffset = $rand.Next(-20, 21)
    $startTime = $startBase.AddMinutes($startOffset)
    $endTime = $endBase.AddMinutes($endOffset)
    $late = [math]::Max(0, [int][math]::Round(($startTime - $startBase).TotalMinutes))
    $early = [math]::Max(0, [int][math]::Round(($endBase - $endTime).TotalMinutes))
    $patch = if ($rand.NextDouble() -lt 0.02) { 1 } else { 0 }
    $rows.Add(@($day, $e.Id, $startTime, $endTime, $late, $early, 0, $patch))
  }
}
Set-Table $ws $header $rows
$ws.Columns.Item(1).NumberFormat = 'yyyy-mm-dd'
$ws.Columns.Item(3).NumberFormat = 'yyyy-mm-dd hh:mm'
$ws.Columns.Item(4).NumberFormat = 'yyyy-mm-dd hh:mm'

$ws = $wb.Worksheets.Item('请假申请表')
$header = @('申请ID','员工ID','请假类型','开始日期','结束日期','天数','备注')
$rows = @(
  @('L001','E003','事假',[datetime]'2024-03-05',[datetime]'2024-03-05',1,'家中事务'),
  @('L002','E004','病假',[datetime]'2024-03-11',[datetime]'2024-03-12',2,'感冒'),
  @('L003','E007','年假',[datetime]'2024-03-25',[datetime]'2024-03-26',2,'旅游'),
  @('L004','E010','事假',[datetime]'2024-03-18',[datetime]'2024-03-18',1,'孩子接送'),
  @('L005','E012','病假',[datetime]'2024-03-28',[datetime]'2024-03-28',1,'牙科'),
  @('L006','E014','事假',[datetime]'2024-03-08',[datetime]'2024-03-08',1,'证件办理'),
  @('L007','E015','年假',[datetime]'2024-03-14',[datetime]'2024-03-15',2,'婚礼'),
  @('L008','E001','病假',[datetime]'2024-03-27',[datetime]'2024-03-27',1,'发烧')
)
Set-Table $ws $header $rows
$ws.Columns.Item(4).NumberFormat = 'yyyy-mm-dd'
$ws.Columns.Item(5).NumberFormat = 'yyyy-mm-dd'

$ws = $wb.Worksheets.Item('加班申请表')
$header = @('申请ID','员工ID','日期','类型','小时','系数','加班费')
$rows = @(
  @('OT001','E002',[datetime]'2024-03-06','工作日',2,"=IF(D2='工作日',1.5,IF(D2='周末',2,3))","=E2*F2*(VLOOKUP(B2,'员工基本信息表'!A:G,5,0)/21.75/8)"),
  @('OT002','E005',[datetime]'2024-03-09','周末',6,"=IF(D3='工作日',1.5,IF(D3='周末',2,3))","=E3*F3*(VLOOKUP(B3,'员工基本信息表'!A:G,5,0)/21.75/8)"),
  @('OT003','E009',[datetime]'2024-03-10','周末',4,"=IF(D4='工作日',1.5,IF(D4='周末',2,3))","=E4*F4*(VLOOKUP(B4,'员工基本信息表'!A:G,5,0)/21.75/8)"),
  @('OT004','E001',[datetime]'2024-03-22','工作日',3,"=IF(D5='工作日',1.5,IF(D5='周末',2,3))","=E5*F5*(VLOOKUP(B5,'员工基本信息表'!A:G,5,0)/21.75/8)"),
  @('OT005','E012',[datetime]'2024-03-17','周末',5,"=IF(D6='工作日',1.5,IF(D6='周末',2,3))","=E6*F6*(VLOOKUP(B6,'员工基本信息表'!A:G,5,0)/21.75/8)"),
  @('OT006','E015',[datetime]'2024-03-30','法定节假日',8,"=IF(D7='工作日',1.5,IF(D7='周末',2,3))","=E7*F7*(VLOOKUP(B7,'员工基本信息表'!A:G,5,0)/21.75/8)")
)
Set-Table $ws $header $rows
$ws.Columns.Item(3).NumberFormat = 'yyyy-mm-dd'

$ws = $wb.Worksheets.Item('绩效考核表')
$header = @('员工ID','部门','绩效等级','系数')
$perfLevels = @(
  @('S',1.3),
  @('A',1.1),
  @('B',1.0),
  @('C',0.6),
  @('D',0)
)
$perfMap = @{
  'E001'='B';'E002'='A';'E003'='B';'E004'='B';'E005'='S';'E006'='A';'E007'='B';'E008'='C';'E009'='B';'E010'='B';'E011'='B';'E012'='C';'E013'='B';'E014'='D';'E015'='B'
}
$rows = @()
foreach ($e in $employees) {
  $level = $perfMap[$e.Id]
  $coef = ($perfLevels | Where-Object { $_[0] -eq $level })[0][1]
  $rows += ,@($e.Id, $e.Dept, $level, $coef)
}
Set-Table $ws $header $rows

$ws = $wb.Worksheets.Item('社保公积金基数表')
$header = @('员工ID','缴费基数','养老比例','医疗比例','失业比例','公积金比例','缴费下限','缴费上限')
$rows = @()
foreach ($e in $employees) {
  $rows += ,@($e.Id, '', 0.08, 0.02, 0.005, 0.10, 5000, 20000)
}
Set-Table $ws $header $rows

$ws = $wb.Worksheets.Item('专项附加扣除表')
$header = @('员工ID','子女教育','房贷利息','赡养老人','继续教育','住房租金','合计')
$rows = @(
  @('E001',1000,0,2000,0,0,'=SUM(B2:F2)'),
  @('E002',0,1000,0,0,0,'=SUM(B3:F3)'),
  @('E003',0,0,2000,0,0,'=SUM(B4:F4)'),
  @('E004',0,0,0,400,0,'=SUM(B5:F5)'),
  @('E005',1000,1000,0,0,0,'=SUM(B6:F6)'),
  @('E006',0,0,0,0,1500,'=SUM(B7:F7)'),
  @('E007',0,0,2000,0,0,'=SUM(B8:F8)'),
  @('E008',0,1000,0,0,0,'=SUM(B9:F9)'),
  @('E009',1000,0,0,0,0,'=SUM(B10:F10)'),
  @('E010',0,0,0,400,0,'=SUM(B11:F11)'),
  @('E011',0,0,2000,0,0,'=SUM(B12:F12)'),
  @('E012',0,1000,0,0,0,'=SUM(B13:F13)'),
  @('E013',0,0,0,0,1500,'=SUM(B14:F14)'),
  @('E014',0,0,0,400,0,'=SUM(B15:F15)'),
  @('E015',1000,0,2000,0,0,'=SUM(B16:F16)')
)
Set-Table $ws $header $rows

$ws = $wb.Worksheets.Item('月度考勤汇总表')
$header = @('员工ID','应出勤天数','实际出勤天数','迟到次数','迟到分钟','事假天数','病假天数','年假天数','旷工半天次数')
$rows = @()
$rowIndex = 2
foreach ($e in $employees) {
  $rows += ,@(
    $e.Id,
    '=NETWORKDAYS(DATE(2024,3,1),DATE(2024,3,31))',
    "=COUNTIFS('考勤原始数据表'!B:B,A$rowIndex,'考勤原始数据表'!C:C,""<>"")",
    "=COUNTIFS('考勤原始数据表'!B:B,A$rowIndex,'考勤原始数据表'!E:E,"">0"")",
    "=SUMIFS('考勤原始数据表'!E:E,'考勤原始数据表'!B:B,A$rowIndex)",
    "=SUMIFS('请假申请表'!F:F,'请假申请表'!B:B,A$rowIndex,'请假申请表'!C:C,'事假')",
    "=SUMIFS('请假申请表'!F:F,'请假申请表'!B:B,A$rowIndex,'请假申请表'!C:C,'病假')",
    "=SUMIFS('请假申请表'!F:F,'请假申请表'!B:B,A$rowIndex,'请假申请表'!C:C,'年假')",
    "=COUNTIFS('考勤原始数据表'!B:B,A$rowIndex,'考勤原始数据表'!E:E,"">30"")"
  )
  $rowIndex++
}
Set-Table $ws $header $rows

$ws = $wb.Worksheets.Item('工资计算明细表')
$header = @(
  '员工ID','姓名','部门','岗位序列','薪级','岗位序列系数','基本工资系数','技能工资系数','基本工资','技能工资',
  '住房补贴','医疗补贴','固定工资小计','固定工资系数','浮动工资系数','浮动工资基数','绩效等级','绩效系数','绩效工资',
  '工龄(月)','工龄工资','加班小时','加班费','应出勤天数','实际出勤天数','迟到次数','迟到分钟','事假天数','病假天数','年假天数',
  '旷工半天次数','事假扣款','病假扣款','旷工扣款','迟到扣款','考勤扣款合计','税前应发','社保缴费基数','养老','医疗','失业','公积金','社保公积金合计',
  '专项附加扣除','应纳税所得额','税率','速算扣除','个税','实发工资','银行卡号','异常标记'
)
$rows = @()
$rowIndex = 2
foreach ($e in $employees) {
  $rows += ,@(
    $e.Id,
    "=VLOOKUP(A$rowIndex,'员工基本信息表'!A:G,2,0)",
    "=VLOOKUP(A$rowIndex,'员工基本信息表'!A:G,3,0)",
    "=VLOOKUP(A$rowIndex,'员工基本信息表'!A:G,4,0)",
    "=VLOOKUP(A$rowIndex,'员工基本信息表'!A:G,5,0)",
    "=IF(D$rowIndex='技术序列',1.1,IF(D$rowIndex='营销序列',1.05,1.0))",
    "=VLOOKUP(A$rowIndex,'薪资基础表'!A:F,2,0)",
    "=VLOOKUP(A$rowIndex,'薪资基础表'!A:F,3,0)",
    "=E$rowIndex*F$rowIndex*G$rowIndex",
    "=E$rowIndex*F$rowIndex*H$rowIndex",
    "=VLOOKUP(A$rowIndex,'薪资基础表'!A:F,4,0)",
    "=VLOOKUP(A$rowIndex,'薪资基础表'!A:F,5,0)",
    "=(I$rowIndex+J$rowIndex+K$rowIndex+L$rowIndex)*VLOOKUP(A$rowIndex,'薪资基础表'!A:F,6,0)",
    "=VLOOKUP(A$rowIndex,'薪资基础表'!A:F,6,0)",
    0.3,
    "=E$rowIndex*O$rowIndex",
    "=VLOOKUP(A$rowIndex,'绩效考核表'!A:D,3,0)",
    "=VLOOKUP(A$rowIndex,'绩效考核表'!A:D,4,0)",
    "=P$rowIndex*R$rowIndex",
    "=DATEDIF(VLOOKUP(A$rowIndex,'员工基本信息表'!A:G,6,0),DATE(2024,3,31),'m')",
    "=MIN(T$rowIndex,120)*20",
    "=SUMIFS('加班申请表'!E:E,'加班申请表'!B:B,A$rowIndex)",
    "=SUMIFS('加班申请表'!G:G,'加班申请表'!B:B,A$rowIndex)",
    "=VLOOKUP(A$rowIndex,'月度考勤汇总表'!A:I,2,0)",
    "=VLOOKUP(A$rowIndex,'月度考勤汇总表'!A:I,3,0)",
    "=VLOOKUP(A$rowIndex,'月度考勤汇总表'!A:I,4,0)",
    "=VLOOKUP(A$rowIndex,'月度考勤汇总表'!A:I,5,0)",
    "=VLOOKUP(A$rowIndex,'月度考勤汇总表'!A:I,6,0)",
    "=VLOOKUP(A$rowIndex,'月度考勤汇总表'!A:I,7,0)",
    "=VLOOKUP(A$rowIndex,'月度考勤汇总表'!A:I,8,0)",
    "=VLOOKUP(A$rowIndex,'月度考勤汇总表'!A:I,9,0)",
    "=IF(X$rowIndex=0,0,ROUND(E$rowIndex/X$rowIndex*AB$rowIndex,2))",
    "=IF(X$rowIndex=0,0,ROUND(E$rowIndex/X$rowIndex*AC$rowIndex*0.5,2))",
    "=IF(X$rowIndex=0,0,ROUND(E$rowIndex/X$rowIndex*AD$rowIndex*0.5,2))",
    "=ROUNDUP(AA$rowIndex/10,0)*5",
    "=SUM(AE$rowIndex:AH$rowIndex)",
    "=M$rowIndex+S$rowIndex+U$rowIndex+W$rowIndex-AI$rowIndex",
    "=IF('社保公积金基数表'!B2<>'',VLOOKUP(A$rowIndex,'社保公积金基数表'!A:H,2,0),MIN(MAX(E$rowIndex,VLOOKUP(A$rowIndex,'社保公积金基数表'!A:H,7,0)),VLOOKUP(A$rowIndex,'社保公积金基数表'!A:H,8,0)))",
    "=AL$rowIndex*VLOOKUP(A$rowIndex,'社保公积金基数表'!A:H,3,0)",
    "=AL$rowIndex*VLOOKUP(A$rowIndex,'社保公积金基数表'!A:H,4,0)",
    "=AL$rowIndex*VLOOKUP(A$rowIndex,'社保公积金基数表'!A:H,5,0)",
    "=AL$rowIndex*VLOOKUP(A$rowIndex,'社保公积金基数表'!A:H,6,0)",
    "=SUM(AM$rowIndex:AP$rowIndex)",
    "=VLOOKUP(A$rowIndex,'专项附加扣除表'!A:G,7,0)",
    "=MAX(0,AJ$rowIndex-AQ$rowIndex-AR$rowIndex-5000)",
    "=IF(AS$rowIndex<=36000,0.03,IF(AS$rowIndex<=144000,0.1,IF(AS$rowIndex<=300000,0.2,IF(AS$rowIndex<=420000,0.25,IF(AS$rowIndex<=660000,0.3,IF(AS$rowIndex<=960000,0.35,0.45))))))",
    "=IF(AS$rowIndex<=36000,0,IF(AS$rowIndex<=144000,2520,IF(AS$rowIndex<=300000,16920,IF(AS$rowIndex<=420000,31920,IF(AS$rowIndex<=660000,52920,IF(AS$rowIndex<=960000,85920,181920))))))",
    "=AS$rowIndex*AT$rowIndex-AU$rowIndex",
    "=AJ$rowIndex-AQ$rowIndex-AV$rowIndex",
    "=VLOOKUP(A$rowIndex,'员工基本信息表'!A:G,7,0)",
    "=IF(OR(AW$rowIndex='',AX$rowIndex<0,AD$rowIndex>2,Q$rowIndex='D'),'异常','')"
  )
  $rowIndex++
}
Set-Table $ws $header $rows

$ws = $wb.Worksheets.Item('银行报盘表')
$header = @('银行卡号','实发金额','姓名','报盘格式')
$rows = @()
$rowIndex = 2
foreach ($e in $employees) {
  $rows += ,@(
    "=VLOOKUP(A$rowIndex-1,'工资计算明细表'!A:AY,50,0)",
    "=VLOOKUP(A$rowIndex-1,'工资计算明细表'!A:AY,49,0)",
    "=VLOOKUP(A$rowIndex-1,'工资计算明细表'!A:AY,2,0)",
    "=A$rowIndex&'|'&TEXT(B$rowIndex,'0.00')&'|'&C$rowIndex"
  )
  $rowIndex++
}
Set-Table $ws $header $rows

$wb.SaveAs($path)
$wb.Close($true)
$excel.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
Write-Output \"已生成: $path\"
