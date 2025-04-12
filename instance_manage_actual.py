import boto3
ec2 = boto3.client('ec2',region_name='ap-south-1')

userDataScript = '''#!/bin/bash -x
exec > /home/ubuntu/setup.log 2>&1
echo "=== User Data Script Started ==="
attempt=0
while ! ping -c 1 8.8.8.8 &> /dev/null; do
    echo "Waiting for network..."
    sleep 5
    attempt=$((attempt+1))
    if [ $attempt -ge 10 ]; then
        echo "Network not available after 50 seconds, exiting."
        exit 1
    fi
done
echo "Network is up, proceeding with installation"
sudo apt update && sudo apt upgrade -y 
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - 
sudo apt install -y nodejs 
node -v 
npm -v 
sudo apt install git -y 
cd /home/ubuntu 
sleep 10
sudo -u ubuntu git clone "https://github.com/UnpredictablePrashant/TravelMemory.git" /home/ubuntu/TravelMemory
if [ $? -eq 0 ]; then
    echo  "Clone completed" >> /home/ubuntu/logs.txt
    cd TravelMemory/backend
    echo "MONGO_URI='mongodb+srv://avinjaymewada25:1wKVfxoZizex5R2s@cluster0.k6qhq.mongodb.net/travelmemory'" > .env
    echo "PORT=3001" >> .env
    npm install
    cd ../frontend
    pub_ip=`curl http://checkip.amazonaws.com`
    echo "REACT_APP_BACKEND_URL=http://"$pub_ip":3001" > .env
    npm install
    cd ../backend
    nohup node index.js > nodejs.log 2>&1 &
    cd ../frontend
    nohup npm start > react.log 2>&1 &
else
    echo "Clone failed" >> /home/ubuntu/logs.txt
fi
'''

instance = ec2.run_instances(
    ImageId='ami-0d01904ee0d806ca5',
    InstanceType='t3.micro',
    MaxCount=2,
    MinCount=1,
    KeyName='avinjay',
    SecurityGroupIds=['sg-018bb12a634e0b365'],
    UserData=userDataScript,
    SubnetId='subnet-0c1842aca7dc1b6b0',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'Avinjay_auto_Mern_project_instances_1'
                },
            ]
        },
    ],
)

print("Launching instance: ", instance)