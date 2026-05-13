const playwright = require('playwright');
const fs = require('fs').promises;
const path = require('path');

const INPUT_HTML = process.argv[2] || "/home/tarcisio/instagram_veronica/slides/mitos-verdades-nutricao-oncologica/carousel.html";
const OUTPUT_DIR = process.argv[3] || path.dirname(INPUT_HTML);
const VIEW_W = 420;
const VIEW_H = 525;
const SCALE = 1080 / 420;  // = 2.5714...

async function exportSlides() {
    const browser = await playwright.chromium.launch();
    const page = await browser.newPage({
        viewport: { width: VIEW_W, height: VIEW_H },
        deviceScaleFactor: SCALE,
    });

    let htmlContent = await fs.readFile(INPUT_HTML, 'utf-8');
    
    // Embed all slide images as base64
    const htmlDir = path.dirname(INPUT_HTML);
    for (let slideNum = 1; slideNum <= 8; slideNum++) {
        const imgPath = path.join(htmlDir, `slide_${slideNum}.png`);
        try {
            const imgData = await fs.readFile(imgPath);
            const base64 = imgData.toString('base64');
            const mimeType = 'image/png';
            htmlContent = htmlContent.replace(
                `src="slide_${slideNum}.png"`,
                `src="data:${mimeType};base64,${base64}"`
            );
        } catch (e) {
            // Slide image not found, skip
        }
    }
    
    await page.setContent(htmlContent, { waitUntil: 'networkidle' });
    await page.waitForTimeout(3000);  // Wait for Google Fonts to load

    // Count total slides
    const TOTAL_SLIDES = await page.evaluate(() => {
        return document.querySelectorAll('.carousel-track .slide').length;
    });
    console.log(`Found ${TOTAL_SLIDES} slides`);

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
            
            // Add progress bar to all slides
            const slides = document.querySelectorAll('.carousel-track .slide');
            slides.forEach((slide, slideIdx) => {
                let bar = slide.querySelector('.progress-bar');
                if (!bar) {
                    bar = document.createElement('div');
                    bar.className = 'progress-bar';
                    bar.style.cssText = 'position:absolute;bottom:0;left:0;right:0;padding:16px 28px 28px;z-index:10;display:flex;align-items:center;gap:10px;background:linear-gradient(to top,rgba(0,0,0,0.7),transparent);';
                    const pct = ((slideIdx + 1) / slides.length) * 100;
                    const label = slideIdx === slides.length - 1 ? 'Fim' : `${slideIdx + 1}/${slides.length}`;
                    bar.innerHTML = '<div style="flex:1;height:3px;background:rgba(255,255,255,0.12);border-radius:2px;overflow:hidden;"><div style="height:100%;background:#fff;border-radius:2px;width:' + pct + '%"></div></div><span style="font-size:11px;color:rgba(255,255,255,0.4);font-weight:500;">' + label + '</span>';
                    slide.appendChild(bar);
                }
            });
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