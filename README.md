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
├── pre-training
    └── pre-train.sh
```



### Pre-installation

```
git clone git@github.com:wikiformer/wikiformer.git
cd caseformer
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```



### Prepare the Training Data

#### SRR Task



#### RWI Task



#### ATI Task



#### LTM Task



### Running Pre-training

**We will disclose the complete code and data in this repository.**