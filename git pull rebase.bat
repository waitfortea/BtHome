git add .
git commit -m "%date% %time%"
git pull origin master --rebase
cd api/lib/ToolKits
git add .
git commit -m "%date% %time%"
git pull origin master --rebase
cd ../sql
git add .
git commit -m "%date% %time%"
git pull origin master:sql  --rebase
cd ../../..
pause