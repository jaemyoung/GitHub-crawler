from github import Github
from material_ import crawling_material
import numpy as np
import pandas as pd
import time


#%%
def crawling_data(repo, crawled_data, idx, keyword) :
    try :
    	contributors = [contributor.id for contributor in repo.get_contributors()]
    	url = repo.url
    	owner_type = crawling_material.find_owner_type(repo.organization)
    
    	try :
            row = [idx, repo.id, repo.name, repo.owner.id, owner_type, repo.full_name, repo.created_at, repo.updated_at, repo.get_topics(), repo.language, 
               contributors, len(contributors), repo.stargazers_count, repo.forks_count, keyword, crawling_material.url_organizer(url), repo.get_readme().size, repo.fork, 
               repo.open_issues, repo.parent, repo.contents_url,repo.description] # description 추가

    	except :
        	row = [idx, repo.id, repo.name, repo.owner.id, owner_type, repo.full_name, repo.created_at, repo.updated_at, repo.get_topics(), repo.language, 
               contributors, len(contributors), repo.stargazers_count, repo.forks_count, keyword, crawling_material.url_organizer(url), None, repo.fork, 
               repo.open_issues, repo.parent, repo.contents_url,repo.description] # readme 없을 떄
    
    	crawled_data.append(row)
        
    except :
        print('error occur')
    
    return crawled_data


def crawling_user(user_list) :
    # modify 'repos'
    # can not crawling where user contribute and fork
    
    doc_idx = 0; idx = 0; tiredness = 0; crawled_data = []
    
    for user_id in user_list : 
        user = git.get_user_by_id(user_id)
        repos = [repo for repo in user.get_repos()]
        followers = [follower for follower in user.get_followers()]
        followings = [following for following in user.get_followings()]
        organizations = [organization for organization in user.get_orgs()]
        
        row = [idx, user_id, user.name, repos, len(repos), user.company, user.email, user.location, followers, len(followers), followings, len(followings), organizations, user.contributions,
               user.url]
        
        crawled_data.append(row)
        idx += 1; tiredness += 1
        
        if tiredness == 300 :
            save_data(crawled_data, doc_idx, mode='user')
            tiredness = crawling_material.rest(tiredness)
            doc_idx += 1
        
    
def save_data(crawled_data, year, mode) :
    
    if mode == 'repo' :
        data = crawling_material.data_processing(pd.DataFrame(crawled_data, columns=crawling_material.repository_column), ['topics', 'contributors'])
        data.to_csv('C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/repo' + '_' + str(year)  + '.csv', mode='a', index=False)
        print('csv saved \n')
        
    elif mode == 'user' :
        data = crawling_material.data_processing(pd.DataFrame(crawled_data, columns=crawling_material.user_column), ['repo_id', 'followers', 'following', 'organization_list'])
        data.to_csv('C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/user' + str(year) + '.csv', index=False)


def search_by_keyword(start_date, end_date, save_point) :
    
    # watchers have error -> print stargazer data 
    # variable declare
    crawled_data = []; tiredness = 0 ; doc_idx = 0; idx = 0
    
    for period in crawling_material.make_periods_list(start_date, end_date) :  
        for keyword in crawling_material.keywords :
            if idx < save_point : 
                #idx += crawling_material.number_of_repos[keyword][period]
                idx += save_point
                break
            
            else :
                try :
                    count_per_iteration = 0
                    query = '+'.join([keyword]) +' created:' + str(period)
                    result = git.search_repositories(query, sort='stars', order='desc')
                    
                    for repo in result :
                        crawled_data = crawling_data(repo, crawled_data, idx, keyword)
                            
                        print('{0} \t keyword : {1}, period : {2} \t {3}th data crawling out of {4} total data \t tiredness : {5}'.format(idx, keyword, period, 
                                                                                                                                              result.totalCount, count_per_iteration, tiredness))
                        count_per_iteration += 1
                        
                        time.sleep(np.random.random())
                        tiredness += 1
                        idx += 1
                        if tiredness == 300 or tiredness == 600 :
                            save_data(crawled_data, start_date[:4], mode='repo')
                            tiredness = crawling_material.rest(tiredness)
                            doc_idx+=1
                            crawled_data.clear()
                except :
                    print('repository does not exist')
                    
    save_data(crawled_data, start_date, mode='repo')


#%%
if __name__ == '__main__' :
   
    # set constant 
    ACCESS_TOKEN = ["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","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","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",
                    "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","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"]
    #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 새롬누나
    #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 민찬
    #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 재명
    #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 현호
    #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 예빈
    SAVE_POINT = 112
    
    git = Github("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") #7/08 재명 토큰
    git = Github("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") #7/11 새롬 토큰

    # topics 
    # machine-leaning
    # processed : image-processing, deep-learning
    # complete : aritificial-intelligence, autonomous-vehicle, automl, nlp, speech-recognition
    search_by_keyword('2015-06-01','2016-01-01', SAVE_POINT)
    
    
    del git


