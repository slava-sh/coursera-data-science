#!/bin/bash -ex

sudo mkdir -p /workspace
sudo chown ubuntu:ubuntu /workspace
sudo mount /dev/xvdf /workspace

cat >>~/.bashrc <<'EOF'
export PATH="/workspace/conda/bin:$PATH"
source activate ds
export PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
export PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@$PUBLIC_IP\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n\$ '
alias l='ls -lah'
EOF

cat >>~/.ssh/config <<'EOF'
Host github.com
  IdentityFile /workspace/github/id_rsa
EOF

cat >>~/.gitconfig <<'EOF'
[user]
    name = Slava Shklyaev
    email = slava@slava.sh
[core]
    editor = vim
EOF

sudo apt --yes install htop
