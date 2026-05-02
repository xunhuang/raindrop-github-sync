#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "raindrop" / "poi-analysis"


PROFILES = {
    "1701182518": {
        "name": "Black Wood Izakaya / 黑木亭居酒屋",
        "city": "Hong Kong",
        "district": "Tsim Sha Tsui, Kowloon",
        "address": "G/F-1/F, Kok Pah Mansion, 58-60 Cameron Road, Tsim Sha Tsui, Hong Kong",
        "transit": "Tsim Sha Tsui / East Tsim Sha Tsui MTR, Exit B2, about 5 minutes on foot",
        "genre": "Japanese izakaya, sushi/sashimi, all-you-can-eat sashimi set",
        "price": "Post says HK$300-plus per person for 4 hours; OpenRice lists HK$201-400.",
        "reservation": "Recommended. OpenRice/Apple Maps list reservations, phone booking, and WhatsApp booking; the restaurant is social-media popular and has long meal windows.",
        "must_try": ["thick-cut sashimi", "salmon", "yellowtail", "toro", "scallop", "sea urchin sushi"],
        "gist": "A value-focused Tsim Sha Tsui Japanese izakaya clip promoting a four-hour sashimi/all-you-can-eat experience. The pitch is that sashimi in Hong Kong does not have to be extremely expensive: whole fish are brought in, the cuts look thick, and the narrator emphasizes freshness and a per-person price in the HK$300 range.",
        "visible": "The OCR itself is noisy, but the video/audio meaning is clear: it shows platters of sashimi and izakaya food, with captions reinforcing the value claim, freshness, and four-hour dining time.",
        "sources": [
            "Post metadata and transcript in this folder",
            "OpenRice: https://www.openrice.com/en/hongkong/r-black-wood-izakaya-tsim-sha-tsui-japanese-all-you-can-eat-r726262",
            "Apple Maps snippet from web lookup: accepts reservations and lists the same Cameron Road address",
        ],
    },
    "1700494133": {
        "name": "Dawu Yakiniku / 大無燒肉 (Shenzhen Bay MixC)",
        "city": "Shenzhen",
        "district": "Nanshan / Houhai",
        "address": "Unit CL310, L3, Area C, Shenzhen Bay MixC, 1218 Haide 1st Road, Yuehai Subdistrict, Nanshan, Shenzhen",
        "transit": "Houhai Station, Line 13, Exit K1",
        "genre": "Japanese yakiniku / premium wagyu grill",
        "price": "OpenRice categorizes it as ¥301+; Apple Maps lookup showed average cost around ¥676. The post positions it as high-value but premium.",
        "reservation": "Needed or strongly recommended. The post asks viewers to comment “yum” for booking details, and Apple Maps lists reservations/private rooms.",
        "must_try": ["crab roe and sea urchin kamameshi", "sea urchin sweet shrimp tart", "cubed wagyu", "wagyu tongue", "chicken oil with hokki clam"],
        "gist": "A premium Japanese yakiniku reel for Shenzhen diners, focused on hands-free grilling/service and rich seafood-wagyu combinations. The creator frames it as one of the highest-value upscale yakiniku meals in Shenzhen, with the main selling points being crab roe/sea urchin rice, wagyu fat, tender tongue, and a Japanese garden atmosphere.",
        "visible": "The clip mostly shows close-ups of grilling and plated seafood/wagyu. The visible captions align with the description: “hands-free,” sea urchin and wagyu, crab roe/sea urchin kamameshi, cubed wagyu, wagyu tongue, and the juicy chicken-oil/hokki-clam pairing.",
        "sources": [
            "Post metadata and transcript in this folder",
            "OpenRice: https://www.openrice.com.cn/zh/shenzhen/r-%E5%A4%A7%E7%84%A1%E7%87%92%E8%82%89-%E5%90%8E%E6%B5%B7-%E7%87%92%E7%83%A4-r10518993",
            "Apple Maps snippet from web lookup for reservation/average-cost signal",
        ],
    },
    "1700490320": {
        "name": "Alcohol-Infused Adult Ice Cream / 微醺大人冰淇淋",
        "city": "Unknown from available post data",
        "district": "Unknown",
        "address": "Unknown",
        "transit": "Unknown",
        "genre": "Dessert / homemade alcohol-infused ice cream concept",
        "price": "Unknown; this appears to be a recipe/process clip rather than a restaurant listing.",
        "reservation": "Not applicable unless the original Xiaohongshu post identifies a shop; no shop name or booking signal was exposed.",
        "must_try": ["Baraka Black rum or similar dark rum", "rum-soaked raisins", "cream/milk base frozen into cubes"],
        "gist": "This does not provide enough evidence for a specific POI. It looks like a short Xiaohongshu recipe/process video for “adult ice cream”: soak raisins in rum for a day, whip a light cream base, fold in rum raisins, freeze in an ice-cube tray, then eat slowly while watching shows because it has a noticeable alcohol note.",
        "visible": "The contact sheet makes the visible text much clearer than OCR: “朗姆酒,” “泡一天,” “淡奶油,” “打发,” “朗姆酒和葡萄干一起倒入,” “搅拌均匀,” “冰格,” “冷冻,” “吃了会微醺的,” “葡萄干朗姆酒冰淇淋,” “葡萄干吸满了酒味,” “统一脱模放盒子里,” and “追剧的时候慢慢吃.”",
        "sources": ["Post metadata, video frames, and contact sheet in this folder"],
    },
    "1700372224": {
        "name": "Maguro Mart / マグロマート",
        "city": "Tokyo",
        "district": "Nakano",
        "address": "1F/2F, 5-50-3 Nakano, Nakano-ku, Tokyo 164-0001, Japan",
        "transit": "Nakano Station, about 6 minutes on foot; post mentions Tokyo Metro Tozai Line",
        "genre": "Tuna-specialty seafood izakaya; sushi/sashimi/tuna dishes",
        "price": "TableCheck lists tuna courses around ¥3,580-¥4,280 before tax; other listings place dinner roughly around ¥3,500 to ¥6,000+ depending order/course.",
        "reservation": "Recommended and likely needed at peak times. Official/company and TableCheck pages expose reservation flows; third-party listings describe it as popular.",
        "must_try": ["nakaochi scraped from tuna spine", "Maguro Mart tuna platter", "tuna yukke", "fresh bluefin tuna", "tuna bento/takeout"],
        "gist": "A Tokyo food-tour reel presenting Maguro Mart as a destination for tuna lovers near Nakano Station. The hook is the spoon-served nakaochi: scraping tuna from the spine, plus a range of bluefin tuna preparations from sashimi to sushi/yukke.",
        "visible": "The visible captions are mostly English and mirror the narration: best tuna in Tokyo, Tozai Line to Nakano, fresh bluefin only, nakaochi served with a spoon, sashimi/sushi/yukke, and the call to visit Maguro Mart.",
        "sources": [
            "Post metadata and transcript in this folder",
            "Official operator page: https://bout2010.com/",
            "TableCheck: https://www.tablecheck.com/ja/maguro-mart",
            "Enjoy Tokyo: https://www.enjoytokyo.jp/spot/l_20112820/",
        ],
    },
    "1700305381": {
        "name": "鮨冠 OMAKASE食べ放題 (Shenzhen first shop)",
        "city": "Shenzhen",
        "district": "Futian / Xiangmihu",
        "address": "Room 203, 2F, Hengbang Zhidi Building, 3089 Qiaoxiang Road, Xiangmihu Subdistrict, Futian, Shenzhen",
        "transit": "Shenkang Station Exit A, about 1.4 km on foot; also near Qiaocheng North Exit B",
        "genre": "Japanese omakase-style sushi all-you-can-eat / sushi buffet",
        "price": "Post lists two tiers: ¥680 and ¥980. Article/source lookup also describes ¥680 classic and ¥980 premium/limited options.",
        "reservation": "Needed or strongly recommended. The post asks viewers to comment “大壽司” for booking details and lists phone/WeChat 13352907120; another listing says the ¥980 option requires choosing limited or giant sushi format when booking.",
        "must_try": ["giant hand-size sushi", "toro", "sea urchin", "geoduck/large shrimp", "wagyu/foie gras-style items", "15 limited sushi option"],
        "gist": "A Shenzhen omakase-all-you-can-eat clip built around spectacle and value: very large pieces of sushi, a ¥680 entry tier, and a ¥980 upgrade that either unlocks 15 limited sushi pieces or 8 oversized sushi pieces. The creator emphasizes freshness, counter-made sushi, and the visual impact of sushi larger than a phone.",
        "visible": "The useful visible captions match the audio/description: two price tiers, giant sushi several times normal size, ¥680 entry tier, ¥980 higher tier, seafood such as abalone/octopus/shrimp/sea urchin, and a call to comment for booking info.",
        "sources": [
            "Post metadata and transcript in this folder",
            "Headline Daily article: https://www.stheadline.com/food/3486361/",
            "YouTube description lookup for address/booking phone: https://www.youtube.com/watch?v=67LL5suMSIE",
        ],
    },
    "1700301715": {
        "name": "Sushi Song / 壽司宋 SUSHI SONG",
        "city": "Shenzhen",
        "district": "Nanshan / Houhai",
        "address": "Shop 149, 1F, Coastal City Shopping Center, Wenxin 4th Road, Nanshan, Shenzhen",
        "transit": "Houhai Station Exit E2, about 550 m on foot",
        "genre": "High-end Japanese omakase / sushi counter",
        "price": "Post says per-person price is in the ¥500-plus range.",
        "reservation": "Strongly recommended. The post says there are only 12 counter seats; an external Hong Kong database lookup listed booking phone numbers 0755-86699499 and 18025327167.",
        "must_try": ["70g giant sushi", "sea urchin", "black truffle", "botan shrimp", "caviar/French-style item", "wagyu sukiyaki", "large ark shell", "sea urchin hand roll"],
        "gist": "A luxury but comparatively affordable Shenzhen omakase reel, selling the shock value of 65-70g palm-size sushi made by a chef associated with Beijing Black Pearl credentials. The analysis of the video/audio suggests a rich course progression: botan shrimp and sea urchin sashimi, caviar, abalone udon, wagyu sukiyaki, fish-bone tempura, black truffle, flower-maw soup, giant hand-held sushi, large shellfish, sea urchin hand roll, and layered dessert.",
        "visible": "OCR is noisy, but the readable captions and transcript point to the same thesis: ¥500-plus per person, rare ingredients, 70g giant sushi, only 12 counter seats, and a visually dramatic chef-counter experience.",
        "sources": [
            "Post metadata and transcript in this folder",
            "OpenRice: https://www.openrice.com.cn/zh/shenzhen/r-%E5%A3%BD%E5%8F%B8%E5%AE%8Bsushi-song-%E5%90%8E%E6%B5%B7-%E6%97%A5%E6%9C%AC%E8%8F%9C-r10329464",
            "Hong Kong web database lookup: https://magnumho.com/archives/20770",
        ],
    },
    "1700298280": {
        "name": "Yingu Omakase / 隐谷Omakase (Futian Fortune Building)",
        "city": "Shenzhen",
        "district": "Futian / Gangxia / Convention and Exhibition Center area",
        "address": "Room 41B, Fortune Building, 88 Fuhua 3rd Road, Gangxia Community, Futian Subdistrict, Shenzhen",
        "transit": "Gangxia / Futian CBD area; exact station not stated in the post",
        "genre": "High-rise Japanese omakase / sushi and sashimi counter",
        "price": "Apple Maps lookup showed average cost about ¥634; Trip.com listed US$128; OpenRice categorizes it as ¥301+.",
        "reservation": "Recommended. It is a 41st-floor omakase with award/chef positioning; Trip.com lists phone +86 19925479087.",
        "must_try": ["Russian botan shrimp", "scallop hand roll", "teppan kuruma/prawn", "chawanmushi", "sea urchin crab cup", "sea urchin sashimi trio", "toro mince with three layers of sea urchin", "bluefin tuna sushi", "wild honey tamagoyaki"],
        "gist": "A high-rise Futian omakase reel emphasizing skyline views over Shenzhen/Hong Kong and a seafood-heavy course. The strongest selling points are the 41st-floor setting, premium shellfish/sea urchin/toro sequence, and a progression from appetizers to teppan seafood, chawanmushi, sushi, and fruit ice cream.",
        "visible": "OCR is noisy, but enough visible/video context supports the main interpretation: high-rise omakase, Shenzhen/Hong Kong view, sea urchin-focused dishes, sushi sequence, and a high-end but social-media-friendly dining experience.",
        "sources": [
            "Post metadata and transcript in this folder",
            "Trip.com: https://us.trip.com/restaurant/china/shenzhen/detail/restaurant-114846698",
            "OpenRice search result and Apple Maps snippet from web lookup",
        ],
    },
    "1700297979": "1700298280",
}


