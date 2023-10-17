---
layout: software
title: clustuneR
year: 2019
authors: ConnorChato, ArtPoon
github: https://github.com/PoonLab/clustuneR
license: License(name="GNU General Public License v3.0")
description: "Implementing clustering algorithms on genetic data and finding optimal parameters through the performance of predictive growth models."
forks: 0
stars: 0
image: /assets/images/Default_software.png
---

# clustuneR

### Implementing clustering algorithms on genetic data and finding optimal parameters through the performance of predictive growth models.

clustuneR builds clusters from inputted sequence alignments and/or
phylogenetic trees, allowing users to choose between multiple
cluster-building algorithms implemented in the package. These algorithms
can be further augmented through the selection of parameters, such as a
required similarity for cluster formation, or a required level of
certainty. The package also takes in meta-data associated with sequences
such as a known collection date or subtype/variant classification. These
can also allow users to identify cluster-level characteristics, such as
the range of collection dates or the most common subtype/variant within
a cluster.

If a subset of sequences are specified as “New”, then clustuneR
simulates cluster growth by building clusters in two stages: first
clusters are built from sequences which are not specified as new, then
the new sequences are added to clusters. Depending on the clustering
method used, this second step may include compromises to insure that new
sequences do not retroactively change the membership of clusters. For
example, if a single new sequence forms a cluster with two, previously
separate clusters, then those two clusters would have ambiguous growth.
Pairing cluster-level meta-data, with the growth of clusters is a common
goal in research and clustuneR contains some functions to help test
predictive models based on cluster data. Furthermore, clustuneR
facilitates the assignment of multiple cluster sets from the same data
using different methods and parameters. Pairing these with the
effectiveness of growth models can be useful in method/parameter
selection.

## Installation

