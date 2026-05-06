import unittest

from extractmarkdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdown(unittest.TestCase):
####EXTRACT MARKDOWN IMAGES TESTS
    def test_extract_markdown_images_eq1(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_eq2(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), but it also has a second ![butt](https://i.like.com/chocolate.milk)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("butt", "https://i.like.com/chocolate.milk")], matches)

    def test_extract_markdown_images_not_eq1(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png), but it also has a second ![image](https://is.an.com/actual.image)"
        )
        self.assertNotEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("butt", "https://i.like.com/chocolate.milk")], matches)

####EXTRACT MARKDOWN LINKS TESTS
    def test_extract_markdown_links_eq1(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_eq2(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png), but it also has a second [butt](https://i.like.com/chocolate.milk), here is a fake []link(badda.bingus"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png"), ("butt", "https://i.like.com/chocolate.milk")], matches)
