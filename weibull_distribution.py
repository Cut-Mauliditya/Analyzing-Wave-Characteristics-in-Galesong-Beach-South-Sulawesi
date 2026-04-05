
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

ds = pd.read_excel('data_sortir.xlsx')

# obs data
wh = ds['h'].values     # wave height
wp = ds['p'].values     # wave period

year = ds['YEAR']
month = ds['MO'].astype(int)

#cal data
H_SPM = ds['HSPM'].values; T_SPM = ds['TSPM'].values
H_CEM = ds['HCEM'].values; T_CEM = ds['TCEM'].values
H_SMB = ds['HSMB'].values; T_SMB = ds['TSMB'].values
H_PM = ds['Hpierson'].values; T_PM = ds['Tpierson'].values


''''

Monthly Wave Height and Period

'''


if 8 not in month.values:
    jul_data = ds[month == 7][H_PM, T_SPM].mean()
    sep_data = ds[month == 9][H_PM, T_SPM].mean()

    aug_mean = (jul_data + sep_data) / 2
    aug_row = {'month': 8, 'Hpierson': aug_mean['Hpierson'], 'TSPM': aug_mean['TSPM'], 'year': year.mode()[0]}
    df = pd.concat([ds, pd.DataFrame([aug_row])], ignore_index=True)

all_months = pd.DataFrame({'month': np.arange(1, 13)})
df = all_months.merge(df, on=month, how='left')
overall_mean = df.groupby(month)[H_PM, T_SPM].mean().reset_index()
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


''''

weibull distribution

'''

d = pd.read_excel('data_weibul.xlsx')

hsw = d['HSW'].values
tsw = d['TSW'].values
hw = d['HW'].values
tw = d['TW'].values
hnw = d['HNW'].values
tnw = d['TNW'].values

hsw = hsw[np.isfinite(hsw)]
tsw = tsw[np.isfinite(tsw)]
hnw = hnw[np.isfinite(hnw)]
tnw = tnw[np.isfinite(tnw)]

from scipy.stats import weibull_min

def weibull(h, t):
    lambda_h = np.mean(h)
    params_h = weibull_min.fit(h, floc=0)
    k_h, loc, lambda_h = params_h

    lambda_t = np.mean(t)
    params_t = weibull_min.fit(t, floc=0)
    k_t, loc, lambda_t = params_t
    
    x1 = np.linspace(np.min(h), np.max(h), 100)
    h_pdf = weibull_min.pdf(x1, k_h, scale=lambda_h)
    h_cdf = weibull_min.cdf(x1, k_h, scale=lambda_h)
    
    x2 = np.linspace(np.min(t), np.max(t), 100)
    t_pdf = weibull_min.pdf(x2, k_t, scale=lambda_t)
    t_cdf = weibull_min.cdf(x2, k_t, scale=lambda_t)
    
    return h_pdf, t_pdf, h_cdf, t_cdf

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))

sns.kdeplot(hsw, ax=ax1, label='H SW', fill=True)
sns.kdeplot(hw, ax=ax1, label='H W', fill=True)
sns.kdeplot(hnw, ax=ax1, label='H NW', fill=True)
ax1.set_xlabel('(m)', fontsize=9)
ax1.set_ylabel('Kepadatan Tinggi Gelombang', fontsize=9)
ax1.tick_params(axis='x', labelsize=7)
ax1.tick_params(axis='y', labelsize=7)
ax1.legend(loc='upper right', fontsize=7)

sns.kdeplot(tsw, ax=ax2, label='T SW', fill=True)
sns.kdeplot(tw, ax=ax2, label='T W', fill=True)
sns.kdeplot(tnw, ax=ax2, label='T NW', fill=True)
ax2.set_xlabel('(s)', fontsize=9)
ax2.set_ylabel('Kepadatan Periode Gelombang', fontsize=9)
ax2.tick_params(axis='x', labelsize=7)
ax2.tick_params(axis='y', labelsize=7)
ax2.legend(loc='upper right', fontsize=7)

fig.tight_layout(rect=[0.05, 0.05, 1, 0.95])
plt.show()
