import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from dotenv import load_dotenv
import isodate

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def parse_duration(duration_str):
    try:
        dur = isodate.parse_duration(duration_str)
        return int(dur.total_seconds() / 60)
    except Exception as e:
        print(f"[!] Error parsing duration '{duration_str}': {e}")
        return 0

def search_youtube(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    published_after = (datetime.utcnow() - timedelta(days=14)).isoformat("T") + "Z"

    print("\n🔍 Searching YouTube...")
    search_response = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=25,
        publishedAfter=published_after,
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
    if not video_ids:
        print("[!] No video IDs found. Try a simpler query.")
        return []

    video_response = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=",".join(video_ids)
    ).execute()

    videos = []

    print("\n🎥 Raw Videos (Pre-filtered):")
    for item in video_response.get("items", []):
        title = item["snippet"]["title"]
        duration_str = item["contentDetails"]["duration"]
        duration = parse_duration(duration_str)
        views = int(item.get("statistics", {}).get("viewCount", 0))
        url = f"https://www.youtube.com/watch?v={item['id']}"

        print(f"- {title} | {duration} mins | {views} views")

        # Filter duration between 4 and 20 mins
        if 4 <= duration <= 20:
            videos.append({
                "title": title,
                "url": url,
                "duration": duration,
                "views": views
            })

    return videos

def find_best_video(videos, query):
    query_words = query.lower().split()
    scored = []

    for v in videos:
        title_words = v['title'].lower().split()
        match_count = sum(1 for word in query_words if word in title_words)
        scored.append((match_count, v['views'], v))

    scored.sort(reverse=True)
    return scored[0][2] if scored else None

def main():
    query = input("🎤 Enter your search query (English/Hindi): ").strip()
    print(f"\n🔍 Searching for: '{query}'")

    videos = search_youtube(query)

    if not videos:
        print("\n❌ No suitable videos found. Try a different query.")
        return

    print("\n✅ Filtered Videos (4–20 mins):")
    for i, v in enumerate(videos):
        print(f"{i+1}. {v['title']} ({v['duration']} mins, {v['views']} views)\n   🔗 {v['url']}")

    best = find_best_video(videos, query)
    if best:
        print(f"\n🏆 Best Match:\n📌 {best['title']} ({best['duration']} mins, {best['views']} views)\n🔗 {best['url']}")
    else:
        print("⚠️ Couldn't determine best video.")

if __name__ == "__main__":
    main()
