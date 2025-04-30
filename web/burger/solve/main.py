from bs4 import BeautifulSoup

mapping = {
    "patty":0,
    "tomato":1,
    "lettuce":2,
}


with open('./index.html') as f:
    soup = BeautifulSoup(f, 'html.parser')

ingredients = soup.find_all('div', class_='ingredient')
res = []
tmp = ''
for i in ingredients:
    if i['class'][1] == 'middle-bun':
        res.append(tmp)
        tmp = ''
    else:
        tmp += str(mapping[i['class'][1]])
for i in res:
    print(chr(int(i, 3)), end='')
print()