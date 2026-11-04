# WordPress

## Options

- `options.wordpress.title`: required. The post title.
- `options.wordpress.tags`: tag names. WordPress creates any tag that does not exist yet and reuses one that does. A name must not contain a comma.
- `options.wordpress.featureImageMediaId`: a media id to use as the featured image. Uplika uploads a copy to the site's media library.
- `options.wordpress.draftOnly`: `true` saves it as a draft in WordPress. The permalink is then the WordPress editor page for that draft, not a public address.

## Always ask

- The title, if the person did not give one.
- Whether it should go live or wait as a WordPress draft, when the person did not say.

## Body

- Write Markdown. Uplika turns it into HTML for WordPress.
- Raw HTML tags are refused outside code (`wordpress_html_not_supported`, with the line number). Write that part in Markdown.
- Place a photo with `![alt](media:<id>)` on a line of its own. Uplika uploads each photo to the site's media library; photos you attach without placing them go at the end.
- Do not use Naver Blog syntax (`@group`, `@video`, `@card`, `{.small}` and other `{…}` attributes). WordPress refuses those lines (`wordpress_directive_not_supported`).
- A post with media references can go to WordPress and Ghost in the same call. It cannot go to WordPress and Naver Blog in the same call; publish each on its own.

## Not available

Read `list_platforms` and its features table. Uplika does not read WordPress comments or report view counts, and WordPress posts take photos only. Categories are not set: WordPress files the post under the site's default category.

## Pitfalls

- Connecting takes the site address, the WordPress username and an application password made under Users, Profile in WordPress. The login password does not work.
- WordPress.com sites cannot connect yet (`wordpress_com_site`). Self-hosted WordPress can.
- The WordPress user needs the Author role or higher (`wordpress_role_insufficient`).
- `update_post` rewrites only the title and body, in place. Tags, the featured image and the post's status stay as they are, so those options are ignored on an edit. WordPress has no edit lock: changes someone made in the WordPress editor since are overwritten, so check first when the person may have edited it there.
- `delete_post` moves the post to the WordPress trash, where an admin can restore it until the site empties the trash. A site with the trash turned off deletes it for good, and the response's `note` says so. Tell the person.
