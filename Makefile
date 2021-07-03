commit_count=$(shell git rev-list --count HEAD)
version?=0.3.$(commit_count)
m_dir=$(CURDIR)
deploy_dir=$(m_dir)/build

build: $(deploy_dir)/kodi.plugin.lrt-mediateka-$(version).zip

$(deploy_dir): 
	mkdir -p $@

$(deploy_dir)/kodi.plugin.lrt-mediateka-$(version).zip: addon.xml | $(deploy_dir)
	cd .. && zip -r $@ kodi.plugin.lrt-mediateka -x *.git* -x *.idea* -x *build* -x Makefile \
		-x addon.xml.in

addon.xml: addon.xml.in
	cat $< | envsubst > $@


clean:
	rm -rf $(deploy_dir)
	rm -f addon.xml

.PHONY: 
.EXPORT_ALL_VARIABLES: