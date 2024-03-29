import os
from tqdm import tqdm
import json
import re
import random
cnt = 0
cnt1 = 0
cnt_error = 0
file = '/root_of_articles/'
writter = open('path ','a')
error_writter =open('path','a')
'''
list[doc,doc1,...] or jsonl-doc

doc = {}
'docid'=''
'title':''
'max_level':n
'abstract':''
'section_list':[{},{},...]
    subtitle:''
    level:n
    merged_title:[]
    text:''
'error':0
'''

def one_file(path):
    global cnt,cnt1,cnt_error
    with open(path,'r') as f:
        txt = f.read()
        docs = txt.split('<doc')

        # 处理每一个doc
        for doc in docs[1:]:
            out_dict = {}
            out_subtitle_list = []
            structure = []
            doc = doc.strip('</doc>\n')
            lines = doc.split('\n')
            if len(lines) < 4:
                continue

            # 存下来title
            docid = lines[0].split('\"')[1]
            title = lines[1]
            # print(docid,title)

            tree = []
            tree.append(title)
            top_level =1
            max_level = 0

            out_dict['title'] = title
            out_dict['docid'] = docid
            error_flag = 0
            session_list = []


            for i in range(len(lines)):
                line = lines[i]
                if not line:
                    continue
                if '#' in line.split(' ')[0]:
                    title_grade = len(line.split(' ')[0])
                    sub = ' '.join(line.split(' ')[1:])
                    structure.append((sub,i,title_grade))
                    # print(line,title_grade,i)

            if len(structure)!=0:
                first_title = structure[0][1]
                abstract = (lines[2:first_title])
                # abstract = ' '.join(lines[2:first_title])
            else:
                abstract = (line[2:])
                # abstract = ' '.join(line[2:])

            for i in range(len(structure)):
                out_section = {}
                start = structure[i][1]
                if i !=len(structure)-1:
                    end = structure[i+1][1]
                else:
                    end = len(lines)

                subtitle = structure[i][0]
                curr_level = structure[i][2]
                if curr_level>max_level:
                    max_level=curr_level

                if curr_level==top_level:
                    tree.pop()
                    tree.append(subtitle)
                elif curr_level == top_level +1:
                    tree.append(subtitle)
                elif curr_level < top_level:
                    times = top_level - curr_level
                    for _ in range(times+1):
                        try:
                            tree.pop()
                        except:
                            # print(path)
                            # print(docid)
                            error_writter.write(path + ',' + docid + '\n')
                            cnt_error += 1
                            error_flag = 1
                            break
                    tree.append(subtitle)
                else:
                    cnt_error += 1
                    error_flag = 1
                    error_writter.write(path + ',' + docid + '\n')
                    break
                top_level=curr_level
                # deep copy
                curr_tree = []
                for ___ in tree:
                    curr_tree.append(___)

                txt_ = lines[start+1:end]
                txt = ' '.join(txt_)
                out_section['subtitle'] = subtitle
                out_section['level'] = curr_level
                out_section['merged_title'] = curr_tree
                out_section['text'] = txt
                session_list.append(out_section)

            out_dict['section_list'] = session_list
            out_dict['max_level'] = max_level
            out_dict['abstract'] = abstract
            out_dict['error'] = error_flag
            if error_flag ==0:
                cnt += 1
            else:
                cnt1 += 1
            writter.write(json.dumps(out_dict) + '\n')




for root, dirs, files in tqdm(os.walk(file),total=165):
    for f in (files):
        path = os.path.join(root, f)
        one_file(path)


print(cnt,cnt1,cnt_error)
