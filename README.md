# Wikiformer

## Source code of our submitted paper:

## Wikiformer: Pre-training with Structured Information of Wikipedia for Ad-hoc Retrieval



### Some notes about this anonymous repository

- **This GitHub repository has been anonymized.**

- **The core code of this paper is publicly available in this GitHub repository. As the paper is currently under submission, once it is accepted, we will disclose the complete code and data in this repository.**
- **Some of the code in this repository involves absolute paths. Once the paper is accepted, we will make all the files corresponding to these paths publicly available.**

### The file structure of this repository:

```
.
├── demo_data
│   ├── Wikipedia_corpus
│   │   └── articles.txt
│   ├── preprocessed_training_data
│       ├── SRR_task.jsonl
│       ├── RWI_task.jsonl
│       ├── ATI_task.jsonl
│       ├── LTM_task.jsonl
│       └── file_format.txt
├── data_preprocess
│   ├── raw_to_tree.py
│   └── build_graph.py
├── pre-training_data_generation
│   ├── demo_data
│   │   ├── articles_tree_structure.jsonl
│   │   ├── SAG.jsonl
│   │   └── title_abstract.jsonl
│   ├── generate_SRR_task_data.py
│   ├── generate_RWI_task_data.py
│   ├── generate_ATI_task_data.py
│   └── generate_LTM_task_data.py
	(Once the paper is accepted, we will make them publicly available.)
├── pre-training
    └── pre-train.sh
```



### Pre-installation

```
git clone git@github.com:wikiformer/wikiformer.git
cd caseformer
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```



#### Building Wiki Trees

Firstly, we process each article in the wikidump in the following format: Before the title of level 'i', we mark it with 'i' number of '#'.



Then, use the following code to convert the article into a tree structure stored in JSON format:

```
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

```

After running the code, it outputs the tree structure of each article, as follows:

