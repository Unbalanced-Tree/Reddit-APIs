import praw
import re

print('Logging in...')

reddit = praw.Reddit(client_id='client_id app',
                     client_secret='client_secret of app',
                     username='bot account username',
                     password='account password',
                     user_agent='user_agent')

print('Logged in!')
print('Bot Name:- ', reddit.user.me())


def bot_set(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    subreddit_new_submission = subreddit.new(limit=50)  # sort post by new, get latest 50, 1st post = oldest in new
    return subreddit_new_submission


def run_bot(string_for_search):
    subreddit_new_submission = bot_set('python') # 'sub_name'

    for submission in subreddit_new_submission:
        if not submission.saved:
            submission.save()  # save to bot's profile/save
            if re.search(string_for_search, submission.title, re.IGNORECASE):
                subject = 'sub  ' + submission.title[0:30]
                reddit.redditor('master_account_name').message(subject, submission.url)

            submission.comments.replace_more()

            for comment in submission.comments.list():
                if not comment.saved:
                    comment.save()
                    if re.search(string_for_search, comment.body, re.IGNORECASE):
                        subject = 'comm   ' + comment.body[0:30]
                        reddit.redditor('master_account_name').message(subject, comment.permalink)


while True:
    run_bot('python project') # change string b/w '' for different search input 
