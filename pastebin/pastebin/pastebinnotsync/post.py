from urllib import urlopen, urlencode
import sys

paste_data = sys.argv[1]
paste_title = sys.argv[2]

url="http://pastebin.com/api/api_post.php"

args={

	'api_dev_key' : '6e502d38900d77c3cce85a679e5ae1f0',
	'api_option' : 'paste',
	'api_paste_code' : paste_data,
	'api_paste_name' : paste_title
}

print urlopen(url,urlencode(args)).read()
