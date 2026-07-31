const { chromium } = require("playwright");
(async () => {
  const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  const p = await b.newPage({ viewport: { width: 1300, height: 760 } });
  await p.goto("file:///home/user/Detty-December/deck/qa/preview.html");
  const slides = await p.$$(".slide");
  for (let i = 0; i < slides.length; i++) {
    await slides[i].screenshot({ path: `/home/user/Detty-December/deck/qa/s${String(i + 1).padStart(2, "0")}.png` });
  }
  console.log("shot", slides.length);
  await b.close();
})();
