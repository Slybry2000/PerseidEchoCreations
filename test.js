import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

async function testWebsite() {
    const browser = await chromium.launch({ headless: true });
    const context = await browser.newContext();
    const page = await context.newPage();

    const errors = [];
    const warnings = [];

    // Capture console messages
    page.on('console', msg => {
        if (msg.type() === 'error') {
            errors.push(msg.text());
        } else if (msg.type() === 'warning') {
            warnings.push(msg.text());
        }
    });

    // Capture page errors
    page.on('pageerror', err => {
        errors.push(err.message);
    });

    try {
        // Load the page
        const filePath = join(__dirname, 'index.html');
        await page.goto(`file://${filePath}`, { waitUntil: 'networkidle' });
        console.log('✓ Page loaded successfully');

        // Check key elements exist
        const checks = [
            { selector: '.nav', name: 'Navigation' },
            { selector: '.hero', name: 'Hero section' },
            { selector: '#what-we-build', name: 'What We Build section' },
            { selector: '#featured-products', name: 'Featured Products section' },
            { selector: '#our-approach', name: 'Our Approach section' },
            { selector: '#how-we-work', name: 'How We Work section' },
            { selector: '#transparency', name: 'Transparency section' },
            { selector: '#about', name: 'About section' },
            { selector: '#founder', name: 'Founder section' },
            { selector: '#contact', name: 'Contact section' },
            { selector: 'footer', name: 'Footer' }
        ];

        for (const check of checks) {
            const element = await page.$(check.selector);
            if (element) {
                console.log(`✓ ${check.name} found`);
            } else {
                errors.push(`${check.name} not found`);
            }
        }

        // Check images loaded
        const images = await page.$$('img');
        console.log(`✓ Found ${images.length} images`);

        // Test navigation links
        const navLinks = await page.$$('.nav-links a');
        console.log(`✓ Found ${navLinks.length} navigation links`);

        // Check form exists
        const form = await page.$('#contact-form');
        if (form) {
            console.log('✓ Contact form found');
        } else {
            errors.push('Contact form not found');
        }

        // Test mobile menu button
        const mobileMenuBtn = await page.$('.mobile-menu-btn');
        if (mobileMenuBtn) {
            console.log('✓ Mobile menu button found');
        } else {
            errors.push('Mobile menu button not found');
        }

        // Report results
        console.log('\n--- Test Results ---');
        if (errors.length === 0) {
            console.log('✓ All tests passed! No errors detected.');
        } else {
            console.log(`✗ ${errors.length} error(s) found:`);
            errors.forEach(err => console.log(`  - ${err}`));
        }

        if (warnings.length > 0) {
            console.log(`⚠ ${warnings.length} warning(s):`);
            warnings.forEach(warn => console.log(`  - ${warn}`));
        }

    } catch (err) {
        console.error('Test failed:', err.message);
        process.exit(1);
    } finally {
        await browser.close();
    }

    // Exit with error code if errors found
    process.exit(errors.length > 0 ? 1 : 0);
}

testWebsite();
