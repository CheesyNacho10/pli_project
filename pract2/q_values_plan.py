import argparse
import pandas as pd
import os
import json
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Get Q-values plan')
parser.add_argument('experiment_dir', metavar='experiment_dir', type=str, help='experiment directory')

args = parser.parse_args()

experiment_dir = os.path.join(os.getcwd(), args.experiment_dir)
if (not os.path.exists(experiment_dir)):
  print("Error: Experiment directory does not exist")
  exit(1)

metadata_path = os.path.join(experiment_dir, 'metadata.json')
metadata_dict = json.loads(open(metadata_path, 'r').read())

plan_path = os.path.join(experiment_dir, 'planing.csv')
plan_df = pd.read_csv(plan_path)

plt.hist(plan_df['action_q'], bins=10)
plt.xlabel('Q-values')
plt.ylabel('Number of actions')
plt.title('Q-values plan histogram\n' + os.path.basename(os.path.normpath(args.experiment_dir)))
plt.savefig('q_values_plan_histogram_' + os.path.basename(os.path.normpath(args.experiment_dir)) + '.png')