def read_text(path):
    return path.read_text(errors="replace").strip() if path.exists() else ""


def compact(text, limit=3500):
    text = (text or "").strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "\n[truncated]"


def profile_for(bookmark_id):
    profile = PROFILES[str(bookmark_id)]
    if isinstance(profile, str):
        profile = PROFILES[profile]
    return profile


def render(out_dir):
    manifest_path = out_dir / "analysis.json"
    manifest = json.loads(manifest_path.read_text())
    bookmark_id = str(manifest["bookmark_id"])

    if manifest["status"] != "success":
        md = f"""# Analysis unavailable

Source: {manifest.get("source_url", "")}

Bookmark id: {bookmark_id}
Updated: {datetime.now(timezone.utc).isoformat()}

## Status

This bookmark could not be downloaded or parsed, so there is no reliable video/audio-based POI analysis.

## Failure

{compact(manifest.get("error") or read_text(out_dir / "error.txt"), 2000)}
"""
        (out_dir / "analysis.md").write_text(md)
        return

    profile = profile_for(bookmark_id)
    info = json.loads((out_dir / "source.info.json").read_text()) if (out_dir / "source.info.json").exists() else {}
    transcript = read_text(out_dir / "audio.txt")
    visible = read_text(out_dir / "visible_text.txt")
    description = info.get("description") or info.get("title") or ""
    comments = info.get("comments")
    if comments:
        comments_text = "\n".join(f"- {c.get('text', c)}" if isinstance(c, dict) else f"- {c}" for c in comments[:10])
    else:
        comments_text = "Top comments unavailable. `yt-dlp` metadata, including a dedicated `--write-comments` probe, did not expose public comments for this post. Facebook/Xiaohongshu often require logged-in app/browser access for comment threads."

    md = f"""# {profile["name"]}

Source: {manifest.get("source_url", "")}

Bookmark id: {bookmark_id}
Updated: {datetime.now(timezone.utc).isoformat()}

## POI Snapshot

- City: {profile["city"]}
- Area: {profile["district"]}
- Address: {profile["address"]}
- Transit: {profile["transit"]}
- Food genre: {profile["genre"]}
- Price point: {profile["price"]}
- Reservations: {profile["reservation"]}

## What The Post Says

{compact(description, 4000) or "No post description was exposed."}

## Top Comments

{comments_text}

## Deeper Analysis

{profile["gist"]}

## Food / Experience Notes

- Best-fit genre: {profile["genre"]}
- Price interpretation: {profile["price"]}
- Reservation interpretation: {profile["reservation"]}
- Items to pay attention to: {", ".join(profile["must_try"])}

## Visible Text Interpreted

{profile["visible"]}

## Audio Transcript

{compact(transcript, 5000) or "No usable speech transcript was produced."}

## Raw OCR

The raw OCR is kept for traceability, but the interpreted visible-text section above should be used for analysis because vertical short-form videos produced noisy OCR.

{compact(visible, 5000) or "No visible text OCR was produced."}

## Source Notes

{chr(10).join(f"- {source}" for source in profile["sources"])}
"""
    (out_dir / "analysis.md").write_text(md)
    manifest["enriched_at"] = datetime.now(timezone.utc).isoformat()
    manifest["analysis_version"] = 2
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def main():
    for out_dir in sorted(OUT_ROOT.iterdir()):
        if out_dir.is_dir() and (out_dir / "analysis.json").exists():
            render(out_dir)


if __name__ == "__main__":
    main()
