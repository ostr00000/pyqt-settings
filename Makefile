MAIN_PACKAGE_NAME=pyqt_settings

UIC=pyuic5
RCC=pyrcc5

UI_DIR=src/ui
COMPILED_UI_DIR=lib/$(MAIN_PACKAGE_NAME)/ui
RESOURCES=src/resources.qrc
####################################

UI_FILES=$(wildcard $(UI_DIR)/*.ui)
COMPILED_UI_FILES=$(UI_FILES:$(UI_DIR)/%.ui=$(COMPILED_UI_DIR)/ui_%.py)
RESOURCES_SRC=$(shell grep '^ *<file' $(RESOURCES) | sed 's@</file>@@g;s@.*>@src/@g' | tr '\n' ' ')

all: ui resources
	@echo "Make all finished"


ui: $(COMPILED_UI_FILES)

$(COMPILED_UI_DIR)/ui_%.py : $(UI_DIR)/%.ui
	mkdir -p $(COMPILED_UI_DIR)
	$(UIC) $< --from-imports -o $@

resources: $(COMPILED_UI_DIR)/resources_rc.py

$(COMPILED_UI_DIR)/resources_rc.py: $(RESOURCES) $(RESOURCES_SRC)
	mkdir -p $(COMPILED_UI_DIR)
	echo 'from . import resources_rc' > $(COMPILED_UI_DIR)/__init__.py
	$(RCC) -o $(COMPILED_UI_DIR)/resources_rc.py  $<


.PHONY: all ui resources compile
