# discord-bot
## Greeting
### $hello
- Responds with Hello!

## Ai Question
### $ask
- Requires ollama installed and open
- Responds to prompt after $ask e.g. $ask <ins>what colour is the sky</ins>

## Music player
- Requires ffmpeg
### $play
- Plays youtube url in vc you are currently in after $play e.g. $play <ins>https://www.youtube.com/watch?v=dQw4w9WgXcQ</ins>
- If bot is already playing audio, song/url will be added to queue
- Must be in a vc
### $search
- Returns title, channel, and url of the top 5 search results from youtube of query after $search e.g. $search <ins>Never gonna give you up</ins>
### $queue
- Check the current queue
### $skip
- Skip the currently playing song
### $clear
- Clears the queue

## Pokemon
- Requires sqlite for db
### $pokemon_info
- Gets universal info on a specified pokemon after $pokemon_info e.g. $pokemon_info <ins>pikachu</ins>
### $random_pokemon
- Gets random pokemon and adds it to your collection
### $view_pokemon
- View your currently owned pokemon