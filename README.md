# VSCode-Coding-Activity-on-Github-Profile

Have an activity graph on your GitHub profile showcasing your activity in visual studio code. 


# Setup

- Setting this up is a bit tricky. So please follow the instructions clearly. 
1. *IMPORTANT*!!!! Install the [Local Time Tracker](https://marketplace.visualstudio.com/items?itemName=FabricioRojas.localtimetracker) created by [Fabricio Rojas](https://github.com/FabricioRojas). 
2. Clone your profile repository.
    - E.x: `git clone https://github.com/JareBear12418/JareBear12418/`
    - Your username twice basicly.
3. *Copy* **ALL** python scripts from this repository into your cloned repository on your system, along side with the __logos folder__.
4.  Create a `.gitignore` file in your repository. 
    - Add `*.py`, `.gitignore` and `/logos` to the `.gitignore` file.

So far your directory should look like the following:

![image](https://user-images.githubusercontent.com/25397800/110671702-73085180-8194-11eb-81ae-6bde03897263.png)

- That is everything setup for script, Now all we need to do is run the script daily. This repository is basicly just a clone of [Daily Git Commit](https://github.com/JareBear12418/Daily-Git-Commit) in terms of doing the same thing, commiting to a repository. So alot of tips and instructions are listed there if you encounter any errors with `gitpython` I will not repeat them here. The script should handle everyhing else, all thats left to do call it daily.

make sure you correct your path to the shell script.

my crontab looks like so:
```sh
0 0 * * * /home/jared/Documents/Python-Projects/VSCode-Coding-Activity-on-Github-Profile/run.sh
```

Again, make sure path's are set to your paths, the above command only works for my system. Change the paths to your need. I am using full paths just to play it safe, you might not need to use full paths.

It's a good idea to store your git credentials so you don't always have to log in (LINUX ONLY)
```bash
git config --global credential.helper store
```

Now we need to edit our [README.md](https://github.com/JareBear12418/JareBear12418/blob/main/README.md) file to show our coding activity. My profile page as a decent showcase of this.

```markdown
<h3 align="center"> &#x1f4c8; Coding Activity </h3>
<p align="center">
<img width="65%" align="center" src="https://github.com/GITHUB_USERNAME/GITHUB_USERNAME/blob/main/stats.png" alt="Activity" />
<h4 align="center"> 2021/02/28 4:11 PM - TODAY </h4>
</p>
```

yields:

<h3 align="center"> &#x1f4c8; Coding Activity </h3>
<p align="center">
<img width="65%" align="center" src="https://github.com/jarebear12418/jarebear12418/blob/main/stats.png" alt="Activity" />
<h4 align="center"> 2021/02/28 4:11 PM - TODAY </h4>
</p>

Whenever you update the `stats.png` via the script, your github profile automaticly updates the preview, so your all done setting up. It's a bit of a crude setup. You're better off just using wakatime but even that its still tricky to get it set up properly. I prefer this solution because wakatime is to complicated to setup. This way I can make my own solution.
