import unittest

from pymo import (
        _get_new_filename,
        _transform_filename,
        _get_file_tags,
        _walk,
        )

class TestTransforms(unittest.TestCase):
    text = "Folder/A Test File!.name"

    def testLowercase(self):
        self.assertEqual(
                _transform_filename(self.text,["lc",]),
                "folder/a test file!.name"
                )

    def testUppercase(self):
        self.assertEqual(
                _transform_filename(self.text,["uc",]),
                "FOLDER/A TEST FILE!.NAME"
                )

    def testCamelCase(self):
        self.assertEqual(
                _transform_filename(self.text,["cc",]),
                "Folder/ATestFile!.name"
                )

    def testJavaCase(self):
        self.assertEqual(
                _transform_filename(self.text,["jc",]),
                "folder/aTestFile!.name"
                )

    def testSpacesToUnderscores(self):
        self.assertEqual(
                _transform_filename(self.text,["us",]),
                "Folder/A_Test_File!.name"
                )

    def testRemoveSpaces(self):
        self.assertEqual(
                _transform_filename(self.text,["rs",]),
                "Folder/ATestFile!.name"
                )

    def testRemovePunctuation(self):
        self.assertEqual(
                _transform_filename(self.text,["rp",]),
                "Folder/A Test File.name"
                )

    def testPunctuationToUnderscores(self):
        self.assertEqual(
                _transform_filename(self.text,["pu",]),
                "Folder/A Test File_.name"
                )

    def testCompoundStatement(self):
        self.assertEqual(
                _transform_filename(self.text,["jc", "us", "rp"]),
                "folder/aTestFile.name"
                )



if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=3)
    unittest.main(testRunner=runner)
