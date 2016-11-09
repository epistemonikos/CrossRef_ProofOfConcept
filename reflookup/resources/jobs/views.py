from reflookup.utils.restful.utils import DeferredResource


class JobResource(DeferredResource):
    def get(self):
        return self.check_job()
