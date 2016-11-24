import requests
import datetime


def get_trending_repositories(top_size):
    days_count = 7
    today = datetime.date.today()
    week = datetime.timedelta(days=days_count)
    week_ago = today - week

    params_list = {'q': 'created:>={0}'.format(week_ago), 'sort': 'stars'}
    url = 'https://api.github.com/search/repositories'
    response = requests.get(url, params=params_list)
    trending_repositories = response.json()
       
    return trending_repositories['items'][:top_size]


def get_open_issues(repo_owner, repo_name):
    url = 'https://api.github.com/repos/{0}/{1}/issues'.format(
        repo_owner,
        repo_name
    )    
    
    response = requests.get(url)
    open_issues_list = response.json()
    
    return open_issues_list


def print_open_issues_data(open_issues_list):
    for num, issue in enumerate(open_issues_list):
        print('Issue {0}: {1} (URL: {2})'.format(
            num + 1,
            issue['title'],
            issue['html_url'])
        )


if __name__ == '__main__':
    top_size = 20
    trending_repositories = get_trending_repositories(top_size)
    
    for (num, repo) in enumerate(trending_repositories):
        open_issues_amount = repo['open_issues_count']
        
        print('{0}. {1}. (Stars: {2}. Issues amount: {3}. URL: {4})'.format(
            num + 1,
            repo['name'],
            repo['stargazers_count'],
            open_issues_amount,
            repo['html_url']
            )
        )
        
        if open_issues_amount:
            open_issues = get_open_issues(repo['owner']['login'], repo['name'])
            print_open_issues_data(open_issues)
