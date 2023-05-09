#!/home/pi/software/bin/python3

import cgi, cgitb
import subprocess

cgitb.enable( )
form = cgi.FieldStorage( )

cards = form.getvalue('cards')
numOfCards = len(cards)

def piInfo():
   print(subprocess.check_output("date", shell=True, text=True))
   print(subprocess.check_output("ps ax | grep nginx", shell=True, text=True))
   print(subprocess.check_output("uname -a", shell=True, text=True))
   print(subprocess.check_output("cat /sys/class/net/eth0/address", shell=True, text=True))
   print(subprocess.check_output("cat /proc/cpuinfo | tail -5", shell=True, text=True))
   print(subprocess.check_output("ifconfig | grep netmask", shell=True, text=True))

def findCategory(cards) :
   cate = []
   if isHighCard(cards) :
        cate.append("HC")
        print("High Card")
   elif isOnePair(cards) :
        cate.append("1P")
        print("One Pair")
   elif isTwoPair(cards) :
        cate.append("2P")
        print("Two Pair")
   elif isThreeOfAKind(cards) :
        cate.append("3K")
        print("Three Of A Kind")
   elif isStraight(cards) :
        cate.append("ST")
        print("Straight")
   elif isFlush(cards) :
        cate.append("FL")
        print("Flush")
   elif isFullHouse(cards) :
        cate.append("FH")
        print("Full House")
   elif isFourOfAKind(cards) :
        cate.append("4K")
        print("Four Of A Kind")
   elif isStraightFlush(cards) :
        cate.append("SF")
        print("Straight Flush")
   return cate

def isHighCard(cards) :
   if not (isOnePair(cards) or isTwoPair(cards) or isThreeOfAKind(cards) or isStraight(cards) or isFlush(cards) or isFullHouse(cards) or isFourOfAKind(cards) or isStraightFlush(cards)) :
        return 0

def isOnePair(cards) :
   cardList = []
   cnt = {}
   for i in range (len(cards)) :
      cardList += cards[i][0]
   for i in cardList :
      try: cnt[i] += 1
      except: cnt[i] = 1
   value = [card for card in cardList if cardList.count(card) == 2]
   pairCnt = sum(1 for val in cnt.values() if val == 2)
   if pairCnt == 1 and len(cnt) == 4:
      return True
   return False

def isTwoPair(cards) :
   cardList = []
   cnt = {}
   for i in range (len(cards)) :
        cardList += cards[i][0]
   for i in cardList :
        try: cnt[i] += 1
        except: cnt[i] = 1
   value = [card for card in cardList if cardList.count(card) == 2]
   pairCnt = sum(1 for val in cnt.values() if val == 2)
   if pairCnt == 2 :
        return True
   return False

def isThreeOfAKind(cards) :
   cardList = []
   cnt = {}
   for i in range (len(cards)) :
        cardList += cards[i][0]
   for i in cardList :
        try: cnt[i] += 1
        except: cnt[i] = 1
   value = [card for card in cardList if cardList.count(card) == 3]
   pairCnt = sum(1 for val in cnt.values() if val == 3)
   if pairCnt == 1 and len(cnt) == 3:
        return True
   return False

def isStraight(cards) :
   cardList = []
   cnt = {}
   if isFlush(cards) :
        return False
   for i in range (len(cards)) :
        cardList += cards[i][0]
   for i in cardList :
        try: cnt[i] += 1
        except: cnt[i] = 1
   value = [card for card in cardList if cardList.count(card) == 1]
   if len(value) == 5 :
        return True
   return False

def isFlush(cards) :
   cardList = []
   cnt = {}
   for i in range (len(cards)) :
        cardList += cards[i][1]
   cardOne = set(cardList)
   if len(cardOne) ==  1:
        return True
   return False

def isFullHouse(cards) :
   cardList = []
   cnt = {}
   for i in range (len(cards)) :
        cardList += cards[i][0]
   for i in cardList :
        try: cnt[i] += 1
        except: cnt[i] = 1
   pairCnt1 = sum(1 for val in cnt.values() if val == 3)
   pairCnt2 = sum(1 for val in cnt.values() if val == 2)
   if pairCnt1 == 1 and pairCnt2 == 1:
        return True
   return False

def isFourOfAKind(cards) :
   cardList = []
   cnt = {}
   for i in range (len(cards)) :
        cardList += cards[i][0]
   for i in cardList :
        try: cnt[i] += 1
        except: cnt[i] = 1
   if 4 in cnt.values() :
        return True
   return False

def isStraightFlush(cards) :
   cardList = []
   cnt = {}
   for i in range (len(cards)) :
        cardList += cards[i][1]
   for i in cardList :
        try: cnt[i] += 1
        except: cnt[i] = 1
   if 5 in cnt.values() :
        return True
   return False

print("Content-type: text/html\n\n")
print("<html>\n")
print("<head>\n")
print("<title>Reply from PRG550 Assignment #2</title>\n")
print("</head>\n")
print("<body>\n")
print("<body bgcolor='%s'>\n" % "#BA55D3")
print("<font size='%d'>\n" % 6)
if numOfCards != 5 :
   print("<p>Sorry, you must select exactly 5 cards!", "\n</p>")
   print("<p>Please go back to your selected page.</p>")
else :
   print("<p>cards selected:", cards, "\n</p>")
   print("<img src=", cards[0], "/>\n")
   print("<img src=", cards[1], "/>\n")
   print("<img src=", cards[2], "/>\n")
   print("<img src=", cards[3], "/>\n")
   print("<img src=", cards[4], "/>\n")
   print("<font size='%d'>\n" % 8)
   print("<font color='%s'>\n" %  "#07E819")
   print("<p>Your Poker Hand represents a")
   findCategory(cards)
   print("</font>\n")
   print("</font>\n")
   print("</p>")
piInfo()
print("</font>\n")
print("</body>\n")
print("</html>\n")
