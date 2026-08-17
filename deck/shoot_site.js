const { chromium } = require("playwright");
const SRC = "file:///home/user/Detty-December/site/index.html";
const OUT = "/home/user/Detty-December/deck/qa";
(async () => {
  const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium" });
  for (const [tag, w] of [["desk", 1280], ["mob", 390]]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(SRC, { waitUntil: "load" });
    await p.screenshot({ path: `${OUT}/site-${tag}.png`, fullPage: true });
    // horizontal overflow check
    const of = await p.evaluate(() => ({
      scroll: document.documentElement.scrollWidth,
      client: document.documentElement.clientWidth,
    }));
    console.log(tag, w, "scrollW", of.scroll, "clientW", of.client,
      of.scroll > of.client + 1 ? "*** H-OVERFLOW ***" : "ok");
    await p.close();
  }
  await b.close();
})();
