import boto3
ec2 = boto3.client('ec2',region_name='<region name>')

userDataScript = '''#!/bin/bash -x
exec > /<home folder>/setup.log 2>&1
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
cd /<home folder> 
sleep 10
sudo -u ubuntu git clone "https://github.com/UnpredictablePrashant/TravelMemory.git" /<home Folder>/TravelMemory
if [ $? -eq 0 ]; then
    echo  "Clone completed" >> /<home Folder>/logs.txt
    cd TravelMemory/backend
    echo "MONGO_URI='mongodb+srv://mongo_username:mongo_password@cluster0.k6qhq.mongodb.net/travelmemory'" > .env
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
    echo "Clone failed" >> /<home Folder>/logs.txt
fi
'''

instance = ec2.run_instances(
    ImageId='ami-0d01904ee0d806ca5',
    InstanceType='t3.micro',
    MaxCount=2, #will create 2 ubuntu instances
    MinCount=2,
    KeyName='<private keyname>',
    SecurityGroupIds=['sg-<security group id>'],
    UserData=userDataScript,
    SubnetId='subnet-<subnet id>',
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': '<key name>',
                    'Value': '<key value>'
                },
            ]
        },
    ],
)

print("Launching instance: ", instance)