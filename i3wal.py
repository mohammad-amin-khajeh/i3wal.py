#!/usr/bin/env python
"""a script that dynamically changes the wallpaper along with i3's theme(requires xwallpaper, pywal and Xresources)"""

from os import getenv, listdir
from subprocess import check_output, run
from sys import argv
from glob import glob


home = getenv("HOME")
i3_config = f"{home}/.config/i3/config"
wallpath = f"{home}/Pictures/wallpapers"
xresources = f"{home}/.cache/wal/colors.Xresources"
launcher = "rofi -dmenu -p 'select the wallpaper: '"


def main():
    to_set = arg_checker()
    reload_theme(to_set)
    edit_config_file(to_set)
    edit_xresources_file(xresources)


# check whether a parameter is provided
def arg_checker() -> str:
    if len(argv) > 1:
        return argv[1]
    else:
        return chosen_wallpaper()


# launch rofi if no parameters were provided
def chosen_wallpaper() -> str:
    wallpaper_list = listdir(wallpath)
    choices = "\n".join(wallpaper_list)
    chosen = check_output(f"echo '{choices}' | {launcher}", shell=True)
    chosen = chosen.decode().removesuffix("\n")
    return f"{wallpath}/{chosen}"


# make wallpaper load across restarts by setting it in the i3 config file
def edit_config_file(wallpaper: str) -> None:
    with open(i3_config, "r+") as file:
        data = file.readlines()
        for line_number, line_content in enumerate(data):
            if "xwallpaper" in line_content:
                before_wallpaper = data[line_number].split('"')[0]
                wallpaper = data[line_number].split('"')[1] = wallpaper
                data[line_number] = before_wallpaper + '"' + wallpaper + '"\n'
                break
        file.seek(0)
        file.writelines(data)
        file.truncate()


# add some font display goodies to .xresources
def edit_xresources_file(file: str) -> None:
    if glob(f"{file}"):
        with open(file, "a") as xresources:
            xresources.write(
                """
Xft.antialias: 1
Xft.autohint: 0
Xft.dpi: 96
Xft.hinting: 1
Xft.hintstyle: hintslight
Xft.lcdfilter: lcddefault
Xft.rgba: none"""
            )


# set the new wallpaper and use it for pywal
def reload_theme(wallpaper: str) -> None:
    run(
        f"xwallpaper --zoom '{wallpaper}'; wal -i '{wallpaper}' 1> /dev/null",
        shell=True,
    )


if __name__ == "__main__":
    main()
