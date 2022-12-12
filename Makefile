.DEFAULT_GOAL := build
SHELL := /bin/bash
MAKEFILE := $(abspath $(lastword $(MAKEFILE_LIST)))

ROOT_DIR ?= $(patsubst %/,%,$(dir $(MAKEFILE)))
SRC_DIR := $(ROOT_DIR)/src

HOST_ROOT_DIR ?= $(ROOT_DIR)
HOST_SRC_DIR := $(HOST_ROOT_DIR)/$(notdir $(SRC_DIR))

DOCKER_SERVICE ?= app

MANAGE = python manage.py

TAG_LOCAL := latest

ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
$(eval $(ARGS):;@:)


.PHONY: bash
bash:
	@docker-compose run --rm --workdir=/app --entrypoint=bash $(DOCKER_SERVICE) || true


.PHONY: reset
reset:
	docker-compose down -v
	docker-compose up -d $(DOCKER_SERVICE)
	make docker:dummydata


.PHONY: manage
manage: wait-for-services
	@cd $(SRC_DIR); \
	$(MANAGE) $(manage)


.PHONY: runserver
runserver: wait-for-services
	@cd $(SRC_DIR); \
	python manage.py runserver 0.0.0.0:8000


.PHONY: shell  # Starts a python django shell
shell:
	@cd $(SRC_DIR) && \
	python manage.py shell


.PHONY: attach  # Attaches to running service container
attach:
	docker attach --detach-keys="ctrl-d" `docker-compose ps -q $(DOCKER_SERVICE)`


TRANSLATION_MANAGE := manage.py makemessages --no-obsolete --no-location -l sv

.PHONY: translations
translations:
	@cd $(SRC_DIR) && \
	python $(TRANSLATION_MANAGE)

.PHONY: check-translations
check-translations:
	@cd $(SRC_DIR); \
	old="$$(cat locale/*/LC_MESSAGES/django.po | grep -v 'POT-Creation-Date' | sha256sum)"; \
	python $(TRANSLATION_MANAGE); \
	new="$$(cat locale/*/LC_MESSAGES/django.po | grep -v 'POT-Creation-Date' | sha256sum)"; \
	if [ "$$old" = "$$new" ]; then \
		printf 'Up to date!\n'; \
	else \
		printf 'Translation files are out of date!\nYou might want to run `make docker:translations` and commit the updated PO files.\n'; \
		exit 1; \
	fi

.PHONY: check-migrations
check-migrations:
	@cd $(SRC_DIR); \
	python manage.py makemigrations -n 'empty' --check --dry-run


.PHONY: wait-for-database
wait-for-database:
	@wait-for-it -t 60 database:5432

.PHONY: wait-for-services
wait-for-services: wait-for-database


########################################################################################
#
#   DOCKER WRAPPER
#
########################################################################################

#| docker-compose proxy function running this Makefile within
#| a service container with given target, args and options.
#|
#| Usage: $(call docker,<make-target>,<target-args>)
#| Example: $(call docker,test,foo.tests)
define docker
	@docker-compose run \
		--rm \
		--user="root" \
		--workdir="/backend" \
		--entrypoint="make" \
		$$(if [ "$1" = "runserver" ]; then echo --service-ports; fi) \
		$(DOCKER_SERVICE) \
		-e HOST_ROOT_DIR="$(ROOT_DIR)" \
		$(if $(2),-e $(1)="$(2)") \
		$(1)
endef

#| Evaluate all "proxy" targets given on command line as real targets
#| which when invoked runs a mandatory defined proxy function with
#| the sub target, argument and options as function parameters.
#|
#| Usage:
#|   make <proxy>:<target>
#|   make <proxy>:<target>:<arg>
#|   make <proxy>:<target>:<arg> <target>="<options>"
#|
#| Example:
#|   make docker:test
#|   make docker:test:foo
#|   make docker:test:foo.tests test="--failfast"
#|
#| Last example will result in the following function call:
#|   $(call docker,test,--failfast foo.tests)

PROXY_DELIMITER := :
PROXY_DEBUG ?=
PROXY_TARGETS := $(foreach t,$(MAKECMDGOALS),$(if $(findstring $(PROXY_DELIMITER),$(t)),$(t)))

define create-proxy-target
.PHONY: $(subst $(PROXY_DELIMITER),\$(PROXY_DELIMITER),$(1))
$(subst $(PROXY_DELIMITER),\$(PROXY_DELIMITER),$(1)): PROXY := $(wordlist 1,1,$(subst $(PROXY_DELIMITER), ,$(1)))
$(subst $(PROXY_DELIMITER),\$(PROXY_DELIMITER),$(1)): TARGET := $(wordlist 2,2,$(subst $(PROXY_DELIMITER), ,$(1)))
$(subst $(PROXY_DELIMITER),\$(PROXY_DELIMITER),$(1)): ARGS := $(strip ${$(wordlist 2,2,$(subst $(PROXY_DELIMITER), ,$(1)))} $(wordlist 3,3,$(subst $(PROXY_DELIMITER), ,$(1))))
$(subst $(PROXY_DELIMITER),\$(PROXY_DELIMITER),$(1)):
	$(if $(PROXY_DEBUG),$$(info Calling proxy "$$(PROXY)" with $$$$(1)="$$(TARGET)" $$(if $$(ARGS),$$$$(2)="$$(ARGS)")))
	$$(call $$(PROXY),$$(TARGET),$$(ARGS))
endef

$(foreach t,$(PROXY_TARGETS),$(eval $(call create-proxy-target,$(t))))
