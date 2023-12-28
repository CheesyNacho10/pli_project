import numpy as np
import pddlgym
import random
import argparse
import os
import pandas as pd
import json
import time

parser = argparse.ArgumentParser(description='Q-learning planner')
parser.add_argument('domain', metavar='domain', type=str, help='domain name')
parser.add_argument('--episodes', default=1000, metavar='episodes', type=int, help='number of episodes')
parser.add_argument('--lr', default=0.2, metavar='lr', type=float, help='learning rate')
parser.add_argument('--max_steps', default=100, metavar='max_steps', type=int, help='maximum number of steps per episode')
parser.add_argument('--gamma', default=0.99, metavar='gamma', type=float, help='discount factor')
parser.add_argument('--epsilon', default=0.9, metavar='epsilon', type=float, help='initial exploration rate')
parser.add_argument('--decay', default=0.001, metavar='decay', type=float, help='exponential decay rate for exploration prob')
parser.add_argument('--verbose', default=False, metavar='verbose', type=bool, help='verbose mode')
args = parser.parse_args()

'''
EXPERIMENTAL SETUP
'''

# Create results directory
results_dir = os.path.join(os.getcwd(), 'experiments')
if not os.path.exists(results_dir):
  os.mkdir(results_dir)
results_dir = os.path.join(results_dir, args.domain)
if not os.path.exists(results_dir):
  os.mkdir(results_dir)
results_dir = os.path.join(results_dir, 'episodes_' + str(args.episodes) + \
                           '_lr_' + str(args.lr) + '_max_steps_' + str(args.max_steps) + \
                           '_gamma_' + str(args.gamma) + '_epsilon_' + str(args.epsilon) + \
                           '_decay_' + str(args.decay))
if not os.path.exists(results_dir):
  os.mkdir(results_dir)

# Results metadata
metadata = {
  'domain': args.domain,
  'max_episodes': args.episodes,
  'lr': args.lr,
  'max_steps': args.max_steps,
  'gamma': args.gamma,
  'initial_epsilon': args.epsilon,
  'decay': args.decay
}
with open(os.path.join(results_dir, 'metadata.json'), 'w') as f:
  json.dump(metadata, f)

# Results dataframe
training_df = pd.DataFrame(columns=['episode', 'episode_time', 'num_steps', 'steps_times', 'rewards', 'epsilon'])
plan_df = pd.DataFrame(columns=['action_q', 'action_time', 'reward'])

'''
INITIALIZATION OF THE ENVIRONMENT
'''

# Create pddlgym environment with the domain
env = pddlgym.make("PDDLEnv" + args.domain + "-v0")
env.fix_problem_index(0)

q_table = {}

'''
DEFINITION OF THE PARAMETERS OF THE ALGORITHM
'''

# Hyperparameters
total_episodes = args.episodes
learning_rate = args.lr # Alpha in Q-learning algorithm
max_steps = args.max_steps
gamma = args.gamma # Discount factor

# Exploration parameters
epsilon = args.epsilon # Initial exploration rate
decay_rate = args.decay # Exponential decay rate for exploration prob

print("Executing experiment with the following parameters:")
print("\tDomain: " + args.domain)
print("\tEpisodes: " + str(total_episodes))
print("\tLearning rate: " + str(learning_rate))
print("\tMax steps: " + str(max_steps))
print("\tGamma: " + str(gamma))
print("\tInitial epsilon: " + str(epsilon))
print("\tDecay: " + str(decay_rate))

'''
Q-LEARNING ALGORITHM
'''
print("Training...")

num_all_actions = None

