#!/usr/bin/env python

import os
import sys

themes_path = "/home/moktar/.oh-my-zsh/themes/"
zsh_config = "/%s/.zshrc"
temporary_config = "/tmp/.zshrc"


def user_config_path():
    user_name = os.popen("whoami").read().strip()
    return ( "/home/" if user_name != "root" else "") + zsh_config %( user_name )

def themes_list():
    items = os.popen("ls " + themes_path).read().split()
    return map(lambda q: q.split('.')[0], items)

def set_theme(theme_name):
    zsh_config = user_config_path()
    if theme_name in themes_list():
        with open(temporary_config, "w") as out:
            with open(zsh_config) as current_config:
                data = current_config.read().split('\n')
                theme_var = data[7].split('=')
                theme_var[1] = '"' + theme_name + '"'
                data[7] = '='.join(theme_var)
                data = '\n'.join(data)
            out.write(data)
        os.popen("cp %s %s" %( temporary_config, zsh_config ))
        return True
    return False

def current_theme():
    zsh_config = user_config_path()
    with open(zsh_config) as current_config:
        data = current_config.read().split('\n')
        theme = data[7].split('=')[-1]
        transformer = lambda s: s if s not in [ "\"" ] else ""
        return ''.join(map(transformer, theme))


def show_theme_list():
    themes = themes_list()
    def transformer(items):
        (size, step, out) = ( len(items), 8, [] )
        for i in range(0, size, step):
            current = items[i: i + step]
            out.append(current)
        return out
    max_size = max(map(len, themes))
    
    to_serial = transformer(themes)
    m_lambda = lambda x: ''.join(map(lambda q: " " * (max_size - len(q)) + q, x))
    serialized = map(m_lambda, to_serial)
    print '\n'.join(serialized)

def usage():
    print "%s [theme-name] [-show-theme-list | --st]" %( sys.argv[0] )

def some(lst, args=[]):
    return any(map(lambda s: s in lst, args))


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print usage()
    elif some(sys.argv, ["--st", "-show_theme_list"]):
        show_theme_list()
    elif some(sys.argv, ['--current-theme','--ct']):
        print current_theme()
    else:
        theme = sys.argv[1]
        if not set_theme(theme):
            print "Your theme name is not valid"
            exit(0)
        print "Relauch your terminal."
    
