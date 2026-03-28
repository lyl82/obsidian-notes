const fs = require('fs');
const path = require('path');

const outputPath = path.join(__dirname, '2024-03工资核算_模拟数据.xml');

function xmlEscape(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function cell(value, type = 'String', formula = null) {
  const formulaAttr = formula ? ` ss:Formula="${xmlEscape(formula)}"` : '';
  if (value === null || value === undefined) {
    return `<Cell${formulaAttr}/>`;
  }
  return `<Cell${formulaAttr}><Data ss:Type="${type}">${xmlEscape(value)}</Data></Cell>`;
}

function row(cells) {
  return `<Row>${cells.join('')}</Row>`;
}

function formatDate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}T00:00:00.000`;
}

function formatDateTime(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, '0');
  const d = String(date.getDate()).padStart(2, '0');
  const hh = String(date.getHours()).padStart(2, '0');
  const mm = String(date.getMinutes()).padStart(2, '0');
  const ss = String(date.getSeconds()).padStart(2, '0');
  return `${y}-${m}-${d}T${hh}:${mm}:${ss}.000`;
}

function rng(seed) {
  let s = seed;
  return () => {
    s = (s * 9301 + 49297) % 233280;
    return s / 233280;
  };
}

const employees = [
  { id: 'E001', name: '张睿', dept: '技术部', seq: '技术序列', grade: 12000, hire: '2019-06-15', card: '6222021000000000011' },
  { id: 'E002', name: '李婧', dept: '产品部', seq: '技术序列', grade: 10000, hire: '2020-03-10', card: '6222021000000000028' },
  { id: 'E003', name: '王琪', dept: '销售部', seq: '营销序列', grade: 9000, hire: '2018-09-01', card: '6222021000000000035' },
  { id: 'E004', name: '赵敏', dept: '行政部', seq: '行政序列', grade: 8000, hire: '2021-01-20', card: '6222021000000000042' },
  { id: 'E005', name: '陈浩', dept: '技术部', seq: '技术序列', grade: 15000, hire: '2017-11-05', card: '6222021000000000059' },
  { id: 'E006', name: '周雅', dept: '产品部', seq: '技术序列', grade: 11000, hire: '2022-05-16', card: '6222021000000000066' },
  { id: 'E007', name: '孙航', dept: '销售部', seq: '营销序列', grade: 7000, hire: '2023-08-01', card: '6222021000000000073' },
  { id: 'E008', name: '胡琳', dept: '行政部', seq: '行政序列', grade: 6000, hire: '2020-12-12', card: '6222021000000000080' },
  { id: 'E009', name: '高峰', dept: '技术部', seq: '技术序列', grade: 14000, hire: '2018-03-25', card: '6222021000000000097' },
  { id: 'E010', name: '林雪', dept: '产品部', seq: '技术序列', grade: 9500, hire: '2019-02-18', card: '6222021000000000104' },
  { id: 'E011', name: '宋妍', dept: '行政部', seq: '行政序列', grade: 5000, hire: '2024-02-01', card: '6222021000000000111' },
  { id: 'E012', name: '徐哲', dept: '销售部', seq: '营销序列', grade: 8500, hire: '2020-07-07', card: '6222021000000000128' },
  { id: 'E013', name: '邓杰', dept: '技术部', seq: '技术序列', grade: 13000, hire: '2021-09-09', card: '' },
  { id: 'E014', name: '韩悦', dept: '产品部', seq: '技术序列', grade: 4000, hire: '2023-04-03', card: '6222021000000000142' },
  { id: 'E015', name: '罗楠', dept: '销售部', seq: '营销序列', grade: 16000, hire: '2016-10-30', card: '6222021000000000159' }
];

const workdays = [];
for (let d = new Date('2024-03-01'); d <= new Date('2024-03-31'); d.setDate(d.getDate() + 1)) {
  const day = d.getDay();
  if (day !== 0 && day !== 6) {
    workdays.push(new Date(d));
  }
}

const random = rng(20240315);
const lateOverrides = new Map([
  ['E005|2024-03-12', 45],
  ['E009|2024-03-20', 35]
]);
const missingOverrides = new Set(['E009|2024-03-18', 'E013|2024-03-08', 'E011|2024-03-22']);

const sheets = [];

function pushSheet(name, rows) {
  const table = rows.join('');
  sheets.push(`<Worksheet ss:Name="${xmlEscape(name)}"><Table>${table}</Table></Worksheet>`);
}

const sheet1 = [];
sheet1.push(row([
  cell('员工ID'), cell('姓名'), cell('部门'), cell('岗位序列'), cell('工资标准（薪级）'), cell('入职日期'), cell('银行卡号')
]));
for (const e of employees) {
  sheet1.push(row([
    cell(e.id),
    cell(e.name),
    cell(e.dept),
    cell(e.seq),
    cell(e.grade, 'Number'),
    cell(formatDate(new Date(e.hire)), 'DateTime'),
    cell(e.card)
  ]));
}
pushSheet('员工基本信息表', sheet1);

const randomBase = rng(202403);
const sheet2 = [];
sheet2.push(row([
  cell('员工ID'), cell('基本工资系数'), cell('技能工资系数'), cell('住房补贴'), cell('医疗补贴'), cell('固定工资系数')
]));
for (const e of employees) {
  const base = Math.round((0.55 + randomBase() * 0.15) * 100) / 100;
  const skill = Math.round((0.10 + randomBase() * 0.10) * 100) / 100;
  const house = 600 + Math.floor(randomBase() * 6) * 100;
  const medical = 200 + Math.floor(randomBase() * 5) * 50;
  sheet2.push(row([
    cell(e.id),
    cell(base, 'Number'),
    cell(skill, 'Number'),
    cell(house, 'Number'),
    cell(medical, 'Number'),
    cell(0.7, 'Number')
  ]));
}
pushSheet('薪资基础表', sheet2);

const sheet3 = [];
sheet3.push(row([
  cell('日期'), cell('员工ID'), cell('上班打卡'), cell('下班打卡'), cell('迟到分钟'), cell('早退分钟'), cell('缺卡'), cell('补签')
]));
for (const e of employees) {
  for (const day of workdays) {
    const key = `${e.id}|${day.toISOString().slice(0, 10)}`;
    const missing = missingOverrides.has(key) || random() < 0.015;
    if (missing) {
      sheet3.push(row([
        cell(formatDate(day), 'DateTime'),
        cell(e.id),
        cell(null),
        cell(null),
        cell(0, 'Number'),
        cell(0, 'Number'),
        cell(1, 'Number'),
        cell(0, 'Number')
      ]));
      continue;
    }
    const startBase = new Date(day);
    startBase.setHours(9, 30, 0, 0);
    const endBase = new Date(day);
    endBase.setHours(18, 30, 0, 0);
    let startOffset = Math.floor(random() * 46) - 5;
    if (lateOverrides.has(key)) startOffset = lateOverrides.get(key);
    const endOffset = Math.floor(random() * 41) - 20;
    const startTime = new Date(startBase.getTime() + startOffset * 60000);
    const endTime = new Date(endBase.getTime() + endOffset * 60000);
    const late = Math.max(0, Math.round((startTime - startBase) / 60000));
    const early = Math.max(0, Math.round((endBase - endTime) / 60000));
    const patch = random() < 0.02 ? 1 : 0;
    sheet3.push(row([
      cell(formatDate(day), 'DateTime'),
      cell(e.id),
      cell(formatDateTime(startTime), 'DateTime'),
      cell(formatDateTime(endTime), 'DateTime'),
      cell(late, 'Number'),
      cell(early, 'Number'),
      cell(0, 'Number'),
      cell(patch, 'Number')
    ]));
  }
}
pushSheet('考勤原始数据表', sheet3);

const sheet4 = [];
sheet4.push(row([
  cell('申请ID'), cell('员工ID'), cell('请假类型'), cell('开始日期'), cell('结束日期'), cell('天数'), cell('备注')
]));
const leaves = [
  ['L001', 'E003', '事假', '2024-03-05', '2024-03-05', 1, '家中事务'],
  ['L002', 'E004', '病假', '2024-03-11', '2024-03-12', 2, '感冒'],
  ['L003', 'E007', '年假', '2024-03-25', '2024-03-26', 2, '旅游'],
  ['L004', 'E010', '事假', '2024-03-18', '2024-03-18', 1, '孩子接送'],
  ['L005', 'E012', '病假', '2024-03-28', '2024-03-28', 1, '牙科'],
  ['L006', 'E014', '事假', '2024-03-08', '2024-03-08', 1, '证件办理'],
  ['L007', 'E015', '年假', '2024-03-14', '2024-03-15', 2, '婚礼'],
  ['L008', 'E001', '病假', '2024-03-27', '2024-03-27', 1, '发烧']
];
for (const l of leaves) {
  sheet4.push(row([
    cell(l[0]),
    cell(l[1]),
    cell(l[2]),
    cell(formatDate(new Date(l[3])), 'DateTime'),
    cell(formatDate(new Date(l[4])), 'DateTime'),
    cell(l[5], 'Number'),
    cell(l[6])
  ]));
}
pushSheet('请假申请表', sheet4);

const sheet5 = [];
sheet5.push(row([
  cell('申请ID'), cell('员工ID'), cell('日期'), cell('类型'), cell('小时'), cell('系数'), cell('加班费')
]));
const overtimes = [
  ['OT001', 'E002', '2024-03-06', '工作日', 2],
  ['OT002', 'E005', '2024-03-09', '周末', 6],
  ['OT003', 'E009', '2024-03-10', '周末', 4],
  ['OT004', 'E001', '2024-03-22', '工作日', 3],
  ['OT005', 'E012', '2024-03-17', '周末', 5],
  ['OT006', 'E015', '2024-03-30', '法定节假日', 8]
];
overtimes.forEach((o, idx) => {
  const r = idx + 2;
  sheet5.push(row([
    cell(o[0]),
    cell(o[1]),
    cell(formatDate(new Date(o[2])), 'DateTime'),
    cell(o[3]),
    cell(o[4], 'Number'),
    cell(0, 'Number', `=IF(D${r}="工作日",1.5,IF(D${r}="周末",2,3))`),
    cell(0, 'Number', `=E${r}*F${r}*(VLOOKUP(B${r},'员工基本信息表'!A:G,5,0)/21.75/8)`)
  ]));
});
pushSheet('加班申请表', sheet5);

const sheet6 = [];
sheet6.push(row([cell('员工ID'), cell('部门'), cell('绩效等级'), cell('系数')]));
const perfMap = {
  E001: 'B', E002: 'A', E003: 'B', E004: 'B', E005: 'S',
  E006: 'A', E007: 'B', E008: 'C', E009: 'B', E010: 'B',
  E011: 'B', E012: 'C', E013: 'B', E014: 'D', E015: 'B'
};
const perfCoef = { S: 1.3, A: 1.1, B: 1.0, C: 0.6, D: 0 };
for (const e of employees) {
  sheet6.push(row([
    cell(e.id),
    cell(e.dept),
    cell(perfMap[e.id]),
    cell(perfCoef[perfMap[e.id]], 'Number')
  ]));
}
pushSheet('绩效考核表', sheet6);

const sheet7 = [];
sheet7.push(row([
  cell('员工ID'), cell('缴费基数'), cell('养老比例'), cell('医疗比例'), cell('失业比例'), cell('公积金比例'), cell('缴费下限'), cell('缴费上限')
]));
for (const e of employees) {
  sheet7.push(row([
    cell(e.id),
    cell('', 'String'),
    cell(0.08, 'Number'),
    cell(0.02, 'Number'),
    cell(0.005, 'Number'),
    cell(0.10, 'Number'),
    cell(5000, 'Number'),
    cell(20000, 'Number')
  ]));
}
pushSheet('社保公积金基数表', sheet7);

const sheet8 = [];
sheet8.push(row([
  cell('员工ID'), cell('子女教育'), cell('房贷利息'), cell('赡养老人'), cell('继续教育'), cell('住房租金'), cell('合计')
]));
const deductions = [
  ['E001', 1000, 0, 2000, 0, 0],
  ['E002', 0, 1000, 0, 0, 0],
  ['E003', 0, 0, 2000, 0, 0],
  ['E004', 0, 0, 0, 400, 0],
  ['E005', 1000, 1000, 0, 0, 0],
  ['E006', 0, 0, 0, 0, 1500],
  ['E007', 0, 0, 2000, 0, 0],
  ['E008', 0, 1000, 0, 0, 0],
  ['E009', 1000, 0, 0, 0, 0],
  ['E010', 0, 0, 0, 400, 0],
  ['E011', 0, 0, 2000, 0, 0],
  ['E012', 0, 1000, 0, 0, 0],
  ['E013', 0, 0, 0, 0, 1500],
  ['E014', 0, 0, 0, 400, 0],
  ['E015', 1000, 0, 2000, 0, 0]
];
deductions.forEach((d, idx) => {
  const r = idx + 2;
  sheet8.push(row([
    cell(d[0]),
    cell(d[1], 'Number'),
    cell(d[2], 'Number'),
    cell(d[3], 'Number'),
    cell(d[4], 'Number'),
    cell(d[5], 'Number'),
    cell(0, 'Number', `=SUM(B${r}:F${r})`)
  ]));
});
pushSheet('专项附加扣除表', sheet8);

const sheet9 = [];
sheet9.push(row([
  cell('员工ID'), cell('应出勤天数'), cell('实际出勤天数'), cell('迟到次数'), cell('迟到分钟'), cell('事假天数'), cell('病假天数'), cell('年假天数'), cell('旷工半天次数')
]));
for (let i = 0; i < employees.length; i++) {
  const r = i + 2;
  sheet9.push(row([
    cell(employees[i].id),
    cell(0, 'Number', '=NETWORKDAYS(DATE(2024,3,1),DATE(2024,3,31))'),
    cell(0, 'Number', `=COUNTIFS('考勤原始数据表'!B:B,A${r},'考勤原始数据表'!C:C,"<>")`),
    cell(0, 'Number', `=COUNTIFS('考勤原始数据表'!B:B,A${r},'考勤原始数据表'!E:E,">0")`),
    cell(0, 'Number', `=SUMIFS('考勤原始数据表'!E:E,'考勤原始数据表'!B:B,A${r})`),
    cell(0, 'Number', `=SUMIFS('请假申请表'!F:F,'请假申请表'!B:B,A${r},'请假申请表'!C:C,"事假")`),
    cell(0, 'Number', `=SUMIFS('请假申请表'!F:F,'请假申请表'!B:B,A${r},'请假申请表'!C:C,"病假")`),
    cell(0, 'Number', `=SUMIFS('请假申请表'!F:F,'请假申请表'!B:B,A${r},'请假申请表'!C:C,"年假")`),
    cell(0, 'Number', `=COUNTIFS('考勤原始数据表'!B:B,A${r},'考勤原始数据表'!E:E,">30")`)
  ]));
}
pushSheet('月度考勤汇总表', sheet9);

const sheet10 = [];
sheet10.push(row([
  cell('员工ID'), cell('姓名'), cell('部门'), cell('岗位序列'), cell('薪级'), cell('岗位序列系数'), cell('基本工资系数'), cell('技能工资系数'), cell('基本工资'), cell('技能工资'),
  cell('住房补贴'), cell('医疗补贴'), cell('固定工资小计'), cell('固定工资系数'), cell('浮动工资系数'), cell('浮动工资基数'), cell('绩效等级'), cell('绩效系数'), cell('绩效工资'),
  cell('工龄(月)'), cell('工龄工资'), cell('加班小时'), cell('加班费'), cell('应出勤天数'), cell('实际出勤天数'), cell('迟到次数'), cell('迟到分钟'), cell('事假天数'), cell('病假天数'), cell('年假天数'),
  cell('旷工半天次数'), cell('事假扣款'), cell('病假扣款'), cell('旷工扣款'), cell('迟到扣款'), cell('考勤扣款合计'), cell('税前应发'), cell('社保缴费基数'), cell('养老'), cell('医疗'), cell('失业'), cell('公积金'), cell('社保公积金合计'),
  cell('专项附加扣除'), cell('应纳税所得额'), cell('税率'), cell('速算扣除'), cell('个税'), cell('实发工资'), cell('银行卡号'), cell('异常标记')
]));
for (let i = 0; i < employees.length; i++) {
  const r = i + 2;
  sheet10.push(row([
    cell(employees[i].id),
    cell('', 'String', `=VLOOKUP(A${r},'员工基本信息表'!A:G,2,0)`),
    cell('', 'String', `=VLOOKUP(A${r},'员工基本信息表'!A:G,3,0)`),
    cell('', 'String', `=VLOOKUP(A${r},'员工基本信息表'!A:G,4,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'员工基本信息表'!A:G,5,0)`),
    cell(0, 'Number', `=IF(D${r}="技术序列",1.1,IF(D${r}="营销序列",1.05,1.0))`),
    cell(0, 'Number', `=VLOOKUP(A${r},'薪资基础表'!A:F,2,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'薪资基础表'!A:F,3,0)`),
    cell(0, 'Number', `=E${r}*F${r}*G${r}`),
    cell(0, 'Number', `=E${r}*F${r}*H${r}`),
    cell(0, 'Number', `=VLOOKUP(A${r},'薪资基础表'!A:F,4,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'薪资基础表'!A:F,5,0)`),
    cell(0, 'Number', `=(I${r}+J${r}+K${r}+L${r})*VLOOKUP(A${r},'薪资基础表'!A:F,6,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'薪资基础表'!A:F,6,0)`),
    cell(0.3, 'Number'),
    cell(0, 'Number', `=E${r}*O${r}`),
    cell('', 'String', `=VLOOKUP(A${r},'绩效考核表'!A:D,3,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'绩效考核表'!A:D,4,0)`),
    cell(0, 'Number', `=P${r}*R${r}`),
    cell(0, 'Number', `=DATEDIF(VLOOKUP(A${r},'员工基本信息表'!A:G,6,0),DATE(2024,3,31),"m")`),
    cell(0, 'Number', `=MIN(T${r},120)*20`),
    cell(0, 'Number', `=SUMIFS('加班申请表'!E:E,'加班申请表'!B:B,A${r})`),
    cell(0, 'Number', `=SUMIFS('加班申请表'!G:G,'加班申请表'!B:B,A${r})`),
    cell(0, 'Number', `=VLOOKUP(A${r},'月度考勤汇总表'!A:I,2,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'月度考勤汇总表'!A:I,3,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'月度考勤汇总表'!A:I,4,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'月度考勤汇总表'!A:I,5,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'月度考勤汇总表'!A:I,6,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'月度考勤汇总表'!A:I,7,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'月度考勤汇总表'!A:I,8,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r},'月度考勤汇总表'!A:I,9,0)`),
    cell(0, 'Number', `=IF(X${r}=0,0,ROUND(E${r}/X${r}*AB${r},2))`),
    cell(0, 'Number', `=IF(X${r}=0,0,ROUND(E${r}/X${r}*AC${r}*0.5,2))`),
    cell(0, 'Number', `=IF(X${r}=0,0,ROUND(E${r}/X${r}*AD${r}*0.5,2))`),
    cell(0, 'Number', `=ROUNDUP(AA${r}/10,0)*5`),
    cell(0, 'Number', `=SUM(AE${r}:AH${r})`),
    cell(0, 'Number', `=M${r}+S${r}+U${r}+W${r}-AI${r}`),
    cell(0, 'Number', `=IF('社保公积金基数表'!B2<>"",VLOOKUP(A${r},'社保公积金基数表'!A:H,2,0),MIN(MAX(E${r},VLOOKUP(A${r},'社保公积金基数表'!A:H,7,0)),VLOOKUP(A${r},'社保公积金基数表'!A:H,8,0)))`),
    cell(0, 'Number', `=AL${r}*VLOOKUP(A${r},'社保公积金基数表'!A:H,3,0)`),
    cell(0, 'Number', `=AL${r}*VLOOKUP(A${r},'社保公积金基数表'!A:H,4,0)`),
    cell(0, 'Number', `=AL${r}*VLOOKUP(A${r},'社保公积金基数表'!A:H,5,0)`),
    cell(0, 'Number', `=AL${r}*VLOOKUP(A${r},'社保公积金基数表'!A:H,6,0)`),
    cell(0, 'Number', `=SUM(AM${r}:AP${r})`),
    cell(0, 'Number', `=VLOOKUP(A${r},'专项附加扣除表'!A:G,7,0)`),
    cell(0, 'Number', `=MAX(0,AJ${r}-AQ${r}-AR${r}-5000)`),
    cell(0, 'Number', `=IF(AS${r}<=36000,0.03,IF(AS${r}<=144000,0.1,IF(AS${r}<=300000,0.2,IF(AS${r}<=420000,0.25,IF(AS${r}<=660000,0.3,IF(AS${r}<=960000,0.35,0.45))))))`),
    cell(0, 'Number', `=IF(AS${r}<=36000,0,IF(AS${r}<=144000,2520,IF(AS${r}<=300000,16920,IF(AS${r}<=420000,31920,IF(AS${r}<=660000,52920,IF(AS${r}<=960000,85920,181920))))))`),
    cell(0, 'Number', `=AS${r}*AT${r}-AU${r}`),
    cell(0, 'Number', `=AJ${r}-AQ${r}-AV${r}`),
    cell('', 'String', `=VLOOKUP(A${r},'员工基本信息表'!A:G,7,0)`),
    cell('', 'String', `=IF(OR(AW${r}="",AX${r}<0,AD${r}>2,Q${r}="D"),"异常","")`)
  ]));
}
pushSheet('工资计算明细表', sheet10);

const sheet11 = [];
sheet11.push(row([cell('银行卡号'), cell('实发金额'), cell('姓名'), cell('报盘格式')]));
for (let i = 0; i < employees.length; i++) {
  const r = i + 2;
  sheet11.push(row([
    cell('', 'String', `=VLOOKUP(A${r}-1,'工资计算明细表'!A:AY,50,0)`),
    cell(0, 'Number', `=VLOOKUP(A${r}-1,'工资计算明细表'!A:AY,49,0)`),
    cell('', 'String', `=VLOOKUP(A${r}-1,'工资计算明细表'!A:AY,2,0)`),
    cell('', 'String', `=A${r}&"|"&TEXT(B${r},"0.00")&"|"&C${r}`)
  ]));
}
pushSheet('银行报盘表', sheet11);

const workbook = `<?xml version="1.0"?>\n<?mso-application progid="Excel.Sheet"?>\n<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"\n xmlns:o="urn:schemas-microsoft-com:office:office"\n xmlns:x="urn:schemas-microsoft-com:office:excel"\n xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"\n xmlns:html="http://www.w3.org/TR/REC-html40">\n${sheets.join('\n')}\n</Workbook>\n`;

fs.writeFileSync(outputPath, workbook, 'utf8');
console.log(`已生成: ${outputPath}`);
