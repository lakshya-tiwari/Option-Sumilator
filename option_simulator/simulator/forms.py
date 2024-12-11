from django import forms
from datetime import date
import pandas as pd

class OptionStrategyForm(forms.Form):
    #stock_price = forms.FloatField(label='Stock Price', required=True)
    strike_price = forms.ChoiceField(label='Strike Price', choices=[('', 'Select Strike Price')])
    option_type = forms.ChoiceField(choices=[('CE', 'CE'), ('PE', 'PE')])
    #premium = forms.FloatField(label='Option Premium', required=True)
    quantity = forms.IntegerField(label='Quantity', required=True)

    # Start Date - Use a calendar input for the date
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    # Expiry Date - Dropdown list
    expiry_date = forms.ChoiceField(label='Expiry Date', choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially populate expiry_date choices with an empty selection
        self.fields['expiry_date'].choices = [('', 'Select an expiry date')]
        self.fields['strike_price'].choices = [('', 'Select Strike Price')]  

        # Check if a start_date is passed
        start_date = self.data.get('start_date') or None
        exp_date = self.data.get('expiry_date') or None
        strike_price = self.data.get('strike_price') or None
        

        if start_date:
            print(f'start date--->{start_date}, expiry--->{exp_date}, strike_price--->{strike_price}')
        #     self.fields['expiry_date'].choices = self.get_expiry_choices(start_date)
            

    # def get_expiry_choices(self, start_date):
    #     """Return expiry choices based on the selected start date."""
    #     # expiry_dates = []
    #     try:
    #         # Read the data from a CSV file (or from database if necessary)
    #         data = pd.read_csv(r'D:\DATA\purchase_data\purchase_intraday_data2019.csv')
    #         data['Date'] = pd.to_datetime(data['Date'])
    #         data['Expiry'] = pd.to_datetime(data['Expiry'])
    #         start_date = pd.to_datetime(start_date)

    #         Data = data[data['Date']==start_date]
    #         expiry_dates = (Data['Expiry'].sort_values().unique())

    #         # Convert numpy.datetime64 to string format
    #         expiry_dates = [str(str(date).split('T')[0]) for date in expiry_dates]
    #         print('---------->',expiry_dates)
    #     except Exception as e:
    #         print(f"Error reading CSV: {e}")
    #         expiry_dates = []

    #     return expiry_dates
    
    # def is_valid_expiry(self, start_date, expiry_date):
    #     """Check if expiry date is valid for the selected start date."""
    #     # Implement your logic to check whether the expiry date is active for the selected start date
    #     # For example, expiry_date could be converted to a datetime object and compared with start_date
    #     return True  # Placeholder logic, replace with actual validation
