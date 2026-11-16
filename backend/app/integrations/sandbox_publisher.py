"""
ContentIQ - Sandbox Social Media Publisher Adapter
Simulates posting to Instagram, LinkedIn, and YouTube without calling external APIs.
Guarantees zero external network dependencies for demo, viva, and academic evaluation.
"""
import uuid
from datetime import datetime
from typing import Dict, Any

class SandboxPublisher:
    """
    Sandbox adapter simulating social media platform publishing.
    Generates deterministic mock external IDs and platform responses.
    """

    @staticmethod
    def publish(post: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate publishing a post to the designated platform.
        
        Args:
            post: Post dictionary containing platform, caption, media_url, etc.
            
        Returns:
            Dictionary containing simulated platform status and external reference ID.
        """
        platform = post.get("platform", "unknown").lower()
        post_id = str(post.get("_id", post.get("id", uuid.uuid4())))
        now_local = datetime.now().isoformat()

        # Generate realistic platform-specific external identifiers
        if platform == "instagram":
            external_id = f"ig_media_{uuid.uuid4().hex[:12]}"
            permalink = f"https://sandbox.instagram.com/p/{external_id}"
        elif platform == "linkedin":
            external_id = f"urn:li:share:{uuid.uuid4().int % 10000000000}"
            permalink = f"https://sandbox.linkedin.com/feed/update/{external_id}"
        elif platform == "youtube":
            external_id = f"yt_{uuid.uuid4().hex[:11]}"
            permalink = f"https://sandbox.youtube.com/watch?v={external_id}"
        else:
            external_id = f"sandbox_{uuid.uuid4().hex[:10]}"
            permalink = f"https://sandbox.contentiq.io/posts/{external_id}"

        return {
            "status": "success",
            "simulated": True,
            "platform": platform,
            "platform_post_id": external_id,
            "permalink": permalink,
            "published_at": now_local,
            "message": f"Successfully published to {platform.capitalize()} via ContentIQ Sandbox Publisher (Simulated)."
        }
