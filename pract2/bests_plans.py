import argparse
import pandas as pd
import os
import json
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Get best plans')
parser.add_argument('results_dir', metavar='results_dir', type=str, help='results directory')

args = parser.parse_args()

results_dir = args.results_dir
if (not os.path.exists(results_dir)):
  print("Error: Results directory does not exist")
  exit(1)

plans_results = {}
for subdir in os.listdir(results_dir):
  subdir_path = os.path.join(results_dir, subdir)
  if os.path.isdir(subdir_path):
    planning_results_path = os.path.join(subdir_path, 'planing.csv')
    planning_df = pd.read_csv(planning_results_path)
    num_steps = planning_df.shape[0]

    metadata_path = os.path.join(subdir_path, 'metadata.json')
    metadata_dict = json.loads(open(metadata_path, 'r').read())

    plans_results[num_steps] = plans_results.get(num_steps, []) + [metadata_dict]

plans_results_histogram = []
for key in plans_results.keys():
  for value in plans_results[key]:
    plans_results_histogram.append(key)

plt.hist(plans_results_histogram, bins=100)
plt.xlabel('Number of steps')
plt.ylabel('Number of plans')
plt.savefig(os.path.join(results_dir, 'num_steps_distirbution.png'))

plt.clf()

# Histogram of number of plans of each length, only for usable plans (less than 100 steps)
plt.hist([num_steps for num_steps in plans_results_histogram if num_steps < 500], bins=50)
plt.xlabel('Number of steps')
plt.ylabel('Number of plans')
plt.savefig(os.path.join(results_dir, 'num_steps_distirbution_usable.png'))

sorted_results = sorted(plans_results.items(), key=lambda x: x[0])
with open(os.path.join(results_dir, 'sorted_num_steps.txt'), 'w') as f:
  for num_steps, metadata_list in sorted_results:
    f.write("Number of steps: " + str(num_steps) + "\n")
    for metadata_dict in metadata_list:
      f.write('\t' + str(metadata_dict) + "\n")
    f.write("\n")
