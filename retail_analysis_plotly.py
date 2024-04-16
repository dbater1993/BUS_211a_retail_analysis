import pandas as pd
import plotly.express as px

def display_statistics(data, filter_value):
    """ Display basic statistics for the filtered data. """
    print(f"Statistics for {filter_value}:")
    if data.empty or data['sales'].dropna().empty:
        print("No data matches your selection. Please try different filters.")
    else:
        print(f"Total Sales: {data['sales'].sum():,.2f}")
        print(f"Average Sales: {data['sales'].mean():,.2f}")
        print(f"Median Sales: {data['sales'].median():,.2f}")
        print(f"Minimum Sales: {data['sales'].min():,.2f}")
        print(f"Maximum Sales: {data['sales'].max():,.2f}")
        print(f"Standard Deviation: {data['sales'].std():,.2f}")
        print(f"Variance: {data['sales'].var():,.2f}\n")

def display_sales_ranking(data):
    """ Display ranking of kinds of business by total sales over the selected time period,
        along with the best and worst performing time periods for each included business,
        as well as the average annual and average period amount of sales.
    """
    print("Sales Ranking by Total Sales:")
    if data.empty or data['sales'].dropna().empty:
        print("No data matches your selection. Please try different filters.")
        return
    
    total_sales = data.groupby('kind_of_business')['sales'].sum().sort_values(ascending=False)
    for kind_of_business, total_sale in total_sales.items():
        business_data = data[data['kind_of_business'] == kind_of_business]
        if business_data.empty:
            continue
        best_period = business_data.loc[business_data['sales'].idxmax()]['sales_month'].strftime('%Y-%m-%d')
        worst_period = business_data.loc[business_data['sales'].idxmin()]['sales_month'].strftime('%Y-%m-%d')
        total_months = len(business_data['sales_month'].dt.to_period('M').unique())
        average_annual_sales = total_sale / (total_months / 12)
        average_period_sales = total_sale / len(business_data)
        print(f"{kind_of_business}: Best Period: {best_period}, Worst Period: {worst_period}, Total Sales: {total_sale:,.2f}, Average Annual Sales: {average_annual_sales:,.2f}, Average Period Sales: {average_period_sales:,.2f}")

# Load data
df = pd.read_csv(r'C:\Users\dbate\OneDrive\Desktop\Brandeis MBA\BUS 211 Foundations of Data Analytics\us_retail_sales.csv')
df['sales_month'] = pd.to_datetime(df['sales_month'])

while True:
    # Get unique kinds of business
    kinds_of_business = df['kind_of_business'].unique()

    # Display kinds of business and allow selection
    print("Select kinds of business (multiple selections allowed):")
    print("0. Select All")
    for i, business in enumerate(kinds_of_business, 1):
        print(f"{i}. {business}")

    selected_business_indices = input("Enter the numbers of the kinds of business you want to select (e.g., '1 3 5' for multiple selections): ")
    selected_business_indices = selected_business_indices.split()
    selected_businesses = [kinds_of_business[int(i) - 1] for i in selected_business_indices]

    # Get date range
    print("\nEnter date range:")
    start_date = pd.Timestamp(input("Enter the start date (YYYY-MM-DD), or leave blank for the earliest date: ") or df['sales_month'].min())
    end_date = pd.Timestamp(input("Enter the end date (YYYY-MM-DD), or leave blank for the latest date: ") or df['sales_month'].max())

    # Filter data based on selections
    filtered_data = df.copy()
    if '0' not in selected_business_indices:
        filtered_data = filtered_data[filtered_data['kind_of_business'].isin(selected_businesses)]
    if start_date != df['sales_month'].min() or end_date != df['sales_month'].max():
        filtered_data = filtered_data[(filtered_data['sales_month'] >= start_date) & (filtered_data['sales_month'] <= end_date)]

    # Display statistics for the filtered data
    for selected_business in selected_businesses:
        display_statistics(filtered_data[filtered_data['kind_of_business'] == selected_business], selected_business)

    # Create a time series graph
    fig = px.line(filtered_data, x='sales_month', y='sales', color='kind_of_business',
                  hover_data={'sales_month': '|%Y-%m-%d', 'kind_of_business': True, 'naics_code': True, 'sales': ':.2f'},
                  labels={'sales_month': 'Date', 'sales': 'Sales Amount', 'kind_of_business': 'Kind of Business', 'naics_code': 'NAICS Code'},
                  title='Retail Sales Over Time')
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(hovermode='closest')

    # Show the graph
    fig.show()

    # Display sales ranking
    display_sales_ranking(filtered_data)

    # Ask if user wants to run the program again
    if input("Do you want to run the program again? (yes/no): ").lower() != 'yes':
        break