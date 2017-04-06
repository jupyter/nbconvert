from __future__ import print_function

from .base import PostProcessorBase

from zipfile import ZipFile, ZIP_DEFLATED
import os

class ZipPostProcessor(PostProcessorBase):

    def postprocess(self, input):
        dirname, filename = os.path.split(input)
        base_name = os.path.splitext(filename)[0]
        #  print(self.config.output_files_dir)
        #  output_files_dir = (self.config.NbConvertApp.output_files_dir).format(notebook_name=base_name)
        output_files_dir = '{notebook_name}_files'.format(notebook_name=base_name)
        zip_filename = base_name + '.zip'
        zippath = os.path.join(dirname,zip_filename)
        with ZipFile(zippath, mode='w', compression=ZIP_DEFLATED) as zipf:
            zipf.write(input, arcname = filename)
            for output_path, _, output_filenames in os.walk(os.path.join(dirname,output_files_dir)):
                for output_filename in output_filenames: 
                    zipf.write(os.path.join(output_path,output_filename), 
                               arcname = os.path.join(output_files_dir,output_filename))


