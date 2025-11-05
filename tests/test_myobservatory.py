### Initialize Appium WebDriver
import pytest
import datetime
import re
from appium import webdriver
from appium.options.common import AppiumOptions         # for webdriver.remote() Options parameter
from appium.webdriver.common.appiumby import AppiumBy   # for UI navigation after connection with the device

@pytest.fixture(scope="module")     # so that pytest knows all tests in same file would be using the same session

### 1. Define your desired capabilities, connect to device
### These capabilities tell Appium about the device, app, and automation settings.
### Recommend to execute the code within "def" in a separate file to test connection first.
def driver():
    #Initialize Appium driver connection to Android device
    desired_caps = {                        # replace with your own capabilities, can add "appPackage" and "appActivity"
        "platformName": "Android",
        "platformVersion": "16",
        "deviceName": "Pixel 8a",
        "automationName": "UiAutomator2",   # "UIAutomator 2" for Android, "XCUITest" for IOS
        "android_sdk_root": "SDK\root\folder",     # the path to local SDK root folder (if applicable)
        "android_home": "SDK\root\folder",           # the path to local SDK root folder (if applicable)
        "NoReset" : True,
        "newCommandTimeout": 300,
    }
    ### Create an AppiumOptions object and set capabilities
    options = AppiumOptions()
    options.load_capabilities(desired_caps)

    # web_driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)           # desired_caps as dict[] is for older version
    # remote_driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", options=options)     # /wd/hub is for older version
    remote_driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    yield remote_driver
    remote_driver.quit()

### 2. With device connected, navigate to destination element
def test_nine_day_forecast(driver):

    ## print("driver current activity = " + str(driver.current_activity))
    forecast_button = driver.find_element("accessibility id", "MyObservatory")
    forecast_button.click()

    ### Wait a bit for the screen to load, especially for starting an app
    driver.implicitly_wait(180)

    ### Tap "next" and "X" button to go through and exit pop-ups (3 pages)
    forecast_button = driver.find_element("accessibility id", "Next page")
    forecast_button.click()
    forecast_button.click()
    forecast_button.click()

    ### Wait a bit for the screen to load
    driver.implicitly_wait(5)

    ### Tap "menu button at top left corner"
    forecast_button = driver.find_element("accessibility id", "Navigate up")
    forecast_button.click()

    ### Wait a bit for the screen to load
    driver.implicitly_wait(5)

    ### Tap down arrow of "Forecast and Warnings Services" from drop down menu
    xpath_string = "//android.widget.TextView[@resource-id ='hko.MyObservatory_v1_0:id/title' and @text='Forecast & Warning Services']"
    forecast_button = driver.find_element(AppiumBy.XPATH, xpath_string)
    forecast_button.click()

    ### Wait a bit for the screen to load
    driver.implicitly_wait(10)

    ### Tap "9-Day Forecast" from extended menu
    xpath_string = "//android.widget.TextView[@resource-id='hko.MyObservatory_v1_0:id/title' and @text='9-Day Forecast']"
    forecast_button = driver.find_element(AppiumBy.XPATH, xpath_string)
    forecast_button.click()

    ### Wait a bit for the screen to load
    driver.implicitly_wait(10)

    ### Locate the first forecast block dynamically (ignoring date)
    ### first day
    first_day = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,
                                     'new UiSelector().resourceIdMatches(".*sevenday_forecast_date.*")')[0]
    first_day_desc = first_day.get_attribute("contentDescription")
    print(f"\nDate: {first_day_desc}")

    ### first day's temperatures
    first_day_temp = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,
                                     'new UiSelector().resourceIdMatches(".*sevenday_forecast_temp.*")')[0]
    temp_desc = first_day_temp.get_attribute("contentDescription")

    ### Verify the date matches today or tomorrow
    today = datetime.datetime.now()
    today_desc = today.strftime("%d %B")  # %B for full month name, %d for day
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_desc = tomorrow.strftime("%d %B")  # %B for full month name, %d for day

    assert today_desc in first_day_desc or tomorrow_desc in first_day_desc, f"Expected {tomorrow} in forecast, got {first_day_desc}"

    ### extract high and low temperature
    ### Pattern: finds two numbers separated by "and", before "degree"
    pattern = r'between\s+(\d+)\s+and\s+(\d+)\s+degree'
    match = re.search(pattern, temp_desc)
    if match:
        lowest_temp = int(match.group(1))
        highest_temp = int(match.group(2))
        print(f"Low: {lowest_temp}°C")
        print(f"High: {highest_temp}°C")
        assert highest_temp >= lowest_temp, "Temperature range is incorrect."
    else:
        print("Temperature range not found.")

