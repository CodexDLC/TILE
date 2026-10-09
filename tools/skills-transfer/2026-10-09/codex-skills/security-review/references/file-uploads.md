# Untrusted files and image uploads

Trace upload acceptance through processing, storage, retrieval, and deletion. Extension, client MIME, and magic-byte checks are useful filters but do not make content safe. For raster images, verify the server actually decodes and re-encodes to an allowed format, discards unnecessary metadata and original bytes, and uses a maintained parser. Re-encoding reduces some risks but is not proof of safety: the decoder itself processes hostile input.

Enforce limits before and during processing: request and file size, dimensions, frame/page count, decompressed pixel or memory budget, processing time, and quotas. Consider decompression bombs and parser vulnerabilities, including dependencies used for thumbnails. Reject malformed content safely and clean temporary files.

Treat SVG as active content with a separate policy. If SVG is allowed, assess scripts, external references, embedded content, XML processing, and serving context; a raster-only policy should reject it. Store untrusted originals outside executable paths, use generated names, restrict access by owner or tenant, and serve from a separate non-executable origin or download context with appropriate response headers. Check whether private objects are accessible through predictable URLs or permissive buckets.

Malware scanning can add a defense layer, but a clean scan is not proof that a file is safe. Never use live malware samples in an audit without a separately authorized and controlled procedure.

Primary guidance: [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html).
