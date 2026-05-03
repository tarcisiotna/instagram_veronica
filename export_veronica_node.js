const playwright = require('playwright');
const fs = require('fs').promises;
const path = require('path');

const INPUT_HTML = "/home/tarcisio/instagram_veronica/slides/reeducacao-alimentar/carousel.html";
const OUTPUT_DIR = "/home/tarcisio/instagram_veronica/slides/reeducacao-alimentar";
const TOTAL_SLIDES = 7;
const VIEW_W = 420;
const VIEW_H = 525;
const SCALE = 1080 / 420;  // = 2.5714...

async function exportSlides() {
    const browser = await playwright.chromium.launch();
    const page = await browser.newPage({
        viewport: { width: VIEW_W, height: VIEW_H },
        deviceScaleFactor: SCALE,
    });

    const htmlContent = await fs.readFile(INPUT_HTML, 'utf-8');
    await page.setContent(htmlContent, { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);  // Wait for Google Fonts to load

    // Hide IG frame chrome, show only the slide viewport
    await page.evaluate(() => {
        document.querySelectorAll('.ig-header,.ig-dots,.ig-actions,.ig-caption')
            .forEach(el => el.style.display='none');

        const frame = document.querySelector('.ig-frame');
        frame.style.cssText = 'width:420px;height:525px;max-width:none;border-radius:0;box-shadow:none;overflow:hidden;margin:0;';

        const viewport = document.querySelector('.carousel-viewport');
        viewport.style.cssText = 'width:420px;height:525px;aspect-ratio:unset;overflow:hidden;cursor:default;';

        document.body.style.cssText = 'padding:0;margin:0;display:block;overflow:hidden;';
    });
    await page.waitForTimeout(500);

    for (let i = 0; i < TOTAL_SLIDES; i++) {
        await page.evaluate((idx) => {
            const track = document.querySelector('.carousel-track');
            track.style.transition = 'none';
            track.style.transform = 'translateX(' + (-idx * 420) + 'px)';
        }, i);
        await page.waitForTimeout(400);

        await page.screenshot({
            path: path.join(OUTPUT_DIR, `slide_${i+1}.png`),
            clip: { x: 0, y: 0, width: VIEW_W, height: VIEW_H }
        });
        console.log(`Exported slide ${i+1}/${TOTAL_SLIDES}`);
    }

    await browser.close();
    console.log('Slides exported successfully with high quality scaling!');
}

exportSlides().catch(console.error);