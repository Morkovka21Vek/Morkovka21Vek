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
from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook
import os

mod = "mod4"
terminal = "gnome-terminal"

@hook.subscribe.startup
def autostart():
    os.system("xinput set-prop 12 'libinput Accel Speed' -0.7")
    os.system("redshift -m randr -P -O 4000 &")
    #os.system("flameshot")

    wallpaper_path = "/home/morkovka21vek/Pictures/dog_programming.png"
    for screen in qtile.screens:
        screen.cmd_set_wallpaper(wallpaper_path, "fill")

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod, "control"], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Яркость +
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    # Яркость -
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),

    #Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout"),

    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    Key(["mod1"], "space", lazy.spawn("rofi -show window -theme Arc-Dark.rasi"), desc="Spawn rofi window"),
    Key(["mod1", "shift"], "space", lazy.spawn("rofi -show run -theme Arc-Dark.rasi"), desc="Spawn rofi run"),

    #Key([], "Print", lazy.spawn("flameshot full -p ~/Pictures/Screenshots")),
    #Key([], "XF86Display", lazy.spawn("flameshot gui")),

    Key([mod], "e", lazy.spawn("pcmanfm-qt"), desc="open pcmanfm-qt"),

    Key([mod], "a", lazy.spawn("rofi -show drun -theme Arc-Dark.rasi"), desc="spawn rofi app"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    #layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
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
        bottom=bar.Bar(
            [
                widget.TextBox("default config", name="default", foreground="#e3aa0e"),
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
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
                widget.Volume(
                    fmt='🔈 {}',
                    foreground='#55aaff',
                    padding=5,
                    volume_app='pavucontrol',  # GUI-микшер
                    step=5,
                    mouse_callbacks={
                        'Button1': lazy.spawn('pavucontrol'),
                        'Button3': lazy.spawn('amixer -q set Master toggle'),
                    }
                ),
                widget.Battery(
                    format='{char} {percent:2.0%} {hour:d}:{min:02d}',
                    foreground='#55ff55',
                    padding=5,
                    charge_char='⚡',
                    discharge_char='🔋',
                    empty_char='⚠',
                    full_char='🈵',
                    low_percentage=0.2,
                    low_foreground='#ff5555',
                    notify_below=15,
                    update_interval=10
                ),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                #widget.KeyboardLayout(
                #    configured_keyboards=['us', 'ru'],
                #    display_map={'us': 'EN', 'ru': 'RU'},
                #    foreground='#ffffff',
                #    padding=5
                #),
                widget.Systray(),
                widget.CPU(
                    format='CPU {load_percent}%',
                    foreground='#ff5555',
                    padding=5,
                    update_interval=3
                ),
                widget.CPUGraph(
                    type='line',
                    graph_color='#ff5555',
                    fill_color='#ff555555',
                    border_color='#000000',
                    frequency=1
                ),
                widget.Memory(
                    format='RAM {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}',
                    foreground='#50fa7b',
                    padding=5,
                    update_interval=3
                ),
                widget.GenPollText(
                    func=lambda: get_wifi_status(),
                    update_interval=10,
                    foreground="#ffb86c",
                    mouse_callbacks={
                        'Button1': lambda: lazy.cmd_spawn("alacritty -e nmtui")
                    }
                ),
                widget.Clock(format="%d.%m.%y %a %H:%M"),
                #widget.MemoryGraph(
                #    type='line',
                #    graph_color='#50fa7b',
                #    fill_color='#50fa7b55',
                #    frequency=1
                #),
                widget.QuickExit(),
            ],
            size=30,
            background="#282a36",
            margin=[10, 10, 5, 10],  # отступы [верх, право, низ, лево]
            border_width=[0, 0, 0, 0],  # границы
            border_color=["#282a36"],

            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
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
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

keyboard = widget.KeyboardLayout(
    configured_keyboards=['us', 'ru'],
    display_map={'us': 'EN', 'ru': 'RU'},
    backend='xkb'
)

keys.extend([
    Key([mod], "i", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout"),
 ])


def get_wifi_status():
    import subprocess
    try:
        wifi = subprocess.check_output("iwgetid -r", shell=True).decode().strip()
        strength = subprocess.check_output(
            "awk 'NR==3 {print $3}' /proc/net/wireless", shell=True
        ).decode().strip()
        return f"📶 {wifi} ({strength})"
    except:
        return "❌ Wi-Fi"
