subway-line-sets
================

A simple tool for generating subway-style line sets

[Live deployment](https://alex-r-bigelow.github.io/subway-line-sets)

Installation
============
1) Install node.js

To install with `nvm` (there are other ways, but this has some advantages):
```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
command -v nvm
nvm install node
```

2) Install this repo + its dependencies
```bash
git clone https://github.com/alex-r-bigelow/subway-line-sets.git
cd subway-line-sets
npm install
```

Running locally
===============
```bash
npm run serve
```

Deploying
=========
For now, pushing to master is all you should need to do; github pages takes it from there