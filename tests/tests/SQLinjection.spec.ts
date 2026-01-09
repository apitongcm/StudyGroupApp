import { test, expect } from '@playwright/test';
import { WEBSITEURL,SQLPayload,UNREGISTERED_DUMMY} from './auth/constant';

test('SQL Injection: Login Bypass Attempt', async({page}) =>{
    //Case - Perform sql injection to confirm if it is possible to bypass the login authentication. 
    //Judgment Criteria - Confirm that it will not be able to bypass authentication, cannot access/tamper database and will remain in the login page.
    await page.goto(WEBSITEURL+'/login/');
    await expect(page).toHaveTitle('Login');

    for (const payload of SQLPayload){

        console.log(`Trying Username: ${payload}`);
        
        await page.getByTestId('tc-login-001').fill(payload);
        await page.getByTestId('tc-login-002').fill(UNREGISTERED_DUMMY.PASSWORD);
        await page.getByTestId('tc-login-003').click(); //Login Button

        const url = page.url();
        if (!(url.includes('/login/'))) {
            console.log(`SUCCESS:you can modify and access database!`);
            break; 
        }
        
    }


})