for episode in range(total_episodes):
  state, debug = env.reset()

  episode_start_time = time.time()

  if not num_all_actions:
    env.action_space.all_ground_literals(state)
    all_actions = env.action_space._all_ground_literals
    num_all_actions = len(env.action_space._all_ground_literals)

    if args.verbose:
      print("Number of avaliable actions: " + str(num_all_actions))
      print("Avaliable actions:\n\t" + str(all_actions) + "\n")

  if args.verbose:
    print("\tEpisode " + str(episode))

  steps_times = []
  rewards = []

  for step in range(max_steps):
    '''
    EXPLORATION VS EXPLOITATION
    '''
    step_start_time = time.time()

    if args.verbose:
      print("\t\tStep " + str(step))
      print("\t\t\tState: " + str(state))

    possible_actions = list(env.action_space.all_ground_literals(state))
    possible_actions_indexes = [all_actions.index(action) for action in possible_actions]

    if random.uniform(0, 1) > epsilon: # EXPLOITATION (greedy action)
      sorted_all_actions_indexes = np.argsort(q_table.get(str(state), np.zeros(num_all_actions)))[::-1]
      posibles_sorted_actions_index = [action_index for action_index in sorted_all_actions_indexes if action_index in possible_actions_indexes]
      best_posible_action_index = posibles_sorted_actions_index[0]
      action = all_actions[best_posible_action_index]

      if args.verbose:
        print("\t\t\tAction by explotation: " + str(action))
    else: # EXPLORATION (random action)
      action = random.choice(possible_actions)

      if args.verbose:
        print("\t\t\tAction by exploration: " + str(action))

    new_state, reward, done, info = env.step(action)

    # Update Q-table
    old_value = q_table.get(str(state), np.zeros(num_all_actions))[all_actions.index(action)]
    next_max = np.max(q_table.get(str(new_state), np.zeros(num_all_actions)))

    # Q-learning formula
    new_value = old_value + learning_rate * (reward + gamma * next_max - old_value)
    q_table[str(state)] = q_table.get(str(state), np.zeros(num_all_actions))
    q_table[str(state)][all_actions.index(action)] = new_value

    # Update state
    state = new_state

    # Update metrics
    steps_times.append(time.time() - step_start_time)
    rewards.append(reward)

    # If done, finish episode
    if done:
      break
  
  # Reduce epsilon (because we need less and less exploration)
  epsilon = epsilon - decay_rate if epsilon > decay_rate else 0

  training_df.loc[len(training_df)] = {
    'episode': episode,
    'episode_time': time.time() - episode_start_time,
    'num_steps': step,
    'steps_times': steps_times,
    'rewards': rewards,
    'epsilon': epsilon,
  }

print("Training finished.")
q_table_tuples = [(state, value) for state, value in q_table.items()]
q_table_df = pd.DataFrame(q_table_tuples, columns=['state', 'actions'])
q_table_df.to_csv(os.path.join(results_dir, 'q_table.csv'))
training_df.to_csv(os.path.join(results_dir, 'training.csv'))

'''
PLANIFICATION
'''

state, debug = env.reset()
plan = []
done = False

print("Planning...")

while not done and len(plan) < 500: # HACK: limit plan length to 500 actions
  action_start_time = time.time()

  # Choose action with highest Q-value
  action_index = np.argmax(q_table.get(str(state), np.zeros(num_all_actions)))
  action = all_actions[action_index]

  # Add action to plan
  plan.append(action)

  # Update metrics
  action_q = q_table.get(str(state), np.zeros(num_all_actions))[action_index]

  # Apply action and generate new state
  state, reward, done, info = env.step(action)

  plan_df.loc[len(plan_df)] = {
    'action_q': action_q,
    'action_time': time.time() - action_start_time,
    'reward': reward
  }

if len(plan) == 500:
  print("WARNING: Plan length limit reached.")
else:
  print("Planning finished.\n")
plan_df.to_csv(os.path.join(results_dir, 'planing.csv'))

# Write plan to file
with open(os.path.join(results_dir, 'plan.txt'), 'w') as f:
  f.write('Number of actions: ' + str(len(plan)) + '\n\n')
  for action in plan:
    f.write(str(action) + '\n')
