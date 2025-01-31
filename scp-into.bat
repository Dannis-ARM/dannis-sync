set target=ec2-user@ec2-3-36-90-57.ap-northeast-2.compute.amazonaws.com
scp -i "C:\Users\18905\.ssh\skylab-ssh-seoul_hz.pem" %userprofile%/.gitconfig %target%:/home/ec2-user