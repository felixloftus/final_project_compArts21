echo "SLEEPING"
sleep 60
echo "AWAKE"
export DISPLAY=:0
cd /home/pi/marksMade/
echo "EXECUTING"
python3 main.py
