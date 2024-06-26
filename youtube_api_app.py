from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_youtube_channel_info(api_key, channel_id):
    url = 'https://www.googleapis.com/youtube/v3/channels'
    params = {
        'part': 'snippet,statistics',
        'id': channel_id,
        'key': api_key
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'items' in data and len(data['items']) > 0:
            channel = data['items'][0]
            basic_info = {
                'title': channel['snippet']['title'],
                'description': channel['snippet']['description'],
                'published_at': channel['snippet']['publishedAt'],
                'subscriber_count': channel['statistics']['subscriberCount'],
                'video_count': channel['statistics']['videoCount'],
                'view_count': channel['statistics']['viewCount']
            }
            return basic_info
        else:
            return None
    else:
        return None

@app.route('/channel/info', methods=['GET'])
def get_channel_info():
    api_key = request.args.get('api_key')
    channel_ids = request.args.getlist('channel_id')

    if not api_key or not channel_ids:
        return jsonify({"error": "API key and at least one channel ID are required"}), 400
    
    if len(channel_ids) > 3:
        return jsonify({"error": "Up to 3 channel IDs can be specified"}), 400
    
    results = {}
    for channel_id in channel_ids:
        info = get_youtube_channel_info(api_key, channel_id)
        if info:
            results[channel_id] = info
        else:
            results[channel_id] = "Channel not found or error occurred"

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
