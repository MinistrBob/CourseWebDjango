from bs4 import BeautifulSoup


def list_has_parent_list(tag):
    for parent in tag.parents:
        print(parent.name)
        if parent.name == "ul" or parent.name == "ol":
            return True
    return False


html = """<html>
 <body>
 <ul>
 </ul>
  <ul>
   <li class="nv-view">
   </li>
   <ul>
    <p>
     dddd
    </p>
   </ul>
   <li class="nv-edit">
    <ul>
    </ul>
    <br/>
   </li>
  </ul>
  <p>sss</p>
 </body>
</html>
"""
lists = 0
body = BeautifulSoup(html, "lxml")
# print(body.prettify())
# print("="*45)
all = body.find_all(True)
for i in all:
    if i.name == "ul" or i.name == "ol":
        lists += 1
        i.decompose()
    print(i)
    print("-" * 45)
print(lists)
"""
ll = body.find_all(['ul', 'ol'])
# print(ll)
for i in ll:
    print(i)
    for parent in i:
        if parent is None:
            print(parent)
        else:
            print(parent.name)
    # mm = i.find_all(list_has_parent_list)
    # print(f"LEN={len(mm)}")
    # for k in mm:
    #     print(k)
    #     print("-" * 45)
    print("="*45)
"""
