# WoonNetRijnmondreact

The script reacts to houses posted on the website of the Woonnet Rijnmond housing association in Rotterdam.

## Table of Contents
- [Motivation](#motivation)
- [Installation](#installation)
- [Usage](#usage)
- [Full Automation Consideration](#full-automation-consideration)
- [Final words](#final-words)

---

## 😴 Motivation

The motivation for this project stems from the growing difficulty of securing social housing in the Netherlands, particularly due to the ongoing housing crisis. In Rotterdam, the only official platform for renting these types of homes is **Woonnet Rijnmond**. Among the various models on the platform, one called **"DirectKans"** allows eligible users to apply for select listings that appear at **20:00** and remain online for only **15 minutes**, until **20:15**. By **20:30**, randomized applicant positions are published, determining who gets a chance at the property.

This means that to have a chance at getting an invitation to view one of these houses, you need to react every single day during this time slot. For me, this became a tedious and disruptive routine:
1. You must be available at exactly 20:00, which can interfere with evening plans or make it easy to forget, resulting in missed opportunities.
2. Managing multiple accounts (I use four between myself and my girlfriend) becomes repetitive and annoying manual work.

To address this, I created a script that automates the reacting process for the accounts specified. The script logs into each account and reacts to the first two available *DirectKans* listings as soon as they go live. This reduces daily friction and ensures no opportunity is missed due to timing or forgetfulness.

For full automation, where one does not need to run the scripts daily (reducing all work to non-existent levels), please refer to the [Full Automation Consideration](#full-automation-consideration) section.

> ⚠️ **Note**: This tool is intended for light personal use. Woonnet Rijnmond actively employs bot detection, so this project includes basic efforts to mimic human interaction patterns and avoid detection. It is not guaranteed to be undetectable and should be used responsibly.

---

## Installation

### Step 1: Clone the Repository
Clone this repository using the following command:
```bash
git clone https://github.com/Stefan142/WoonNetRijnmondreact.git
cd WoonNetRijnmondreact
```

### Step 2: Install Dependencies
Ensure you have Python installed. Use pip to install the required Python libraries:

```bash
pip install -r requirements.txt
```

### Step 3: Install Geckodriver
The script uses Selenium with Firefox, which requires **Geckodriver**. Download the correct Geckodriver version for your operating system from the [official Geckodriver page](https://github.com/mozilla/geckodriver/releases).

Once downloaded:

 - Place the Geckodriver executable in a directory that is in your system's PATH, or
- Update the path to Geckodriver in the [`helper.py`](https://github.com/Stefan142/WoonNetRijnmondreact/blob/main/helper.py) file on line 37:
```Python
service = Service("/path/to/your/geckodriver")
```
### Step 4: Verify Setup
Test the script locally by running:

```bash
python main.py
```
For guidelines on automating this process further, see the [Full Automation Consideration](#full-automation-consideration) section.

---
## Usage
To run the script:

1. Open main.py.

2. Use the account_runner function to add multiple accounts.

3. Add your Woonnet Rijnmond username and password in the designated section in the main and add multiple accounts if neccessary by making multiple function calls.
```python
account_runner(your_username, your_password)
```
- Execute the script:
```bash
python main.py
```
### Notes:
- The core functionality for interacting with the Woonnet Rijnmond platform is implemented in the WoonnetBot class in [`helper.py`](https://github.com/Stefan142/WoonNetRijnmondreact/blob/main/helper.py).
- The script includes randomized waiting statements to mimic human interaction.
- If you manage a larger number of accounts, you may need to reduce or remove some waiting statements to ensure all reactions occur within the 15-minute timeframe.
For example, review and adjust the wait_random method in [`helper.py`](https://github.com/Stefan142/WoonNetRijnmondreact/blob/main/helper.py) to optimize performance:

```Python
def wait_random(self):
    """Random waiting time, reduces likelihood of bot detection."""
    time.sleep(np.random.uniform(1, 1.5))
```
---

## Full Automation Consideration
For full automation, the script can be scheduled to run daily at 20:00 using a cloud-based environment. Below is a step-by-step guide:

### Step 1: Set Up a Cloud Environment
A free-tier Ubuntu ARM virtual machine from Oracle Cloud is recommended for this project. Follow online tutorials to request and configure your virtual machine:

- [Oracle Free Tier Setup Official Guide](https://www.oracle.com/cloud/free/)
- [Oracle Free Tier tutorial](https://www.youtube.com/watch?v=NKc3k7xceT8)

### Step 2: Configure the Virtual Machine
Clone this repository onto the VM.
Follow the installation steps outlined in the [Installation](#installation) section.
### Step 3: Automate Script Execution
Use a cron job to schedule the script at 20:00 daily:

Open the crontab editor:
```bash
crontab -e
```
Add the following line to schedule the script:
```bash
0 20 * * * /path/to/python /path/to/main.py >> /path/to/logs/script.log 2>&1
```
Replace `/path/to/python`, `/path/to/main.py`, and `/path/to/logs/script.log` with the appropriate paths.

### Step 4: Monitor Logs
Ensure the cron job outputs logs to a file (e.g., script.log) for debugging and monitoring.

---
## Final Words
If a step in this project is unclear or you have any suggestions, feel free to reach out!

> ⚠️ **Note**: This tool is intended for light personal use. Woonnet Rijnmond actively employs bot detection, so this project includes basic efforts to mimic human interaction patterns and avoid detection. It is not guaranteed to be undetectable and should be used responsibly.
