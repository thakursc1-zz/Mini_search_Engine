
def build_index(file_name):
    file = open("%s"%file_name,'r')
    lines = file.read().splitlines()
    lines = [x for x in lines if x !="***"]
    index ={}
    while lines:
        link=lines.pop()
        words = lines.pop().strip()
        if words:
            words = words.split()
            for word in words:
                if word in index:
                    index[word].append(link)
                else:
                    index[word]=[link]
    return index

def Query(keywords,index):
    words=keywords.split()
    result={}
    for word in words:
        if word in index:
            for url in index[word]:
                if url in result:
                    if word not in result[url]:
                        result[url].append(word)
                else:
                    result[url]=[word]
    result =sorted(result.items(),key = lambda x:len(x[1]), reverse = True)
    return result


index = build_index("index123.txt")

print Query("Boyce",index)


           
    
    
