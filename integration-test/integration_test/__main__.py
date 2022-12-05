import os
import logging
import signal
import subprocess
import time
import argparse
from datetime import datetime

from data_visualization.create_post_run_plots import clean_data, create_run_plot


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number_messages",
                        default="1000",
                        type=str,
                        help="Number of messages to send to the consumers")
    parser.add_argument("-b", "--broker",
                        required=True,
                        help="The running broker")
    parser.add_argument("-d", "--docker-compose",
                        type=str,
                        default='../../infrastructure/docker-compose.yml',
                        help="The docker-compose file to run.")
    parser.add_argument("-t", "--time",
                        type=int,
                        default=None,
                        help="The amount of time to let the process run.")

    parser.add_argument("-m", "--message-rate",
                        type=str,
                        default='0',
                        help="The amount of time the generator sleeps before sending new messages.")
    args = parser.parse_args()
    return args


def start_docker_compose(docker_compose_file: str, log_folder: str = './logs/',
                         branch_type: str = '', run_time: int = 0):
    # Store CWD
    curr_wd = os.path.dirname(os.path.realpath(__file__))
    os.chdir(curr_wd)

    if not os.path.exists(docker_compose_file):
        logging.error(f'Unable to open: {docker_compose_file}')
        exit(-1)

    os.system(f'docker-compose -f {docker_compose_file} build')

    docker_command = ['docker-compose', '-f', docker_compose_file, 'up']
    process = subprocess.Popen(docker_command, stdout=subprocess.PIPE, preexec_fn=os.setsid)

    stats_process = subprocess.Popen(['docker', 'stats', '--format={{.Name}},{{.CPUPerc}},{{.MemPerc}}'],
                                     stdout=subprocess.PIPE, preexec_fn=os.setsid)

    # Stop the docker-compose process after n seconds if time flag is set
    if run_time is not None:
        time.sleep(run_time)
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)

    stdout = process.communicate()

    os.killpg(os.getpgid(stats_process.pid), signal.SIGTERM)
    stats_stdout = stats_process.communicate()

    file_name = log_folder + branch_type + datetime.now().strftime("%m-%d-%Y-%H:%M:%S") + '.txt'
    with open(file_name, 'w+') as f:
        f.write(stdout[0].decode("utf-8"))
    # Create metric file
    stats_file_name = branch_type + '-metrics-' + datetime.now().strftime("%m-%d-%Y-%H:%M:%S") + '.txt'
    with open(log_folder + stats_file_name, 'w+') as f:
        f.write('Name,CPUPerc,MemPerc\n')
        output = stats_stdout
        for i in output:
            if i is not None:
                i = i.decode("utf-8")
                i = i.split("\n")
                for j in i:
                    j = j.strip('\x1b[2J\x1b[H')
                    k = j.split(',')
                    if '--' not in k:
                        f.write(j + '\n')

    return stats_file_name


if __name__ == '__main__':
    args = parse_args()
    # Set the number of messages
    os.environ["NUMBER_MESSAGES"] = args.number_messages
    os.environ["MESSAGE_RATE_MS"] = args.message_rate
    branch_type = f'{args.broker}-{args.number_messages}-messages-'
    if args.message_rate != '0':
        branch_type += f'{args.message_rate}-delay-{args.time}-duration'
    stat_file_name = start_docker_compose(args.docker_compose,
                                          branch_type=branch_type,
                                          run_time=args.time)
    # Make sure there is time for the files to be closed properly before trying to be reopened.
    time.sleep(3)
    clean_data(stat_file_name)
    create_run_plot(stat_file_name)
