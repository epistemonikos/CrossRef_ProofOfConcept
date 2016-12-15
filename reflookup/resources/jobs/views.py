from reflookup.utils.restful.utils import DeferredResource


class JobResource(DeferredResource):
    def __init__(self):
        super().__init__()
        self.get_parser.add_argument('id', type=str, location='values',
                                     required=True)

    def get(self):
        job_id = self.get_parser.parse_args()['id']
        return self.check_job(job_id)
