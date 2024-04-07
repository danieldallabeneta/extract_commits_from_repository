from github import Github
import csv
import pandas as pd

token = ''

df = pd.DataFrame(columns=['Commit', 'Tag Hash','Release'])

github = Github(token)

def find_tag_for_commit(repository_name):
    try:
        df = pd.DataFrame(columns=['Commit Hash', 'Tag Hash'])
        
        repo = github.get_repo(repository_name)

        #começa meu codigo
        tags = repo.get_tags()

        for tag in tags:
            tag_name = tag.name
            tag_atual = repo.get_git_ref(f'tags/{tag_name}')
            
            commits = repo.get_commits(sha=tag_atual.object.sha)
            for commit in commits:  
                df = df.append({'Commit Hash': commit.sha, 'Tag Hash': tag.commit.sha}, ignore_index=True) 
        
    except Exception as e:
        print("Ocorreu um erro:", e)        

def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Commit Hash", "Tag"])
        writer.writerows(data)

def read_commit_hashes_from_txt(filename):
    with open(filename, 'r') as file:
        commit_hashes = [line.strip() for line in file]
    return commit_hashes

txt_filename = "lista_hashes_commits.txt"

# Lê os hashes de commit do arquivo TXT
#commit_hashes = read_commit_hashes_from_txt(txt_filename)

# Lista para armazenar os resultados
#results = []

repository_name = "apache/commons-bcel"

#find_tag_for_commit(repository_name)

repo = github.get_repo(repository_name)

tags = repo.get_tags()
release = len(list(tags))

for tag in tags:
    tag_name = tag.name
    tag_atual = repo.get_git_ref(f'tags/{tag_name}')
    commits = repo.get_commits(sha=tag_atual.object.sha)
    for commit in commits:  
        #print(commit.sha,tag_atual.object.sha)
        novo_dado = {'Commit': commit.sha, 'Tag Hash': tag.commit.sha, 'Release':release}        
        df = pd.concat([df, pd.DataFrame([novo_dado])], ignore_index=True)
    release = release - 1

# Nome do arquivo CSV
csv_filename = "resultado_commits_tags.csv"

df.to_csv(csv_filename, index=False)
# Exporta os resultados para um arquivo CSV
#export_to_csv(results, csv_filename)

print(f"Os resultados foram exportados para o arquivo '{csv_filename}'.")
