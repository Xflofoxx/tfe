#!/usr/bin/env bash
echo "Creating starter at ./starter-generated" 
mkdir -p starter-generated
rsync -a --delete starter/template/ starter-generated/
echo "Starter skeleton copied to ./starter-generated/" 
