if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    alias diff='diff --color=auto'
    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

alias apt='sudo apt-fast'
alias ..='cd ..'
alias update_upgrade='sudo apt-fast update && sudo apt-fast upgrade'
alias h='history'
alias hgrep='history | grep'
alias higrep='history | grep -i'
alias ff='find / -type f -name'
alias fd='find / -type d -name'

# Подтверждение при перезаписи файлов
alias mv='mv -i'
alias cp='cp -i'
alias ln='ln -i'

alias fastping='ping -c 100 -s 1 -i 0.01'
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'


mkcdir() {
    mkdir -p -- "$1" &&
    cd -P -- "$1"
}
alias mkcdir="mkcdir $@"


alias cl="clear && echo -e -n \"\033[0;32m\" && funnyPhrases \"$USER\" && echo -e \"\033[00m\""
alias c="cl"

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

alias buffer_help="echo \"xclip -sel c < <filename>\""
alias tar_unzip_help="echo \"tar -xvzf <filename> [-C <dir name>]\""
alias linters_help="echo \"shellcheck pylint clang-format\""
