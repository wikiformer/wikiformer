writer = open('sag.json','w')
import json
from tqdm import tqdm
import time
id_title = {}
title_id = {}
cnt_error = 0
with open('enwiki-20220101-pages-articles-multistream.xml') as f:
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    txt = f.read()
    sections = txt.split('<page>')
    print(len(sections))  # 21726008
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    for sec in tqdm(sections[1:len(sections)-1]):
        sa = []
        lines = sec.split('\n')
        title = 'null'
        see_also = 0
        id_flag = False
        for i in range(1,len(lines)):
            # <title>Abydos, Egypt</title>
            line = lines[i]
            if '<id>' in line and id_flag==False:
                # id = int(line.strip('    <id>').strip('</id>'))
                id = line.split('<id>')[1]
                id = id.split('</id>')[0]
                id = int(id)
                id_flag=True
            if '<title>' in line:
                title = line.split('<title>')[1]
                title = title.split('</title>')[0]
                # exit(9)
            if '==See also==' in line:
                # print(line)
                see_also = i
                break


        if title != 'null':
            id_title[id] = title
            title_id[title] = id

        if title == 'null':
            cnt_error = 1
            continue

        if see_also == 0:
            continue

        for i in range(see_also+1,len(lines)):
            if '==' in lines[i]:
                break
            if '* [[' in lines[i]:
                line = lines[i]
                tt = line.split('* [[')[1]
                tt = tt.split(']]')[0]
                sa.append(tt)
                # print(lines[i])

        writer.write(title + '\t' + json.dumps(sa) + '\n')


