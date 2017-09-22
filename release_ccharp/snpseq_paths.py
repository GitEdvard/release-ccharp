import os
import re
import yaml
from release_ccharp.exceptions import SnpseqReleaseException
from release_ccharp.snpseq_workflow import *


class SnpseqPaths:
    def __init__(self, config, repo):
        self.config = config
        self.repo = repo
        self.workflow = None
        sub_paths = self._load_subpaths()
        self.release_tools_subpath = sub_paths['release_tools_subpath']
        self.confluence_tools_subpath = sub_paths['confluence_tools_subpath']
        self.candidate_subpath = sub_paths['candidate_subpath']
        self.devel_environment_subpath = sub_paths['devel_environment_subpath']
        self.doc_subpath = sub_paths['doc_subpath']
        self.doc_metadata_subpath = sub_paths['doc_metadata_subpath']
        self.user_validations_subpath = sub_paths['user_validations_subpath']
        self.user_validations_all_version_subpath = sub_paths['user_validations_all_version_subpath']
        self.user_validations_next_hotfix_subpath = sub_paths ['user_validations_next_hotfix_subpath']
        self.user_validations_next_release_subpath = sub_paths['user_validations_next_release_subpath']
        self.user_validations_validation_files_subpath = sub_paths['user_validations_validation_files_subpath']
        self.user_validations_sql_updates_subpath = sub_paths['user_validations_sql_updates_subpath']
        self.user_validations_latest_subpath = sub_paths['user_validations_latest_subpath']

    def _load_subpaths(self):
        here = os.path.dirname(__file__)
        path = os.path.join(here, 'paths.config')
        with open(path, 'r') as f:
            sub_paths = yaml.load(f)
        return sub_paths

    @property
    def _repo_root(self):
        return os.path.join(self.config['root_path'], self.repo)

    @property
    def _candidate_tag(self):
        """
        Get the version of the latest candidate branch
        :param workflow: 
        :return: Version of latest candidate branch
        """
        queue = self.workflow.get_queue()
        branch = queue[0]
        tag = Conventions.get_tag_from_branch(branch)
        return tag

    @property
    def candidate_root_path(self):
        return os.path.join(self._repo_root, self.candidate_subpath)

    @property
    def release_tools_config(self):
        return os.path.join(self._repo_root, self.release_tools_subpath)

    @property
    def confluence_tools_config(self):
        return os.path.join(self._repo_root, self.confluence_tools_subpath)

    @property
    def user_manual_download_path(self):
        """
        Generates user manual name for coming version, and use the artifact path,
        i.e. the path to the download directory (not the doc path)
        :return: 
        """
        version = str(self._candidate_tag)
        latest_path = self.current_candidate_dir
        manual_base_name = "{}-user-manual".format(self.repo)
        manual_name = "{}-{}.pdf".format(manual_base_name, version)
        return os.path.join(latest_path, manual_name)

    @property
    def user_manual_path_previous(self):
        manual_base_name = "{}-user-manual".format(self.repo)
        latest_version = self.workflow.get_latest_version()
        manual_name = "{}-v{}.pdf".format(manual_base_name, latest_version)
        latest_path = self.latest_accepted_candidate_dir
        return os.path.join(latest_path, manual_name)

    @property
    def latest_accepted_candidate_dir(self):
        """
        Find the download catalog for the latest accepted branch
        :return: The path of latest accepted branch
        """
        current_version = self.workflow.get_latest_version()
        subdirs = os.listdir(self.candidate_root_path)
        subdir_path = None
        for subdir in subdirs:
            if re.match('(release|hotfix)-{}'.format(current_version), subdir):
                subdir_path = os.path.join(self.candidate_root_path, subdir)
        if subdir_path is None:
            raise SnpseqReleaseException("Could not find the download catalog for latest version")
        return subdir_path

    @property
    def current_candidate_dir(self):
        """
        Find the download catalog for the latest candidate branch
        :param workflow: 
        :return: The path of the latest candidate branch
        """
        queue = self.workflow.get_queue()
        branch = queue[0]
        return os.path.join(self.candidate_root_path, branch)
