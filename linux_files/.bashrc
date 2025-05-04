# shellcheck shell=bash
case $- in
    *i*) ;;
      *) return;;
esac

shopt -s histappend
HISTSIZE=900000
HISTFILESIZE=900000
HISTIGNORE="shutdown*:cd *:cd:ls:cl:clear:exit:ps:history*:.."
HISTCONTROL=ignoreboth:erasedups

if [[ -n "$PROMPT_COMMAND" ]]; then
    PROMPT_COMMAND="$PROMPT_COMMAND;"
fi
PROMPT_COMMAND="$PROMPT_COMMAND history -a"

shopt -s checkwinsize

shopt -s globstar # **
#shopt -s extglob  # (*.txt|*.pdf)
shopt -s cdspell  # Автоисправление опечаток в cd
shopt -s autocd   # ~/projects
shopt -s dirspell # Автодополнение директорий с исправлением опечаток
#shopt -s cmdhist  # Сохраняет многострочные команды как одну запись в истории

[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

on_enter_window_width() {
    relative_path="${PWD/#$HOME/\~}"
  
    if [ "$color_prompt" = yes ]; then
        if [ $(($(tput cols) - $(echo -n "$relative_path" | wc -c) - $(echo -n "$HOME" | wc -c))) -le 90 ]; then
            PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\W\[\033[00m\]\$ '
            PS2=" \033[0;34m>\033[0m "
        else
            PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
            PS2="\033[0;32mСомневаюсь, но вот\033[0m \033[0;34m>\033[0m "
        fi
    else
        if [ $(($(tput cols) - $(echo -n "$relative_path" | wc -c) - $(echo -n "$HOME" | wc -c))) -le 90 ]; then
          PS1='${debian_chroot:+($debian_chroot)}\u@\h:\W\$ '
        else
          PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
        fi
        PS2=" > "
    fi
}
on_enter_window_width

if [[ -n "$PROMPT_COMMAND" ]]; then
    PROMPT_COMMAND="$PROMPT_COMMAND;"
fi
PROMPT_COMMAND="$PROMPT_COMMAND on_enter_window_width"

#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

if [ -f "$HOME/.bash_aliases" ]; then
    ". $HOME/.bash_aliases"
fi

if ! shopt -oq posix; then
  if [ -f "/usr/share/bash-completion/bash_completion" ]; then
    ". /usr/share/bash-completion/bash_completion"
  elif [ -f /etc/bash_completion ]; then
    ". /etc/bash_completion"
  fi
fi

#echo -e "\033[1;32mЗдравструйте, $USER!\n\033[0;32m"
#funnyPhrases "Morkovka21Vek"
#echo -e "\033[0m"


if [[ "$TERM" == "linux" ]]; then
  echo -e -n "\033[?6c";
fi

#echo -e '\033[?17;7;113c'
