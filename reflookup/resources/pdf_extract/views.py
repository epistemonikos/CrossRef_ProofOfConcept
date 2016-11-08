import os
from reflookup import app
from reflookup.resources.lookup_functions.citation_extract import \
    pdf_extract_references
from reflookup.utils.restful.utils import DeferredResource
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from flask_restful import abort

"""
This file contains the endpoint resources for retrieving references from a pdf file
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] == 'pdf'

def mama(filename):
    return {
        'nan' : filename
    }

class PdfReferenceExtractResource(DeferredResource):
    """
        This resource represents the /refs/pdf endpoint on the API.
    """

    def __init__(self):
        super().__init__()
        self.post_parser.add_argument('pdf_file', type=FileStorage, location='files')

    def post(self):
        data = self.post_parser.parse_args()
        file = data.get('pdf_file')
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['PDF_UPLOAD_FOLDER'], secure_filename(file.filename))
            file.save(filename)
            return self.enqueue_task_and_return(pdf_extract_references, filename)
        else:
            return abort(400, message='no such file')
