#!/usr/bin/python
# encoding: utf-8
import sys
from workflow import Workflow3

def main(wf):
    import os
    import urllib
    import urllib2
    import time
    from xml.etree import ElementTree

    # Get args from Workflow as normalized Unicode
    args = wf.args

    #sUrl = 'http://www.stands4.com/services/v2/syno.php?%s'
    sUrl = 'https://www.abbreviations.com/services/v2/syno.php?%s'

    iMaxResults = 25
    iUid = os.getenv('uid')         # <- this value is configured in the workflow variables in Alfred
    sTokenID = os.getenv('tokenid') # <- this value is configured in the workflow variables in Alfred
    sSearchTerm = args[0]
    sSearchType = args[1]

    if not iUid or not sTokenID:    # if not configured in workflow, use default/shared account
        iUid = 2909
        sTokenID = "HOoAQOAKYGutZOMk"

    #print "using iUid %s" % (iUid)
    #print "using sTokenID %s" % (sTokenID)

    if len(sSearchTerm) > 1:
        params = urllib.urlencode({
            'uid': iUid,
            'tokenid': sTokenID,
            'word': sSearchTerm,
            })
        data = urllib2.urlopen(sUrl, params).read()
        res = ElementTree.fromstring(data)
        #print "data is " + data

        if sSearchType == "synonyms":
            sArg = "http://www.synonyms.net/synonym/%s" % (sSearchTerm)
        else:
            sArg = "http://www.synonyms.net/%s/%s" % (sSearchType, sSearchTerm)

        aTitles = []
        aSubtitles = []
        i = 0
        for node in res.findall('result'):
            node2 = node.find(sSearchType).text
            if node2 is not None:
                tmp = node2.split(", ")
                while tmp:
                    if not tmp[0] in aTitles and tmp[0] != sSearchTerm:
                        node3 = node.find('definition').text
                        if node3 is not None:
                            if sSearchType == 'synonyms':
                                sSubtitle = node3
                            else:
                                sSubtitle = ''
                            sTitle = tmp[0]
                            aTitles.append(sTitle)
                            aSubtitles.append(sSubtitle)
                            i += 1

                    del tmp[0]
                    if i >= iMaxResults:
                        break

        for idx, iTitle in enumerate(aTitles):
            wf.add_item(title=iTitle, subtitle=aSubtitles[idx], arg=sArg, valid=True)

        # Send output to Alfred
        wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    sys.exit(wf.run(main))
