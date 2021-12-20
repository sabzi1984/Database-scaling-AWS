sudo apt install -y default-jre
sudo wget https://github.com/powerapi-ng/powerapi-scala/releases/download/4.2.1/powerapi-cli-4.2.1.tgz

sudo tar xzf powerapi-cli-4.2.1.tgz

cd powerapi-cli-4.2.1

cat << EOF >> conf/powerapi.conf
powerapi.cpu.tdp = 35
powerapi.cpu.tdp-factor = 0.7
EOF

pid=$(pidof mysqld)

./bin/powerapi \
    modules procfs-cpu-simple \
    monitor \
      --frequency 500 \
      --pids $pid \
      --file /tmp/data.txt \
      duration 900 # 15 min

# run application
python3 /home/LOG8415_Proj/proxy_pattern.py "direct" &

# launch powerapi
pid=$(ps aux | grep "python3.*[proxy_pattern|gatekeeper_pattern]\.py" | awk 'NR==1{ print $2 }')

sudo /powerapi-cli-4.2.1/bin/powerapi modules procfs-cpu-simple monitor --frequency 1000 --pids $pid --file /tmp/powerapi_proxy.txt \



# run application
python3 /home/LOG8415_Proj/gatekeeper_pattern.py &

# launch powerapi
pid=$(ps aux | grep "python3.*[proxy_pattern|gatekeeper_pattern]\.py" | awk 'NR==1{ print $2 }')

sudo /powerapi-cli-4.2.1/bin/powerapi modules procfs-cpu-simple monitor --frequency 1000 --pids $pid --file /tmp/gatekeeper_insert_direct.txt \

scp -i C:\Users\rabin\Downloads\Ali.pem ubuntu@ec2-54-237-135-3.compute-1.amazonaws.com:/tmp/powerapi_proxy.txt C:\Users\rabin\