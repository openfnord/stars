# YOLOv5 🚀 by Ultralytics, GPL-3.0 license
"""
Count GitHub repository stars over a time period

Usage:
    $ python path/to/count_stars.py
"""

from datetime import datetime

import pandas as pd
from github import Github  # pip install PyGithub
from tqdm import tqdm

# Settings
TOKEN = "ghp_YEKVmKSn1Z9..."  # GitHub access token
# date = datetime(2022, 3, 1)  # count stars since this day, i.e. March 1st 2022
# days = (datetime.now() - date).total_seconds() / 86400  # compute number of days
days = 30  # specify days directly, i.e. last 30 days

repos = [
    'ultralytics/yolov5',  # YOLOv5 🚀

    'facebookresearch/detectron2',  # FAANG companies
    'deepmind/deepmind-research',
    'aws/amazon-sagemaker-examples',
    'awslabs/autogluon',
    'microsoft/lightgbm',
    'openai/gpt-3',
    'apple/turicreate',
    'apple/coremltools',

    'tencent/ncnn',  # Chinese companies
    'Megvii-BaseDetection/YOLOX',
    'PaddlePaddle/Paddle',

    'rwightman/pytorch-image-models',  # Startups/architectures
    'streamlit/streamlit',
    'explosion/spaCy',
    'PyTorchLightning/pytorch-lightning',
    'ray-project/ray',
    'fastai/fastai',
    'google/automl',
    'alexeyab/darknet',
    'pjreddie/darknet',
    'WongKinYiu/yolor',
    'wandb/client',
    'Deci-AI/super-gradients',
    # 'huggingface/transformers',  # known issue over 40k stars https://github.com/PyGithub/PyGithub/issues/1876
]
save = False  # save user info

# Parameters
g = Github(TOKEN)  # create a Github instance
print(f'Counting stars for last {days:.1f} days\n')
pd.options.display.max_columns = None

# Run
users = []
for repo in repos:
    r = g.get_repo(repo)
    s = r.get_stargazers_with_dates().reversed
    total = s.totalCount

    try:
        n = 0
        pbar = tqdm(s, total=total, desc=r.full_name)
        for x in pbar:
            dt = (datetime.now() - x.starred_at).total_seconds() / 86400
            if dt < days:
                n += 1
                if save:
                    u = x.user
                    if u.email is not None:
                        users.append([r.full_name, u.name, u.company, u.email, u.location, u.html_url, u.followers])
            else:
                s1 = f'{n} stars'
                s2 = f'({n / days:.1f}/day)'
                pbar.desc = f'{r.full_name:40s}{s1:12s}{s2:12s}'
                break
    except Exception as e:
        print(e)

    # Threaded
    # from multiprocessing.pool import Pool, ThreadPool
    # fcn = lambda x: x.starred_at > date
    # results = ThreadPool(8).imap(fcn, s)
    # pbar = tqdm(enumerate(results), total=total)
    # for i, x in pbar:
    #     n += x  # im, hw_orig, hw_resized = load_image(self, i)

if save:
    x = pd.DataFrame(users, columns=['Repo', 'Name', 'Company', 'Email', 'Location', 'GitHub', 'Followers'])
    x.to_csv(f'users.csv')
    print(f'{len(x)} users saved to users.csv')
