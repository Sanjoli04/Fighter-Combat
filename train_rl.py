if __name__ == "__main__":
    import random
    import numpy as np
    import collections
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from fighter_env import FighterEnv
    # CONFIG
    BATCH_SIZE = 64
    GAMMA = 0.99
    EPS_START = 1.0
    EPS_END = 0.05
    EPS_DECAY = 0.999988
    TARGET_UPDATE_FREQUENCY = 2000
    MEMORY_CAPCITY = 80000
    LEARNING_RATE = 5e-4
    TOTAL_STEPS = 500000


    # DQN NETWORK
    class QNetwork(nn.Module):
        def __init__(self, state_dim, action_dim):
            super(QNetwork, self).__init__()
            self.fc1 = nn.Linear(state_dim, 128)
            self.fc2 = nn.Linear(128, 128)
            self.fc3 = nn.Linear(128, action_dim)

        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = torch.relu(self.fc2(x))
            return self.fc3(x)

    class ReplayBuffer:
        def __init__(self, capacity):
            self.buffer = collections.deque(maxlen=capacity)

        def push(self, state, action, reward, next_state, done):
            self.buffer.append((state, action, reward, next_state, done))

        def sample(self, batch_size):
            # Breaks correlation between subsequent gameplay sequence frames
            state, action, reward, next_state, done = zip(*random.sample(self.buffer, batch_size))
            return (torch.FloatTensor(np.array(state)),
                    torch.LongTensor(action),
                    torch.FloatTensor(reward),
                    torch.FloatTensor(np.array(next_state)),
                    torch.FloatTensor(done))
        def __len__(self):
            return len(self.buffer)
    env = FighterEnv(render_mode=None)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    policy_net = QNetwork(state_dim, action_dim).to(device)
    target_net = QNetwork(state_dim, action_dim).to(device)
    target_net.load_state_dict(policy_net.state_dict())

    optimizer = optim.Adam(policy_net.parameters(), lr = LEARNING_RATE)
    memory = ReplayBuffer(MEMORY_CAPCITY)
    loss_fn = nn.MSELoss()

    obs, _ = env.reset()
    epsilon = EPS_START
    episode_reward = 0.0
    all_episode_rewards = []
    total_fights = 0
    ai_wins = 0

    for step in range(TOTAL_STEPS):        
        if random.random() < epsilon:
            action = env.action_space.sample()
        else:
            state_tensor = torch.FloatTensor(obs).to(device)
            with torch.no_grad():
                action = policy_net(state_tensor).argmax().item()

        next_obs, reward, terminated, truncated, _= env.step(action)
        done = terminated or truncated
        episode_reward += reward 

        memory.push(obs, action, reward, next_obs, done)
        obs = next_obs

        if done:
            total_fights += 1
            if env.human_target.health <=0: ai_wins += 1
            obs,_ = env.reset()
            all_episode_rewards.append(episode_reward)
            episode_reward = 0.0

        epsilon = max(EPS_END, epsilon * EPS_DECAY)

        if len(memory) > BATCH_SIZE:
            states,actions,rewards, next_states,dones = memory.sample(BATCH_SIZE)
            states = states.to(device)
            actions  = actions.unsqueeze(1).to(device)
            rewards = rewards.to(device)
            next_states = next_states.to(device)
            dones = dones.to(device)

            current_q_values = policy_net(states).gather(1, actions).squeeze()

            with torch.no_grad():
                next_max_q = target_net(next_states).max(1)[0]

                target_q_values = rewards + (GAMMA * next_max_q * (1- dones))
            loss = loss_fn(current_q_values,  target_q_values)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        if step % TARGET_UPDATE_FREQUENCY == 0:
            target_net.load_state_dict(policy_net.state_dict())
        if (step + 1) % 5000 == 0:
            mean_rew = np.mean(all_episode_rewards[-15:] if all_episode_rewards else 0.0)
            print("AI Wins: ", ai_wins, " | Total Fights: ", total_fights)
            print(f"Step Array Element Count: {step+1}/{TOTAL_STEPS} | Epsilon Boundary: {epsilon:.3f} | Recent 15 Episodes Mean Reward Scalar: {mean_rew:.2f}")
            ai_wins, total_fights = 0, 0
    torch.save(policy_net.state_dict(), "custom_pytorch_dqn_fighter.pth")
    print("Model tensors written out to filesystem successfully as custom_pytorch_dqn_fighter.pth")