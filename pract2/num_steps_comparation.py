import argparse
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Number of steps comparison')

variables_choices = ['episodes', 'lr', 'maxSteps', 'gamma', 'epsilon', 'decay']
parser.add_argument('results_dir', type=str, help='results directory')
parser.add_argument('first_variable', type=str, choices=variables_choices, help='first variable to compare')
parser.add_argument('second_variable', type=str, choices=variables_choices, help='second variable to compare')

args = parser.parse_args()

results_dir = os.path.join(os.getcwd(), args.results_dir)
if not os.path.exists(results_dir):
  print("Error: Results directory does not exist")
  exit(1)

if args.first_variable == args.second_variable:
  print("Error: The two variables must be different")
  exit(1)

# Dictionary to store default variable values
variables = {'episodes': 1000, 'lr': 0.2, 'maxSteps': 100, 'gamma': 0.99, 'epsilon': 0.9, 'decay': 0.001}

# Set the variables to be compared to None
variables[args.first_variable] = None
variables[args.second_variable] = None

# Build regex pattern
pattern_parts = []
for var in variables_choices:
  if variables[var] is not None:
    pattern_parts.append(f"{var}_{str(variables[var]).replace('.', '-')}")
  else:
    pattern_parts.append(f"{var}_\\d+-?\\d*")

regex_pattern = '_'.join(pattern_parts)
regex = re.compile(regex_pattern)

# Find matching directories
dirs = [d for d in os.listdir(results_dir) if os.path.isdir(os.path.join(results_dir, d)) and regex.match(d)]

# Initialize results dictionary
results_dict = {}

variables_indices = {var: i for i, var in enumerate(variables_choices, start=1)}

# Loop over directories and read data
for d in dirs:
  dir_parts = d.split('_')
  
  first_index = variables_indices[args.first_variable] * 2 - 1
  second_index = variables_indices[args.second_variable] * 2 - 1
  
  try:
    first_value = float(dir_parts[first_index].replace('-', '.'))
  except ValueError:
    print(f"Error: Invalid value for {args.first_variable} in directory name {d}")
    continue
  
  try:
    second_value = float(dir_parts[second_index].replace('-', '.'))
  except ValueError:
    print(f"Error: Invalid value for {args.second_variable} in directory name {d}")
    continue

  planning_results_path = os.path.join(results_dir, d, 'planing.csv')
  if not os.path.isfile(planning_results_path):
    print(f"Error: File does not exist {planning_results_path}")
    continue

  planning_df = pd.read_csv(planning_results_path)
  num_steps = planning_df.shape[0]

  if first_value not in results_dict:
    results_dict[first_value] = {}
  results_dict[first_value][second_value] = num_steps

# Iterate through results to plot
max_num_steps = 0
for first_value, second_dict in results_dict.items():
  second_values = list(second_dict.keys())
  num_steps = [num_step for num_step in list(second_dict.values()) if num_step < 500]
  if len(num_steps) == 0:
    continue
  max_num_steps = max(max_num_steps, max(num_steps))
  plt.plot(second_values, num_steps, 'o-', label=f'{args.first_variable}={first_value}')

plt.xlabel(args.second_variable + ' values')
plt.ylabel('Number of steps')
plt.title('Number of steps comparison')
plt.legend()
# y from 0 to 1.1 * max(y)
axes = plt.gca()
axes.set_ylim([0, 1.5 * max_num_steps])
plt.savefig(os.path.join(results_dir, f"{args.first_variable}_vs_{args.second_variable}.png"))