#%% organization 단위 크롤러
def get_organization(repo) :
    try :
    	contributors = [contributor.id for contributor in repo.get_contributors()]
    	url = repo.url
    	owner_type = crawling_material.find_owner_type(repo.organization)
    
    	try :
            row = [repo.id, repo.name, repo.owner.id, repo.full_name, repo.created_at, repo.updated_at, repo.get_topics(), repo.language, 
               contributors, len(contributors), repo.stargazers_count, repo.forks_count, repo.get_readme(), repo.fork, 
               repo.open_issues, repo.parent, repo.contents_url,repo.description]

    	except :
        	row = [repo.id, repo.name, repo.owner.id, repo.full_name, repo.created_at, repo.updated_at, repo.get_topics(), repo.language, 
               contributors, len(contributors), repo.stargazers_count, repo.forks_count, None, repo.fork, 
               repo.open_issues, repo.parent, repo.contents_url,repo.description] # readme 없을 떄
    
	
    except :
        print('error occur')
        row = []
        
    return row

#빈 리스트 제거
intel_repo =list(filter(None, intel_repo))
#중복 리스트 value 제거
set()

git = Github("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") #8/04 재명 토큰
git = Github("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") #근수형
organization = git.get_organization("intel")
user = git.get_user_by_id(organization.id)
repos = repos = [repo for repo in user.get_repos()]

intel_repo = []
for repo in repos[490:]: 
    if len(intel_repo) - len(list(filter(None,intel_repo)))<10:
        intel_repo.append(get_organization(repo))
    else:
        break
    
aws_repo = []
for repo in repos:
    if len(list(filter(None,aws_repo)))> 10:
        aws_repo.append(get_organization(repo))
    
microsoft_repo = []
for repo in repos[4184:]: #1401
    if len(microsoft_repo) - len(list(filter(None,microsoft_repo)))<10:
        microsoft_repo.append(get_organization(repo))
    else:
        break
    

google_repo = []
for repo in repos[2043:]: #2053 부터
    if len(google_repo) - len(list(filter(None,google_repo)))<10:
        google_repo.append(get_organization(repo))
    else:
        break
    

meta_repo = []
for repo in repos:
    if len(meta_repo) - len(list(filter(None,meta_repo)))<10:
        meta_repo.append(get_organization(repo))
    else:
        break

IBM_repo = []
for repo in repos[1567:]:
    if len(IBM_repo) - len(list(filter(None,IBM_repo)))<10:
        IBM_repo.append(get_organization(repo))
    else:
        break

import pickle
file_path = "C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/intel.pickle"
with open(file_path,"wb") as fw:
    pickle.dump(intel_repo, fw)   
    
#%% 크롤링 데이터 결합
import pickle
file_path = "C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/microsoft.pickle"
with open(file_path,"rb") as fr:
    microsoft = pickle.load(fr) 

file_path = "C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/IBM.pickle"
with open(file_path,"rb") as fr:
    IBM = pickle.load(fr) 
    
file_path = "C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/google.pickle"
with open(file_path,"rb") as fr:
    google = pickle.load(fr) 
    
file_path = "C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/aws.pickle"
with open(file_path,"rb") as fr:
    aws = pickle.load(fr) 

file_path = "C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/meta.pickle"
with open(file_path,"rb") as fr:
    meta = pickle.load(fr) 

file_path = "C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/intel.pickle"
with open(file_path,"rb") as fr:
    intel = pickle.load(fr) 
    
#데이터 결합
total_data = microsoft + IBM + google + aws + intel + meta
#빈 리스트 제거 후 dataframe 생성
total_data =list(filter(None, total_data))
total_data = pd.DataFrame(total_data, columns= ['repo.id', 'repo.name', 'repo.owner.id', 'repo.full_name', 'repo.created_at', 'repo.updated_at', 'repo.get_topics()', 'repo.language', 
               'contributors', 'len(contributors)', 'repo.stargazers_count', 'repo.forks_count', 'repo.get_readme()', 'repo.fork', 
               'repo.open_issues', 'repo.parent', 'repo.contents_url', 'repo.description'])
repo.name
repo.network_count

for row in total_data: # 중간 null값 제외
    print(list(row[6])
    break
    new = [row[1],row[3],row[7],row[4],row[5],row[6],row[9],row[10],row[11],row[17]]# ['repo_name', 'full_name', 'create_date', 'update_date', 'topics','contributro_counts','stargazer_counts', 'forker_counts',"description"]
    data.append(new)

data = pd.DataFrame(data, columns=['repo_name', 'full_name', 'programing_language','create_date', 'update_date', 'topics','contributro_counts','stargazer_counts', 'forker_counts',"description"])
data.to_csv('C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/total_organiztion_11106repo.csv', mode='a', index=False)
    
#%%
data = pd.read_csv("C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/total_organiztion_11106repo.csv")

data["owner"] = data["full_name"].apply(lambda x: x.split("/")[0])
data["topic_exists"] = data["topics"].apply(lambda x : x if len(x)>2 else None) # topic이 존재하는 repo만 추출
data = data.dropna(axis= 0)
data[data["owner"] == "microsoft"] 
data[data["owner"] == "IBM"]
data[data["owner"] == "google"]
data[data["owner"] == "aws"]
data[data["owner"] == "intel"]
data[data["owner"] == "facebook"]

data["after_topics"]=data["topics"].apply(lambda x : x.replace(",","").replace("[","").replace("]","").replace("'","").split(" ")) # 문자열 -> 리스트로 변환
data = data.reset_index()
data.to_csv("C:/Users/user/Documents/GitHub/GitHub-crawler/crawled_data/2332.csv")

