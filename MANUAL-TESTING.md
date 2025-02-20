# Manual Test Plan

## Requirements

- A web browser
- A Posit account and login credentials

## Scope

This test plan covers aspects of *Posit Cloud* and as such does *not* cover:

- The RStudio IDE
- The Jupyter IDE
- The Shiny Apps hosting service

This tests plan should be executed manually and should take no longer than 15 minutes.

Follow the test cases below, in order, and record the results.

## Test Cases

### 1. Login

Steps:

- i. Open a web browser and navigate to [Posit Cloud](https://posit.cloud/)
- ii. Click on the "Log In" link
- iii. Enter your test username and click continue
- iv. Enter your test password and click "Log In"

Expected Results:

- You should be redirected to the Posit Cloud dashboard
- The dashboard should display your full name in the top right corner

### 2. Create a new RStudio project

Steps:

- i. Click on the "New Project" button
- ii. Click on "New RStudio Project" in the dropdown
- iii. Click the default project title, "Untitled Project", and change it to "Manual Test Project"
- iv. Wait for the project to be created and for RStudio to load.

Expected Results:

- The project should be created successfully
- RStudio should load and display the default new project files

### 3. Create a Shiny App Project from a Template

Steps:

- i. Click on the "Your Workspace" item in the "Spaces" menu on the left
- ii. Click on the "New Project" button
- iii. Click on "New Project from Template" in the dropdown
- iv. Click the template named "Shiny App Publishing with RStudio"
- v. Click "OK" to create the project
- i. Wait for the project to be created and for RStudio to load.

Expected Results:

- RStudio should be loaded with the project files from the template
- The "Files" tab in the bottom right should display the project files, including the `app.R` file

### 4. Run the Shiny App

Steps:

- i. Click the file "app.R" in the "Files" tab
- ii. Click on the "Run App" button in the editor

Expected Results:

- The Shiny App should be displayed in a new browser window
- The open app should be loaded and interactive

### 5. Deploy the Shiny App

Steps:

- i. Click on the blue publish button next to the "Run App" button
- ii. In the popup window that appears, click "Add new account" in the top-right
- iii. Click "ShinyApps.io" in the list of services
- iv. Click the "your account on ShinyApps" link to log into Shiny Apps
- v. If prompted, log in with your Posit credentials
- vi. In the dashboard, find the section labeled "Step 2 - AUTHORIZE ACCOUNT"
- vii. Click the "Copy to Clipboard" button, press Ctrl+C or Cmd+C to copy the token
- viii. Return to RStudio and paste the token in the "Authorization Token" field
- ix. Click the "Connect Account" button
- x. In the list of accounts, click the "ShinyApps.io" account
- xi. Click "Publish" to deploy the app

Expected Results:

- You should observe the deploy tab opening in the bottom-left panel of RStudio
- You should observe the app being built and deployed to ShinyApps.io
- The app should open in its new shinyapps.io URL in a new browser tab

### 6. Edit the App's Description

Steps:

- i. Click the gear icon in the top-right of the Posit Cloud interface
- ii. Click the placeholder text in the "Description" section
- iii. Enter a new description for the app
- iv. Navigate back to the workspace's project list

Expected Results:

- The description should be updated and visible in the project list

### 7. Archive the Project

Steps:

- i. Click the three-dot icon next to the project name in the workspace's project list
- ii. Click "Move to Archive" in the dropdown
- iii. Navigate to the "Archive" tab in the workspace's project list

Expected Results:

- The project should be moved to the archive and removed from the workspace's project list
- The project should be visible in the archive list

### 8. Restore the Archived Project

Steps:

- i. Click the "Archive" tab in the workspace's project list, on the left
- ii. Click "Restore" next to the project name
- iii. Navigate back to the workspace's project list

Expected Results:

- The project should be removed from the archive list
- The project should be restored and visible in the workspace's project list

### 9. Delete the Project

Steps:

- i. Click the trashcan icon next to the project name in the workspace's project list

Expected Results:

- The project should be deleted and removed from the workspace's project list, immediately

### 10. Restore the Deleted Project

Steps:

- i. Click the "Trash" tab in the workspace's project list, on the left
- ii. Click "Restore" next to the project name
- iii. Navigate back to the workspace's project list

Expected Results:

- The project should be removed from the trash list
- The project should be restored and visible in the workspace's project list
