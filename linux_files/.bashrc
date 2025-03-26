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
HISTSIZE=900000
HISTFILESIZE=900000

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

#tput cols 
##if [ "$color_prompt" = yes ]; then
##    #PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
##    if [ $((`tput cols` - $(echo -n "$relative_path" | wc -c) - $(echo -n "$(whoami)" | wc -c))) -le 90 ]; then
##      PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ '
##    else
##      PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
##    fi
##else
##    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
##fi
##PS2="\033[0;32mСомневаюсь, что ты хотел это, но вот\033[0m \033[0;34m>\033[0m "

unset force_color_prompt

#on_enter_window_width() {
#    relative_path="${PWD/#$HOME/\~}"
#  
#  if [ "$color_prompt" = yes ]; then
#      if [ $((`tput cols` - $(echo -n "$relative_path" | wc -c) - $(echo -n "$(whoami)" | wc -c))) -le 90 ]; then
#        PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ '
#      else
#        PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
#      fi
#  else
#      if [ $((`tput cols` - $(echo -n "$relative_path" | wc -c) - $(echo -n "$(whoami)" | wc -c))) -le 90 ]; then
#        PS1='${debian_chroot:+($debian_chroot)}\u@\h:\W\$ '
#      else
#        PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
#      fi
#  fi
#
#  if [ $((`tput cols` - $(echo -n "$relative_path" | wc -c) - $(echo -n "$(whoami)" | wc -c))) -le 90 ]; then
#    PS2=" \033[0;34m>\033[0m "
#  else
#    PS2="\033[0;32mСомневаюсь, что ты хотел это, но вот\033[0m \033[0;34m>\033[0m "
#  fi
#}

export HISTIGNORE="shutdown*:cd *:cd:ls *:ls:cl:clear:exit:ps:history*"
export HISTCONTROL=ignoreboth:erasedups
if [[ -n "$PROMPT_COMMAND" ]]; then
  PROMPT_COMMAND="$PROMPT_COMMAND; history -a"
else
  PROMPT_COMMAND="history -a"
fi
export HISTTIMEFORMAT='%d.%m.%Y %H:%M:%S: '

on_enter_window_width() {
    relative_path="${PWD/#$HOME/\~}"
  
    if [ "$color_prompt" = yes ]; then
        if [ $((`tput cols` - $(echo -n "$relative_path" | wc -c) - $(echo -n "$HOME" | wc -c))) -le 90 ]; then
          PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ '
        else
          PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
        fi

        if [ $((`tput cols` - $(echo -n "$relative_path" | wc -c) - $(echo -n "$HOME" | wc -c))) -le 90 ]; then
          PS2=" \033[0;34m>\033[0m "
        else
          PS2="\033[0;32mСомневаюсь, что ты хотел это, но вот\033[0m \033[0;34m>\033[0m "
        fi

    else
        if [ $((`tput cols` - $(echo -n "$relative_path" | wc -c) - $(echo -n "$HOME" | wc -c))) -le 90 ]; then
          PS1='${debian_chroot:+($debian_chroot)}\u@\h:\W\$ '
        else
          PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
        fi

        PS2=" > "
    fi

}

on_enter_window_width
if [[ -n "$PROMPT_COMMAND" ]]; then
  PROMPT_COMMAND="$PROMPT_COMMAND; on_enter_window_width"
else
  PROMPT_COMMAND="on_enter_window_width"
fi
#trap 'resize_window' SIGWINCH

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

