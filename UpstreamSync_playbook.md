# Upstream Sync Playbook

This repo is a fork of [datahub](https://github.com/acryldata/datahub). There are a few actions added to help with keeping this repo up to date with changes from the upstream repo.

## Actions

### fork-upstream-sync.yml

This action runs every night and pulls all changes from the master branch of upstream and pushes them to the `upstream-mirror` branch. This is a clean, untouched copy of the upstream.

### fork-upstream-sync-pr.yml

This action runs once a week (Monday 12:30 am). It checks to see if a PR is already open (uses `label:upstream-sync`):

- PR does not exist — makes a new PR with the label; the PR targets the `intermediate-sync` branch mentioned below.
- PR hasn't had any changes pushed to it — pulls in new changes from the nightly sync.
- PR exists and has new changes — updates the PR description but doesn't update the branch.

### fork-intermediate-sync.yml

This action runs once changes are pushed to `develop` and keeps the `intermediate-sync` branch up to date with `develop`.

### fork-intermediate-merge.yml

This action runs when the PR branch (from the sync) is merged into the `intermediate-sync` branch. It merges `intermediate-sync` into `develop` (note: this is a merge, not a rebase, so all commits are kept).

## Sync process

### Merging

The first thing to do is to find the PR created by the actions above. These will be named something like `Sync upstream datahub changes - 2026-02-24`.

It's possible that one does not exist; this should only happen if one has already been merged this week. If that's the case, you can locate and run the `Fork - Create Upstream Sync PR` action.

Once you've located that PR, get the branch name (something like `sync/upstream-mirror-pr-22351868093`) and run the following in your local clone of the [repo](https://github.com/National-Digital-Twin/ndt-data-catalogue.git):

```sh
git fetch
git checkout sync/upstream-mirror-pr-22351868093 # <-- change name to match the PR branch name
```

> [!IMPORTANT]
> You **MUST** merge the `develop` branch into the PR branch before doing anything else. The PR branch is a snapshot of the `upstream-mirror` branch, which is a clean copy of the DataHub fork's default branch. We need to merge in any changes that have happened in our fork since the last sync to avoid losing work.

```sh
git fetch
git merge origin/develop --no-ff
```

You will now need to fix up merge conflicts. Do this in your chosen way — I use VS Code to resolve the conflicts, then `git commit` to finalise the merge.

Often these conflicts arise from new imports being added upstream as well as us adding a licence header, so you just need to ensure the header comes first and then add/alter the import. (Most of the time, accepting the merged (local-first) version is enough to resolve them.)

### Licence Headers

Once the merge is complete the next step is to find and add files that need licence headers, run the following:

``` bash
docker run --rm -v "$PWD":/work -w /work apache/skywalking-eyes:latest header check -c .licenserc.yaml | tee /tmp/skywalkingeyes-output.txt
```

If you see results, run the following to patch those up:

``` bash
python licence-header-utils/src/license_header_migration/migrate.py --file-list /tmp/skywalkingeyes-output.txt
```

Now do the same for any documentation files:

``` bash
docker run --rm -v "$PWD":/work -w /work apache/skywalking-eyes:latest header check -c .licenserc-markdown.yaml | tee /tmp/skywalkingeyes-output.txt
```

And again, if you see any results:

``` bash
python licence-header-utils/src/license_header_migration/migrate.py --file-list /tmp/skywalkingeyes-output.txt
```

Once done (and you've checked that the files now have the correct licence headers):

```bash
git commit -s -S -m 'chore: adding licence headers' #<-- or something similar
```

As a merge has happened, you will need to force-push your changes:

```bash
git push --force-with-lease origin sync/upstream-mirror-pr-22351868093 #<-- use correct branch name here
```
