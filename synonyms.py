import urllib
import urllib2
import alfred
import time
from xml.etree import ElementTree

url = 'http://www.stands4.com/services/v2/syno.php?%s'
#example url:  http://www.stands4.com/services/v2/syno.php?uid=2909&tokenid=HOoAQOAKYGutZOMk&word=consistent

MAX_RESULT = 20


def search_synonyms(iUid, sTokenID, sSearchTerm, sSearchType):

    if len(sSearchTerm) > 1:
        params = urllib.urlencode({
            'uid': iUid,
            'tokenid': sTokenID,
            'word': sSearchTerm,
            })
        data = urllib2.urlopen(url, params).read()
        res = ElementTree.fromstring(data)

        feedback = alfred.Feedback()
        feedback.addItem(title=u"Search synonyms.net for \"%s\"" % "".join(sSearchTerm),
                         subtitle=u"Opens search results in webbrowser",
                         arg="http://www.synonyms.net/synonym/%s" % sSearchTerm,
                         valid=True,
                         )

        synonyms = []
        i = 0
        for node in res.findall('result'):
            node2 = node.find(sSearchType).text
            if node2 is not None:
                tmp = node2.split(", ")
                while tmp:
                    if not tmp[0] in synonyms and tmp[0] != sSearchTerm:
                        node3 = node.find('definition').text
                        if node3 is not None:
                            if sSearchType == 'synonyms':
                                sSubtitle = node3
                            else:
                                sSubtitle = ''
                            feedback.addItem(title=tmp[0],
                                             subtitle=sSubtitle,
                                             arg="http://www.synonyms.net/%s/%s" % (sSearchType, sSearchTerm),
                                             valid=True,)
                            synonyms.append(tmp[0])
                            i += 1

                    del tmp[0]
                    if i >= MAX_RESULT:
                        break

        return feedback
    else:
        return None


# search_synonyms(2909, 'HOoAQOAKYGutZOMk', 'consistent', 'synonyms')
# search_synonyms(2909, 'HOoAQOAKYGutZOMk', 'consistent', 'antonyms')