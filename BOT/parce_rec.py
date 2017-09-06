from AI import search
#def get_text():
#    text = [("./to/dir/a.mes.utf","A部門 すぎた",0.8111),("./to/dir/a.mes.utf","A部門 すずき",0.5111),("./to/dir/a.mes.utf","B部門 やまだ",0.38),("./to/dir/a.mes.utf","C部門 たろう",0.01),("./to/dir/a.mes.utf","B部門 やまだ",0.18),("./to/dir/a.mes.utf","C部門 たろう",0.01),("./to/dir/a.mes.utf","B部門 やまだ",0.18),("./to/dir/a.mes.utf","C部門 たろう",0.01)]
#    return text

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

sim_list = search_similar_docs()
rec = get_top3(sim_list)
#print(rec)
