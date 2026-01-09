import { test, expect } from '@playwright/test';
import { WEBSITEURL,DUMMY_USER , DUMMY_CREATE, UNREGISTERED_DUMMY} from './auth/constant';

test('Create Existing Account', async ({ page }) => {
    //Case - Existing Account credentials used to register a new account
    //Judgement Criteria - Registration of new user should be unsuccessful and remain in registration page.
    await page.goto(WEBSITEURL + '/register/');
    await expect(page).toHaveTitle("Create Account");

    await page.getByTestId('tc-register-001').fill(DUMMY_USER.USERNAME);
    await page.getByTestId('tc-register-002').fill(DUMMY_USER.PASSWORD);
    await page.getByTestId('tc-register-003').click(); //Register Button

    
    const TARGET = page.getByTestId('tc-register-004')
    await expect(TARGET).toContainText("Username already exists. Please choose another.");
    await expect(page).toHaveTitle("Create Account");

});

test('Create New Account', async ({ page }) => {
    //Case - New Account credentials used to register a new account
    //Judgement Criteria - Registration of new user should be successful and redirect to login page.
    await page.goto(WEBSITEURL+ '/register/');
    await expect(page).toHaveTitle("Create Account");

    await page.getByTestId('tc-register-001').fill(DUMMY_CREATE.USERNAME);
    await page.getByTestId('tc-register-002').fill(DUMMY_CREATE.PASSWORD);
    await page.getByTestId('tc-register-003').click(); //Register Button 

    const TARGET = page.getByTestId('tc-login-004')

    await expect(page).toHaveURL(WEBSITEURL+"/login/", { timeout: 5000 })
    await expect(page).toHaveTitle("Login");

});

test('Login Registered User', async ({page}) =>{
    //Case -  Existing Account credentials used to login
    //Judgement Criteria - Login of user should be successful and redirect to home page.
    await page.goto(WEBSITEURL+'/login/');
    await expect(page).toHaveTitle('Login');

    await page.getByTestId('tc-login-001').fill(DUMMY_USER.USERNAME);
    await page.getByTestId('tc-login-002').fill(DUMMY_USER.PASSWORD);
    await page.getByTestId('tc-login-003').click(); //Login Button

    await expect(page).toHaveURL(WEBSITEURL);
    await expect(page).toHaveTitle('Minimal Feed');

    await page.getByTestId('tc-home-001').click(); // Logout Button
    await expect(page).toHaveURL(WEBSITEURL+'/login/');
    await expect(page).toHaveTitle('Login');
})

test('Login Unregistered User', async ({page}) =>{
    //Case - Non-existing account credentials used to login
    //Judgement Criteria - Login of user should be unsuccessful and remains to login page.
     await page.goto(WEBSITEURL+'/login/');
     await expect(page).toHaveTitle('Login');

    //Case - Unregistered User
    await page.getByTestId('tc-login-001').fill(UNREGISTERED_DUMMY.USERNAME);
    await page.getByTestId('tc-login-002').fill(UNREGISTERED_DUMMY.PASSWORD);
    await page.getByTestId('tc-login-003').click(); //Login Button

    await expect(page).toHaveURL(WEBSITEURL+'/login/');
    await expect(page).toHaveTitle('Login');
    await expect(page.getByTestId('tc-login-004')).toBeVisible()
})

test('Login Unregistered Username', async ({page}) =>{
    //Case - Non-existing account credentials used to login
     //Judgement Criteria - Login of user should be unsuccessful and remains to login page.
     await page.goto(WEBSITEURL+'/login/');
     await expect(page).toHaveTitle('Login');

    //Case - Unregistered username
    await page.getByTestId('tc-login-001').fill(UNREGISTERED_DUMMY.USERNAME);
    await page.getByTestId('tc-login-002').fill(DUMMY_USER.PASSWORD);
    await page.getByTestId('tc-login-003').click(); //Login Button

    await expect(page).toHaveURL(WEBSITEURL+'/login/');
    await expect(page).toHaveTitle('Login');
    await expect(page.getByTestId('tc-login-004')).toBeVisible()
})

test('Login Incorrect Password', async ({page}) =>{
    //Case - Non-existing account credentials used to login
     //Judgement Criteria - Login of user should be unsuccessful and remains to login page.
     await page.goto(WEBSITEURL+'/login/');
     await expect(page).toHaveTitle('Login');

    //Case - Incorrect Password
    await page.getByTestId('tc-login-001').fill(DUMMY_USER.USERNAME);
    await page.getByTestId('tc-login-002').fill(UNREGISTERED_DUMMY.PASSWORD);
    await page.getByTestId('tc-login-003').click(); //Login Button

    await expect(page).toHaveURL(WEBSITEURL+'/login/');
    await expect(page).toHaveTitle('Login');
    await expect(page.getByTestId('tc-login-004')).toBeVisible()
})