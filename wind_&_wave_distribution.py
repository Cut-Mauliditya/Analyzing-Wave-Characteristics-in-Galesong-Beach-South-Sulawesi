import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


''''

 Windrose function

'''

from windrose import WindroseAxes

d = pd.read_excel('data2.xlsx')

def season(month):
    if month in [1, 2, 12]:  
        return 'West'
    elif month in [3, 4, 5]:  
        return 'Transition 1'
    elif month in [6, 7, 8]:  
        return 'East'
    elif month in [9, 10, 11]:  
        return 'Transition 2'
    else:
        return None

d['Musim'] = d['M'].apply(season)
d.to_csv('data_musim.csv', index=False)

max_speed = max(d[['Sb', 'Sp1', 'St', 'Sp2']].max())

def windrose(Dm, Sm, ax, title, cmap, legend, bin): 

    ''''
    Dm: wind direction at m season
    Sm: wind speed at m season
    title: ('_plot_title_')
    legend: ('_legend_title_')

    '''

    valid_data = d[[Dm, Sm]].dropna()
    
    if valid_data.empty:
        print(f"no data for {Dm} and {Sm}.")
        return

    D = valid_data[Dm].values
    S = valid_data[Sm].values

    try:
        ax.bar(D, S, normed=True, opening=0.8, edgecolor='white', cmap=cmap, bins=bin)
        ax.set_title(title, fontsize=12)
        ax.legend(title=legend, loc='lower left')
    except Exception as e:
        print(f"Error : {e}")

''''

plotting windrose 

'''

fig = plt.figure(figsize=(16, 8))  

# wind plot
ax1 = fig.add_subplot(2, 4, 1, projection='windrose')  
windrose('Db', 'Sb', ax1, 'DJF', cm.viridis, 'WS (m/s)', np.linspace(1, 11, 5))     #West monsoon
ax2 = fig.add_subplot(2, 4, 2, projection='windrose')  
windrose('Dp1', 'Sp1', ax2, 'MAM', cm.viridis, 'WS (m/s)', np.linspace(1, 11, 5))   #Transition season 1
ax3 = fig.add_subplot(2, 4, 3, projection='windrose') 
windrose('Dt', 'St', ax3, 'JJA', cm.viridis, 'WS (m/s)', np.linspace(1, 11, 5))     #East monsoon
ax4 = fig.add_subplot(2, 4, 4, projection='windrose')  
windrose('Dp2', 'Sp2', ax4, 'SON', cm.viridis, 'WS (m/s)', np.linspace(1, 11, 5))   #Transition season 2

# wave plot
ax5 = fig.add_subplot(2, 4, 5, projection='windrose')  
windrose('wb', 'Hb', ax5, 'DJF', cm.viridis, 'H (m)', np.linspace(0, 2, 5))     #West monsoon
ax6 = fig.add_subplot(2, 4, 6, projection='windrose')  
windrose('wp1', 'Hp1', ax6, 'MAM', cm.viridis, 'H (m)', np.linspace(0, 2, 5))   #Transition season 1
ax7 = fig.add_subplot(2, 4, 7, projection='windrose') 
windrose('wt', 'Ht', ax7, 'JJA', cm.viridis, 'H (m)', np.linspace(0, 2, 5))     #East monsoon
ax8 = fig.add_subplot(2, 4, 8, projection='windrose')  
windrose('wp2', 'Hp2', ax8, 'SON', cm.viridis, 'H (m)', np.linspace(0, 2, 5))   #Transition season 2

plt.tight_layout()
plt.show()


''''
Percentage of wave height and direction
'''

df = pd.read_excel('data_sortir.xlsx')

def fetch_class(f):
    if f == 340.9889:
        return 'SW'     #SW: South West
    elif f == 495.7826:
        return 'W'      #W: West
    elif f == 347.426:
        return 'NW'     #NW: North West
    else:
        return None  

def wave_height_class(h):
    if 0.0 <= h < 0.4:
        return '0.0-0.4'
    elif 0.4 <= h < 0.8:
        return '0.4-0.8'
    elif 0.8 <= h < 1.2:
        return '0.8-1.2'
    elif 1.2 <= h < 1.5:
        return '1.2-1.5'
    elif 1.5 <= h < 1.9:
        return '1.5-1.9'
    else:
        return '>=1.9'

df['Fetch'] = df['F'].apply(fetch_class)
df['Wave Height'] = df['h'].apply(wave_height_class)
df = df.dropna(subset=['Fetch'])

pivot_table = df.pivot_table(
    values='h', 
    index='Fetch Category', 
    columns='Wave Height Category', 
    aggfunc='count',  
    fill_value=0
)
pivot_table['Total'] = pivot_table.sum(axis=1)
pivot_table.loc['Total'] = pivot_table.sum(axis=0)
pivot_table_percentage = (pivot_table / pivot_table.loc['Total', 'Total'])*100
pivot_table_percentage.loc['Total', 'Total'] = 100

print(pivot_table_percentage)
pivot_table_percentage.to_excel('hasil_persentase_wave_height.xlsx')

''''

data distribution 

'''

dm = pd.read_excel('data_musimb.xlsx')

colors_wd = ['steelblue', 'royalblue']
colors_ws = ['salmon', 'peru']

