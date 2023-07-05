# How to


# Docs

```
# to fix generated file for editing do sudo chmod -R 777 docs/*

docker-compose -f docs/docker-compose.yml build

# clean
# sudo rm -rd docs/build

# generate terraform doc
# sudo rm infrastructure/terraform/backend/DOC-Terraform.md
# sudo rm infrastructure/terraform/frontend/DOC-Terraform.md
docker-compose -f docs/docker-compose.yml run sphinx terraform-docs markdown table --output-file DOC-Terraform.md --output-mode inject ../infrastructure/terraform/frontend/
docker-compose -f docs/docker-compose.yml run sphinx terraform-docs markdown table --output-file DOC-Terraform.md --output-mode inject ../infrastructure/terraform/backend/

# generate backend code doc
# sudo rm -rf docs/source/code
docker-compose -f docs/docker-compose.yml run sphinx sphinx-apidoc -o source/code ../backend

# generate db doc
# sudo rm -rf docs/source/_static/db.png
docker-compose -f docs/docker-compose.yml run sphinx ../backend/manage.py graph_models --pydot -a -g -o source/_static/db.png

# generate statics and run server
docker-compose -f docs/docker-compose.yml run sphinx make html
docker-compose -f docs/docker-compose.yml up
# open browser at localhost:9001
```