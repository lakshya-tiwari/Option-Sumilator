from django.shortcuts import render
from django.http import JsonResponse
from .forms import OptionStrategyForm
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Add this line to set the non-GUI backend

import matplotlib.pyplot as plt
import plotly.graph_objects as go
import io
import urllib, base64

import pandas as pd
from datetime import datetime



data = pd.read_csv(r'D:\DATA\purchase_data\purchase_intraday_data2019.csv')
data['DateTime'] = pd.to_datetime(data['Date']+' '+data['Time'])
data['Date'] = pd.to_datetime(data['Date'])
data['Expiry'] = pd.to_datetime(data['Expiry'])
print('Data is ready to Use')


# Utility to calculate the payoff
def calculate_payoff(option_data, tradeType, qty):
    
    # Ensure premium is a scalar
    premium = float(option_data['Last'].iloc[0])
    payoff_data = pd.DataFrame(columns=['DateTime','PayOff','Spot','OptionPrice'])
    
    payoff_data['DateTime'] = option_data['DateTime']
    payoff_data['Spot'] = option_data['Underlying']
    payoff_data['OptionPrice'] = option_data['Last']
    
    if tradeType == 'BUY':
        payoff_data['PayOff'] = (option_data['Last'] - premium) * qty
        
    elif tradeType == 'SELL':
        payoff_data['PayOff'] = (premium - option_data['Last']) * qty

    return payoff_data.reset_index(drop=True)

# Utility to plot the payoff
def plot_payoff(plot_data):
    X = plot_data['DateTime']
    Y = plot_data['OptionPrice']

    fig, ax = plt.subplots()
    ax.plot(X, Y, label='Payoff')
    ax.set_title('Option Payoff')
    ax.set_xlabel('Stock Price at Expiration')
    ax.set_ylabel('Profit/Loss')
    plt.legend()
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')  # Ensure it's decoded to string
    uri = 'data:image/png;base64,' + string  # Use base64 encoded string
    return uri



# New view to generate and return the chart image URL or base64 string
def get_option_data_for_chart(request):
    start_date = request.GET.get('start_date')
    expiry_date = request.GET.get('expiry_date')
    option_type = request.GET.get('option_type')
    strike_price = request.GET.get('strike_price')

    

    option_data = get_option_data_from_csv(start_date, expiry_date, strike_price, option_type)
    
    if option_data is None:
        return JsonResponse({'error': 'No option data available'}, status=400)

    # Calculate the payoff
    quantity = 1  # Example quantity
    payoff_data = calculate_payoff(option_data, 'BUY', quantity)
    
    # Prepare the data for the Chart.js plot (option price chart)
    chart_data = {
        'labels': payoff_data['DateTime'].astype(str).tolist(),  # Date as x-axis labels
        'data': payoff_data['OptionPrice'].tolist(),  # Payoff values as y-axis data
    }

    # Prepare the spot price chart data
    payoff_data = payoff_data.dropna()
    chart_spot = { 
        'labels': payoff_data['DateTime'].astype(str).tolist(),  # Date as x-axis labels
        'data': payoff_data['Spot'].tolist(),  # Spot prices as y-axis data 
    }
    
    return JsonResponse({'chart_data': chart_data, 'spot_chart': chart_spot})

    


# Function to get the option price from the CSV based on expiry date
def get_option_data_from_csv(start_date, expiry_date, strike_price, option_type):

    start_date = pd.to_datetime(start_date)
    expiry_date = pd.to_datetime(expiry_date)
    strike_price = int(strike_price)
    filtered_data = None
    try:
        # Filter the dataframe
        filtered_data = data[(data['DateTime'] >= start_date) &
                             (data['Expiry'] == expiry_date) &
                             (data['Strike Price'] == strike_price) &
                             (data['Option Type'] == option_type)]
        if filtered_data.empty:
            print(f"Filtered_data is empty")
            
    except Exception as e:
        print(f"Error reading CSV: {e}")
    
    return filtered_data


# Function to get available expiry dates based on the selected start date
def get_expiry_dates_for_start_date(start_date):

    try:
        # Read the data from a CSV file (or from database if necessary)
        start_date = pd.to_datetime(start_date)

        Data = data[data['DateTime']==start_date]
        expiry_dates = (Data['Expiry'].sort_values().unique())
        
    except Exception as e:
        print(f"Error reading CSV: {e}")
    
    return expiry_dates

def get_strike_prices_for_start_expiry(start_date, expiry_date, option_type):
    try:
        # Filter data based on start date and expiry date
        start_date = pd.to_datetime(start_date, '%Y-%m-%dT%H:%M')
        strike_prices = list(data[(data['DateTime'] == start_date) & (data['Expiry'] == expiry_date) & (data['Option Type'] == option_type)]['Strike Price'].sort_values().unique())

    except Exception as e:
        print(f"Error retrieving strike prices: {e}")
        strike_prices = []

    return strike_prices

# Function to check if expiry date is valid for the selected start date
def is_valid_expiry(start_date, expiry_date):
    # Example logic to check whether expiry date is after the start date.
    # You can modify this based on your logic to calculate validity.
    try:
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
        return expiry_date >= start_date
    except ValueError:
        return False

# AJAX view to return expiry dates based on selected start_date
def get_expiry_dates(request):
    start_date = request.GET.get('start_date')

    if start_date:
        
        # Get expiry dates filtered by start_date
        expiry_dates = get_expiry_dates_for_start_date(start_date)
        
        # Convert expiry dates to string format (YYYY-MM-DD)
        expiry_dates = [str(expiry_date).split('T')[0] for expiry_date in expiry_dates]

    return JsonResponse({'expiry_dates': expiry_dates})

# AJAX view to return strike prices based on selected start_date and expiry_date
def get_strike_prices(request):
    start_date = pd.to_datetime(request.GET.get('start_date'))
    expiry_date = pd.to_datetime(request.GET.get('expiry_date'))
    option_type = request.GET.get('option_type')
    
    strike_prices = []
    if start_date and expiry_date and option_type:
        strike_prices = get_strike_prices_for_start_expiry(start_date, expiry_date, option_type)
        
    # Convert all values to regular Python int, if necessary
    strike_prices = [int(price) for price in strike_prices]
    
    return JsonResponse({'strike_prices': strike_prices})


# Main view to render the option simulator and handle form submission
def option_simulator(request):
    if request.method == 'POST':
        form = OptionStrategyForm(request.POST)
        if form.is_valid():
            #stock_price = form.cleaned_data['stock_price']
            strike_price = form.cleaned_data['strike_price']
            #premium = form.cleaned_data['premium']
            quantity = form.cleaned_data['quantity']
            option_type = form.cleaned_data['option_type']
            start_date = form.cleaned_data['start_date']
            expiry_date = form.cleaned_data['expiry_date']
            
            # Get the option price from the CSV based on expiry_date
            option_price = get_option_data_from_csv(start_date,expiry_date,strike_price,option_type)
            if option_price is None:
                option_price = premium  # Fallback to the input premium if not found
            
            # Calculate payoff using the retrieved option price
            price_range, payoff = calculate_payoff(stock_price, strike_price, option_price, quantity, option_type)
            chart = plot_payoff(price_range, payoff)

            return render(request, 'simulator/result.html', {'form': form, 'chart': chart})
    else:
        form = OptionStrategyForm()

    return render(request, 'simulator/index.html', {'form': form})
