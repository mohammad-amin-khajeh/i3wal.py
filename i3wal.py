#!/usr/bin/env python
"""a script that dynamically changes the wallpaper along with i3's theme(requires xwallpaper, pywal and Xresources)"""

from os import getenv, listdir
from subprocess import check_output, run
from sys import argv
from glob import glob


home = getenv("HOME")
I3_CONFIG = f"{home}/.config/i3/config"
WALLPATH = f"{home}/Pictures/wallpapers"
XRESOURCES = f"{home}/.cache/wal/colors.Xresources"
LAUNCHER = "rofi -dmenu -p 'select the wallpaper: '"
VALID_FORMATS = (".mp4", ".webm", ".mkv", ".webp", ".jpg", ".jpeg", ".png")
INITIALIZER = "xargs --arg-file=.cache/wal/wal -d $ xwallpaper"


def main():
    to_set = chosen_wallpaper()
    reload_theme(to_set)
    edit_config_file()
    edit_xresources_file(XRESOURCES)


# check whether a parameter(picture or video) is provided
def chosen_wallpaper() -> str:
    if len(argv) == 1:
        return chosen_from_rofi()
    if argv[1].endswith(VALID_FORMATS):
        return argv[1]
    else:
        print("cannot extract colors from the file you provided, exiting...")
        exit(1)


# set the new wallpaper and use it for pywal
def reload_theme(wallpaper: str) -> None:
    run(
        f"xwallpaper --zoom '{wallpaper}'; wal -i '{wallpaper}' 1> /dev/null",
        shell=True,
    )


# launch rofi if no parameters were provided
def chosen_from_rofi() -> str:
    wallpaper_list = listdir(WALLPATH)
    choices = "\n".join(wallpaper_list)
    chosen = check_output(f"echo '{choices}' | {LAUNCHER}", shell=True)
    chosen = chosen.decode().removesuffix("\n")
    return f"{WALLPATH}/{chosen}"


# make wallpaper load across restarts by setting it in the i3 config file
def edit_config_file() -> None:
    with open(I3_CONFIG, "a+") as file:
        file.seek(0)
        data = file.read()
        if INITIALIZER.lower() not in data.lower():
            file.write(f"exec --no-startup-id {INITIALIZER} --zoom\n")


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


if __name__ == "__main__":
    main()
