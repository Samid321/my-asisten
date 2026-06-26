from bs4 import BeautifulSoup
with open('./workspace/index.html','r') as file:
    data=BeautifulSoup(file,'html.parser')
hasil=data.find('body')
hasil.append(
    data.new_tag("p")
)
hasil.p.string='jadi'
print(data.prettify())
with open('./workspace/index.html','w') as file:

    jadi=file.write(f"{data.prettify()}")
    