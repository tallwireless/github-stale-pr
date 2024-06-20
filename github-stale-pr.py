from github import Auth
from github import Github
from os import environ
import arrow

env = dict(environ)

exclude_labels = env["INPUT_EXCLUDELABELS"].split(",")
exclude_labels = [x.lower() for x in exclude_labels]
ignore_drafts = bool(env["INPUT_IGNOREDRAFTS"])
required_label = env["INPUT_REQUIREDLABELS"].split(",")
days = int(env["INPUT_DAYS_SINCE_CREATED"])


handle = Github(auth=Auth.Token(env["INPUT_GITHUB_TOKEN"]))
repo = handle.get_repo(env["GITHUB_REPOSITORY"])

pull_requests = []

output = []
for pr in repo.get_pulls():
    if ignore_drafts and pr.draft:
        continue

    label_list = [str(x.name).lower() for x in pr.labels]
    label_exit = False
    for label in label_list:
        if label in exclude_labels:
            label_exit = True
            break
    if label_exit:
        continue
    date = pr.created_at
    if pr.last_modified_datetime is not None:
        date = pr.last_modified_datetime
    delta = arrow.utcnow() - arrow.get(date)
    if delta.days >= days:
        pull_requests.append(pr)
        name = pr.user.login
        if pr.user.name is not None:
            name = f"{pr.user.name} ({pr.user.login})"
        output.append(
            f"<{pr.html_url}|{pr.title}> opened by {name} untouched in {delta.days} days."
        )


output_str = "\n".join(output)
fout = open(env["GITHUB_OUTPUT"], "a")
fout.write(f'message="{output_str}"')
