import fs from "node:fs/promises";

const token = process.env.RAINDROP_TOKEN;
const collectionId = process.env.RAINDROP_COLLECTION_ID || "0";

if (!token) {
  throw new Error("Missing RAINDROP_TOKEN");
}

const all = [];
let page = 0;

while (true) {
  const url = new URL(`https://api.raindrop.io/rest/v1/raindrops/${collectionId}`);
  url.searchParams.set("page", String(page));
  url.searchParams.set("perpage", "50");

  const res = await fetch(url, {
    headers: {
      Authorization: `Bearer ${token}`,
      "User-Agent": "raindrop-github-sync",
    },
  });

  if (!res.ok) {
    throw new Error(`Raindrop API failed: ${res.status} ${await res.text()}`);
  }

  const data = await res.json();
  const items = data.items || [];
  all.push(...items);

  if (items.length < 50) break;
  page += 1;
}

all.sort((a, b) => new Date(b.created) - new Date(a.created));

await fs.mkdir("raindrop", { recursive: true });

await fs.writeFile("raindrop/bookmarks.json", JSON.stringify(all, null, 2) + "\n");

const md = [
  "# Raindrop Bookmarks",
  "",
  `Synced: ${new Date().toISOString()}`,
  "",
  ...all.map((item) => {
    const title = item.title || item.link;
    const tags = item.tags?.length ? `\nTags: ${item.tags.join(", ")}` : "";
    const excerpt = item.excerpt ? `\n\n${item.excerpt}` : "";
    return `## [${title}](${item.link})\n\nCreated: ${item.created}${tags}${excerpt}\n`;
  }),
].join("\n");

await fs.writeFile("raindrop/bookmarks.md", md);
console.log(`Synced ${all.length} bookmarks`);
