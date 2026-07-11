import json
from datetime import datetime, timezone


def current_timestamp():
    return datetime.now(timezone.utc).isoformat()


# ------------------------------------
# VIDEO
# ------------------------------------

def transform_video(video, snapshot_date):
    stats = video.get("statistics", {})
    category_id = video["snippet"].get("categoryId")

    return {
        "video_id": video["id"],
        "channel_id": video["snippet"]["channelId"],
        "title": video["snippet"]["title"],
        "published_at": video["snippet"]["publishedAt"],
        "category_id": int(category_id) if category_id else None,
        "duration_iso": video["contentDetails"]["duration"],
        "view_count": int(stats.get("viewCount", 0)),
        "like_count": int(stats.get("likeCount", 0)),
        "comment_count": int(stats.get("commentCount", 0)),
        "tags": video["snippet"].get("tags", []),
        "snapshot_date": snapshot_date,
        "raw_data": json.dumps(video),
        "loaded_at": current_timestamp()
    }


# ------------------------------------
# COMMENT
# ------------------------------------

def transform_comment(comment):

    return {

        "comment_id": comment["comment_id"],
        "video_id": comment["video_id"],
        "author": comment["author"],
        "comment_text": comment["text"],
        "like_count": int(comment.get("like_count", 0)),
        "reply_count": int(comment.get("reply_count", 0)),
        "published_at": comment["published_at"],
        "raw_data": json.dumps(comment),
        "loaded_at": current_timestamp()

    }


# ------------------------------------
# CHANNEL
# ------------------------------------

def transform_channel(channel, snapshot_date):

    stats = channel.get("statistics", {})

    return {

        "channel_id": channel["id"],
        "title": channel["snippet"]["title"],
        "custom_url": channel["snippet"].get("customUrl"),
        "published_at": channel["snippet"]["publishedAt"],
        "subscriber_count": int(stats.get("subscriberCount", 0)),
        "view_count_total": int(stats.get("viewCount", 0)),
        "video_count": int(stats.get("videoCount", 0)),
        "snapshot_date": snapshot_date,
        "raw_data": json.dumps(channel),
        "loaded_at": current_timestamp()

    }


# ------------------------------------
# PLAYLIST
# ------------------------------------

def transform_playlist(playlist):

    return {

        "playlist_id": playlist["id"],
        "channel_id": playlist["snippet"]["channelId"],
        "title": playlist["snippet"]["title"],
        "description": playlist["snippet"].get("description", ""),
        "published_at": playlist["snippet"]["publishedAt"],
        "item_count": int(
            playlist["contentDetails"]["itemCount"]
        ),
        "raw_data": json.dumps(playlist),
        "loaded_at": current_timestamp()

    }


# ------------------------------------
# PLAYLIST ITEM
# ------------------------------------

def transform_playlist_item(item):

    return {

        "playlist_id": item["playlist_id"],
        "video_id": item["video_id"],
        "position": int(item["position"]),
        "added_at": item["added_at"],
        "loaded_at": current_timestamp()

    }


# ------------------------------------
# CATEGORY
# ------------------------------------

def transform_category(category):

    return {
        "category_id": category["id"],
        "title": category["snippet"]["title"],
        "assignable": category["snippet"].get(
            "assignable",
            False
        ),
        "raw_data": json.dumps(category),
        "loaded_at": current_timestamp()
    }