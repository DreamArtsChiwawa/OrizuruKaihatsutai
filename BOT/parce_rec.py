import sys
import os
# sys.path.append(os.pardir)
# print(os.pardir)
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../AI")
import search
import train

#def get_text():
#   text = [("./to/dir/a.mes.utf","A部門 すぎた",0.8111),("./to/dir/a.mes.utf","A部門 すずき",0.5111),("./to/dir/a.mes.utf","B部門 やまだ",0.38),("./to/dir/a.mes.utf","C部門 たろう",0.01),("./to/dir/a.mes.utf","B部門 やまだ",0.18),("./to/dir/a.mes.utf","C部門 たろう",0.01),("./to/dir/a.mes.utf","B部門 やまだ",0.18),("./to/dir/a.mes.utf","C部門 たろう",0.01)]
#   return text

#AI側からのレコメンド結果を受け取る
def get_top3(message):
    text = message
    rec = []
    for i in text:
        if len(rec) != 3 and i not in rec:
            rec.append(i)
        else:
            break
    return rec

# sim_list = search.search_similar_docs()
a = get_text()
rec = get_top3(a)

print(rec)
