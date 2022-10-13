# Friquifund.org site

## Quick notes

Main page starts from `index.html` which includes the home page located in `pages/home.md`. All other pages are also located in `pages/`.

Top right menu is defined in `_data/navigation.yml`.

Team member content is in `_data/team.csv` (this file is a (manual) CSV export of FriquiFundDB).

A Jekyll theme is used to manage basic style:

- Theme: https://jekyll-themes.com/agency-jekyll-theme/
- Repo: https://github.com/raviriley/agency-jekyll-theme)

## Repository structure

It pretty much follows Jekyll documentation:

- [https://jekyllrb.com/docs/structure/](https://jekyllrb.com/docs/structure/)

### Folder `_data/`

Well-formatted site data should be placed here. The Jekyll engine will autoload all data files (using either the `.yml`, `.yaml`, `.json`, `.csv` or `.tsv` formats and extensions) in this directory, and they will be accessible via `site.data`. If there's a file `members.yml` under the directory, then you can access contents of the file through `site.data.members`.

- `_data/navigation.yml`: Defines the menu in the top-right navigation bar.
- `_data/sitetext.yml`: ????
- `_data/style.yml`: Right now, basically defines the home page background image.
- `_data/team.csv`: FriquiFund members details.

### Folder `_includes/`

These are the partials that can be mixed and matched by your layouts and posts to facilitate reuse. The liquid tag `{% include file.ext %}` can be used to include the partial in `_includes/file.ext`.

- `_includes/home/`: Sections included in home page and `html` chunk used to wrap this sections and included using liquid tag `include`.
- `_includes/members/`: `html` chunk used to wrap members' information in members page.
- `footer.html`: Web footer.
- `head.html`: Web `<head>` tag.
- `header.html`: Web `<header>` tag. Basically used to include the home page background image.
- `nav.html`: Web top-side navigation bar.

### Folder `_layouts/`

These are the templates that wrap posts. Layouts are chosen on a post-by-post basis in the front matter. The liquid tag `{{ content }}` is used to inject content into the web page.

- `_layouts/default.html`: Base layout. Includes basic `html` page structure, `<head>` tag, navigation bar, page content, footer and assets links.
- `_layouts/page.html`: Page layout. Inherits from `default` layout and includes some additional margin.

### Folder `_posts/`

Your dynamic content, so to speak. The naming convention of these files is important, and must follow the format: `YYYY-MM-DD-title.md`. The permalinks can be customized for each post, but the date and markup language are determined solely by the file name.

### Folder `img/`

Logos, background images and other images used in the web.

### Folder `pages/`

Web pages. Can be implemented using both `html` and `markdown`. They include

### Folder `pics/`

Pictures of FriquiFund members.
