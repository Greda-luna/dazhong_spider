import urllib.request
from lxml import etree
import re
import json

#获取url和请求头
url = 'https://www.dianping.com/shop/HajqBkC81dr9cwHs/review_all'
#第二页url = 'https://www.dianping.com/shop/HajqBkC81dr9cwHs/review_all/p2'
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'cookie':'fspop=test; _lxsdk_cuid=18ddc69eee1c8-0c61af463b05f9-4c657b58-15f900-18ddc69eee1c8; _lxsdk=18ddc69eee1c8-0c61af463b05f9-4c657b58-15f900-18ddc69eee1c8; _hc.v=bb66ceb9-747d-16ed-bec4-fbbc6e3ef91c.1708799946; s_ViewType=10; WEBDFPID=90xzx4y7ux6957y6z984v78524wy72z781wwx3z504u9795896725207-2024159969835-1708799969835MACUWGEfd79fef3d01d5e9aadc18ccd4d0c95072493; qruuid=16e33ae5-4a2c-48b6-b5b4-5b90d8209fa7; dplet=1f284d93e446d6c1bc46878fa63a49d1; dper=02029e1d784f15af8a1af6c8dd47641f83a1bb2f15a4f6d2b759986dc56393ed06c9317a289193e550d42d6e055137866a87fbc22d6c5afe4c8000000000501e0000d6602b221220913e7b030ad01a55629f5c170ab540a962c64d01b98cf7134265069eba8d07ca7ed07488c43a6d72b90b; ua=%E9%9B%84%E4%BB%81%E4%B8%93%E4%B8%9A%E7%9A%84%E5%B0%8F%E4%B8%BD; ctu=e5fbee4e58fbca08f026a0d2f85d1f9604558fe5f77a79bfb9401a8c332ab537; ll=7fd06e815b796be3df069dec7836c3df; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1708799949,1708876552,1708997765,1709023252; cy=5; cye=nanjing; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1709023535; _lxsdk_s=18de9b94b03-ba-a89-74d%7C%7C279'
}
#获取网页源码
request = urllib.request.Request(url=url,headers=headers)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')
tree = etree.HTML(content)
#通过xpath路径获取初步用户名，评论内容和星级内容
first_name = tree.xpath('//div[@class="dper-info"]//a/text()')
first_comment = tree.xpath('//div[@class="reviews-items"]//li//div[@class="main-review"]/div[@class="review-words Hide"]/text()')
first_star = tree.xpath('//div[@class="reviews-items"]//li//div[@class="review-rank"]/span/@class')
#存储处理过的数据
comment = []
name = []
star = []
end_star = []
dict1 = []
#处理数据
#去掉评论内容中的回车符，前后空格和换行符
for i in range(len(first_comment)):
    comment.append(first_comment[i].replace('\n','').strip().replace('\t',''))
#去掉评论内容中的空白元素
comment = list(filter(None, comment))
#去掉用户名中的前后空格和换行符
for i in range(len(first_name)):
    name.append(first_name[i].replace('\n','').strip())
#由于获取到的星级数据是一串字符串，其中包含着具体星级，提取出星级内容，并将其转换成五分制
#从字符串中提取数字
for i in range(len(first_star)):
    star.append(re.findall("\d+\.?\d*", first_star[i]))
#获取到的是一个二维数组，要将其合并展开为一维数组
for x in range(len(star)):
    for y in range(len(star[x])):
        end_star.append(float(star[x][y])/10)
#将获取到的评论内容和星级内容合并成一个列表
comment_and_star_list = list(zip(comment,end_star))
the_all = dict(zip(name,comment_and_star_list))
page = 1

with open('数据页/comment_all_'+str(page)+'.json', 'w', encoding='utf-8') as f:
    json.dump(the_all, f, ensure_ascii=False)



