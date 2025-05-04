# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from qtile_extras.widget.decorations import BorderDecoration
from libqtile import bar, layout, qtile, widget, popup, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras.popup import (
    PopupRelativeLayout,
    PopupImage,
    PopupText
)

from libqtile.popup import Popup
import subprocess, os

from modules import BombTimer, NvidiaGpuWidget, wifi
bomb_timer = BombTimer.BombTimer()

#clipboard_history = ["Hello", "Hi"]
#
#def get_clipboard_text():
#    try:
#        return subprocess.check_output(["xclip", "-sel", "c", "-o"], text=True).strip()
#    except subprocess.CalledProcessError:
#        return ""
#
#def update_clipboard_history():
#    text = get_clipboard_text()
#    os.system(f"notify-send \"{text}\"")
#    if text and text not in clipboard_history:
#        clipboard_history.append(str(text))
#        if len(clipboard_history) > 10:  # Ограничиваем историю 10 элементами
#            clipboard_history.pop(0)
#
#@hook.subscribe.selection_change
#def clipboard_update(*args, **kwargs):
#    update_clipboard_history()
#
#def show_clipboard_history(qtile):
#    # Получаем текущую позицию курсора
#    try:
#        result = subprocess.check_output(["xdotool", "getmouselocation"], text=True)
#        x = int(result.split()[0].split(":")[1])
#        y = int(result.split()[1].split(":")[1])
#    except:
#        x, y = 100, 100  # Значения по умолчанию, если xdotool не установлен
#
#    # Создаем всплывающее окно
#    popup = Popup(
#        qtile,
#        x=x,
#        y=y,
#        width=400,
#        height=300,
#        background="#282828",
#        opacity=0.9,
#        font="sans",
#        font_size=12,
#        font_color="#ffffff",
#    )
#
#    # Форматируем текст для отображения
#    text = "\n".join([f"{i+1}. {item[:50]}{'...' if len(item) > 50 else ''}"
#                     for i, item in enumerate(reversed(clipboard_history))])
#
#    popup.text = text or "Clipboard history is empty"
#    os.system(f"notify-send \"{text}\"")
#    popup.place()
#    popup.unhide()
#    popup.draw()
#
#    # Закрываем окно через 5 секунд
#    def close_popup():
#        popup.hide()
#        popup.kill()
#
#    qtile.call_later(5, close_popup)

@hook.subscribe.startup_once
def autostart_once():
    os.system(os.path.join(os.getenv("HOME"), ".config", "qtile", "autostart.sh&"))

@hook.subscribe.startup
def autostart():
    import random
    os.system("redshift -m randr -P -O 4200 &")

    wallpaper_path = os.path.join(os.getenv("HOME"), "Pictures", "wallpaper")
    wallpapers = [os.path.join(wallpaper_path, wallpaper) for wallpaper in os.listdir(wallpaper_path)]
    for screen in qtile.screens:
        screen.cmd_set_wallpaper(random.choice(wallpapers), "fill")

mod = "mod4"
alt_mod = "mod1"

keys = [
    # https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Windows control
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "control"], "space", lazy.layout.next(), desc="Move window focus to other window"),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod], "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),

    # qtile control
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "control", "shift"], "l", lazy.spawn("xscreensaver-command -lock")),

    # brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),

    # Media
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Run apps
    Key([mod], "space", lazy.spawn("rofi -show window -theme Arc-Dark.rasi"), desc="rofi select window"),
    Key([mod, "shift"], "r", lazy.spawn("rofi -show run -theme Arc-Dark.rasi"), desc="rofi run command"),
    Key([mod], "a", lazy.spawn("rofi -show drun -theme Arc-Dark.rasi"), desc="rofi run app"),

    # Programs
    Key([mod], "x", lazy.function(lambda qtile: bomb_timer.cmd_start(40)), desc="Start CS2 bomb timer"),
    Key([], "XF86Calculator", lazy.spawn("gnome-calculator"), desc="gnome calculator"),
    Key([mod], "Return", lazy.spawn("gnome-terminal"), desc="Launch terminal"),
    Key([mod, "shift"], "w", lazy.spawn("kitty -e nmtui"), desc="spawn nmtui"),
    Key([mod, "shift"], "f", lazy.spawn("firefox"), desc="spawn firefox"),

    Key([mod], "e", lazy.spawn("nemo"), desc="open nemo"),
    Key([mod, "shift"], "e", lazy.spawn("pcmanfm-qt"), desc="open pcmanfm-qt"),

    Key([mod], "s", lazy.spawn("flameshot gui")),
]

