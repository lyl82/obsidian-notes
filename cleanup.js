const fs = require('fs');
const path = 'd:\\个人记录\\obsidian-file\\wjmber\\LifeOS\\1_ControlPlane\\关于bug\\历史记录-遗精及惊恐经历总结(性).md';

if (!fs.existsSync(path)) {
    console.error('File not found:', path);
    process.exit(1);
}

let content = fs.readFileSync(path, 'utf8');

// Remove Base64 images
content = content.replace(/!\[\]\(data:image\/[^)]+\)/g, '');

// Remove local file links
content = content.replace(/!\[\]\(file:\/\/\/[^)]+\)/g, '');

fs.writeFileSync(path, content, 'utf8');
console.log('Cleanup complete.');
