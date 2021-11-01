import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
from matplotlib.dates import MonthLocator
import seaborn as sns

data = pd.read_csv('//data/tbl_sp_take_home_subset.csv')


#Data Clean
data['IS_GIFT'] = data['IS_GIFT'].replace({'false': False, 'true': True, "\\\\N": None})
data['DELIVERED_DATE'] = pd.to_datetime(data['DELIVERED_DATE'], errors='coerce')
data['row_sub_total'] = data['UNIT_PRICE'] * data['QUANTITY']

delivery_months = data[['row_sub_total', 'QUANTITY', 'UNIT_PRICE', 'VOLUME','VOLUME_UNITS','IS_GIFT', 'DELIVERED_DATE']].groupby([pd.Grouper(key='DELIVERED_DATE', freq='M')]).sum()

data_bs_sub = data[data['COMPANY_NAME'] == "Beam Suntory"]
dm_bs = data_bs_sub[['row_sub_total', 'QUANTITY', 'UNIT_PRICE', 'VOLUME','VOLUME_UNITS','IS_GIFT', 'DELIVERED_DATE']].groupby([pd.Grouper(key='DELIVERED_DATE', freq='M')]).sum()

sns.lineplot(data=delivery_months, x= delivery_months.index, y='row_sub_total')
sns.lineplot(data=dm_bs, x=dm_bs.index, y='row_sub_total')

sns.lineplot(data=dm_bs, x=dm_bs.index, y='UNIT_PRICE')
axes = plt.gca()
axes.xaxis.set_minor_locator(MonthLocator(bymonth=range(1, 13)))
#plt.axes().tick_params(axis='x', which='minor')
axes.set_ylim(ymin=0)
axes.ticklabel_format(axis='y', style='plain')
plt.xticks(dm_bs.index, rotation=90)

fig = plt.gcf()
fig.tight_layout()
#ax = plt.gca()
plt.show()

delivery_months_counts = data[['row_sub_total', 'QUANTITY', 'UNIT_PRICE', 'VOLUME','VOLUME_UNITS','IS_GIFT', 'DELIVERED_DATE']].groupby([pd.Grouper(key='DELIVERED_DATE', freq='M')]).count()

sns.lineplot(data=delivery_months_counts, x=delivery_months_counts.index, y='row_sub_total')

delivery_months_avg = data[['row_sub_total', 'QUANTITY', 'UNIT_PRICE', 'VOLUME','VOLUME_UNITS','IS_GIFT', 'DELIVERED_DATE']].groupby([pd.Grouper(key='DELIVERED_DATE', freq='M')]).mean()
sns.lineplot(data=delivery_months_avg, x=delivery_months_counts.index, y='row_sub_total')

delivery_months_avg_bs = data_bs_sub[['row_sub_total', 'QUANTITY', 'UNIT_PRICE', 'VOLUME','VOLUME_UNITS','IS_GIFT', 'DELIVERED_DATE']].groupby([pd.Grouper(key='DELIVERED_DATE', freq='M')]).mean()
sns.lineplot(data=delivery_months_avg_bs, x=delivery_months_counts.index, y='row_sub_total')

data.groupby('ORDER_ID')['QUANTITY'].count()

unique_orders = data.groupby([pd.Grouper(key='DELIVERED_DATE', freq='M')])['ORDER_ID'].nunique()
sns.lineplot(data=unique_orders, x=unique_orders.index, y=unique_orders.values)
unique_orders_sub = data_bs_sub.groupby([pd.Grouper(key='DELIVERED_DATE', freq='M')])['ORDER_ID'].nunique()
sns.lineplot(data=unique_orders_sub, x=unique_orders_sub.index, y=unique_orders_sub.values)

dma_bucket = data[['row_sub_total', 'DELIVERED_DATE', 'DELIVERY_DMA']].groupby([pd.Grouper(key='DELIVERED_DATE', freq='M'), 'DELIVERY_DMA']).count()
dma_bucket.reset_index(inplace=True)

sns.catplot(data=dma_bucket, kind="swarm", x='DELIVERED_DATE', y="row_sub_total", hue='DELIVERY_DMA')

accounts = data[['USER_ID', 'DELIVERED_DATE']].groupby([pd.Grouper(key='DELIVERED_DATE', freq='M')]).nunique()