commit_count=$(shell git rev-list --count HEAD)
repo_version?=0.1.$(commit_count)
repo_url?=http://localhost:10003
m_dir=$(CURDIR)
deploy_dir=$(m_dir)/build

build: $(deploy_dir)/lrt-repo-$(repo_version).zip

$(deploy_dir): 
	mkdir -p $@

$(deploy_dir)/lrt-repo-$(repo_version).zip: lrt-repo/addon.xml | $(deploy_dir)
	zip -r $@ lrt-repo -x *build* -x addon.xml.in

lrt-repo/addon.xml: lrt-repo/addon.xml.in
	cat $< | envsubst > $@


clean:
	rm -rf $(deploy_dir)
	rm -f lrt-repo/addon.xml

.PHONY: 
.EXPORT_ALL_VARIABLES: