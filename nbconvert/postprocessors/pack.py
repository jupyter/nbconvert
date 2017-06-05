from __future__ import print_function

from .base import PostProcessorBase

# from traitlets import dotted string

from zipfile import ZipFile, ZIP_DEFLATED
import os



class ZipPostProcessor(PostProcessorBase):

    # need to actually write this and look at the api
    # def compression_type = DottedStringImport 

    def postprocess(self, input):
        dirname, filename = os.path.split(input)
        base_name = os.path.splitext(filename)[0]
        #  print(self.config.output_files_dir)
        #  output_files_dir = (self.config.NbConvertApp.output_files_dir).format(notebook_name=base_name)
        output_files_dir = '{notebook_name}_files'.format(notebook_name=base_name)
        zip_filename = base_name + '.zip'
        zippath = os.path.join(dirname, zip_filename)
        with ZipFile(zippath, mode='w', compression=ZIP_DEFLATED) as zipf:
            zipf.write(input, arcname = filename)
            os.remove(input)
            for output_path, _, output_filenames in os.walk(os.path.join(dirname,output_files_dir)):
                for output_filename in output_filenames: 
                    file_location = os.path.join(output_path, output_filename)
                    zipf.write(file_location,
                               arcname = os.path.join(output_files_dir,output_filename))
                    os.remove(file_location)
                os.rmdir(output_path)


