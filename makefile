procs := watershed/ canny/

.PHONY: has_sample $(procs)

all: $(procs) | has_sample

has_sample:
	@if [ -z "$(sample)" ]; then \
		printf -- >&2 "sample image not specified (make sample=<img>)\n"; \
		false; \
	fi

clean:
	+for proc in $(procs); do make -C $${proc} clean; rm -f $${proc}/sample.jpg; done

$(procs): $(sample) | has_sample
	ln -srf $(sample) $@/sample.jpg
	+make -C $@
