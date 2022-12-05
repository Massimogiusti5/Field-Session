import pandas as pd
import matplotlib.pyplot as plt


def create_run_plot(filename: str):
    df = pd.read_csv(f'./data_visualization/clean_data/{filename}')

    # Create subplots
    f, (ax1, ax2) = plt.subplots(1, 2)
    f.suptitle(f'{filename[:-4]}')

    # Left plot CPUPerc
    df.groupby('Name')['CPUPerc'].plot(ax=ax1)
    ax1.set_ylabel("CPU Percentage")

    # Right plot Memory Percent
    df.groupby('Name')['MemPerc'].plot(ax=ax2)
    ax2.set_ylabel("Memory Percentage")

    handles, labels = ax2.get_legend_handles_labels()
    f.legend(handles, labels)
    plt.show()


def clean_data(filename: str):
    with open(f'./logs/{filename}', 'r') as f_in:
        with open(f'./data_visualization/clean_data/{filename}', 'w+') as f_out:

            input = f_in.read().split('\n')
            for i in input:
                j = i.split(',')
                if len(j) == 3:
                    j[1] = j[1].strip('%')
                    j[2] = j[2].strip('%')
                    f_out.write(','.join(j) + '\n')
