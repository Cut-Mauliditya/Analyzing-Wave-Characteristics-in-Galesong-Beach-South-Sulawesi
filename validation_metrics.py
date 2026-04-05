import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


ds = pd.read_excel('data_sortir.xlsx')

# obs data
wh = ds['h'].values     # wave height
wp = ds['p'].values     # wave period

#cal data
H_SPM = ds['HSPM'].values; T_SPM = ds['TSPM'].values
H_CEM = ds['HCEM'].values; T_CEM = ds['TCEM'].values
H_SMB = ds['HSMB'].values; T_SMB = ds['TSMB'].values
H_PM = ds['Hpierson'].values; T_PM = ds['Tpierson'].values

f_eff = ds['F'].values  # fetch effective
year = ds['YEAR'].values
month = ds['MO'].values

''''

scatter plot

'''

def bin_average(x, y, bins=50):
    bin_means_x = []
    bin_means_y = []
    bin_edges = np.linspace(0, 1, bins + 1)
    for i in range(bins):
        indices = (x >= bin_edges[i]) & (x < bin_edges[i + 1])
        if indices.any():
            bin_means_x.append(x[indices].mean())
            bin_means_y.append(y[indices].mean())
    return np.array(bin_means_x), np.array(bin_means_y)

methods = ['SPM', 'SMB', 'PM', 'CEM']
data_pairs = {
    'Tinggi': [(wh, H_SPM), (wh, H_SMB), (wh, H_PM), (wh, H_CEM)],
    'Periode': [(wp, T_SPM), (wp, T_SMB), (wp, T_PM), (wp, T_CEM)]
}

colors = ['blue', 'teal', 'red', 'green']
markers = ['^', '+', 'x', '*']

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
titles = ['Wave Height Validation', 'Wave Period Validation']

for i, (key, pairs) in enumerate(data_pairs.items()):
    ax = axes[i]
    for (obs, calc), method, color, marker in zip(pairs, methods, colors, markers):
        sorted_indices = np.argsort(obs)
        obs_sorted = obs[sorted_indices]
        calc_sorted = calc[sorted_indices]
        
        obs_norm = (obs - np.min(obs)) / (np.max(obs) - np.min(obs))
        calc_norm = (calc - np.min(calc)) / (np.max(calc) - np.min(calc))
        obs_binned, calc_binned = bin_average(obs_norm, calc_norm, bins=50)
        ax.scatter(obs_binned, calc_binned, label=method,  color=color, marker=marker, alpha=0.7, s=30)
    ax.plot([0, 1], [0, 1], 'k--', label='Identity Line') 
    ax.set_title(titles[i], fontsize=9)
    ax.set_xlabel('Obs', fontsize=9)
    ax.set_ylabel('Cal', fontsize=9)
    ax.legend(loc='upper left')
    ax.grid(True)

plt.tight_layout()
plt.show()

''''

validation metrics

'''

def rmse(h, t):
    HRMSE = ((np.sum((wh - h) ** 2)) / len(wh)) ** 0.5
    TRMSE = ((np.sum((wp - t) ** 2)) / len(wp)) ** 0.5
    
    return HRMSE, TRMSE

def mae(h, t):
    HMAE = (np.sum(np.abs(h - wh))) / len(wh)
    TMAE = (np.sum(np.abs(t - wp))) / len(wp)
    
    return HMAE, TMAE

def bias(h, t):
    Hbias = np.sum((h - wh) / len(wh))
    Tbias = np.sum((t - wp) / len(wp))
    
    return Hbias, Tbias

def coor(h, t):
    Hcoor = (np.sum((wh - np.mean(wh)) * (h - np.mean(h)))) / (
        np.sqrt(np.sum((h - np.mean(h)) ** 2)) * np.sqrt(np.sum((wh - np.mean(wh)) ** 2)))
    Tcoor = (np.sum((wp - np.mean(wp)) * (t - np.mean(t)))) / (
        np.sqrt(np.sum((t - np.mean(t)) ** 2)) * np.sqrt(np.sum((wp - np.mean(wp)) ** 2)))
    
    return Hcoor, Tcoor

def rs(h, t):
    Hrs = 1 - ((np.sum((h - wh) ** 2)) / (np.sum((h - np.mean(wh)) ** 2)))
    Trs = 1 - ((np.sum((t - wp) ** 2)) / (np.sum((t - np.mean(wp)) ** 2)))
    
    return Hrs, Trs

