# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi

alias get_idf='. $HOME/esp/esp-idf/export.sh'

export PS1="\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ "
export PS2="\033[0;32mСомневаюсь, что ты хотел это, но вот\033[0m \033[0;34m>\033[0m "

#PS1="\[\e]0;\u: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$"
#export PS1="\[\e]0;\u: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$"

mkcdir ()
{
    mkdir -p -- "$1" &&
    cd -P -- "$1"
}
cl ()
{
  clear
  echo -e "\033[0;36mВывод очищен!\033[0;32m"

  funnyPhrases "Morkovka21Vek"
  echo -e -n "\033[00m"
}
gcomp ()
{
  g++ "$1.cpp" -o "$1.out"
}

funnyPhrases() {
  hoursTime=$(date +%H)
  dayOfWeek=$(date +%u)

  if [ $hoursTime -le 4 ]; then
    echo "Чего не спим, $1?"
  elif [ $hoursTime -le 6 ]; then
    echo "Ты вообще спишь, $1?" 
  elif [ $hoursTime -le 7 ]; then
    echo "Проснись и пой, $1?" 
  elif [ $hoursTime -le 9 ]; then
    echo "Как завтрак, $1?" 
  elif [ $hoursTime -le 11 -a $dayOfWeek -eq 7 ]; then
    echo "На занятиях, $1?" 
  elif [ $hoursTime -le 11 ]; then
    echo "Чё делаешь, $1?" 
  elif [ $hoursTime -le 13 ]; then
    echo "Hello World ($1)!" 
  elif [ $hoursTime -le 15 ]; then
    echo "Пообедал, $1?" 
  elif [ $hoursTime -le 18 ]; then
    echo "Как жизнь, $1?" 
  elif [ $hoursTime -le 20 ]; then
    echo "А вот и ужин!" 
  elif [ $hoursTime -le 22 ]; then
    echo "Закругляйся уже, $1!" 
  elif [ $hoursTime -le 23 ]; then
    echo "Это последнее предупреждение, $1!" 
  fi
}

#echo -e '\e]8;;http://example.com\e\\This is a link\e]8;;\e\\'
echo -e "\033[1;32mЗдравструйте, $USER!\nНапоминаю, если вы забыли:\nСегодня $(date)\nНикнейм: Morkovka21Vek\nБыстрые ссылки: \e]8;;https://morkovka21vek.github.io\e\\Сайт\e]8;;\e\\ \e]8;;https://github.com/Morkovka21Vek\e\\github\e]8;;\e\\ \n\033[0;32m"
funnyPhrases "Morkovka21Vek"
echo -e -n "\033[00m"


#becup settings
export BACKUPS_DIR="$HOME/backups_creator/Morkovka21Vek/linux_files/"
cp "$HOME/.bashrc" "$BACKUPS_DIR/.bashrc"
cp "$HOME/.vimrc" "$BACKUPS_DIR/.vimrc"
#git --git-dir=$BACKUPS_DIR/../.git --work-tree=$BACKUPS_DIR/../ status
git --git-dir=$BACKUPS_DIR/../.git --work-tree=$BACKUPS_DIR/../ diff --name-only HEAD $BACKUPS_DIR
#git diff --name-only HEAD $BACKUPS_DIR 
#end bucup settings