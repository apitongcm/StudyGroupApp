import { test, expect } from '@playwright/test';
import { WEBSITEURL,DUMMY_USER, PASSWORDS} from './auth/constant';

test('Dictionary Attack', async ({ page }) => {
     //Case - Using the list of Passwords, confirm that rate limiting of request is working.
     //Judgement Criteria - confirm that login request will be disabled after 5 unsuccessful request.
    await page.goto(WEBSITEURL+'/login/');
    await expect(page).toHaveTitle('Login');

    for (const password of PASSWORDS){
        console.log(`Trying password: ${password}`);

        await page.getByTestId('tc-login-001').fill(DUMMY_USER.USERNAME);
        await page.getByTestId('tc-login-002').fill(password);
        await page.getByTestId('tc-login-003').click(); //Login Button

        const url = page.url();
        if (!(url.includes('/login/'))) {
            console.log(`SUCCESS: Password is ${password}`);
            break; 
        }

        await expect(page.getByTestId('tc-login-004')).toBeVisible();
    }

    await expect(page.getByTestId('tc-login-004')).toHaveText('Too many failed login attempts. Try again later.');
})