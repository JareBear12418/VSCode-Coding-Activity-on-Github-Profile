class Language_Names:
    '''
    Replace the un-formatted name that is generated by Local Time Tracker with something more pretty and accurate.
    **DONT** use emojies, matplotlib doesn't like them. There are workaround's, but there 'hacky' and require you to change defualt font path.

    'python':'snek lang'
    will replace every occurence of 'python' to 'snek lang'.
    '''
    def __init__(self):
        self.Names: dict = {
            'python': 'Python',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'csharp': 'C#',
            'c': 'C',
            'cpp': 'C++',
            'java': 'Java',
            'markdown': '.md',
            'txt':'.txt',
            'Log':'.Log',
            'json':'.json',
            'jsonc':'.jsonc',
            'yaml':'.yaml',
            'gitignore':'.gitignore'
        }