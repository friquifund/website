# How to create new posts

## Step 1: Connect to the webpage repository

1. Open a web browser.
2. Sign in [GitHub](https://github.com) using your GitHub account account.
3. Go to the [FriquiFund website GitHub repository](https://github.com/friquifund/website).

## Step 2: Upload images, PDF files or other assets referenced in the new post

1. Make sure the files you want to upload have no spaces in the name.
2. Open folder `assets/`.
3. Click "Add file > Upload files" (top-right corner).
4. Drag or choose your files. You can upload a whole folder.
5. Click green button "Commit changes"

## Step 3: Create the post text

1. Go back to the [FriquiFund website GitHub repository](https://github.com/friquifund/website).
2. Open folder `_posts/`.
3. Click "Add file > Create new file" (top-right corner).
4. Name the file. It must follow the format `YYYY-MM-DD-Some-hyphen-separated-name.md` (e.g. "2022-12-05-Plenary-Session-Dec22.md").
5. Edit the content (see section "Markdown format" section).
6. Check whether you like the final view using the "Preview" tab.
7. Click green button "Commit new file"

# Markdown format

The post has to be written in Markdown format. This format can automatically be translated into `HTML`. We already mentioned the importance of following a specific name format. In this section we specify some other formats that must be followed and other Markdown topics you might want to include.

We recommend copy-pasting the raw content of an older post. This can be done by clicking into the file (in GitHub), clicking button "Raw", selecting all content and copying it.

The post file has to start with the lines of metadata below. Do not forget the "---":

``` jekyll
---
layout: page
author: <Your name here> (e.g. Pau Agulló)
title: <Your post name here. This will be the clickable title shown in https://friquifund.org/blog> (e.g. FriquiFund Plenary Session - Dec22)
---
```

The rest of the file will have the content that will be shown on the website. Here are some tips:

## Title

Use `# <Your title here>` to add a title to your post. This title can be different from the one you used in the metadata lines.

Use multiple leading `#` to have smaller titles.

## Paragraphs

A new paragraph is created when a blank line is found in the text. If you start a new line, but there is no blank line between the previous and the new one, it will be formatted as a single paragraph. Examples:

``` markdown
This will be rendered
in the same paragraph

This will be a new paragraph
```

This will be rendered
in the same paragraph

This will be a new paragraph

## Lists

Use `-` to list items. Example:

``` markdown
This is my unordered shopping list:
- Cookies
- Vegetables
- Bread

This is my ordered task list:
1. Wake up.
2. Eat breakfast.
3. Leave home.
```

This is my shopping list:
- Cookies
- Vegetables
- Bread

This is my ordered task list:
1. Wake up
2. Take a shower
3. Leave home

## Embedded images

Use an HTML `img` tag to include images previously uploaded in the `assets/` folder. The image path should be specified in the `src` parameter as follows: `src="/assets/your-image-name-including-the-file-extension"`. Example:

``` html
<img src="/assets/Plenary-Dec-22.jpeg" width="20%" />
```

<img src="../assets/Plenary-Dec-22.jpeg" width="20%" />

Use a wrapping `div` tag to center the image. Example:

``` html
<div style="text-align: center">
    <img src="/assets/Plenary-Dec-22.jpeg" width="20%" />
</div>
```

*Example is not visible here, please check [this post](https://friquifund.org/2022/12/05/Plenary-Session-Dec22.html) to see how it looks like.*

You can put multiple images in the same line as long as the sum of their with is lower than 100%.

``` html
<div>
    <img src="/assets/Plenary-Dec-22.jpeg" width="19%" />
    <img src="/assets/Plenary-Dec-22.jpeg" width="19%" />
    <img src="/assets/Plenary-Dec-22.jpeg" width="19%" />
    <img src="/assets/Plenary-Dec-22.jpeg" width="19%" />
    <img src="/assets/Plenary-Dec-22.jpeg" width="19%" />
</div>
```

<div>
    <img src="../assets/Plenary-Dec-22.jpeg" width="19%" />
    <img src="../assets/Plenary-Dec-22.jpeg" width="19%" />
    <img src="../assets/Plenary-Dec-22.jpeg" width="19%" />
    <img src="../assets/Plenary-Dec-22.jpeg" width="19%" />
    <img src="../assets/Plenary-Dec-22.jpeg" width="19%" />
</div>

## Embedded PDFs

Use an HTML `object` tag to embed PDF files previously uploaded in the `assets/` folder. The image path should be specified in the `data` parameter like `data="/assets/your-PDF-name-including-the-file-extension"`. Example:

``` html
<object data="../assets/FRIQUIFUND-Plenary-2022-12.pdf" width="90%" height="700" type='application/pdf'></object>
```

*Example is not visible here, please check [this post](https://friquifund.org/2022/12/05/Plenary-Session-Dec22.html) to see how it looks like.*

You can use the wrapper `div` to center the PDF, as explained in other sections.

## Embedded YouTube videos

Use HTML `iframe` tag to embed YouTube videos. The exact HTML code and source can be genetared from YouTube:

1. Go to the video.
2. Click button "Share" below.
3. Click "Embed" option.
4. Copy the `iframe` tag on the right side.

Example:

``` html
<iframe width="560" height="315" src="https://www.youtube.com/embed/VzSEg4iR9e0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
```

*Example is not visible here, please check [this post](https://friquifund.org/2022/12/05/Plenary-Session-Dec22.html) to see how it looks like.*

You can use the wrapper `div` to center the PDF, as explained in other sections.
