const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

async function exportSlides() {
  // Usar o HTML mais recente da pasta reeducacao-alimentar
  const htmlPath = path.join(__dirname, 'slides/reeducacao-alimentar/carousel_veronica.html');
  if (!fs.existsSync(htmlPath)) {
    console.error('HTML não encontrado:', htmlPath);
    return;
  }

  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // Configurar viewport para Instagram Story (1080x1350) com alta densidade
  await page.setViewportSize({ 
    width: 1080, 
    height: 1350,
    deviceScaleFactor: 2  // Essencial para qualidade retina/Instagram
  });
  
  // Carregar conteúdo HTML
  const htmlContent = fs.readFileSync(htmlPath, 'utf-8');
  await page.setContent(htmlContent, { waitUntil: 'networkidle' });
  
  // Aguardar carregamento de fontes e imagens
  await page.waitForTimeout(1000);
  
  // Criar diretório de saída
  const outputDir = path.join(__dirname, 'slides/reeducacao-alimentar');
  
  // Exportar 7 slides
  const totalSlides = 7;
  
  for (let i = 0; i < totalSlides; i++) {
    console.log(`Exportando slide ${i + 1}/${totalSlides}...`);
    
    // Navegar para o slide
    await page.evaluate((idx) => {
      if (window.goTo) window.goTo(idx);
    }, i);
    
    // Aguardar transição
    await page.waitForTimeout(800);
    
    // Capturar screenshot em alta qualidade
    await page.screenshot({
      path: path.join(outputDir, `slide-${i + 1}.png`),
      type: 'png',
      animations: 'disabled',
      // Capturar na resolução exata do Instagram
      clip: { x: 0, y: 0, width: 1080, height: 1350 }
    });
  }
  
  await browser.close();
  console.log(`Slides exportados com sucesso para: ${outputDir}`);
}

exportSlides().catch(console.error);
