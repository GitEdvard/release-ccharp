from __future__ import print_function
from release_ccharp.apps.common import BinaryVersionUpdater
from release_ccharp.apps.common import ApplicationBase
from release_ccharp.apps.chiasma_scripts.builder import ChiasmaBuilder
from release_ccharp.apps.chiasma_scripts.validation_deployer import ChiasmaValidationDeployer


class Application(ApplicationBase):
    """
    Uses the chiasma code for testing purposes. Uses a local folder tree
    """
    def __init__(self, snpseq_workflow, branch_provider, os_service, windows_commands, whatif):
        super(Application, self).__init__(snpseq_workflow, branch_provider, os_service,
                                          windows_commands, whatif)
        self.binary_version_updater = BinaryVersionUpdater(
            whatif=False, config=self.config, path_properties=self.path_properties,
            branch_provider=branch_provider, app_paths=self.app_paths, os_service=os_service)
        self.chiasma_builder = ChiasmaBuilder(self)
        self.validation_deployer = ChiasmaValidationDeployer(self)

    def build(self):
        self.chiasma_builder.run()

    def deploy_validation(self):
        self.validation_deployer.run()