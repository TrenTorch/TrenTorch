# Adding a blog post

The `/blogs` pages are built from the folders in this directory, the same way `/papers` is. To add a
post you only add folders and files. You do not touch any code.

```
15-blogs/
  00-engineering/                a track (one card on /blogs)
    meta.json                    { "title": "Engineering", "description": "How we build TrenTorch" }
    01-my-first-post/            a post, served at /blogs/my-first-post
      meta.json                  the post's details (below)
      post.md                    the post, in Markdown (math as $x$ and $$x$$)
```

The numbers in the folder names only decide the order. The folder name without the number is the
post's web address.

`meta.json` of a post:

```json
{
	"title": "The full title",
	"post": {
		"title": "The full title",
		"author": "Your Name",
		"date": "2026-11-24",
		"summary": "One or two sentences that say what the post is about."
	}
}
```

A track with no posts is ignored, so a folder can be a placeholder. A mistake in a `meta.json` stops the
build with a message that names the file.
