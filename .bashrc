alias ls='ls -A --color'
alias cp='cp -r'
alias chext='changeextension'
alias repos='cd ~/Repositories'
alias e3mat='cd ~/Repositories/e3mat'
alias stas='cd "$sta2025"'
alias ut='unzipTrajectory'
alias git-clean-remote='git fetch --prune origin'
alias git-clean-local='git branch -d $(git branch --merged=main | grep -v main); git fetch --prune'
alias git-clean-all='git-clean-remote; git-clean-local; echo -e "\nAll Remaining Branches:\n"; git branch -a'
alias git-last-change='git diff HEAD~1..HEAD'
alias reload='. ~/.bashrc'

function lf {
		# local find
		# input search directory then name
		find "$1" -maxdepth 1 -iname "*$2*"
}

function open-chrome {
		# input file path
		start chrome "$(realpath "$1")"
}
