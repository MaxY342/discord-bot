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
- Plays youtube url in vc you are currently in after $play e.g. $play <ins>(youtube song url)</ins>
- If bot is already playing audio, song/url will be added to queue
- must be in a vc
### $queue
- Check the current queue
### $skip
- Skip the currently playing song
### $clear
- Clears the queue