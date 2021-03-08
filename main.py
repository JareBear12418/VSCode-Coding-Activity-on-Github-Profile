import matplotlib.pyplot as plt
from git import Repo
import numpy as np
import time
import json

plt.style.use("dark_background")

PATH_TO_TIMETRAKED_JSON_FILE: str = '/home/jared/.vscode/extensions/fabriciorojas.localtimetracker-1.0.6/timeTrakedL.json'
# cd /home/jared/Documents/Python-Projects/Activity-Tracker/JareBear12418/; /usr/bin/env /usr/local/bin/python3.8 /home/jared/Documents/Python-Projects/Activity-Tracker/JareBear12418/main.py
def update_file_to_commit():
    # read file
    with open(PATH_TO_TIMETRAKED_JSON_FILE, 'r') as f:
        timeTrakedL = json.load(f)

    time_in_each_lang = {}
    dict_lang_names = []
    # Get all languages from across all projects
    for i, d1 in enumerate(timeTrakedL['dates']):
        lTime = d1['languageTime']
        dict_lang_names.append(list(lTime.keys()))
    # Add all the language names into one list
    all_used_languages = []
    for lst in dict_lang_names:
        for item in lst: all_used_languages.append(item)
    # Remove duplicate languages
    all_used_languages = list(set(all_used_languages))
    # Make a dictionary with all the language names in place
    for langauge in all_used_languages: time_in_each_lang.update({langauge:[]})
    # Add all times in each language into respective language name creating a list of all the times.
    for i, d1 in enumerate(timeTrakedL['dates']):
        lTime = d1['languageTime']
        for name in lTime: time_in_each_lang[name].append(lTime.get(name))
    # addying the sum of each list to get one number and not a list of numbers.
    for i in  time_in_each_lang:
        sum_of_list = (sum(time_in_each_lang[i]))
        time_in_each_lang[i] = sum_of_list

    # Sort the dictionary
    time_in_each_lang = dict(sorted(time_in_each_lang.items(), key=lambda item: item[1]))
    # Reverse dictionary
    time_in_each_lang = dict(reversed(time_in_each_lang.items()))

    # Split up keys and values from the dictionary into two lists.
    time_in_each_lang_KEYS = []
    time_in_each_lang_VALUES = []
    for key, value in time_in_each_lang.items():
        time_formating = (
            time.strftime("%-Hh %-Mm %-Ss",  time.gmtime(value)) if value > 3600 else
            time.strftime("%-Mm %-Ss",  time.gmtime(value)) if value > 60 else
            time.strftime("%-Ss",  time.gmtime(value))
            )
        # print (key, value)
        time_in_each_lang_KEYS.append(key + f' - {time_formating}')
        time_in_each_lang_VALUES.append(value)

    def combine_column_names(column_name,cur_value,sums):
        percentage = round(cur_value/sums*100,2)
        return "{} {}%".format(column_name,percentage)

    # Create a graph with matplotlib with all the data we have in the time_in_each_lang dictionary.
    data = time_in_each_lang
    base_d = sum(list(data.values()))
    final_data = {combine_column_names(k,m,base_d):m/base_d*100 for k,m in data.items()}

    _, ax = plt.subplots(figsize=(6, 5), subplot_kw=dict(aspect="equal"))
    lang_names = list(final_data.keys())
    data = list(final_data.values())
    wedges, _ = ax.pie(data, wedgeprops=dict(width=0.7), startangle=-40)
    kw = dict(arrowprops=dict(arrowstyle="-"),zorder=0, va="center")

    plt.gca().legend(time_in_each_lang_KEYS, loc='center right', bbox_to_anchor=(1,0.5,0.5,0.5))
    for i, p in enumerate(wedges):
        if data[i] > 1:
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(lang_names[i],
                        xy=(x, y),
                        xytext=(1*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)
    plt.xticks([])
    plt.yticks([])
    plt.savefig('/home/jared/Documents/Python-Projects/Activity-Tracker/JareBear12418/stats.png', bbox_inches='tight', dpi=100, transparent=True)

FILE_TO_COMMIT_NAME: str = 'stats.png'

def commit_repository():
    repo = Repo('/home/jared/Documents/Python-Projects/Activity-Tracker/JareBear12418/.git')
    repo.index.add([FILE_TO_COMMIT_NAME])
    repo.index.commit(f'stats.png Updated!')
    origin = repo.remote('origin')
    origin.push()

if __name__ == '__main__':
    update_file_to_commit()
    # commit_repository()