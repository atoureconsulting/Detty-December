const {chromium} = require('playwright');
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const p = await b.newPage({viewport:{width:1160,height:900}, deviceScaleFactor:2});
  await p.goto('file://' + __dirname + '/bbb-deck-v8.html');
  await p.waitForLoadState('networkidle');
  await p.waitForTimeout(1200);
  const n = await p.locator('section.s').count();
  const issues = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('section.s').forEach((s, i) => {
      const no = i + 1;
      const sr = s.getBoundingClientRect();
      // 1. anything spilling past the slide frame
      s.querySelectorAll('*').forEach(el => {
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return;
        if (r.right > sr.right + 1.5 || r.left < sr.left - 1.5 ||
            r.bottom > sr.bottom + 1.5 || r.top < sr.top - 1.5) {
          const t = (el.textContent || '').trim().slice(0, 42);
          out.push(`p${no} SPILL <${el.className || el.tagName}> "${t}"`);
        }
        if (el.scrollHeight - el.clientHeight > 2 && getComputedStyle(el).overflow !== 'visible')
          out.push(`p${no} CLIP <${el.className || el.tagName}> ${el.scrollHeight - el.clientHeight}px`);
      });
      // 2. text blocks overlapping each other
      const leaves = [...s.querySelectorAll('p,h1,h2,li,blockquote,.hand,.kick,.act-t,.act-s,.fig,.lab,.an,.ad,.attr,.masthead,.cl1,.cl2')]
        .filter(e => e.getBoundingClientRect().height > 0);
      for (let a = 0; a < leaves.length; a++) for (let c = a + 1; c < leaves.length; c++) {
        const A = leaves[a], B = leaves[c];
        if (A.contains(B) || B.contains(A)) continue;
        const x = A.getBoundingClientRect(), y = B.getBoundingClientRect();
        const ox = Math.min(x.right, y.right) - Math.max(x.left, y.left);
        const oy = Math.min(x.bottom, y.bottom) - Math.max(x.top, y.top);
        if (ox > 3 && oy > 3)
          out.push(`p${no} OVERLAP "${A.textContent.trim().slice(0,22)}" / "${B.textContent.trim().slice(0,22)}"`);
      }
    });
    return out;
  });
  console.log('slides:', n);
  console.log(issues.length ? issues.join('\n') : 'clean');
  for (let i = 0; i < n; i++)
    await p.locator('section.s').nth(i).screenshot({path:`v8-${i+1}.png`});
  await b.close();
})();
