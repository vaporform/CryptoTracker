# CryptoTracker

A real-time cryptocurrency dashboard that displays ticker information, order books, and trade history.
![An image preview of the app](https://github.com/vaporform/CryptoTracker/blob/main/Preview.png)

## Features

- **Real-time Ticker:** View live price updates for various cryptocurrencies.
- **Order Book:** See the current buy and sell orders.
- **Trade History:** Track recent trades as they happen.
- **Kline Chart:** Candlestick chart to visualize price changes.

## Project Structure

```
CryptoTracker/
├─ README.md              # This file
├─ Preview.png            # Image showing the application
├─ requirements.txt       # Listing of required Python libraries
├─ main.py                # The program itself
├─ Components/
│  ├─ BaseUI.py           # Base widget class with header
│  ├─ Ticker.py           # Single and mini ticker widgets (WS)
│  ├─ Book.py             # Order book with asks and bids (WS)
│  ├─ TradeHistory.py     # Trade listing (WS)
│  ├─ KlineHistory.py     # Candlestick charts and Volume (REST)
│  └─ CryptoHelper.py     # REST/WS helpers
```

## Setup
Before running, ensure Python is installed on your system.
```
python3 --version
```
Next, you can download the repository directly or clone it via
```
git clone https://github.com/vaporform/CryptoTracker.git
```
Open the folder by using prefered IDE or in the terminal:
```
cd path/to/your/folder
```
Next, it is OK to run without using virtual enviroments but it is recommended as to not create dependency conficts.

To create a virtual environement, you can run:
```
python -m venv myvenv
```
Then, activate by do the following:
-   On Windows:
    ```bash
    .\myvenv\Scripts\activate
    ```
-   On macOS or Linux:
    ```bash
    source myvenv/bin/activate
    ```
Next, you can install the dependencies by running:
```
pip install -r requirements.txt
```

## Usage

To run the application, execute the command in the terminal:

```
python main.py
```

This will launch the CryptoTracker dashboard.
