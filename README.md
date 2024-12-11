# Option Strategy Simulator

## Overview

This project is an **Option Strategy Simulator** built using Django and JavaScript. It provides a user interface where users can simulate the payoff of different option strategies based on selected parameters such as strike price, option type (call/put), and expiration date. The simulator uses real financial data and generates interactive charts to visualize the option prices and spot prices over time.

## Features

- **Interactive Form**: Allows users to select the option type (call/put), quantity, start date, expiry date, and strike price.
- **Dynamic Data Fetching**: Fetches available expiry dates and strike prices based on the selected start date.
- **Chart Visualization**: Generates two interactive charts:
- **Option Price Chart**: Shows the payoff of the option over time.
- **Spot Price Chart**: Displays the underlying spot prices.
- **Payoff Calculation**: Calculates the payoff for "BUY" and "SELL" strategies.
- **Zoomable Charts**: The generated charts are interactive and allow users to zoom and pan.

## Project Structure


## Installation

### Prerequisites

- Python 3.x
- Django (>=3.0)
- Pandas
- Matplotlib
- Plotly

### Step 1: Clone the Repository

- git clone https://github.com/your-username/option-strategy-simulator.git
- cd option-strategy-simulator

- python3 -m venv venv
- source venv/bin/activate  # On Windows use: venv\Scripts\activate
- pip install -r requirements.txt

- python manage.py migrate
Visit the app in your browser at http://localhost:8000

## **Usage**

- **Option Type**: Select whether the option is a Call or Put.
- **Quantity**: Enter the number of contracts for the option strategy.
- **Start Date**: Pick the start date for the option.
- **Expiry Date**: Select the expiry date, which is dynamically populated based on the start date.
- **Strike Price**: Choose the strike price from dynamically populated tiles.

Once the form is filled, the **Option Payoff Chart** and **Spot Price Chart** will be displayed, showing the option’s payoff and the spot prices.

## Chart Features

- **Zoom**: You can zoom into the charts using the mouse wheel or pinch gestures (on mobile devices).
- **Pan**: Drag the chart to explore different time periods.

## Key Django Views

- **`option_simulator(request)`**: Handles form submission, calculates payoff, and returns the simulator page with charts.
- **`get_option_data_for_chart(request)`**: Fetches data for generating the option price and spot price charts.
- **`get_expiry_dates(request)`**: Returns available expiry dates based on the selected start date.
- **`get_strike_prices(request)`**: Returns available strike prices based on the selected start date and expiry date.

## Code Explanation

- **Option Strategy Form (`OptionStrategyForm`)**: A Django form that takes input for option type, quantity, start date, expiry date, and strike price.
- **Payoff Calculation (`calculate_payoff`)**: Calculates the payoff for a given option based on the selected option type (BUY/SELL), strike price, and quantity.
- **Chart Plotting (`plot_payoff`)**: Uses `matplotlib` to generate an option payoff plot and returns the image as a base64-encoded string for embedding in the HTML.
- **AJAX Data Fetching**: JavaScript dynamically fetches expiry dates and strike prices based on user input and updates the form in real-time.

## Example Workflow

1. The user selects a **Start Date**, and available expiry dates are fetched via AJAX.
2. Upon selecting an expiry date, the available strike prices are displayed in tiles.
3. Once a strike price is selected, the payoff and spot price data are fetched from the server and displayed in interactive charts.

## Contributing

If you would like to contribute to this project, feel free to fork the repository, submit issues, and send pull requests. Contributions are welcome!


## Contributing

If you would like to contribute to this project, feel free to fork the repository, submit issues, and send pull requests. Contributions are welcome!
