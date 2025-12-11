git add .
git commit -m "%date% %time%"
git push bthome master
cd api/lib/ToolKits
git add .
git commit -m "%date% %time%"
git push origin master
cd ../sql
git add .
git commit -m "%date% %time%"
git push origin master:sql
cd ../../..
pause