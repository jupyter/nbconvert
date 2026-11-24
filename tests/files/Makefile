DIST := dist
FLAGS := -output-directory=$(DIST)
MAIN := notebook6_physics_chemistry
#MAIN := notebook1

.DEFAULT_GOAL := help
.PHONY: help configure build clean
.SILENT: help

help: ## Show this help
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m      %s\n", $$1, $$2}'

installdir: ## setup for building
	mkdir -p $(DIST)

# https://nbconvert.readthedocs.io/en/latest/usage.html#convert-latex
pdf: $(MAIN).ipynb ## build the pdf files
	pdm run jupyter nbconvert --to pdf --output-dir=$(DIST) $<  \
		--LatexPreprocessor.title "NB Convert" \
		--LatexPreprocessor.author_names $(shell whoami) \
		--LatexPreprocessor.date $(shell date --iso)

open: $(DIST)/$(MAIN).pdf ## open the document
ifeq ($(shell uname), Darwin)
	open $<
else
	xdg-open $<
endif
	@echo $(UNAME)

clean: ## clean the build intermediate files
	$(RM) $(DIST)/*.aux $(DIST)/*.log $(DIST)/*.dvi $(DIST)/*.pdf
