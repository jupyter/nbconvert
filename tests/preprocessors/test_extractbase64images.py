"""Tests for the Base64ImageExtractor preprocessor"""

from base64 import b64encode
import os

from nbconvert.preprocessors.extractbase64images import Base64ImageExtractor
from .base import PreprocessorTestsBase


class TestBase64ImageExtractor(PreprocessorTestsBase):
    """Contains test functions for extractbase64images.py"""

    def build_preprocessor(self):
        """Make an instance of a preprocessor"""
        preprocessor = Base64ImageExtractor()
        preprocessor.enabled = True
        return preprocessor

    def test_constructor(self):
        """Can a Base64ImageExtractor be constructed?"""
        self.build_preprocessor()

    def test_base64_extraction(self):
        """Test the extraction of base64 images from markdown cells"""
        # Create a test image
        test_image = b"test_image_data"
        b64_data = b64encode(test_image).decode('utf-8')
        
        # Create notebook with base64 image
        nb = self.build_notebook()
        nb.cells[1].source = f'![test image](data:image/png;base64,{b64_data})'
        
        # Setup resources
        res = self.build_resources()
        res['unique_key'] = 'test_notebook'
        
        # Run preprocessor
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)
        
        # Check if image was extracted
        self.assertEqual(len(res['outputs']), 1)
        
        # Get the filename from the markdown
        filename = nb.cells[1].source.split('(')[1].rstrip(')')
        
        # Verify image data
        self.assertIn(filename, res['outputs'])
        self.assertEqual(res['outputs'][filename], test_image)
        
        # Verify markdown was updated correctly
        self.assertTrue(nb.cells[1].source.startswith('![test image]'))
        self.assertTrue(nb.cells[1].source.endswith('.png)'))

    def test_invalid_base64(self):
        """Test handling of invalid base64 data"""
        nb = self.build_notebook()
        nb.cells[1].source = '![test image](data:image/png;base64,invalid_data)'
        
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)
        
        # Should keep original content when base64 is invalid
        self.assertEqual(nb.cells[1].source, '![test image](data:image/png;base64,invalid_data)')
        self.assertEqual(len(res['outputs']), 0)

    def test_unsupported_image_type(self):
        """Test handling of unsupported image type"""
        test_image = b"test_image_data"
        b64_data = b64encode(test_image).decode('utf-8')
        
        nb = self.build_notebook()
        nb.cells[1].source = f'![test image](data:image/unsupported;base64,{b64_data})'
        
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)
        
        # Should keep original content for unsupported types
        self.assertEqual(nb.cells[1].source, f'![test image](data:image/unsupported;base64,{b64_data})')
        self.assertEqual(len(res['outputs']), 0)

    def test_multiple_images(self):
        """Test handling of multiple images in one cell"""
        test_image = b"test_image_data"
        b64_data = b64encode(test_image).decode('utf-8')
        
        nb = self.build_notebook()
        nb.cells[1].source = (
            f'![image1](data:image/png;base64,{b64_data})\n'
            f'![image2](data:image/png;base64,{b64_data})'
        )
        
        res = self.build_resources()
        preprocessor = self.build_preprocessor()
        nb, res = preprocessor(nb, res)
        
        # Should extract both images
        self.assertEqual(len(res['outputs']), 2)
        self.assertTrue(all('.png' in line for line in nb.cells[1].source.split('\n')))

    def test_separate_dir(self):
        """Test extraction with separate directory option"""
        preprocessor = self.build_preprocessor()
        preprocessor.use_separate_dir = True
        
        test_image = b"test_image_data"
        b64_data = b64encode(test_image).decode('utf-8')
        
        nb = self.build_notebook()
        nb.cells[1].source = f'![test image](data:image/png;base64,{b64_data})'
        
        res = self.build_resources()
        res['unique_key'] = 'test_notebook'
        
        nb, res = preprocessor(nb, res)
        
        # Verify directory structure
        self.assertIn('base64_images_dir', res)
        self.assertEqual(res['base64_images_dir'], 'test_notebook_files')
        
        # Verify image extraction
        self.assertEqual(len(res['base64_images']), 1)
        filename = nb.cells[1].source.split('(')[1].rstrip(')')
        self.assertTrue(filename.startswith('test_notebook_files/'))

    def test_real_notebook(self):
        """Test extraction with a real notebook containing base64 images"""
        # Load the test notebook
        import nbformat
        with open('tests/preprocessors/files/notebook_with_base64.ipynb') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Setup resources
        res = self.build_resources()
        res['unique_key'] = 'notebook_with_base64'
        
        # Run preprocessor
        preprocessor = self.build_preprocessor()
        preprocessor.use_separate_dir = True
        nb, res = preprocessor(nb, res)
        
        # Verify images were extracted
        self.assertGreater(len(res['base64_images']), 0)
        print(f"\nNumber of images extracted: {len(res['base64_images'])}")
        print(f"Image filenames: {list(res['base64_images'].keys())}")
        
        # Verify all extracted files are valid image files
        for filename in res['base64_images'].keys():
            self.assertTrue(any(filename.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']))
            
        # Verify all image references in markdown cells are updated
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                # Check specifically for base64 image data, not just the word 'base64'
                self.assertNotIn('data:image/png;base64,', cell.source)
                self.assertNotIn('data:image/jpeg;base64,', cell.source)
                self.assertNotIn('data:image/jpg;base64,', cell.source)
                self.assertNotIn('data:image/gif;base64,', cell.source)
                self.assertNotIn('data:image/svg;base64,', cell.source)