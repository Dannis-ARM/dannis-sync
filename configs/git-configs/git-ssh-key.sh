# generate ssh key
# ed25519
ssh-keygen -t ed25519 -C "hzzhanyuyang@gmail.com" -f ~/.ssh/my_ed25519_key -N ""
# RSA
ssh-keygen -m pem -t rsa -b 4096 -C "hzzhanyuyang@gmail.com" -f ~/.ssh/skylab-ec2.pem -N ""

chmod 600 ~/.ssh/id_ed25519