#!/bin/bash

version=3.6.5
echo "=== Downloading webgraph..." && curl -#LO http://webgraph.di.unimi.it/webgraph-${version}-bin.tar.gz
echo "=== Downloading dependencies..." &&curl -#LO http://webgraph.di.unimi.it/webgraph-deps.tar.gz
rm -rf jars && mkdir jars
echo "=== Extracting webgraph..."
tar --strip-components 1 -C jars -xvf webgraph-${version}-bin.tar.gz webgraph-${version}/webgraph-${version}.jar
echo "=== Extracting dependencies..."
tar -C jars -xvf webgraph-deps.tar.gz