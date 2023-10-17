"""
source venv/bin/activate
pip install PyGithub
"""
import argparse
import sys
from github import Github, Auth
import os
import time

parser = argparse.ArgumentParser(description="Retrieve public repos given GH username")
parser.add_argument("user", type=str, help="GitHub username")
parser.add_argument("--token", type=str, default=None, 
                    help="GitHub access token. Optional but strongly recommended!")
parser.add_argument("--repo", type=str, default=None, help="optional, retrieve specific repo")
parser.add_argument("-o", "--outdir", type=str, default=sys.path[0], 
                    help="option, directory to write Markdown files. Defaults to directory "
                         "from which user launched this script.")
parser.add_argument("--overwrite", action="store_true", 
                    help="option, if set then script will overwrite any pre-existing "
                         "files with the same path and basename.")
args = parser.parse_args()

if args.token:
    auth = Auth.Token(args.token)
else:
    auth = Auth.Token()  # public access is rate limited

github = Github(auth=auth)
user = github.get_user(args.user)
if args.repo:
    pass
else:
    repos = user.get_repos()  # public only
    for repo in repos:
        # gather metadata
        cdate = repo.created_at.date()
        owner, repo_name = repo.full_name.split('/')
        print(repo_name)
        authors = [c.login for c in repo.get_contributors()]
        try:
            readme = repo.get_readme().decoded_content.decode()
        except:
            readme = None
        license = repo.license
        if license is not None:
            license = license.name

        # write markdown
        ofn = os.path.join(args.outdir, f"{cdate.isoformat()}-{repo_name}.md")
        if os.path.exists(ofn) and not args.overwrite:
            print(f"File {ofn} already exists, skipping this entry! (Set --overwrite to bypass.)")
            continue

        outfile = open(ofn, 'w')
        outfile.write("---\nlayout: software\n")
        outfile.write(f"title: {repo_name}\n")
        outfile.write(f"year: {cdate.year}\n")
        outfile.write(f"authors: {authors}\n")
        outfile.write(f"github: {repo.html_url}\n")
        outfile.write(f"license: {repo.license}\n")
        outfile.write(f"description: \"{repo.description}\"\n")
        outfile.write(f"forks: {repo.forks_count}\n")
        outfile.write(f"stars: {repo.stargazers_count}\n")
        outfile.write(f"image: /assets/images/Default_software.png\n---\n\n")

        if readme:
            outfile.write(readme)
        outfile.close()

        time.sleep(1)  # seconds, avoid triggering rate limiter

github.close()
