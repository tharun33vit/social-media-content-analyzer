"""Generate sample social media post files for manual and integration testing."""

import io
import os
import fitz
from PIL import Image, ImageDraw, ImageFont

os.makedirs("demo_samples", exist_ok=True)

# 1. Generate sample social post PDF
pdf_doc = fitz.open()
page = pdf_doc.new_page()
pdf_text = (
    "Are you still writing social media posts without a clear hook?\n\n"
    "Most founders lose 80% of readers before sentence two because the opening is too vague.\n\n"
    "Here are 3 simple principles to boost engagement today:\n"
    "1. Keep your opening line under 80 characters.\n"
    "2. Share a specific insight rather than generic advice.\n"
    "3. Ask a single question to prompt genuine discussion.\n\n"
    "What has been your most effective social media tip this quarter? Share your thoughts below!\n\n"
    "#ContentStrategy #SocialMediaMarketing #StartupGrowth"
)
page.insert_text((50, 72), pdf_text, fontsize=12)
pdf_doc.save("demo_samples/sample_social_post.pdf")
pdf_doc.close()
print("Created demo_samples/sample_social_post.pdf")

# 2. Generate sample social post Image (PNG)
img = Image.new("RGB", (800, 400), color=(255, 255, 255))
draw = ImageDraw.Draw(img)
# Draw text cleanly with high contrast
draw.text((40, 40), "Top 3 lessons learned after scaling from 0 to 10k users:", fill=(15, 23, 42))
draw.text((40, 90), "1. Ship small features quickly and talk to users weekly.", fill=(51, 65, 85))
draw.text((40, 140), "2. Focus on organic word-of-mouth rather than paid ads early.", fill=(51, 65, 85))
draw.text((40, 190), "3. Clear documentation saves hundreds of support hours.", fill=(51, 65, 85))
draw.text((40, 250), "Which lesson resonates most with you? Let me know below!", fill=(15, 23, 42))
draw.text((40, 310), "#BuildingInPublic #SaaS #Growth", fill=(100, 116, 139))
img.save("demo_samples/sample_social_post.png")
print("Created demo_samples/sample_social_post.png")
