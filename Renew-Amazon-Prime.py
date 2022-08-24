import streamlit as st
import pandas as pd
from pathlib import Path


st.set_page_config(page_title="Renew Amazon Prime 2022",layout="wide")



# CSS STYLING
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


st.markdown('# Should I renew Amazon Prime?')
st.markdown('# A cost-benefit analysis')
st.markdown('[GitHub](https://github.com/aleivaar94/Renew-Amazon-Prime-2022)')
st.markdown('#') # space separator
st.markdown('#') # space separator




col1, col2 = st.columns([2,3])

with col1:
    st.image('https://github.com/aleivaar94/portfolio-images/blob/main/amazon-prime-increase-2022.png?raw=true')
    st.image('https://github.com/aleivaar94/portfolio-images/blob/main/inflation-canada-2022.png?raw=true')
with col2:
    st.markdown('#') # space separator
    st.markdown( 
'''### As inflation increases, companies are not willing to absorb the costs of production, instead, they tend to pass the costs onto consumers. Amazon is one of them. With the price of Amazon Prime increasing by 20\\% (from \\$79 to \\$99 CAD), 
## Should I renew my Amazon Prime?
### In this project I analyse my amazon order history to make a data driven decision taking into consideration my spending habits, budget and benefits of Amazon Prime.''')

st.markdown('#') # space separator
st.markdown('#') # space separator

# INTRO COLUMNS
col1, col2, col3 = st.columns(3)

with col1:
    st.header("Data Collection")
    st.markdown('#') # space separator
    st.image("https://github.com/aleivaar94/portfolio-images/blob/main/amazon-request-data.png?raw=true", caption='Order history can be requested via the Request My Personal Information page. Once requested, a secure download link will be sent to the email address associated with the amazon account. This may take up to 30 days.')

with col2:
    st.header("Analysis")
    st.image("https://github.com/aleivaar94/portfolio-images/blob/main/boxplot-orders-2022.png?raw=true", caption='Most orders are below the minimum order amount to get free shipping for a non prime member ($25). Suggesting that prime is worth renewing.')
   

with col3:
    st.header("Results")
    st.image('https://github.com/aleivaar94/portfolio-images/blob/main/amazon-shipping-savings-2022-1.png?raw=true', caption='Modeling shipping estimates reveal that Amazon Prime saves me money, even after taking into account the cost of prime.')

st.markdown('#') # space separator
st.header('Amazon Order History (sample data)')

# Load data
# order_history_csv = Path(__file__)/'datasets/Retail.OrderHistory.1.csv'
order_history = pd.read_csv('master/datasets/Retail.OrderHistory.1.csv')
st.dataframe(order_history.head())

st.markdown('---') # line divider
st.header('1. Data Cleaning')

st.markdown('''
The code below preps the amazon orders dataset for analysis. Some cleaning and transformations include:
- Converting order date to datetime format.
- Changing the columns name to snake case.
- Converting numeric values to int or float data types.
- Grouping and performing aggregation calculations.
''')

data_cleaning_code = '''
# Rename columns
order_history.columns = order_history.columns.str.lower().str.replace(' ', '_')

# Select columns to work with
order_history = order_history[['website', 'product_name', 'order_id', 'order_date', 'unit_price',
                               'unit_price_tax', 'shipping_charge', 'total_discounts',
                               'total_owed']]

# Convert numeric columns from string to numeric data type
numeric_cols = order_history.iloc[:,4:]
numeric_cols.replace(',','', regex=True, inplace=True)
numeric_cols = list(numeric_cols.columns)
order_history[numeric_cols] = order_history[numeric_cols].apply(pd.to_numeric, errors='coerce', axis=1)

# Convert "order_date" column to datetime type 
order_history['order_date'] = order_history.order_date.str.replace('UTC','').str.strip()
order_history['order_date'] = pd.to_datetime(order_history.order_date, format='%m/%d/%Y %X')

# Filter purchases made after 2018 and in Amazon Canada
order_history = order_history[order_history.website == 'Amazon.ca']
order_history = order_history[(order_history.order_date > '2019-01-01')]

# Group data and perfom sum aggregation
order_history = order_history.groupby(['website','order_id', 'order_date']).agg(unit_price = ('unit_price','sum'),
                                                                         unit_price_tax = ('unit_price_tax', 'sum'),
                                                                         shipping_charge = ('shipping_charge', 'sum'),
                                                                         total_discounts = ('total_discounts', 'sum'),
                                                                         total_owed = ('total_owed', 'sum')).reset_index()

# Split order_date into year, month name and day columns
order_history['year'] = order_history['order_date'].dt.year
order_history['month'] = order_history['order_date'].dt.month_name()
order_history['day'] = order_history['order_date'].dt.day

# Sort data by year
order_history.sort_values(by=['year'], ascending=False, inplace=True)
'''
st.code(data_cleaning_code, language='python')

