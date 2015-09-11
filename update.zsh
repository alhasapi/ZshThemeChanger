#!/bin/zsh
function up_to_date() {
    sudo cp $1 /bin/change_zsh_theme 
}

up_to_date change_zsh_theme.py
