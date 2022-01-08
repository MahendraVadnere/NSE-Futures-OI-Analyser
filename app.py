import streamlit as st
from pynse import *
import datetime
import matplotlib.pyplot as plt
import mplfinance as mpf
import plotly.express as px
nse=Nse()

st.set_page_config(page_title="OI Analyser", page_icon=":bar_chart:", layout="wide")

share = ['NIFTY', 'BANKNIFTY', 'FINNIFTY', 'AARTIIND', 'ABBOTINDIA', 'ABCAPITAL', 'ABFRL', 'ACC', 'ADANIENT','ADANIPORTS','ALKEM','AMARAJABAT','AMBUJACEM','APLLTD','APOLLOHOSP','APOLLOTYRE','ASHOKLEY','ASIANPAINT','ASTRAL',	'ATUL',	'AUBANK',	'AUROPHARMA',	'AXISBANK',	'BAJAJ-AUTO',	'BAJAJFINSV',	'BAJFINANCE',	'BALKRISIND',	'BALRAMCHIN',	'BANDHANBNK',	'BANKBARODA',	'BATAINDIA',	'BEL',	'BERGEPAINT',	'BHARATFORG',	'BHARTIARTL',	'BHEL',	'BIOCON',	'BOSCHLTD',	'BPCL',	'BRITANNIA',	'BSOFT',	'CADILAHC',	'CANBK',	'CANFINHOME',	'CHAMBLFERT',	'CHOLAFIN',	'CIPLA',	'COALINDIA',	'COFORGE',	'COLPAL',	'CONCOR',	'COROMANDEL',	'CROMPTON',	'CUB',	'CUMMINSIND',	'DABUR',	'DALBHARAT',	'DEEPAKNTR',	'DELTACORP',	'DIVISLAB',	'DIXON',	'DLF',	'DRREDDY',	'EICHERMOT',	'ESCORTS',	'EXIDEIND',	'FEDERALBNK',	'FSL',	'GAIL',	'GLENMARK',	'GMRINFRA',	'GNFC',	'GODREJCP',	'GODREJPROP',	'GRANULES',	'GRASIM',	'GSPL',	'GUJGASLTD',	'HAL',	'HAVELLS',	'HCLTECH',	'HDFC',	'HDFCAMC',	'HDFCBANK',	'HDFCLIFE',	'HEROMOTOCO',	'HINDALCO',	'HINDCOPPER',	'HINDPETRO',	'HINDUNILVR',	'HONAUT',	'IBULHSGFIN',	'ICICIBANK',	'ICICIGI',	'ICICIPRULI',	'IDEA',	'IDFC',	'IDFCFIRSTB',	'IEX',	'IGL',	'INDHOTEL',	'INDIACEM',	'INDIAMART',	'INDIGO',	'INDUSINDBK',	'INDUSTOWER',	'INFY',	'IOC',	'IPCALAB',	'IRCTC',	'ITC',	'JINDALSTEL',	'JKCEMENT',	'JSWSTEEL',	'JUBLFOOD',	'KOTAKBANK',	'L&TFH',	'LALPATHLAB',	'LAURUSLABS',	'LICHSGFIN',	'LT',	'LTI',	'LTTS',	'LUPIN',	'M&M',	'M&MFIN',	'MANAPPURAM',	'MARICO',	'MARUTI',	'MCDOWELL-N',	'MCX',	'METROPOLIS',	'MFSL',	'MGL',	'MINDTREE',	'MOTHERSUMI',	'MPHASIS',	'MRF',	'MUTHOOTFIN',	'NAM-INDIA',	'NATIONALUM',	'NAUKRI',	'NAVINFLUOR',	'NBCC',	'NESTLEIND',	'NMDC',	'NTPC',	'OBEROIRLTY',	'OFSS',	'ONGC',	'PAGEIND',	'PEL',	'PERSISTENT',	'PETRONET',	'PFC',	'PFIZER',	'PIDILITIND',	'PIIND',	'PNB',	'POLYCAB',	'POWERGRID',	'PVR',	'RAIN',	'RAMCOCEM',	'RBLBANK',	'RECLTD',	'RELIANCE',	'SAIL',	'SBICARD',	'SBILIFE',	'SBIN',	'SHREECEM',	'SIEMENS',	'SRF',	'SRTRANSFIN',	'STAR',	'SUNPHARMA',	'SUNTV',	'SYNGENE',	'TATACHEM',	'TATACOMM',	'TATACONSUM',	'TATAMOTORS',	'TATAPOWER',	'TATASTEEL',	'TCS',	'TECHM',	'TITAN',	'TORNTPHARM',	'TORNTPOWER',	'TRENT',	'TVSMOTOR',	'UBL',	'ULTRACEMCO',	'UPL',	'VEDL',	'VOLTAS',	'WHIRLPOOL',	'WIPRO',	'ZEEL']

