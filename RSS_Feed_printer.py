import feedparser

#all da feeds
sites = ['https://unit42.paloaltonetworks.com/feed/','https://www.blackhillsinfosec.com/feed/', 'https://www.fireeye.com/blog/threat-research/_jcr_content.feed',
         'https://redcanary.com/blog/feed/','https://www.bleepingcomputer.com/feed/','https://blog.malwarebytes.com/feed/','https://msrc-blog.microsoft.com/feed/']


def news_printer(sites):
    x = 0
    page = feedparser.parse(site)
    num = len(page['feed']['title'])
#Check for FireEyes cause they are formated a bit different, Other wise formats printing of feeds
    if page['feed']['title'] == 'Threat Research':
        print('=======')
        print('FireEye')
        print('=======')
    else:
        print('=' * num)
        print(page['feed']['title'])
        print('=' * num)
# takes the first 3 articles of the site. prints title and link
    for post in page.entries:
        if x < 3:
            print('    ' + post.title + ':')
            print('        ' + post.link)
            x = x + 1

#for loop for running all sites listed
for site in sites:
    news_printer(site)
input("Press enter to exit")
