output=$(ls pastebin/pastebinnotsync/)

bashscript="postonpastebin.sh"
pythonscript="post.py"
file_link=pastebin/pastebinnotsync/links
storescript=links

wget --spider http://google.com
if [ "$?" != 0 ] 
then
  echo "internet is not connected"
	return
fi

for var in $output
do

	if [ $bashscript != $var ] && [ $pythonscript != $var ] && [ $storescript != $var ]
	then
		file_content=$(cat pastebin/pastebinnotsync/$var)
		paste_link=$(python pastebin/pastebinnotsync/post.py "$file_content" $var)
		
		echo $paste_link | grep http://pastebin.com

		if [ $? != 0 ]
		then
			return
		else
			echo "found"
		fi
		echo "hello world"
		echo $var >> $file_link
		echo $paste_link >> $file_link
		echo \n >> $file_link

		mv pastebin/pastebinnotsync/$var pastebin/pastebinsync 
	fi
done