st.title('Futures OI Data Analysis')
with st.sidebar:
    select_share = st.selectbox("Select Share", share)
    from_date = st.date_input(
        "From Date", datetime.date.today() - datetime.timedelta(days=30)
    )
    to_date = st.date_input("To Date", datetime.date.today())
symbol= select_share

if to_date < from_date or to_date > datetime.date.today():
    st.error("check from date and to date")

else:

    trading_days = nse.get_hist(from_date=from_date, to_date=to_date).index
    trading_days = list(trading_days.map(lambda x: x.date()))
    data = pd.DataFrame()

    for date in trading_days:
        try:
            bhav = nse.bhavcopy_fno(date).loc[symbol]
            bhav = bhav[bhav["INSTRUMENT"].isin(["FUTSTK", "FUTIDX"])]
            expiry_list = list(bhav["EXPIRY_DT"].sort_values())
            current_expiry = expiry_list[0]
            #current_expiry = current_expiry.date()

            coi = bhav["OPEN_INT"].sum()
            ccoi = bhav["CHG_IN_OI"].sum()

            bhav["DATE"] = bhav["TIMESTAMP"].apply(
                lambda x: datetime.datetime.strptime(x, "%d-%b-%Y").date()
            )
            
            bhav = bhav[bhav["EXPIRY_DT"] == current_expiry]

            bhav["OPEN_INT"] = coi
            bhav["CHG_IN_OI"] = ccoi
            bhav["SYMBOLS"] = symbol

            bhav.set_index("DATE", inplace=True)
            data = data.append(bhav)
        except Exception as e:
            print(f"error {e} for {date}")

    data = data[
        [
            "SYMBOLS",
            "EXPIRY_DT",
            "OPEN",
            "HIGH",
            "LOW",
            "CLOSE",
            "CONTRACTS",
            "OPEN_INT",
            "CHG_IN_OI",
        ]
    ]  
    data.index = data.index.map(pd.to_datetime)
    data.index = data.index.date

    data['%_CHG_IN_PRICE'] = (data['CLOSE'].pct_change())*100
    data['%_CHG_IN_OI'] = (data['CHG_IN_OI']/(data['OPEN_INT']-data['CHG_IN_OI']))*100
    data['EXPIRY_DT'] = pd.to_datetime(data['EXPIRY_DT']).dt.date
    #data['DATE'] = pd.to_datetime(data['DATE']).dt.date
    
    def color_negative_red(value):
        """
        Colors elements in a dateframe
        green if positive and red if
        negative. Does not color NaN
        values.
        """

        if value < 0:
            color = 'red'
        # elif value > 0:
        #     color = 'green'
        else:
            color = 'white'
        return 'color: %s' % color

    data = data.style.applymap(color_negative_red, subset=['%_CHG_IN_PRICE','%_CHG_IN_OI'])    
    #st.dataframe(data.style.highlight_max(axis = 0))
    st.write(data)
