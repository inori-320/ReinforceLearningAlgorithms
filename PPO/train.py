import torch
import gym
import numpy as np
import matplotlib.pyplot as plt
from ppo import PPO

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")

n_episode = 300
step = 1000
actor_learning_rate = 1e-3
critic_learning_rate = 1e-2
num_episodes = 500
hidden_dim = 128
gamma = 0.98
lmbda = 0.95
epochs = 10
eps = 0.2

env_name = 'CartPole-v1'
env = gym.make(env_name)
torch.manual_seed(0)
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n
agent = PPO(state_dim, hidden_dim, action_dim, actor_learning_rate, critic_learning_rate, lmbda, epochs, eps, gamma)

reward_buffer = []  # 记录积累奖励
reward_mean_buffer = []

for episode_i in range(n_episode):
    state = env.reset()
    episode_reward = 0
    transition_dict = {'states': [], 'actions': [], 'next_states': [], 'rewards': [], 'dones': []}
    for step_i in range(step):
        if isinstance(state, tuple):  # 如果不加这段代码，state后面会多一条{}
            state = state[0]
        action = agent.take_action(state)
        next_state, reward, done, _, _ = env.step(action)
        if isinstance(next_state, tuple):
            next_state = next_state[0]
        transition_dict['states'].append(state)
        transition_dict['actions'].append(action)
        transition_dict['next_states'].append(next_state)
        transition_dict['rewards'].append(reward)
        transition_dict['dones'].append(done)
        state = next_state
        episode_reward += reward
        if done:
            reward_buffer.append(episode_reward)
            break

    agent.update(transition_dict)  # 在每个 episode 结束后更新
    reward_mean_buffer.append(np.mean(reward_buffer[-100:]))
    print(f"Episode: {episode_i}, avg.Reward: {np.mean(reward_buffer[-100:])}, Reward: {episode_reward}")

# 画出奖励轨迹
episodes_list = list(range(len(reward_buffer)))
plt.plot(episodes_list, reward_mean_buffer)
plt.xlabel('Episodes')
plt.ylabel('Returns')
plt.title('PPO on {}'.format(env_name))
plt.show()
