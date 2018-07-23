
import requests
import re

response = requests.get('http://musicforprogramming.net')

# I need some regex to get the list of pages with mp3s.
# div#episodes
#   a href="?one"
#   a href="?two"
#   ...
#   a href="?fiftyone"
#
# That's the structure of a list.
# MP3 filename is located in <audio id="player" src="..."> tag.
# So the task is to from one to fiftyone get pages audio src tag and
# download it as mp3.

num2words = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
             6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
             11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
             15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
             19: 'nineteen', 20: 'twenty', 30: 'thirty', 40: 'forty',
             50: 'fifty', 60: 'sixty', 70: 'seventy', 80: 'eighty',
             90: 'ninety', 0: 'zero'}


def n2w(n):
    try:
        return num2words[n]
    except KeyError:
        try:
            return num2words[n - n % 10] + num2words[n % 10]
        except KeyError:
            return None


def save_mp3(filename, url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open('data/mp3/{}.mp3'.format(filename), 'wb') as f:
            for chunk in response:
                f.write(chunk)


if __name__ == '__main__':
    for i in range(1, 52):
        try:
            number = n2w(i)
            url = 'http://musicforprogramming.net/?{}'.format(number)
            response = requests.get(url).content.decode('utf-8')
            group = re.search(r'audio src="(.+?)"', response)
            save_mp3(number, group[1])
        except Exception as e:
            print(str(e))
            exit()
    print('MP3s downloaded succesfully.')
