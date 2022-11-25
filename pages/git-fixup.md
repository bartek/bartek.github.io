title: Refining my git workflow with --fixup
date: 11-25-2022
---

One of the simplest pleasures of git is it's intuitive enough to use and
get right at the most primitive level within only a few commit cycles. The other
pleasures come from learning small tricks which build upon past experience and
level up your workflow. 

Early in my git career, one of the most helpful features to improve flow was
rebasing. Of course, I was no stranger to *rebase hell* when main was being
rebased onto a feature branch, but I commonly found myself using `git rebase [-i
| --interactive ]` as a means of fixing up, squashing, and deleting commits.
This allowed me to commit earlier, more often, and not worry about quality until
I had reached my goal.

My initial usage of fixup and squash is perhaps typical, but what I would
consider messy. Taking a commit log, which has not yet been pushed for review:

    pick 3f0d667 scratch work
    pick 6add648 added component A
    pick 8558c32 added component B
    pick 655324d wired things up
    pick 7a9c1ce added tests

There was no guarantee each individual commit would build or tests pass. If I
made a mistake in commit `3f0d667`, it would be resolved in a followup scrappy
commit. Everything would eventually squash into a single commit, so I had little
concern for quality of commits. When the work was complete, I'd rebase. It
consistently looked like so:

    reword 3f0d667 scratch work
    fixup 6add648 added component A
    fixup 8558c32 added component B
    fixup 655324d wired things up
    fixup 7a9c1ce added tests

Essentially, squashing all commits into a single one and opening my editor to
rewrite the previously scrappy commit into something more material. It was at
this point I expected the project to build, all tests to pass, and for the code
to be submitted for review.

By the book, this isn't optimal, or even correct usage of git. It did enable a
workflow that was otherwise sufficient for delivering code but it's important to
regularly challenge your understanding and improve.

## A better commit story with --fixup

In the described workflow, my output resulted in feature branches which
generally contained a single commit, and I had abstained from creating PRs which
go beyond a particular cognitive load. If I wanted to tell a broader story,
I'd chain multiple PRs and branch off branches until the story was complete. It
was workable but uh, challenging at times (rebase hell, anyone?)

Rigid would be one way to describe this workflow. A single PR could not tell a
broader story unless I jumped through the aforementioned hoops. I was producing
what I felt were quality commits, but as time went on, I felt my process
restrictive. Plus, I was getting tired of branching off branches and keeping
those organized in the review window.

And then one day, I was introduced to `--fixup`! It's succinctly documented in
the git manual:

     --fixup=<commit>
       Construct a commit message for use with rebase --autosquash. The commit
       message will be the subject line from the specified commit with a prefix
       of "fixup! ". See git-rebase(1) for details.

This made me realize my previous mistakes. Before, I wasn't using fixup
optimally! It was more akin to a means of squashing all commits into one but
the benefit comes in being able to *target* a specific commit and well, fix
it up! 

So I began to adapt my workflow. Scrappy commits and experimental branches
continued to exist and once I made it past this phase I began to construct my
feature branch with the following principles:

1. Aim to deliver the branch with a series of well written commits. A broad set
   of rules continue to exist here, which are beyond the scope of this post.
2. Each individual commit should not go beyond a particular threshold for
   cognitive load.
3. Each commit should build, tests pass, and ultimately, be reversible.
4. Use `--fixup` when I've realized a mistake was made in a previous commit, and
   let git handle the work of cleaning things up!

I now had more optionality in how I wanted to structure my feature branches and
eventual Pull Requests. I had to be more deliberate in how I produced work, but
I also had to worry less about making a mistake in a particular commit. If a
test was missed, a logical mistake made, or there was a simple linting issue, I
could `--fixup` the particular commit and not worry about a messy branch for
eventual review.

Now, when I was preparing a branch for review, my commit log may initially look
like so:

    3f0d667 Introduce Component A
    6add648 Introduce Component B
    8558c32 Wire Up Components

A couple things to resolve, I could target specific commits for fixup:

    git commit --fixup=3f0d667 fixup! Introduce Component A
    git commit --fixup=8558c32 fixup! Wire Up Components


git log then looked like so:

    3f0d667 Introduce Component A
    6add648 Introduce Component B
    8558c32 Wire Up Components
    655324d fixup! Introduce Component A
    7a9c1ce fixup! Wire Up Components

Prior to pushing to an origin for review, I would then rebase `git rebase
--autosquash HEAD~5`. The fixups would be auto-squashed locally by git and I
push a feature branch with three commits. I now have a branch with 3 buildable
commits.

In my Pull Request, I may provide a broader story. In this example about new
components and wiring things up, I may include a simple architectural diagram (I
like [Monodraw](https://monodraw.helftone.com/) for this). I use the PR as a
means of explaining the connections and edges, and each individual commit is
focused on its own particulars.

Reviewers now get a variety of context. The broader story can be important for
building context or allowing reviewers to think beyond the scope of the PR
(*What happens when we introduce Component C?*). Conversely, reviewers may also
hone-in on a particular commit and not concern themselves with the broader
picture.

Of course, maintaining a size threshold for PRs is important, but I'm not too
concerned about the idea of small PRs either. Those reviewing my code may be
comfortable with the introduced Component A & B, but may not be sure about how
I've wired things up. The reviewers could step through those commits and
conditionally approve the PR in that the first two commits could be merged.

Since the commits are clean, buildable, and have passing tests, I could merge
those and leave a feature branch up containing the final *wire up* commit for
later review, after we've had our architectural discussion.

And we can see the optionality described. The rigidness in my previous workflow
has mostly been removed. I can push small feature branches, or larger branches,
and my reviewers have optionality in how they approve and support merger of
code. As a writer of code, I worry less about crafting the perfect, single
commit, because I know I can `--fixup` later. As a team, we build confidence
because we gain more context in a single PR and don't worry about juggling
context between multiple Pull Requests which attempt to tell the story.

The beauty of the described is there's few noticeable differences in the prior
and current, much of it hidden behind the nuance of a refined workflow enabled
by how beautifully git has been crafted. A great piece of software with a
minimum barrier to entry which continues to teach over the years I invest into
it. Lately, I've been refining how I use another new discovery, `git worktree`,
and I'll dedicate a followup post on how my workflow has been further refined.
