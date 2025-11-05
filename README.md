# MyObservatory 9-Day Forecast UI Test
**Automated verification of the first day's forecast date using Appium + pytest + Poetry**

---

## Project Goal
Launch the **MyObservatory** app (Hong Kong Observatory),  
navigate to the **9-day Forecast** screen,  
extract the **first day’s date**,  
and **verify it matches today or tomorrow’s date**.

---

## Tech Stack
- Python 3.9+
- Appium (UiAutomator2 driver)
- Appium-Python-Client
- pytest
- Poetry (dependency + virtual env)

---

## 1. Set Up Environment

### Prerequisites
| Tool              | Install Command / Link |
|-------------------|------------------------|
| JDK 11+           | https://www.oracle.com/java/technologies/downloads/ |
| Node.js + npm     | `brew install node` or https://nodejs.org |
| Android Studio    | https://developer.android.com/studio |
| Appium            | `npm install -g appium` |
| UiAutomator2      | `appium driver install uiautomator2` |
| Appium Inspector  | https://github.com/appium/appium-inspector/releases |

### Android Device / Emulator
1. Settings → About phone → Tap **Build number** 7 times  
2. Developer options → Enable **USB debugging**  
3. Connect via USB → Allow debugging  
4. Verify:     adb devices

## 2. Install Dependencies

### Install Poetry (skip if already installed)
curl -sSL https://install.python-poetry.org | python3 -

### Install project
poetry install

### Activate shell
poetry shell

## 3. Run the Tests

### Start Appium Server
Appium

### Run Pytest
pytest tests/ -v

--- 

## Project Structure

python-app-ui-verification/
├── pyproject.toml
├── src/
├── tests/
│   └── test_myobservatory.py
├── screenshots/
│   └── screenshot_desired_capabilities_script.jpg
│   └── screenshot_shared_element.jpg
└── README.md

--- 

## Appium Inspector Pro Tips

Start session → Copy Desired Capabilities JSON
Prefer Accessibility ID → resource-id → XPath
Record swipe gestures
Save session → paste into capabilities.json




