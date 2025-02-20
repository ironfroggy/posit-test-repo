import logging
import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

import findtext
from trio import fail_after

### SETUP

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

### HELPERS


def ws_name_split(ws_name):
    """Split a workspace list label into name and owner, if available."""
    if "\n" in ws_name:
        return ws_name.split("\n")
    return ws_name, None


### ACTIONS


def do_workspace_create(driver, workspace_name):
    """Create a new workspace with a specified name."""

    driver.refresh()
    driver.implicitly_wait(5)

    # Find and click the "New Space" button
    el = driver.find_element(By.CLASS_NAME, "newSpace")
    el.click()

    # Fill in the random name for the new space
    el = driver.find_element(By.ID, "name")
    el.send_keys(workspace_name)

    # and click Create button
    el = driver.find_element(By.CSS_SELECTOR, "button[type=submit]")
    el.click()
    driver.implicitly_wait(3)
    driver.refresh()


def do_workspace_open(driver, workspace_name):
    """Open the workspace specified by name.

    Refreshes the page first to ensure up-to-date workspace list.
    """

    driver.refresh()
    driver.implicitly_wait(5)

    workspace_list = driver.find_element(By.CSS_SELECTOR, ".spaceMenu ul")
    workspace_items = workspace_list.find_elements(By.TAG_NAME, "li")
    for item in workspace_items:
        ws_name, _ = ws_name_split(item.text)
        if ws_name == workspace_name:
            item.click()
            driver.implicitly_wait(3)
            break
    else:
        pytest.fail(f"Workspace {workspace_name} not found")


def do_workspace_delete(driver, workspace_name=None):
    """Delete the current workspace or the one specified by name."""

    # If we are given a workspace by name, navigate to it first
    if workspace_name:
        do_workspace_open(driver, workspace_name)

    # Get current workspace name and make sure it's a test workspace
    el = driver.find_element(By.ID, "headerTitle")
    workspace_name = el.text
    assert workspace_name.startswith(
        "Test Space"
    ), f"Unexpected workspace name: {workspace_name}"

    # Open the space menu
    el = driver.find_element(
        By.CSS_SELECTOR,
        "#rStudioHeader > div.band > div.innards.bandContent > div.actionBar.menu.aux > div > button",
    )
    el.click()

    # Find and click the "Delete Space" button
    el = driver.find_element(By.CSS_SELECTOR, "#headerDeleteSpaceButton > span")
    el.click()

    # Enter confirmation "Delete <space name>"
    el = driver.find_element(By.ID, "deleteSpaceTest")
    el.send_keys(f"Delete {workspace_name}")

    # Confirm the deletion
    el = driver.find_element(By.CSS_SELECTOR, "#deleteSpaceSubmit")
    el.click()


### TEST FIXTURES


@pytest.fixture(scope="session")
def driver():
    logger.info("setting up webdriver...")
    driver = webdriver.Chrome()
    driver.get("https://posit.cloud/")
    yield driver


@pytest.fixture(scope="session")
def login_session(driver):
    """Fixture to log in to the test account and yield the driver."""

    driver.get("https://posit.cloud/")

    # login
    username = os.environ["POSIT_TEST_USERNAME"]
    el = driver.find_element(
        "link text",
        "Log In",
    )
    el.click()
    driver.implicitly_wait(5)

    # Enter the username
    el = driver.find_element(By.CSS_SELECTOR, "#entry input[type=email]")
    el.send_keys(username)

    el = driver.find_element(By.CSS_SELECTOR, "#entry form button[type=submit]")
    el.click()
    driver.implicitly_wait(5)

    # Enter the password
    el = driver.find_element(By.CSS_SELECTOR, "#entry input[type=password]")
    el.send_keys(os.environ["POSIT_TEST_PASSWORD"])

    el = driver.find_element(By.CSS_SELECTOR, "#entry form button[type=submit]")
    el.click()

    # Wait for the login to complete and load for up to 10 seconds
    # or, until we see the #spaceOwner element has loaded
    logger.info("Waiting for login to complete...")
    timeout = 10
    check_freq = 1
    while timeout > 0:
        try:
            driver.find_element(By.ID, "spaceOwner")
            break
        except Exception as e:
            logger.info(f"{timeout} sec remain to login...")
            time.sleep(check_freq)
            timeout -= check_freq
    else:
        pytest.fail("Login did not complete")

    logger.info(f"Successfully logged in as {username}")

    yield driver


@pytest.fixture(scope="session")
def temp_workspace(driver, login_session):
    """Fixture to create and delete a workspace for each test that needs it."""

    driver.refresh()

    workspace_list = driver.find_element(By.CSS_SELECTOR, ".spaceMenu ul")
    workspace_items = workspace_list.find_elements(By.TAG_NAME, "li")

    # Test Account should only have 1 space + new space button
    # If there are > 2 list items, navigate to the second one and delete it
    if len(workspace_items) > 2:
        ws_name, _ = ws_name_split(workspace_items[1].text)
        assert ws_name.startswith(
            "Test Space"
        ), f"Unexpected (non-test) workspace name: {ws_name}"
        workspace_items[1].click()
        driver.implicitly_wait(3)
        do_workspace_delete(driver)

    # Generate a new workspace name
    workspace_name = f"Test Space {int(time.time())}"
    do_workspace_create(driver, workspace_name)
    do_workspace_open(driver, workspace_name)

    yield workspace_name

    # Cleanup this fixture by deleting the workspace
    do_workspace_delete(driver, workspace_name)


### TESTS


def test_login(driver, login_session):
    el = driver.find_element(By.ID, "spaceOwner")
    assert el.text == os.environ["POSIT_TEST_FULLNAME"]


def test_space_creation(driver, login_session, temp_workspace):
    """A new workspace can be created and opened and is owned correctly."""

    # Open the test workspace
    do_workspace_open(driver, temp_workspace)

    # Check the workspace has been created and we're in it
    el = driver.find_element(By.ID, "headerTitle")
    assert el.text == temp_workspace

    # Check that the correct user owns the space
    el = driver.find_element(By.ID, "spaceOwner")
    assert el.text == os.environ["POSIT_TEST_FULLNAME"]


def test_rstudio_creation(driver, login_session, temp_workspace):
    """In the test workspace, create a new RStudio project."""

    # Open the test workspace
    do_workspace_open(driver, temp_workspace)

    # Find the "New Project" button, by text, and click it
    el = findtext.find_element_by_text(driver, "New Project")
    el.click()

    # Find and click the "New RStudio Project" button
    el = findtext.find_element_by_text(driver, "New RStudio Project")
    el.click()

    # Wait for the RStudio project to load for up to 30 seconds
    # or, until we see the #rstudio_container element has loaded
    logger.info("Waiting for RStudio project to load...")
    timeout = 30
    check_freq = 5
    rstudio = None
    while timeout > 0:
        try:
            try:
                # Switch to the iframe containing the RStudio project
                iframe = driver.find_element(By.ID, "contentIFrame")
                driver.switch_to.frame(iframe)
                # Check that the RStudio project has loaded
                rstudio = driver.find_element(By.ID, "rstudio_container")
                break
            finally:
                driver.switch_to.default_content()
        except Exception as e:
            logger.info(f"{timeout} sec remain to load RStudio...")
            time.sleep(check_freq)
            timeout -= check_freq

    assert rstudio, "RStudio project did not load"
