import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


ds = pd.read_excel('data_sortir.xlsx')

ws = ds['WS'].values    # wind speed
wd = ds['WD'].values    # wind direction
wh = ds['h'].values     # wave height
wp = ds['p'].values     # wave period

f_eff = ds['F'].values  # fetch effective
year = ds['YEAR'].values
month = ds['MO'].values

''''

wave prediction calculation 

'''

###  SPM method  ###

g = 10 
U = 1.026*ws

def SPM(s, f) :
    H_SPM = []
    T_SPM = []
    
    for i in range(len(ws)):
        WS_i = s[i]
        Feff = f[i]
        
        if Feff <= 120 :
            H1 = 0.0016*((WS_i**2)/g)*(((g*Feff)/(WS_i**2))**(1/2))
            T1 = 0.2857*(WS_i/g)*(((g*Feff)/(WS_i**2))**(1/3))
            H_SPM.append(H1)
            T_SPM.append(T1)  
        else :
            H3 = 0.2433*((WS_i**2)/g)
            T3 = 8.134*(WS_i/g)
            H_SPM.append(H3)
            T_SPM.append(T3)
    return H_SPM, T_SPM

###  CEM method  ###

def CEM(s, f) :
    H_CEM = []
    T_CEM = []

    for i in range(len(ws)):
        WS_i = s[i]
        Feff = f[i]
    
        Cd = 0.001 * (1.1 + 0.035 * WS_i)
        u = (Cd * (WS_i**2))**0.5
    
        if Feff <= 200 :
            H_nf = 0.0413*((u**2)/g)*(((g*Feff)/(u**2))**0.5)
            T_nf = 0.651*(u/g)*(((g*Feff)/(u**2))**(1/3))
            H_CEM.append(H_nf)
            T_CEM.append(T_nf)
        else:
            H_fl = (2.115*(10**2))*((u**2)/g)
            T_fl = (2.398*(10**2))*(u/g)
            H_CEM.append(H_fl)
            T_CEM.append(T_fl)
    return H_CEM, T_CEM

###  SMB method  ###

H_SMB = (0.26/g)*(ws**2)
T_SMB = (2.4*3.14)*(ws/g)*(np.tanh(0.077*((g*f_eff)/(ws**2))**(0.25)))
        
###  Pierson-Moskowitz Model  ###

H_PM = 0.21*((U**2)/(g))
T_PM = 1.25*0.83*(U/g)**(0.5)

'''''

plotting wave calculation 

'''

import seaborn as sns

fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12, 10))

### 1
sns.lineplot(data=ds, x='YEAR', y='h', ax=axes[0, 0], label='Obs', color='royalblue')
sns.lineplot(data=ds, x='YEAR', y='HSPM', ax=axes[0, 0], label='SPM', color='darkorange')
axes[0, 0].set_xlabel('')
axes[0, 0].set_ylabel('H (m)')

sns.lineplot(data=ds, x='YEAR', y='p', ax=axes[0, 1], label='Obs', color='navy')
sns.lineplot(data=ds, x='YEAR', y='TSPM', ax=axes[0, 1], label='SPM', color='olivedrab')
axes[0, 1].set_xlabel('')
axes[0, 1].set_ylabel('P (s)')

### 2
sns.lineplot(data=ds, x='YEAR', y='h', ax=axes[1, 0], label='Obs', color='royalblue')
sns.lineplot(data=ds, x='YEAR', y='HCEM', ax=axes[1, 0], label='CEM', color='darkorange')
axes[1, 0].set_xlabel('')
axes[1, 0].set_ylabel('H (m)')

sns.lineplot(data=ds, x='YEAR', y='p', ax=axes[1, 1], label='Obs', color='navy')
sns.lineplot(data=ds, x='YEAR', y='TCEM', ax=axes[1, 1], label='CEM', color='olivedrab')
axes[1, 1].set_xlabel('')
axes[1, 1].set_ylabel('P (s)')

### 3
sns.lineplot(data=ds, x='YEAR', y='h', ax=axes[2, 0], label='Obs', color='royalblue')
sns.lineplot(data=ds, x='YEAR', y='HSMB', ax=axes[2, 0], label='SMB', color='darkorange')
axes[2, 0].set_xlabel('')
axes[2, 0].set_ylabel('H (m)')

sns.lineplot(data=ds, x='YEAR', y='p', ax=axes[2, 1], label='Obs', color='navy')
sns.lineplot(data=ds, x='YEAR', y='TSMB', ax=axes[2, 1], label='SMB', color='olivedrab')
axes[2, 1].set_xlabel('')
axes[2, 1].set_ylabel('P (s)')

### 4
sns.lineplot(data=ds, x='YEAR', y='h', ax=axes[3, 0], label='Obs', color='royalblue')
sns.lineplot(data=ds, x='YEAR', y='Hpierson', ax=axes[3, 0], label='PM', color='darkorange')
axes[3, 0].set_xlabel('')
axes[3, 0].set_ylabel('H (m)')

sns.lineplot(data=ds, x='YEAR', y='p', ax=axes[3, 1], label='Obs', color='navy')
sns.lineplot(data=ds, x='YEAR', y='Tpierson', ax=axes[3, 1], label='PM', color='olivedrab')
axes[3, 1].set_xlabel('')
axes[3, 1].set_ylabel('P (s)')

for ax in axes.flat:
    ax.legend(loc='upper right') 


plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()


''''

Monthly Wave Height and Period

'''

df = pd.read_excel('data_sortir.xlsx')
year = df['YEAR']
month = df['MO'].astype(int)

if 8 not in df['month'].values:
    jul_data = df[month == 7][['Hpierson', 'TSPM']].mean()
    sep_data = df[month == 9][['Hpierson', 'TSPM']].mean()
    aug_mean = (jul_data + sep_data) / 2
    aug_row = {'month': 8, 'Hpierson': aug_mean['Hpierson'], 'TSPM': aug_mean['TSPM'], 'year': year.mode()[0]}
    df = pd.concat([df, pd.DataFrame([aug_row])], ignore_index=True)

all_months = pd.DataFrame({'month': np.arange(1, 13)})
df = all_months.merge(df, on='month', how='left')
overall_mean = df.groupby('month')[['Hpierson', 'TSPM']].mean().reset_index()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']

fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(10, 5), sharex=True, gridspec_kw={'hspace': 0})

sns.boxplot(x=df['month'], y=df['Hpierson'], ax=ax0,  boxprops=dict(color="black", facecolor="white"),
            flierprops=dict(markerfacecolor='black', marker='o', markersize=5), medianprops=dict(color="black"), 
            width=0.3)
ax0.plot(overall_mean['month'] - 1, overall_mean['Hpierson'], linestyle='--', marker='o', color='black', markersize=6, label='wave height')
ax0.set_ylabel('H (m)', fontsize=12)
ax0.set_xlabel('')
ax0.legend(loc='upper right', fontsize=10)

sns.boxplot(x=df['month'], y=df['TSPM'], ax=ax1, boxprops=dict(color="black", facecolor="white"),
            flierprops=dict(markerfacecolor='black', marker='o', markersize=5), medianprops=dict(color="black"), 
            width=0.3)
ax1.plot(overall_mean['month'] - 1, overall_mean['TSPM'], linestyle='--', marker='o', color='black', markersize=6, label='wave periode')
ax1.set_ylabel('P (s)', fontsize=12)
ax1.set_xlabel('')
ax1.set_xticks(np.arange(12))  
ax1.set_xticklabels(month_names, fontsize=11)
ax1.legend(loc='upper right', fontsize=10)

plt.tight_layout()
plt.show()