#for vt in range(1, 8):
#    keys.append(
#        Key(
#            ["control", alt_mod],
#            f"f{vt}",
#            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
#            desc=f"Switch to VT{vt}",
#        )
#    )

groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
        ]
    )

layouts = [
    layout.Columns(
        border_focus="#4bad34",
        border_normal="#4d4d4d",
        border_width=4,

        margin=5,
        margin_on_single=7,

        border_focus_stack=["#ff0000", "#880000"],

        border_on_single=True,         # показывать рамку если окно одно
        split=True,                    # разделитель между колонками
        fair=False,                    # равномерное распределение
    ),

    layout.Max(),

    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(width=27),
                widget.GroupBox(
                    highlight_method='block',
                    this_current_screen_border='#4bad34',
                    this_screen_border='#ffffff',
                    other_current_screen_border='#00ff00',
                    other_screen_border='#0000ff',
                ),
                widget.WindowName(width=150),

                widget.Spacer(),
                widget.Systray(),
                widget.Prompt(),
                widget.Spacer(),

                widget.GenPollText(
                    func=lambda: bomb_timer.get(),
                    update_interval=0.05,
                    foreground="#ff6c6c",
                ),

                widget.Net(
                    interface="all",
                    format="{down:6.1f}{down_suffix:<2}↓↑{up:6.1f}{up_suffix:<2}",
                    foreground="#d8a406",
                    padding=5
                ),
                widget.Wttr(
                    format="%c %t",
                    hide_crash = True,
                    lang = "ru",
                    location = {"Moscow": "Москва"},
                ),
                widget.Volume(
                    unmute_format='🔈{volume}%',
                    mute_format='🔇',
                    foreground='#55aaff',
                    padding=5,
                    step=5,
                    mouse_callbacks={
                        'Button1': lazy.spawn('pavucontrol'),
                        'Button3': lazy.spawn('amixer -q set Master toggle'),
                    }
                ),
                widget.Backlight(
                    backlight_name='intel_backlight',
                    change_command='brightnessctl set {0}%',
                    foreground='#ffcc00',
                    padding=5,
                    brightness_file='brightness',
                    max_brightness_file='max_brightness',
                    format='☀ {percent:2.0%}'
                ),
                NvidiaGpuWidget.NvidiaGpuWidget(
                    update_interval=2,
                    foreground="#ffcc00",
                ),
                widget.CPU(
                    format='{load_percent}%\n<small><small>CPU</small></small>',
                    foreground='#ff5555',
                    padding=5,
                    update_interval=3,
                ),
                widget.CPUGraph(
                    #type='line',
                    graph_color='#ff5555',
                    fill_color='#ff555555',
                    border_color='#000000',
                    frequency=1,
                ),
                widget.Memory(
                    format='{MemPercent: .0f}%\n<small><small>RAM({MemTotal: .1f}G)</small></small>',
                    foreground='#50fa7b',
                    padding=5,
                    update_interval=3,
                    threshold=90,
                    measure_mem='G',
                    warn_color='ff0000',
                ),
                widget.GenPollText(
                    func=lambda: wifi.get_wifi_status(),
                    update_interval=10,
                    foreground="#ffb86c",
                    mouse_callbacks={
                        'Button1': lambda: wifi.show_wifi_con(qtile),
                    },
                ),
                widget.Battery(
                    format='{char}{percent:2.0%}<small>({watt})</small>\n<small>{hour:d}:{min:02d}</small>',
                    foreground='#55ff55',
                    padding=5,
                    charge_char='⚡',
                    discharge_char=' ',
                    empty_char='❌',
                    full_char='🔋',
                    low_percentage=0.2,
                    low_foreground='#ff5555',
                    unknown_char='?',
                    notify_below=15,
                    update_interval=10,
                ),
                widget.Clock(format="%d.%m.%y %a %H:%M"),
            ],
            size=32,
            background="#282a36",
            margin=[10, 10, 5, 10],  # отступы [верх, право, низ, лево]
            border_width=[0, 0, 0, 0],
            border_color=["#282a36"],
        ),
        # x11_drag_polling_rate = 60,
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(title="Calculator"),  # GNOME Calculator
        Match(wm_class="pinentry-gtk-2"),  # ssh key passw
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
