# github - https://github.com/k3s-io/k3s?tab=readme-ov-file
# fetch k3s

rm -fr ~/workplace/k3s-learn && mkdir -p ~/workplace/k3s-learn
cp /mnt/e/Cloud/CloudDownloads/k3s ~/workplace/k3s-learn

export PATH=$PATH:~/workplace/k3s-learn

sudo k3s server &
# Kubeconfig is written to /etc/rancher/k3s/k3s.yaml
sudo k3s kubectl get nodes

sudo cat /var/lib/rancher/k3s/server/node-token
# On a different node run the below. NODE_TOKEN comes from
# /var/lib/rancher/k3s/server/node-token on your server (master - control plane)
# sudo k3s agent --server https://myserver:6443 --token ${REG_TOKEN}