# POI Video Analyses

Generated from `raindrop/bookmarks.json` with `scripts/analyze-poi-videos.py`.

The operation is idempotent: if a bookmark folder contains `analysis.json` with `status: "success"` for the same source URL, future runs skip that bookmark.

The current `analysis.md` files were enriched with `scripts/enrich-poi-analyses.py`. Each enriched analysis includes city, address, food genre, price point, reservation guidance, post description, comment availability, interpreted visible text, audio transcript, and source notes.

For a geography-organized wiki-style overview with inline contact sheets, see [wiki-index.md](wiki-index.md).

## Successful

- [1701182518-facebook.com](1701182518-facebook.com/analysis.md) - Black Wood Izakaya / 黑木亭居酒屋, Hong Kong, Tsim Sha Tsui
- [1700494133-facebook.com](1700494133-facebook.com/analysis.md) - Dawu Yakiniku / 大無燒肉, Shenzhen, Nanshan
- [1700490320-xiaohongshu.com](1700490320-xiaohongshu.com/analysis.md) - alcohol-infused adult ice cream recipe/process clip; no reliable POI exposed
- [1700372224-fb.watch](1700372224-fb.watch/analysis.md) - Maguro Mart / マグロマート, Tokyo, Nakano
- [1700305381-facebook.com](1700305381-facebook.com/analysis.md) - 鮨冠 OMAKASE食べ放題, Shenzhen, Futian
- [1700301715-facebook.com](1700301715-facebook.com/analysis.md) - Sushi Song / 壽司宋 SUSHI SONG, Shenzhen, Nanshan
- [1700298280-fb.watch](1700298280-fb.watch/analysis.md) - Yingu Omakase / 隐谷Omakase, Shenzhen, Futian
- [1700297979-fb.watch](1700297979-fb.watch/analysis.md) - Yingu Omakase / 隐谷Omakase, Shenzhen, Futian

## Failed

- [1700428438-facebook.com](1700428438-facebook.com/analysis.md) - `yt-dlp` failed to parse Facebook reel `942918698565091`; no reliable video/audio analysis is available.

## Comment Availability

The social post comments were not exposed by the downloaded metadata. A dedicated `yt-dlp --write-comments` probe also returned no comment thread for a Facebook reel. The enriched files therefore say “Top comments unavailable” instead of inventing comments.
