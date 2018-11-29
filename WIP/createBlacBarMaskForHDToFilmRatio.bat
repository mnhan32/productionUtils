C:\Users\mnhan\ffmpeg-4.1-win64-static/bin/ffmpeg.exe -f lavfi -i "color=s=1436x1080:color=black@0.0,format=rgba" -vf "pad=w=1920:h=1080:x=(ow-iw)/2:y=0:color=black@1.0,format=rgba" -ss 1 -frames 1 -c:v png -r 1 mask_HDto133.png
REM C:\Users\mnhan\ffmpeg-4.1-win64-static/bin/ffmpeg.exe -f lavfi -i "color=s=1920x803:color=black@0.0,format=rgba" -vf "pad=w=1920:h=1080:x=0:y=(oh-ih)/2:color=black@1.0,format=rgba" -ss 1 -frames 1 -c:v png -r 1 mask_HDto239.png

