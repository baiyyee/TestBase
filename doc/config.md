- ~/.pip/pip.conf

```console

[global]
index-url = https://mirrors.aliyun.com/pypi/simple/
extra-index-url = https://pypi.tuna.tsinghua.edu.cn/simple/

```


- /etc/apt/sources.list

```console

deb http://mirrors.aliyun.com/debian/ stretch main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ stretch main non-free contrib
deb http://mirrors.aliyun.com/debian-security stretch/updates main
deb-src http://mirrors.aliyun.com/debian-security stretch/updates main
deb http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ stretch-updates main non-free contrib
deb http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib
deb-src http://mirrors.aliyun.com/debian/ stretch-backports main non-free contrib

```

- ~/.zshrc

```console

export ZSH=$HOME/.oh-my-zsh

# Python Virtualenv Settings
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export VIRTUALENVWRAPPER_VIRTUALENV=~/.local/bin/virtualenv
source ~/.local/bin/virtualenvwrapper.sh

# Env Settings
export TEST_ENV=dev
export TEST_ROLE=admin
export NACOS_HOST=
export NACOS_USERNAME=
export NACOS_PASSWORD=
export NACOS_TENANT=
export ROBOT_KEY=
export JIRA_USERNAME=
export JIRA_PASSWORD=
export CONFLUENCE_USERNAME=
export CONFLUENCE_PASSWORD=
export AES_KEY=

setopt no_nomatch

ZSH_THEME="robbyrussell"

ZSH_DISABLE_COMPFIX="true"

plugins=(
    git
    autojump
    zsh-autosuggestions
    zsh-syntax-highlighting
    colorize
)

source $ZSH/oh-my-zsh.sh

ZSH_COLORIZE_TOOL="pygmentize"
ZSH_COLORIZE_STYLE="colorful"

# autojump
[[ -s ~/.autojump/etc/profile.d/autojump.sh ]] && source ~/.autojump/etc/profile.d/autojump.sh

```