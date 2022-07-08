SHELL = /bin/bash
package = shagen/csaf-lint

.PHONY: all available
all:
	@echo "usage: "
	@echo "       make clean - removes output files"

clean:
	@echo "- removing output files"
	@rm -f *.log