fig, axs = plt.subplots(4, 4, figsize=(16, 12))

# DJF | West monsoon
axs[0, 0].hist(dm['Db'].values, bins=30, color=colors_wd[0], alpha=0.6, label='DJF')
axs[0, 0].set_ylabel('Probability', fontsize=10)
axs[0, 0].legend(loc='upper left')
axs[0, 0].set_xlabel('WD (°)', fontsize=10)

axs[0, 1].hist(dm['Sb'].values, bins=30, color=colors_ws[0], alpha=0.6, label='DJF')
axs[0, 1].set_ylabel('Probability', fontsize=10)
axs[0, 1].legend(loc='upper right')
axs[0, 1].set_xlabel('WS (m/s)', fontsize=10)

axs[0, 2].hist(dm['wb'].values, bins=30, color=colors_wd[1], alpha=0.6, label='DJF')
axs[0, 2].set_ylabel('Probability', fontsize=10)
axs[0, 2].legend(loc='upper left')
axs[0, 2].set_xlabel('HWD (°)', fontsize=10)

axs[0, 3].hist(dm['Hb'].values, bins=30, color=colors_ws[1], alpha=0.6, label='DJF')
axs[0, 3].set_ylabel('Probability', fontsize=10)
axs[0, 3].legend(loc='upper right')
axs[0, 3].set_xlabel('H (m)', fontsize=10)

# MAM | Transition season 1
axs[1, 0].hist(dm['Dp1'].values, bins=30, color=colors_wd[0], alpha=0.6, label='MAM')
axs[1, 0].set_ylabel('Probability', fontsize=10)
axs[1, 0].legend(loc='upper left')
axs[1, 0].set_xlabel('WD (°)', fontsize=10)

axs[1, 1].hist(dm['Sp1'].values, bins=30, color=colors_ws[0], alpha=0.6, label='MAM')
axs[1, 1].set_ylabel('Probability', fontsize=10)
axs[1, 1].legend(loc='upper right')
axs[1, 1].set_xlabel('WS (m/s)', fontsize=10)

axs[1, 2].hist(dm['wp1'].values, bins=30, color=colors_wd[1], alpha=0.6, label='MAM')
axs[1, 2].set_ylabel('Probability', fontsize=10)
axs[1, 2].legend(loc='upper left')
axs[1, 2].set_xlabel('HWD (°)', fontsize=10)

axs[1, 3].hist(dm['Hp1'].values, bins=30, color=colors_ws[1], alpha=0.6, label='MAM')
axs[1, 3].set_ylabel('Probability', fontsize=10)
axs[1, 3].legend(loc='upper right')
axs[1, 3].set_xlabel('H (m)', fontsize=10)

# JJA | East monsoon
axs[2, 0].hist(dm['Dt'].values, bins=30, color=colors_wd[0], alpha=0.6, label='JJA')
axs[2, 0].set_ylabel('Probability', fontsize=10)
axs[2, 0].legend(loc='upper left')
axs[2, 0].set_xlabel('WD (°)', fontsize=10)

axs[2, 1].hist(dm['St'].values, bins=30, color=colors_ws[0], alpha=0.6, label='JJA')
axs[2, 1].set_ylabel('Probability', fontsize=10)
axs[2, 1].legend(loc='upper right')
axs[2, 1].set_xlabel('WS (m/s)', fontsize=10)

axs[2, 2].hist(dm['wt'].values, bins=30, color=colors_wd[1], alpha=0.6, label='JJA')
axs[2, 2].set_ylabel('Probability', fontsize=10)
axs[2, 2].legend(loc='upper left')
axs[2, 2].set_xlabel('HWD (°)', fontsize=10)

axs[2, 3].hist(dm['Ht'].values, bins=30, color=colors_ws[1], alpha=0.6, label='JJA')
axs[2, 3].set_ylabel('Probability', fontsize=10)
axs[2, 3].legend(loc='upper right')
axs[2, 3].set_xlabel('H (m)', fontsize=10)

# SON | Transition season 2
axs[3, 0].hist(dm['Dp2'].values, bins=30, color=colors_wd[0], alpha=0.6, label='SON')
axs[3, 0].set_xlabel('WD (°)', fontsize=10)
axs[3, 0].set_ylabel('Probability', fontsize=10)
axs[3, 0].legend(loc='upper left')

axs[3, 1].hist(dm['Sp2'].values, bins=30, color=colors_ws[0], alpha=0.6, label='SON')
axs[3, 1].set_xlabel('WS (m/s)', fontsize=10)
axs[3, 1].set_ylabel('Probability', fontsize=10)
axs[3, 1].legend(loc='upper right')

axs[3, 2].hist(dm['wp2'].values, bins=30, color=colors_wd[1], alpha=0.6, label='SON')
axs[3, 2].set_xlabel('HWD (°)', fontsize=10)
axs[3, 2].set_ylabel('Probability', fontsize=10)
axs[3, 2].legend(loc='upper left')

axs[3, 3].hist(dm['Hp2'].values, bins=30, color=colors_ws[1], alpha=0.6, label='SON')
axs[3, 3].set_xlabel('H (m)', fontsize=10)
axs[3, 3].set_ylabel('Probability', fontsize=10)
axs[3, 3].legend(loc='upper right')

plt.tight_layout()
plt.show()

