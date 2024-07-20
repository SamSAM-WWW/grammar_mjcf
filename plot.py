import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# Read the CSV file
df = pd.read_csv('D:\pythoncode\grammar_mjcf\mjcf_model\\2024-05-10_15-40-19\design_rewards.csv')


# Extract data
reward = df['reward']
predict_reward = df['predict_reward']

# Calculate RMSE for each sample
rmse = np.sqrt(mean_squared_error(reward, predict_reward))

# Calculate MAE for each sample
mae_values = [mean_absolute_error(reward[:i+1], predict_reward[:i+1]) for i in range(len(reward))]

# Calculate moving average (MA) for rewards and predicted rewards
window_size = 20
ma_rewards = df['reward'].rolling(window=window_size).mean()
ma_predict_rewards = df['predict_reward'].rolling(window=window_size).mean()

# Calculate exponential moving average (EMA) for rewards and predicted rewards
ema_rewards = df['reward'].ewm(span=window_size, adjust=False).mean()
ema_predict_rewards = df['predict_reward'].ewm(span=window_size, adjust=False).mean()

# Plot reward and predicted reward
plt.figure(figsize=(10, 5))
plt.plot(reward, label='Reward')
plt.plot(predict_reward, label='Predicted Reward')
plt.title('Reward vs Predicted Reward')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Plot RMSE for each sample
samples = np.arange(1, len(reward) + 1)
rmse_values = []
for i in range(len(reward)):
    rmse_values.append(np.sqrt(mean_squared_error(reward[:i+1], predict_reward[:i+1])))
plt.figure(figsize=(10, 5))
plt.plot(samples, rmse_values, label='RMSE')
plt.title('Root Mean Squared Error (RMSE)')
plt.xlabel('Sample')

plt.ylim(0, 60)
plt.ylabel('Value')
plt.grid(True)
plt.tight_layout()

# Plot MA for rewards and predicted rewards
plt.figure(figsize=(10, 5))
# plt.plot(reward, label='Reward')
# plt.plot(predict_reward, label='Predicted Reward')
plt.plot(ma_rewards, label='MA Reward (MA20)')
plt.plot(ma_predict_rewards, label='MA Predicted Reward (MA20)')
# plt.plot(ema_rewards, label='EMA Reward (window=10)')
# plt.plot(ema_predict_rewards, label='EMA Predicted Reward (window=10)')
plt.title('Reward and Predicted Reward with Moving Average')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Plot MAE for each sample
samples = np.arange(1, len(reward) + 1)
plt.figure(figsize=(10, 5))
plt.plot(samples, mae_values, label='MAE')
plt.title('Mean Absolute Error (MAE)')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.grid(True)
plt.tight_layout()


# Plot reward only
plt.figure(figsize=(10, 5))
plt.plot(reward, label='Reward')
plt.title('Reward')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Plot MA for rewards 
plt.figure(figsize=(10, 5))
plt.plot(ma_rewards, label='MA Reward (MA20)')
plt.title('Reward with Moving Average')
plt.xlabel('Sample')
plt.ylabel('Value')
plt.legend()
plt.grid(True)
plt.tight_layout()

# Show plots
plt.show()