import search
import train
import sys

INPUT_PATH = '../../staff_wr/12.mes.utf'

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("test document: " + INPUT_PATH)
        search_str = train.read_document(INPUT_PATH)
        print(train.trim_doc(search_str))
    else if len(sys.argv) == 2 and sys.argv[1] == '-m':
        search_str = input("課題を入力\n")
    else:
        print("引数指定が正しくありません。")
        sys.exit()

    print("================\n\n")
    for path, name, sim in search.search_similar_docs(search_str):
        print(path)
        
        text, _ = train.trim_doc(train.read_document(path))
        print(text)
        print("-------------\n\n")