st.markdown('---') # line divider

st.header('2. Visualizing Distribution of Data')

    
col1, col2 = st.columns(2)

with col1:
    st.image("https://github.com/aleivaar94/portfolio-images/blob/main/boxplot-orders-2022.png?raw=true", caption='Most orders are below the minimum order amount to get free shipping for a non prime member ($25). This is consistent throughout the years. Suggesting that prime is worth renewing.')
    boxplot_code = '''
    fig = plt.figure(figsize = (10,5))
    ax = sns.boxplot(x='year', y='unit_price', data=order_history)
    ax.set_yticks(np.arange(0, max(order_history.unit_price)+15, 15))
    ax.set_xlabel('Year', fontsize = 10)
    ax.set_ylabel('$CAD', fontsize = 10)
    ax.axhline(24, ls='--', color='red')
    '''
    st.code(boxplot_code, language='python')


with col2:
    st.image("https://github.com/aleivaar94/portfolio-images/blob/main/histogram-orders-2022-1.png?raw=true", caption='Purchase amount is not normally distributed. Most purchase orders fall in the range $10 - $18.')
    histogram_code = '''
    fig = plt.figure(figsize = (10,5))
    ax = sns.histplot(x='unit_price', data=order_history)
    ax.set_xticks(np.arange(0, max(order_history.unit_price)+5, 10))
    ax.set_xlabel('$CAD', fontsize = 10)
    ax.set_ylabel('Count', fontsize = 10)
    ax.axvline(24, ls='--', color='red')
    ax.text(x=24, y=50, s='  Median', color='red')
    '''
    st.code(histogram_code, language='python')

st.markdown('---') # line divider

st.header('3. Analyzing Results')

st.markdown("Given that the order amount doesn't have a normal distribution, and because the standard deviation is close to the mean, the median rather than the mean is a better measure of describing the 'average' amount per amazon order. Therefore, most amazon orders are below \\$24 CAD, which is still lower than the minimum amount of \\$25 to obtain free shipping if you are not a prime member in Canada. So close though!")


col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('')

with col2:
    st.image('https://github.com/aleivaar94/portfolio-images/blob/main/orders-descriptive-statistics.png?raw=true')

with col3:
    st.markdown('')


describe_code = '''
# Calculate desciptive statistics
describe = pd.DataFrame(order_history.unit_price.describe())
describe.loc['median'] = order_history.unit_price.median()
describe.drop(['count', 'min'], inplace=True)
describe = describe.reindex(['mean', 'median', 
                            'std', 'max', 
                            '25%','50%','75%'])
'''
st.code(describe_code, language='python')


st.header('3.1 Modeling Shipping costs without Amazon Prime')

st.markdown(''' 
- Shipping rates depend on the shipping speed, the weight and the size of the items. For example, prime customers pay a flat rate of \\$6.99 for orders under \\$25, while non-prime members pay more than \\$11.99 for same-day shipping. 
- On the other hand, shipping rates for items sold by third party sellers and fulfilled by Amazon from outside Canada cost \\$4.99 + \\$3.28/kg and it takes 7-12 business days to arrive.
- As a conservative measure, shipping rates are estimated as \\$7.99 per shipment.
''')

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('')

with col2:
    st.image('https://github.com/aleivaar94/portfolio-images/blob/main/amazon-shipping-savings-2022-1.png?raw=true')
    
with col3:
    st.markdown('')

shipping_code = '''
# Orders with unit_price < 25 are assigned a shipping cost of $7.99 in a new shipping column
order_history['shipping'] = order_history['unit_price'].apply(lambda x: 7.99 if x < 25 else 0.0)

model = order_history.groupby('year')['shipping'].sum()
model = pd.DataFrame(model)
model['End up Saving ($CAD)'] = model.shipping - 99
model.rename(columns={'shipping':'Shipping without Prime ($CAD)'}, inplace=True)
model.index.names = ['Year']
model.style.format({'Shipping without Prime ($CAD)': '{:.2f}','End up Saving ($CAD)': '{:+g}'})
'''

st.code(shipping_code, language='python')

st.markdown('---') # line divider

st.header('4. Conclusion')

st.markdown('Although Amazon prime provides various benefits such as Prime Video, Prime Music, free shipping and exclusive deals, the only benefits I use are free shipping and exlusive deals. Based on my Amazon order history, prime provides value to me by lowering the total shipping costs I would have paid in a year, plus getting faster shipping. For example, in 2021 I would have paid \\$108.74 more on shipping costs if I was not a prime member. Therefore, next year **I will renew my prime membership** even if its price increased 20%. And I will continue to evaluate my decision on a yearly basis.')