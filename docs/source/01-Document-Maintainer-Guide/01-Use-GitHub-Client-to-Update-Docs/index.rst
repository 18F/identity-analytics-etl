.. _use-github-client-to-update-docs:

Step by Step: Use GitHub Client to Update Docs
------------------------------------------------------------------------------

This guide **is for people that doesn't familiar with Git**. If you already a git user, just create a branch from master.

1. Download Github Client here and install it: https://desktop.github.com/
2. Login to your Github account from ``Menu`` -> ``Github Desktop`` -> ``Preference`` -> ``Sign In``
3. Make sure the ``identity-analytics-etl`` repo owner added you to the member list, so you have the access.
4. Clone the repository from ``Menu`` -> ``File`` -> ``Clone Repository``.
5. Switch ``Current Directory`` to ``identity-analytics-etl`` from the main interface.
6. Click ``Fetch Origin`` on the main interface to pull the latest code from Github. (You need to do this every time before creating a new branch in case the repo has been updated by someone else).
7. Click ``Current Branch`` on the main interface, switch to ``master`` branch. Make sure you are on ``master`` branch.
8. Type in a new branch name and click ``Create New Branch``, the naming convention is ``<your-name>/<purpose-of-this-branch>``, switch to the branch you just created.
9. Click ``Publish Branch``, this will publish your branch to cloud, which is identical to ``master`` at this moment, but cause you didn't change anything.
10. Apply doc / file change, writing docs, do the actual works. **Usually it is just adding new** ``.rst`` / ``.md`` file to ``identity-analytics-etl/docs/source``.
11. Select all changes you want to check in, add a summary, and click ``Commit to <your-branch-name>``. (**This will NOT apply any changes to the cloud repo, no worries**)
12. Once everything's ready, click ``Publish origin``, so all your work is available on Github for code review.
13. Start a ``Pull Request`` from <your-branch> to ``master`` on https://github.com/18F/identity-analytics-etl/pulls, write why you are doing this PR and how you solved it. And ask someone to reivew it.
14. Once it is approved, click ``Squash and Merge``, merge changes to master.
