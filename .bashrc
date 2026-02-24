# function shortcuts
alias ls='ls -A --color'
alias cp='cp -r'
alias chext='changeextension'
alias ut='unzipTrajectory'
alias reload='. ~/.bashrc'
alias npp="Notepad++"

# load local path shortcuts
. ~/.localpaths

# set shell prompt
PS1='\[\033]0;$TITLEPREFIX:$PWD\007\]\n\[\033[32m\]\u@\h \[\033[33m\]\w\[\033[36m\]`__git_ps1`\[\033[0m\]\n$ '

# git shortcuts
alias git-clean-remote='git fetch --prune origin'
alias git-clean-local='git branch -d $(git branch --merged=main | grep -v main); git fetch --prune'
alias git-clean-all='git-clean-remote; git-clean-local; echo -e "\nAll Remaining Branches:\n"; git branch -a'
alias git-last-change='git diff HEAD~1..HEAD' 
# git diff A..B compares current A to current B
# git diff A...B compares common ancestor of A to current B
alias gs='git status'

# load key bindings
bind '"\C-[[A": history-search-backward' # Ctrl+UpArrow
bind '"\C-[[B": history-search-forward' # Ctrl+DownArrow
bind '"\C-h": backward-kill-word' # Ctrl+Backspace
bind '"\e[3;5~": kill-word' # Ctrl+Del

function lf {
		# local find
		# input search directory then name
		find "$1" -maxdepth 1 -iname "*$2*"
}

function open-chrome {
		# input file path
		start chrome "$(realpath "$1")"
}
