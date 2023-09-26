# Medical Bioinformatics @ Western research website

Clone the repo with:
```
git clone --recurse-submodules https://github.com/western-bioinfo/western-bioinfo.github.io.git
```

# Build site using Docker

Highly recommended esp for Apple M1/M2 users

```
docker build -t medbioinfo-uwo-website .
docker run -p 4000:4000 medbioinfo-uwo-website

```
When you are finished and no longer need the container, you can stop it by pressing Ctrl+C in the terminal where it is running.

Then, remove the stopped container using `docker rm <container_id_or_name>`. You can find the container's ID or name by running `docker ps -a`, which lists all containers, including stopped ones.

By removing the container when you're done, you free up system resources and keep your Docker environment clean. If you need to run the container again later, you can simply use the docker run command again.

Remember that the Docker image you built (my-jekyll-website) will still exist on your system even after removing the container. You can list all Docker images with `docker images` and remove them using `docker rmi <image_id_or_name>` if you no longer need them.

To run old image, simply run 
`docker run -p 4000:4000 medbioinfo-uwo-website`
To build new image run `docker build` first.

## Build site locally

Then install necessary Ruby dependencies by running:
```
bundle install
```
from within the `western-bioinfo.github.io` directory.

If you do not have root permissions you may need to run:
```
bundle install --path vendor/bundle
```

After this, the site can be be built with:
```
bundle exec jekyll build
```

(If you are getting errors at this stage, it may be due to your version of `bundle`. Try `gem uninstall bundler` + `gem install bundler -v 1.13.1`.)
To view the site, run `bundle exec jekyll serve` and point a browser to `http://localhost:4000/`. More information on Jekyll can be found [here](http://jekyllrb.com/).

To include projects, preprocessing scripts are necessary to clone project repos and update Jekyll metadata. This can be accomplished with:
```
bundle exec ruby _scripts/update-and-preprocess.rb
```

> Note that you need to create a .netrc file to allow the ruby script to pull data using the github api.

Then `bundle exec jekyll build` works as normal.

In short, running `bundle install && bundle exec ruby _scripts/update-and-preprocess.rb && bundle exec jekyll build && bundle exec jekyll serve` will do everything you need.

## Updating

The website is built using Travis, with builds triggered for each commit. If you commit your changes to a branch and do a pull request, Travis will build your branch and you will be able to check your changes build correctly before going live. Commit your changes to master and they will go live in a few minutes.

## Contribute

Blog posts just require YAML top matter that looks something like:
```
---
layout: post
title: Newton Institute presentation
author_handle: Trevor Bedford
link: http://www.newton.ac.uk/programmes/IDD/seminars/2013082213301.html
image: /images/blog/transmission.png
---
```

The `layout`, `title` and `author_handle` tags are required, while `link` and `image` tags are optional. Just save a Markdown file with this top matter as something like `blog/_posts/2013-08-27-newton-institute.md`, where `2013-08-27` is the date of the post and `newton-institute` is the short title. The `author_handle` tag on the blog post must match the `handle` tag in the `.md` file of the team member authoring the post (team member `.md` files can be found in `team/_posts`). This short title is used in the URL of the post, so this becomes `blog/newton-institute/`, so the short title should be long enough and unique enough not to cause conflicts with other posts.

If you are making your faculty profile for the first time, the easiest approach is to copy one of the existing Markdown files in `faculty/_posts` and modifying the YAML header with your personal information, *e.g.*, name, GitHub username.  You can add any Markdown or HTML below the YAML, which will be rendered on your profile page.

## Adding a new publication

There are some Ruby scripts for retrieving papers from PubMed and using this information to automatically generate Markdown posts:

1. Open `_scripts/fetch_pubmed-xml.rb` in a text editor and modify the line `AUTHOR_NAME` with a PubMed author query, *e.g.*, `Surname I[Author]`.  (It is probably a good idea to run this query with the PubMed web interface first, to make sure that you are retrieving the right papers.)
2. Execute the ruby script `_scripts/fetch-pubmed-xml.rb`.  This will update the `xml` file at `assets/pubmed_result.xml`.
3. Execute the ruby script `_scripts/add-papers.rb`.  This will add new Markdown documents at `papers/_posts` for example `2019-7-18-31312429.md`.
4. Download the PDF, rename and place into the assets directory:
    e.g.: ./assets/pdfs/papers/31312429.pdf
5. Create a image for the paper, preferably a square .png file, name and place:
    e.g.: ./assets/images/papers/31312429.png
6. Finally, make sure it appears on the website when the site is hosted locally (use `bundle exec jekyll build && bundle exec jekyll serve` to host a local server).
7. If the local server's website looks okay, commit your changes and push to production

## For more information

* How to add [papers](https://github.com/shahcompbio/shahwebsite)
* Look over the [metadata format guide](http://bedford.io/guide/format/)
* Look over the [Markdown style guide](http://bedford.io/guide/style/)


## License

All source code in this repository, consisting of files with extensions `.html`, `.css`, `.less`, `.rb` or `.js`, is freely available under an MIT license, unless otherwise noted within a file.

**The MIT License (MIT)**

Copyright (c) 2013-2016 Trevor Bedford

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
