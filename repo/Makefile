include ../Makefile.options

repo_version?=0.1.$(commit_count)
repo_url?=http://192.168.1.71:10003
m_dir=$(CURDIR)
deploy_dir=$(m_dir)/build
repo_dir?=$(CURDIR)/data

build: $(deploy_dir)/lrt-repo-$(repo_version).zip

$(deploy_dir): 
	mkdir -p $@

$(deploy_dir)/lrt-repo-$(repo_version).zip: lrt-repo/addon.xml | $(deploy_dir)
	zip -r $@ lrt-repo -x *build* -x addon.xml.in

lrt-repo/addon.xml: lrt-repo/addon.xml.in
	cat $< | envsubst > $@
########################################################################	
$(repo_dir):
	mkdir -p $@
$(repo_dir)/$(name):
	mkdir -p $@

$(repo_dir)/addons.xml: ../addon.xml | $(repo_dir)
	echo '<?xml version="1.0" encoding="UTF-8"?> <addons>' > $@
	cat ../addon.xml | tail -n +2 >> $@
	echo '</addons>' >> $@

$(repo_dir)/addons.xml.md5: $(repo_dir)/addons.xml
	md5sum $< | awk '{ print $$1 }' > $@

$(repo_dir)/lrt-repo-$(repo_version).zip: $(deploy_dir)/lrt-repo-$(repo_version).zip | $(repo_dir)
	cp $< $@

$(repo_dir)/$(name)/$(name)-$(version).zip: ../build/$(name)-$(version).zip | $(repo_dir)/$(name)
	cp $< $@
../build/$(name)-$(version).zip ../addon.xml:
	cd .. && $(MAKE) build	
prepare-repo: $(repo_dir)/addons.xml.md5 $(repo_dir)/lrt-repo-$(repo_version).zip \
	$(repo_dir)/$(name)/$(name)-$(version).zip
run-repo: prepare-repo
	docker run -p $(port):80 -v $(repo_dir):/usr/share/nginx/html nginx:1.17.9
########################################################################	

clean:
	rm -rf $(deploy_dir)
	rm -rf $(repo_dir)
	rm -f lrt-repo/addon.xml
	rm -rf $(repo_dir)/
	cd .. && $(MAKE) clean
	
.PHONY: 
.EXPORT_ALL_VARIABLES: