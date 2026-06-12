# Analyzing-Wave-Characteristics-in-Galesong
Galesong, located in Takalar Regency, is a densely populated coastal area facing threats from high waves during the west monsoon, which lead to coastal erosion and damage to coastal infrastructure. This study was conducted to analyze the characteristics of wave at Galesong Beach and evaluate the accuracy of wave calculation methods, including SPM, CEM, SMB, PM.

## Results
### Observed Wind and Wave
During the west monsoon, speeds ranged was varied in range 1–11 m/s, the first transitional season (March-May) saw speeds of 1–6 m/s. The east monsoon exhibited speeds of 1–9 m/s, while the second transitional season recorded 1–9 m/s.

Wind speed correlated positively with wave height—higher wind speeds generated larger waves. Wave direction followed the prevailing seasonal wind direction that came from the southwest, northwest, and west. Consequently, the west monsoon produced the highest waves, while the first transitional season generated the lowest.

Plots included:
#####
<img height="100" alt="wind_rose" src="https://github.com/user-attachments/assets/0961985c-c999-42f2-81ea-b8c1031ba8e8" />
<img height="100" alt="proba2" src="https://github.com/user-attachments/assets/7d877ba3-665b-4b39-9c06-5bd6d657668d" />


### Wave Calculation
Among the methods tested, PM demonstrated the highest accuracy for wave height estimation, achieving an RMSE of 0.2233, MAE of 0.1638, and R² of 0.68. SPM also performed well, followed by SMB and CEM. However, all methods performed poorly in estimating wave period, with very low R² values. SPM yielded the best results among them (RMSE: 1.4439, MAE: 1.2397, R²: 0.01), followed by CEM. SMB and PM showed substantial errors.

Plots included:
#####
<img height="100" alt="obs-cal" src="https://github.com/user-attachments/assets/add9fcfb-5cf8-44ab-8470-e0b691e283a5" />
<img height="100" alt="2" src="https://github.com/user-attachments/assets/6674d976-85f7-4d9b-96c8-1197eb139014" />
<img height="100" alt="vali" src="https://github.com/user-attachments/assets/e5f9224e-7dcb-42cf-8bba-a5336eeff936" />

### Calculation Data Analysis
In January, wave heights showed significant variation with outliers reaching 2.5 m, though the highest data density was concentrated between 0.5–1 m. Wave periods varied, with outliers up to 7 s and peak density in the 4–5 s range.

Based on Weibull distribution parameters, wave height peaked in the northwest (NW) direction and was lowest in the southwest (SW) direction, indicating a dominance of low waves from the SW. For wave period, NW also exhibited the highest λ, representing the longest propagation duration, while SW showed the shortest period, indicating shorter-duration waves from that direction.

Plots included:
#####
<img height="100" alt="h-t" src="https://github.com/user-attachments/assets/c71605b1-16d0-48b7-8d68-b7a3217eb01e" />
<img height="100" alt="weibull" src="https://github.com/user-attachments/assets/18018a79-ca66-48d1-b525-0e90970380af" />

#####
#####
My undergraduate thesis on wave modeling is available here:
"Seasonal wave dynamics and model validation at Galesong Beach, South Sulawesi"
https://doi.org/10.12912/27197050/204858
