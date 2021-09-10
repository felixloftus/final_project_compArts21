cd /home/pi/marksMade/imageSaves/
mkdir $(date +%d_%H%S)
cd
cd /home/pi/marksMade/
cp -R contoured /home/pi/marksMade/imageSaves/$(date +%d_%H%S)/
cp -R frameDiff /home/pi/marksMade/imageSaves/$(date +%d_%H%S)/
