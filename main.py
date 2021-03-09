import json
import time

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import numpy as np
from git import Repo

import cv2
import numpy as np

from names_class import Language_Names
from logos_class import Logos_Names

plt.style.use("dark_background")

PATH_TO_TIMETRAKED_JSON_FILE: str = 'C:\\Users\\grossj\\.vscode\\extensions\\fabriciorojas.localtimetracker-1.0.6\\timeTrakedL.json'
# cd /home/jared/Documents/Python-Projects/Activity-Tracker/JareBear12418/; /usr/bin/env /usr/local/bin/python3.8 /home/jared/Documents/Python-Projects/Activity-Tracker/JareBear12418/main.py

def img_to_pie( fn, wedge, xy, zoom=1, ax = None):
    if ax is None: ax=plt.gca()
    im = plt.imread(fn, format='png')
    path = wedge.get_path()
    patch = PathPatch(path, facecolor='none')
    ax.add_patch(patch)
    imagebox = OffsetImage(im, zoom=zoom, clip_path=patch, zorder=-10)
    ab = AnnotationBbox(imagebox, xy, xycoords='data', pad=0, frameon=False)
    ax.add_artist(ab)

def update_file_to_commit():
    with open(PATH_TO_TIMETRAKED_JSON_FILE, 'r') as f: timeTrakedL = json.load(f)

    time_in_each_lang = {}
    dict_lang_names = []
    all_used_languages = []
    time_in_each_lang_KEYS = []
    time_in_each_lang_VALUES = []

    # Get all languages from across all projects
    dict_lang_names = [list(i['languageTime'].keys()) for i in timeTrakedL['dates']]

    # Add all the language names into one list
    all_used_languages = [item for lst in dict_lang_names for item in lst]

    # Remove duplicate languages
    all_used_languages = list(set(all_used_languages))

    # Get better language names from language names class
    language_class_names_old, language_class_names_new = zip(*Language_Names().Names.items())

    # Make a dictionary with all the language names in place
    time_in_each_lang = {langauge:[] for langauge in all_used_languages}

    # Add all times in each language into respective language name creating a list of all the times.
    for i, d1 in enumerate(timeTrakedL['dates']):
        for name in d1['languageTime']: time_in_each_lang[name].append(d1['languageTime'].get(name))

    # addying the sum of each list to get one number and not a list of numbers.
    for i in time_in_each_lang: time_in_each_lang[i] = (sum(time_in_each_lang[i]))

    # Sort the dictionary
    time_in_each_lang = dict(sorted(time_in_each_lang.items(), key=lambda item: item[1]))
    # Reverse dictionary
    time_in_each_lang = dict(reversed(time_in_each_lang.items()))

    # Split up keys and values from the dictionary into two lists.
    for key, value in time_in_each_lang.items():
        try: key = [language_class_names_new[index] for index, name in enumerate(language_class_names_old) if key == name][0] # prettify name using language names class
        except IndexError: pass
        time_formating = (
            time.strftime("%Hh %Mm %Ss",  time.gmtime(value)) if value > 3600 else
            time.strftime("%Mm %Ss",  time.gmtime(value)) if value > 60 else
            time.strftime("%Ss",  time.gmtime(value))
            )
        time_in_each_lang_KEYS.append(key + f' - {time_formating}')
        time_in_each_lang_VALUES.append(value)

    def combine_column_names(column_name,
                             cur_value,
                             sums):
        try: column_name = [language_class_names_new[index] for index, name in enumerate(language_class_names_old) if column_name == name][0] # prettify name with langauge class names
        except IndexError: pass
        percentage = round(cur_value/sums*100,2)
        return "{} {}%".format(column_name,percentage)

    # Create a graph with matplotlib with all the data we have in the time_in_each_lang dictionary.
    data = time_in_each_lang
    base_d = sum(list(data.values()))
    final_data = {combine_column_names(k,m,base_d):m/base_d*100 for k,m in data.items()}

    c_list = [np.random.choice(list(mcolors.CSS4_COLORS.values())) for i in range(len(time_in_each_lang_KEYS))]
    _, ax = plt.subplots(figsize=(6, 5),
                         subplot_kw=dict(aspect="equal"))
    lang_names = list(final_data.keys())
    data = list(final_data.values())
    beat = np.array(time_in_each_lang_VALUES)
    wedges, _ = ax.pie(data,
                       shadow=True,
                       explode=(beat == max(beat)) * 0.1,
                       wedgeprops=dict(
                           width=0.7,
                           linewidth=1.5,
                           antialiased=True,
                           edgecolor='k',
                           linestyle='solid'), #dashed
                       startangle=-20,
                       colors=c_list
                       )
    # wedges[0].set_hatch('/')

    kw = dict(arrowprops=dict(arrowstyle="-"),
              zorder=0,
              va="center")

    plt.gca().legend(time_in_each_lang_KEYS,
                     loc='center right',
                     bbox_to_anchor=(1,0.5,0.5,0.5))
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

    # Get better language names from language names class
    logo_name, logo_path = zip(*Logos_Names().Paths.items())
    for index, wedge in enumerate(wedges):
        for i, name in enumerate(logo_name):
            if time_in_each_lang_KEYS[index].__contains__(name):
                img_to_pie(logo_path[i], wedge, xy=(-0.3,0.3), zoom=0.5,ax=ax)
                wedge.set_zorder(3)

    plt.xticks([])
    plt.yticks([])
    plt.savefig('C:\\Users\\grossj\\Desktop\\Code\\VSCode-Coding-Activity-on-Github-Profile\\stats.png',
                bbox_inches='tight',
                dpi=100,
                transparent=True)
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
