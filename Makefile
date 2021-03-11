.PHONY: all
all: ; $(info $$var is [${var}])echo Hello world
	@echo "usage: "
	@echo "       make clean - removes output files"
	@echo "       make image - builds container image"
clean:
	@rm -f *.log
image: SHELL:=/bin/bash
image:
	set -e ;\
	RND_SEED=$$(openssl rand -base64 48) ;\
	BUILD_TS=$$(date +'%Y-%m-%dT%H:%M:%SZ') ;\
	REVISION=$$(git rev-parse --verify HEAD) ;\
	VERSION=$$(grep version setup.py | cut -f2 -d'"') ;\
	echo $$RND_SEED $$BUILD_TS ;\
	docker build \
	--build-arg BUILD_TS=$$BUILD_TS \
	--build-arg REVISION=$$REVISION \
	--build-arg VERSION=$$VERSION \
	--tag shagen/csaf-lint . ;\
