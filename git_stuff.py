from git import Repo

def get_change_type(change):
    if change.deleted_file:
        return 'added' 
    elif change.new_file:
        return 'deleted' 
    else:
        return 'Modified '

def get_last_changes(repository_path):
    stuff = {
        'files': []
    }
    try:
        repo = Repo(repository_path)
        commits = repo.iter_commits()
        last_changes = []
        for commit in commits:
            change= {
                'commit': commit.hexsha[:7],
                'author': commit.author.name, 
                'message': commit.message.strip(),
                'files': []
            }
            for item in commit.diff('HEAD~1'):
                file_change = {
                    'filename': item.a_path,
                    'type': get_change_type(item)
                }
                change['files'].append(file_change)
                stuff['files'].append(file_change)
                last_changes.append(change)
            return stuff
    except Exception as e:
        print(f" Error occured while trying to get last changes: {e}")
        return []

def push_changges(message, repo_path):
    repo = Repo(repo_path)
    repo.git.add('--all')
    repo.index.commit(message)
    remote = repo.remote()
    remote.push()
    print('Changes pushed to remote')

repo_path = ''
a = get_last_changes(repo_path)
print(a)
message = 'test'
#push_changges(message, repo_path)


# why are you making erros

