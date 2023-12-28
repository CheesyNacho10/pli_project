import subprocess

episodes = [500, 1000, 2000]
lrs = [0.1, 0.2, 0.3]
max_steps = [50, 100, 150]
gammas = [0.9, 0.95, 0.99]
epsilons = [0.9, 0.95, 0.99]
decays = [0.001, 0.005, 0.01]

python_env_path = "C:/Users/Nacho/MUIARFID/PLI/pli_project/.env/Scripts/python.exe"
script_path = "practica.py"

# Ejecutar el script con diferentes combinaciones de argumentos
for episode in episodes:
    for lr in lrs:
        for max_step in max_steps:
            for gamma in gammas:
                for epsilon in epsilons:
                    for decay in decays:
                        command = [python_env_path, script_path, "Robots_no_cons", 
                                   "--episodes", str(episode), 
                                   "--lr", str(lr), 
                                   "--max_steps", str(max_step),
                                   "--gamma", str(gamma),
                                   "--epsilon", str(epsilon),
                                   "--decay", str(decay)]
                        subprocess.run(command)
