#!/bin/bash -ex

sudo mkdir -p /workspace
sudo chown ubuntu:ubuntu /workspace
sudo mount /dev/xvdf /workspace

cat >>~/.bashrc <<'EOF'
export PATH="/workspace/conda/bin:$PATH"
source activate ds
export PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
export PS1='\[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@$PUBLIC_IP\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\n\$ '
EOF

mkdir -p ~/.jupyter
cat >~/.jupyter/jupyter_notebook_config.py <<'EOF'
c.NotebookApp.port = 8888
EOF