RMSE_HSPM, RMSE_TSPM = rmse(H_SPM, T_SPM)
RMSE_HCEM, RMSE_TCEM = rmse(H_CEM, T_CEM)
RMSE_HSMB, RMSE_TSMB = rmse(H_SMB, T_SMB)
RMSE_Hpierson, RMSE_Tpierson = rmse(H_PM, T_PM)


MAE_HSPM, MAE_TSPM = mae(H_SPM, T_SPM)
MAE_HCEM, MAE_TCEM = mae(H_CEM, T_CEM)
MAE_HSMB, MAE_TSMB = mae(H_SMB, T_SMB)
MAE_Hpierson, MAE_Tpierson = mae(H_PM, T_PM)

bias_HSPM, bias_TSPM = bias(H_SPM, T_SPM)
bias_HCEM, bias_TCEM = bias(H_CEM, T_CEM)
bias_HSMB, bias_TSMB = bias(H_SMB, T_SMB)
bias_Hpierson, bias_Tpierson = bias(H_PM, T_PM)

rs_HSPM, rs_TSPM = rs(H_SPM, T_SPM)
rs_HCEM, rs_TCEM = rs(H_CEM, T_CEM)
rs_HSMB, rs_TSMB = rs(H_SMB, T_SMB)
rs_Hpierson, rs_Tpierson = rs(H_PM, T_PM)

''''

plotting validation metrics

'''


Hrmse = [RMSE_HSPM, RMSE_HCEM, RMSE_HSMB, RMSE_Hpierson]
Prmse = [RMSE_TSPM, RMSE_TCEM, RMSE_TSMB, RMSE_Tpierson]
Hmae = [MAE_HSPM, MAE_HCEM, MAE_HSMB, MAE_Hpierson]
Pmae = [MAE_TSPM, MAE_TCEM, MAE_TSMB, MAE_Tpierson]
Hrs = [rs_HSPM, rs_HCEM, rs_HSMB, rs_Hpierson]
Prs = [rs_TSPM, rs_TCEM, rs_TSMB, rs_Tpierson]

label = ['SPM', 'CEM', 'SMB', 'PM']
color_rmse = ['teal', 'teal'] 
color_mae = ['steelblue', 'steelblue']
color_rs = ['#9B59B6', '#AF7AC5']

fig, axs = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

def add_values(ax, values, positions):
    for i, v in enumerate(values):
        ax.text(v + 0.05, positions[i], f"{v:.2f}", va='center', fontsize=10)

axs[0].barh(label, Prmse, color=color_rmse[0], edgecolor='black', label='wave periode', alpha=0.7)
axs[0].barh(label, Hrmse, color=color_rmse[1], edgecolor='black', label='wave height', hatch="//")
add_values(axs[0], Prmse, np.arange(len(label)))
add_values(axs[0], Hrmse, np.arange(len(label)))
axs[0].set_title('RMSE', fontsize=13)
axs[0].legend(fontsize=12, loc='upper right')
axs[0].set_xlim(0, 3.3)
axs[0].set_yticklabels(label, rotation=90, fontsize=12, va='center')

axs[1].barh(label, Pmae, color=color_mae[0], edgecolor='black', label='wave periode', alpha=0.7)
axs[1].barh(label, Hmae, color=color_mae[1], edgecolor='black', label='wave height', hatch="//")
add_values(axs[1], Pmae, np.arange(len(label)))
add_values(axs[1], Hmae, np.arange(len(label)))
axs[1].set_title('MAE', fontsize=13)
axs[1].legend(fontsize=12, loc='upper right')
axs[1].set_xlim(0, 3)

axs[2].barh(label, Hrs, color=color_rs[1], edgecolor='black', label='wave height')
axs[2].barh(label, Prs, color=color_rs[0], edgecolor='black', label='wave periode', alpha=0.7, hatch="//")
add_values(axs[2], Prs, np.arange(len(label)))
add_values(axs[2], Hrs, np.arange(len(label)))
axs[2].set_title('R²', fontsize=13)
axs[2].legend(fontsize=12, loc='upper right')
axs[2].set_xlim(0, 1.5)

for ax in axs:
    ax.invert_yaxis()
    #ax.grid(linewidth=0.5)

fig.tight_layout()
plt.show()