```
{
	"title": "Ambulance services of Victoria",
	"docid": "11987285",
	"section_list": [{
		"subtitle": "Volunteers.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "Volunteers."],
		"text": "In some remote areas, Ambulance Victoria oversees volunteer \"Community Emergency Response Teams\" (CERTs) that deliver first aid before professional paramedics can attend to emergency victims. CERTs do not transport patients. \"Ambulance Community Officers\" offer similar services as individuals."
	}, {
		"subtitle": "History.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "History."],
		"text": "In 1883 as a result of a public meeting, a branch of the St John Ambulance Association was set up to teach home nursing and first aid to as many people as possible. In 1887 enough money was raised to purchase six Ashford Litters which were placed at police stations. In 1899 Melbourne's first ambulance station was opened at the rear of the Windsor Hotel off Bourke Street. It housed one horse drawn ambulance that was bought with money raised by the Association of Ladies of St John. In the 1980s, the Metropolitan Ambulance Service was formed from a number of smaller area services; and 16 regional services were amalgamated into five. In 1997, these regional services were consolidated to one rural service, Rural Ambulance Victoria (RAV). On 26 May 2008, the government confirmed that, from 1 July 2008, RAV, the Metropolitan Ambulance Service and the Alexandra District Ambulance Service would be merged to form Ambulance Victoria (AV), bringing Victoria into line with other states, having one ambulance service for the whole of the state. It is stated in the 2009-10 Annual Report that Ambulance Victoria had 2143 operational Ambulance Paramedics and 416 MICA Paramedic. There were also 613 operational support and management staff."
	}, {
		"subtitle": "Metropolitan Ambulance Service.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "Metropolitan Ambulance Service."],
		"text": "In the 1980s, Metropolitan Ambulance Service (MAS) was formed from a number of smaller area services. It serviced an area of 9,000 square kilometres, extending from the Melbourne Central Business District to the Mornington Peninsula and the peripheral rural communities of Bacchus Marsh, Whittlesea, Warburton and Koo-Wee-Rup. Almost 4 million residents lived in this area. The primary vehicles used for emergency attendance and transport was Mercedes Benz 316 Sprinters and Ford F350's. These units were run with two paramedics. MICA (Mobile Intensive Care Ambulance) used the Mercedes Benz 316's, as well as Ford Territory, Ford Falcon, Holden Commodore, Holden Adventra and Subaru Forester. The MICA units were typically staffed with one specially trained paramedic which included advanced life support (ALS), that were used in cases where extensive patient care was required in addition to a regular unit. Bicycle units were used as first responders at major events, including the 2006 Commonwealth Games, Spring Racing Carnival and The Big Day Out. In 2008, Metropolitan Ambulance Service was merged with Rural Ambulance Victoria and Alexandra District Ambulance Service to form Ambulance Victoria (AV). A partnership existed between MAS and the Metropolitan Fire and Emergency Services Board, where firefighters are dispatched to time-critical medical emergencies where their response time may be quicker than that of the closest MAS unit. The primary example of this is cardiac arrest patients, which has led to fire trucks being equipped with defibrillators and the firefighters being trained advanced CPR and defibrillation."
	}, {
		"subtitle": "Rural Ambulance Victoria.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "Rural Ambulance Victoria."],
		"text": "Rural Ambulance Victoria (RAV) was responsible for pre-hospital emergency care and transport for the 1.4 million people living and working in rural Victoria \u2013 an area of more than 215,000 square kilometres extending from the boundaries of Melbourne to the borders with South Australia and New South Wales. In the 1980s, 16 regional ambulance services were amalgamated into five, and in 1997 these were consolidated to one rural service, Rural Ambulance Victoria.  In 2008, RAV merged with the Metropolitan Ambulance Service and the Alexandra District Ambulance Service to form Ambulance Victoria (AV)."
	}, {
		"subtitle": "Alexandra District Ambulance Service.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "Alexandra District Ambulance Service."],
		"text": "Alexandra District Ambulance Services was formed by the community in 1948. The area serviced comprised the districts of Alexandra, Eildon and Marysville (formally the shire of Alexandra)."
	}, {
		"subtitle": "St John Ambulance Victoria.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "St John Ambulance Victoria."],
		"text": "St John Ambulance was the founding ambulance service in Victoria. St John Ambulance Victoria now provides Non-Emergency Patient Transport (NEPT) services in Victoria. It also provides first aid services at major events across the state and at times interstate. First aid services are provided primarily via a volunteer workforce, however, there are also paid staff. St John also provides first aid services during natural disasters across the state and also interstate."
	}, {
		"subtitle": "Life Saving Victoria.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "Life Saving Victoria."],
		"text": "Life Saving Victoria offers volunteer aquatic rescue and first aid services in many coastal areas, and in Mildura. While they do transport patients from the water to land, they do not transport patients to hospitals once landed."
	}, {
		"subtitle": "Hatzolah.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "Hatzolah."],
		"text": "Hatzolah responders are trained by Ambulance Victoria and equipped with oxygen and semi-automatic defibrillators. They usually are used within the Jewish community; but, Hatzolah will also respond to any person's call. Hatzolah responders are trained and equipped to deal with any medical emergency and regularly attend cases such as chest pain, bleeding, full arrest, household accidents, asthma and road trauma. Hatzolah responders are on stand-by 24 hours a day, 365 days a year."
	}, {
		"subtitle": "Australian Volunteer Coast Guard.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "Australian Volunteer Coast Guard."],
		"text": "The Australian Volunteer Coast Guard provides a maritime search and rescue service, and answers distress calls made by vessels off the Victorian coast. This can involve the transportation of emergency patients."
	}, {
		"subtitle": "Emergency medical response.",
		"level": 2,
		"merged_title": ["Ambulance services of Victoria", "Emergency medical response."],
		"text": "Both the Melbourne Metropolitan Fire Brigade (MFB) and the Country Fire Authority (CFA) have emergency medical response programs, which involve members being trained to respond to cases of suspected cardiac arrest, providing CPR, oxygen and defibrillation services before an ambulance arrives."
	}],
	"max_level": 2,
	"abstract": ["", "Since 1 July 2008, Ambulance Victoria has been the sole provider of emergency ambulance services in Victoria, having been formed from the merger of the three previous providers of emergency ambulance services: the Metropolitan Ambulance Service (MAS), Rural Ambulance Victoria (RAV), and the Alexandra District Ambulance Service (ADAS).", "The MAS was responsible for Melbourne and its outer suburbs while RAV was responsible for regional and rural areas of Victoria, except for the Alexandra, Marysville, and Eildon areas, which was serviced by ADAS.", "All services of Ambulance Service Victoria operate under the \"Ambulance Services Act 1986\". In addition, a number of non-emergency patient transport companies operate under the \"Non-Emergency Patient Transport Act 2003\" and use conventional ambulances equipped with emergency lights and sirens, and sometimes attend emergency cases."],
	"error": 0
}

```



### Running Pre-training

**We will disclose the complete code and data in this repository.**