import os
import random
import subprocess
import datetime
import collections

def generate_prompt():
    user = os.getlogin()
    machine_name = os.uname().nodename
    folder_name = os.path.basename(os.getcwd())
    prompt = f"\033[91m[S.A.T] - \033[94mU: \033[34m{user} \033[94m- M: \033[34m{machine_name} \033[37mon \033[37m[\033[34m{folder_name}\033[37m]$\033[0m "
    return prompt


def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Lire les données de sortie en temps réel
    output = ''
    while process.poll() is None:
        line = process.stdout.readline().rstrip('\n')
        if line:
            output += line + '\n'
            print(line)  # Afficher la sortie en temps réel
    
    # Lire les données d'erreur après la fin de l'exécution
    error = process.stderr.read().rstrip('\n')
    
    # Vérifier si des données d'erreur sont présentes
    if error:
        print(f"\033[91m{error}\033[0m")
    
    return output, error


def log_command(command, output, audit_log_name):
    with open(audit_log_name, 'a') as file:
        file.write(f"## Command: {command}\n")
        file.write(f"### Output:\n\n```\n{output}\n```\n\n")


def log_timeline(command, timeline_name):
    with open(timeline_name, 'a') as file:
        file.write(f"- {command}\n")


def generate_timeline_chart(commands, timeline_name):
    command_count = collections.Counter(commands)
    chart_data = ""
    for command, count in command_count.items():
        chart_data += f"{command}: {count}\n"

    with open(timeline_name, 'a') as file:
        file.write("\n## Command Timeline\n")
        file.write("Command | Recurrence\n")
        file.write("--- | ---\n")
        file.write(chart_data)

def main(audit_log_name, timeline_name):
    os.system('clear')
    os.system('echo "-- S.A.T (Security Audit Terminal) -- \n> CTRL + C to exit\n"')
    commands = []

    while True:
        try:
            command = input(generate_prompt())
            if command == "exit":
                break

            output, error = execute_command(command)
            log_command(command, output, audit_log_name)
            log_timeline(command, timeline_name)
            commands.append(command)

            print(output)
            if error:
                print(f"\033[91m{error}\033[0m")
        except KeyboardInterrupt:
            break

    generate_timeline_chart(commands, timeline_name)


if __name__ == "__main__":
    
    audit_log_name = str(input("Enter the name of the audit log file (without extension): "))
    audit_log_name = audit_log_name if audit_log_name else "audit_log" + random.randint(0, 1000)
    audit_log_name = audit_log_name if audit_log_name.endswith(".md") else audit_log_name + ".md"
    timeline_name = "timeline_" + audit_log_name
    
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass
    
    audit_log_name = os.path.join("logs", audit_log_name)
    timeline_name = os.path.join("logs", timeline_name)
    
    with open(audit_log_name, 'w') as file:
        file.write("# Security Audit Log\n")
        file.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    with open(timeline_name, 'w') as file:
        file.write("# Command Timeline\n")

    main(audit_log_name, timeline_name)
