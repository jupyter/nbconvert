# Making an NBConvert Release

## Using `jupyter_releaser`

The recommended way to make a release is to use [`jupyter_releaser`](https://github.com/jupyter-server/jupyter_releaser) from this repository.

- Run the "Step 1: Prep Release" workflow with the appropriate inputs.
- Review the changelog in the draft GitHub release created in Step 1.
- Run the "Step 2: Publish Release" workflow to finalize the release.

## Manual Release

To create a manual release, perform the following steps:

### Set up

```bash
pip install pipx
git pull origin $(git branch --show-current)
git clean -dffx
```

### Update the version and apply the tag

```bash
echo "Enter new version"
read new_version
pipx run hatch version ${new_version}
git tag -a ${new_version} -m "Release ${new_version}"
```

### Build the artifacts

```bash
rm -rf dist
pipx run build .
```

### Publish the artifacts to pypi

```bash
pipx run twine check dist/*
pipx run twine upload dist/*
```