#function format_time {
#    local time_ms=$1
#    local min_length=${2:-9} # 7
#    local time_sec=$(echo "scale=2; $time_ms / 1000" | bc)
#
#    #format_number() {
#    #    local num=$1
#    #    num=$(echo "$num" | sed 's/^\./0./')
#    #    if [[ -z "$num" || ! "$num" =~ ^-?[0-9]+(\.[0-9]+)?$ ]]; then
#    #       echo "Недопустимое число: $num"
#    #       return 1
#    #    fi
#    #    echo "Форматируемое число: $num"
#    #    printf "%.4g" "$num"
#    #}
#
#    if (( $(echo "$time_sec < 60" | bc -l) )); then
#        echo -e "${time_sec}\033[1;33ms\033[0m"
#        #time_sec=$(format_number "$time_sec")
#        #printf "[%s\033[1;33ms\033[0m]%*s\n" "$time_sec" $((min_length - ${#time_sec} - 3)) ""
#    elif (( $(echo "$time_sec < 3600" | bc -l) )); then
#        local minutes=$(echo "scale=2; $time_sec / 60" | bc)
#        echo -e "${minutes}\033[1;33mm\033[0m"
#    else
#        local hours=$(echo "scale=2; $time_sec / 3600" | bc)
#        echo -e "${hours}\033[1;33mh\033[0m"
#    fi
#}
#
#function timer_start {
#  if [ -z "$timer" ]; then
#    timer=${timer:-$(date +%s%3N)}
#  fi;
#}
#
#function timer_stop {
#  if [ -n "$timer" ]; then
#    local now=$(date +%s%3N)
#    local time_elapsed=$((now - timer))
#    timer_show=$(format_time $time_elapsed)
#    unset timer
#  else
#    timer_show=""
#  fi
#  #export PS1="[$timer_show]$PS1"
#}
#
#if [[ $- == *i* ]]; then
#    trap 'timer_start' DEBUG
#fi
#
#if [[ -n "$PROMPT_COMMAND" ]]; then
#  PROMPT_COMMAND="$PROMPT_COMMAND; timer_stop"
#else
#  PROMPT_COMMAND="timer_stop"
#fi



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


mkcdir() {
    mkdir -p -- "$1" &&
    cd -P -- "$1"
}

alias mkcdir="mkcdir $@"

alias cl="clear && echo -e -n \"\033[0;32m\" && funnyPhrases \"Morkovka21Vek\" && echo -e \"\033[00m\""


funnyPhrases() {
  hoursTime=$(date +%H)
  dayOfWeek=$(date +%u)

  if [ $hoursTime -le 4 ]; then
    echo -n "Чего не спим, $1?"
  elif [ $hoursTime -le 6 ]; then
    echo -n "Ты вообще спишь, $1?" 
  elif [ $hoursTime -le 7 ]; then
    echo -n "Проснись и пой, $1?" 
  elif [ $hoursTime -le 9 ]; then
    echo -n "Как завтрак, $1?" 
  elif [ $hoursTime -le 11 -a $dayOfWeek -eq 7 ]; then
    echo -n "На занятиях, $1?" 
  elif [ $hoursTime -le 11 ]; then
    echo -n "Чё делаешь, $1?" 
  elif [ $hoursTime -le 13 ]; then
    echo -n "Hello World ($1)!" 
  elif [ $hoursTime -le 15 ]; then
    echo -n "Пообедал, $1?" 
  elif [ $hoursTime -le 18 ]; then
    echo -n "Как жизнь, $1?" 
  elif [ $hoursTime -le 20 ]; then
    echo -n "А вот и ужин!" 
  elif [ $hoursTime -le 22 ]; then
    echo -n "Закругляйся уже, $1!" 
  elif [ $hoursTime -le 23 ]; then
    echo -n "Это последнее предупреждение, $1!" 
  fi
}

#echo -e '\e]8;;http://example.com\e\\This is a link\e]8;;\e\\'
#echo -e "\033[1;32mЗдравструйте, $USER!\nСегодня $(date)\n\033[0;32m"
echo -e "\033[1;32mЗдравструйте, $USER!\n\033[0;32m"
funnyPhrases "Morkovka21Vek"
echo -e "\033[00m"

alias buffer_help="echo \"xclip -sel c < <filename>\""
alias tar_unzip_help="echo \"tar -xvzf <filename> [-C <dir name>]\""

alias caesiumclt="/home/morkovka21vek/Documents/programs/caesiumclt"

if [[ "$TERM" == "linux" ]]; then
  echo -e -n "\033[?6c";
fi

#echo -e '\033[?17;7;113c'
unset timer
