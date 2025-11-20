

class Repo:

    def __init__( self,
                  repo_name,
                  build: bool,
                  repo_url,
                  branch_name,
                  tags : list[str] ):
        '''
        repo_name: Name of the repo
        build: Whether to build the repo
        repo_url: URL of the repo
        branch_name: Name of the branch
        tags: List of tags
        '''
        self.repo_name = repo_name
        self.build = build
        self.repo_url = repo_url
        self.branch_name = branch_name
        self.tags = tags

    def __str__(self):
        return f"Repo:\n  - Name: {self.repo_name}\n  - Build: {self.build}\n  - Repo URL: {self.repo_url}\n  - Branch Name: {self.branch_name}"

class Profile:

    def __init__( self,
                  project_name : str,
                  repos : list[Repo] ):

        self.project_name = project_name
        self.repos = repos

    def __str__(self):
        return f"Profile Repos: {self.repos}"


