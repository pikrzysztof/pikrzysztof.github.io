all: docs/benchmarks/nop/index.html docs/benchmarks/nop-ht/index.html docs/misc/enc/index.html

docs/benchmarks/nop/index.html: org/benchmarks/nop/index.org
	./orgexport.el $< $@

docs/misc/enc/index.html: org/misc/enc/index.org
	./orgexport.el $< $@
