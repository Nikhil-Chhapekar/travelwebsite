import os
import urllib.request
import ssl

# Bypass SSL certificate verification (for simplicity in this example)
ssl._create_default_https_context = ssl._create_unverified_context

# Create directories if they don't exist
def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Base directories
static_dir = 'static/images'
destinations_dir = os.path.join(static_dir, 'destinations')
accommodations_dir = os.path.join(static_dir, 'accommodations')
activities_dir = os.path.join(static_dir, 'activities')
backgrounds_dir = os.path.join(static_dir, 'backgrounds')
team_dir = os.path.join(static_dir, 'team')

# Ensure all directories exist
for directory in [destinations_dir, accommodations_dir, activities_dir, backgrounds_dir, team_dir]:
    ensure_dir(directory)

# Destination images from Unsplash
destination_images = {
    'bali.jpg': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&auto=format&fit=crop',
    'santorini.jpg': 'https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&auto=format&fit=crop',
    'maldives.jpg': 'https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=800&auto=format&fit=crop',
    'paris.jpg': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&auto=format&fit=crop',
    'kyoto.jpg': 'https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=800&auto=format&fit=crop',
    'machu-picchu.jpg': 'https://images.unsplash.com/photo-1526392060635-9d6019884377?w=800&auto=format&fit=crop',
    'beach-category.jpg': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&auto=format&fit=crop',
    'mountain-category.jpg': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&auto=format&fit=crop',
    'city-category.jpg': 'https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800&auto=format&fit=crop',
    'cultural-category.jpg': 'https://images.unsplash.com/photo-1583422409516-2895a77efded?w=800&auto=format&fit=crop',
    'placeholder.jpg': 'https://images.unsplash.com/photo-1488085061387-422e29b40080?w=800&auto=format&fit=crop',
}

# Accommodation images
accommodation_images = {
    'hotel-1.jpg': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&auto=format&fit=crop',
    'hotel-2.jpg': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&auto=format&fit=crop',
    'hotel-3.jpg': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&auto=format&fit=crop',
    'room-1.jpg': 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&auto=format&fit=crop',
    'room-2.jpg': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&auto=format&fit=crop',
    'placeholder.jpg': 'https://images.unsplash.com/photo-1496417263034-38ec4f0b665a?w=800&auto=format&fit=crop',
}

# Activity images
activity_images = {
    'activity-1.jpg': 'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&auto=format&fit=crop',
    'activity-2.jpg': 'https://images.unsplash.com/photo-1526976668912-1a811878dd37?w=800&auto=format&fit=crop',
    'activity-3.jpg': 'https://images.unsplash.com/photo-1530789253388-582c481c54b0?w=800&auto=format&fit=crop',
    'activity-4.jpg': 'https://images.unsplash.com/photo-1504609773096-104ff2c73ba4?w=800&auto=format&fit=crop',
    'activity-5.jpg': 'https://images.unsplash.com/photo-1505228395891-9a51e7e86bf6?w=800&auto=format&fit=crop',
    'activity-6.jpg': 'https://images.unsplash.com/photo-1514984879728-be0aff75a6e8?w=800&auto=format&fit=crop',
    'placeholder.jpg': 'https://images.unsplash.com/photo-1452421822248-d4c2b47f0c81?w=800&auto=format&fit=crop',
}

# Background images
background_images = {
    'hero-bg.jpg': 'https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?w=1200&auto=format&fit=crop',
    'cta-bg.jpg': 'https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1200&auto=format&fit=crop',
    'destinations-bg.jpg': 'https://images.unsplash.com/photo-1488085061387-422e29b40080?w=1200&auto=format&fit=crop',
}

# Team images
team_images = {
    'team-1.jpg': 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&auto=format&fit=crop',
    'team-2.jpg': 'https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&auto=format&fit=crop',
    'team-3.jpg': 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=400&auto=format&fit=crop',
}

# Other images
other_images = {
    'about-us.jpg': 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=800&auto=format&fit=crop',
    'mission.jpg': 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?w=800&auto=format&fit=crop',
    'default-profile.jpg': 'https://images.unsplash.com/photo-1511367461989-f85a21fda167?w=400&auto=format&fit=crop',
}

# Download images
def download_images(image_dict, directory):
    for filename, url in image_dict.items():
        filepath = os.path.join(directory, filename)
        # Force download even if file exists
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, filepath)
            print(f"Downloaded {filename}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

# Download all images
print("Downloading destination images...")
download_images(destination_images, destinations_dir)

print("\nDownloading accommodation images...")
download_images(accommodation_images, accommodations_dir)

print("\nDownloading activity images...")
download_images(activity_images, activities_dir)

print("\nDownloading background images...")
download_images(background_images, backgrounds_dir)

print("\nDownloading team images...")
download_images(team_images, team_dir)

print("\nDownloading other images...")
download_images(other_images, static_dir)

print("\nAll images downloaded successfully!")