> Because clustuneR uses [pplacer](https://github.com/matsen/pplacer/)
> to graft new sequences onto a phylogenetic tree, it can currently only
> be run on Linux systems.

If you have the [`git`](https://git-scm.com/) version control system
installed on your computer, you can clone the repository by navigating
to a location of your filesystem where the package will be copied, and
then running

    git clone https://github.com/PoonLab/clustuneR.git 

If you do not have `git` installed, then you can download the most
recent (developmental version) package as a ZIP archive at this link:
<https://github.com/PoonLab/clustuneR/archive/refs/heads/master.zip>

or from the Releases page:
<https://github.com/PoonLab/clustuneR/releases>

If you have downloaded a `.zip` or `.tar.gz` archive, you can use
`unzip` or `tar -zvxf` on the command line, or double-click on the
archive file in your desktop environment.

Use `cd clustuneR` to enter the package directory and run the following
command to install the package into R:

    R CMD INSTALL .

You should see something like this on your console:

    * installing to library ‘/Library/Frameworks/R.framework/Versions/4.0/Resources/library’
    * installing *source* package ‘clustuneR’ ...
    ** using staged installation
    ** R
    ** data
    *** moving datasets to lazyload DB
    ** inst
    ** byte-compile and prepare package for lazy loading
    ** help
    *** installing help indices
    ** building package indices
    ** testing if installed package can be loaded from temporary location
    ** testing if installed package can be loaded from final location
    ** testing if installed package keeps a record of temporary installation path
    * DONE (clustuneR)

## Usage example

### Building a tree

We start with a multiple sequence alignment of sequences that are
labelled with sample collection dates. An example of anonymized public
domain HIV-1 sequences from a study based in northern Alberta (Canada)
is provided in `data/na.fasta`. First, we use an R script to exclude the
sequences collected in the most recent year:

``` r
require(clustuneR)
require(ape)
require(lubridate)

setwd("~/git/clustuneR")
seqs <- ape::read.FASTA("data/na.fasta", type="DNA")

# parse sequence headers (alternatively import from another file)
seq.info <- pull.headers(seqs, sep="_", var.names=c('accession', 'coldate', 'subtype'),
var.transformations=c(as.character, as.Date, as.factor))

max.year <- max(year(seq.info$coldate))
old.seqs <- seqs[year(seq.info$coldate) < max.year]
write.FASTA(old.seqs, file="data/na-old.fasta")
```

Next, we use IQ-TREE to reconstruct a maximum likelihood tree relating
the “old” sequences:

``` console
iqtree -bb 1000 -m GTR -nstop 200 -s na-old.fasta
```

Note we’ve specified the generalized time reversible model of nucleotide
substitution to bypass the model selection stage. Even so, this is a
time-consuming step - to speed things up, we’ve provided IQ-TREE output
files at `data/na.nwk` and `data/na.log`.

### Grafting new sequences

Next, we import both the sequence alignment and the ML tree into R. We
will use `clustuneR` to graft the sequences from the most recent year
using the program `pplacer` and the output files from IQ-TREE.

``` r
phy <- ape::read.tree("data/na.nwk")

# use pplacer to graft new sequences onto old tree
phy.extend <- extend.tree(phy, seq.info, seqs, mc.cores=4, log.file="data/na.log")
```

### Finding the optimal threshold

Next, we want to configure `clustuneR` to fit two Poisson regression
models to the distribution of new cases among clusters, for a range of
genetic distance thresholds:

``` r
# generate cluster sets under varying parameter settings
param.list <- lapply(seq(0.001, 0.04, 0.001), function(x) list(t=phy.extend, branch.thresh=x, boot.thresh=0.95))
cluster.sets <- multi.cluster(step.cluster, param.list) 

# configure Poisson regression models
p.models = list(
    "NullModel" = function(x){
        glm(Growth~Size, data=x, family="poisson")
    },
    "TimeModel" = function(x){
        glm(Growth~Size+coldate, data=x, family="poisson")
    }
)
p.trans = list(  # average sample collection dates across nodes in each cluster
    "coldate" = function(x){mean(x)}
)

res <- fit.analysis(cluster.sets, predictive.models=p.models, 
                    predictor.transformations=p.trans)
AICs <- get.AIC(res)
delta.AIC <- AICs$TimeModelAIC - AICs$NullModelAIC
```

We can visualize the difference in AICs between models as a function of
the distance threshold:

``` r
cutoffs <- sapply(param.list, function(x) x$branch.thresh)
par(mar=c(5,5,1,1))
plot(cutoffs, delta.AIC, type='l', col='cadetblue', lwd=2)
abline(h=0, lty=2)
```

![](README_files/figure-gfm/unnamed-chunk-4-1.png)<!-- -->

### Explanation

The optimal distance threshold is associated with the lowest value of
`delta.AIC`. We expect that adding information on sample collection
dates should improve our ability to predict where the next infections
will occur. However, this improvement will depend on how we have
partitioned the database of known infections into clusters. If every
known infection is merged into a single giant cluster, then there is no
meaningful way to predict where new cases will occur, since there is no
variation for a sample of one cluster. If every infection each becomes a
cluster of one, then there will be excessive information loss due to
random variation in sampling dates. At the threshold that minimizes
`delta.AIC`, the known infections are partitioned into clusters in such
a way that minimizes the information loss associated with incorporating
sample dates into the predictive model.

## References

This package includes the binaries for pplacer and guppy
(<https://matsen.fhcrc.org/pplacer>, released under the GPLv3 license),
which are used to add new tips onto a fixed tree to simulate cluster
growth prospectively.

-   Matsen FA, Kodner RB, Armbrust EV. pplacer: linear time
    maximum-likelihood and Bayesian phylogenetic placement of sequences
    onto a fixed reference tree. BMC bioinformatics. 2010 Dec;11(1):1-6.

As an example, this package includes a subset of a larger published
HIV-1 *pol* sequence data set. These sequences were originally published
in a study by Vrancken *et al.* (2017) and publicly accessible in the
GenBank database under the PopSet accession `1033910942`.

-   Benson DA, Karsch-Mizrachi I, Lipman DJ, Ostell J, Rapp BA,
    Wheeler DL. GenBank. Nucleic acids research. 2000 Jan 1;28(1):15-8.

-   Vrancken B, Adachi D, Benedet M, Singh A, Read R, Shafran S, Taylor
    GD, Simmonds K, Sikora C, Lemey P, Charlton CL. The multi-faceted
    dynamics of HIV-1 transmission in Northern Alberta: A combined
    analysis of virus genetic and public health data. Infection,
    Genetics and Evolution. 2017 Aug 1;52:100-5.
