import search
import train

INPUT_PATH = ''

if __name__ == '__main__':
    print("test document: " + INPUT_PATH)
    search_str = train.read_document(INPUT_PATH)
    print(train.trim_doc(search_str))
    print("================\n\n")
    for path, name, sim in search.search_similar_docs(search_str):
        print(path)
        
        text, _ = train.trim_doc(train.read_document(path))
        print(text)
        print("-------------\n\n")
