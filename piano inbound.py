import logging
import asyncio
from signalwire.relay.consumer import Consumer

#+1 (201) 277-7289

class CustomConsumer(Consumer):
    def setup(self):
        self.project = '39110476-c4c2-4d14-bc31-649124db175f'
        self.token = 'PTc77486d2a6276b3f00469f9c23096d7ee980ed1e4fb23f56'
        self.contexts = ['office']

    async def ready(self):
        logging.info('CustomConsumer is ready!')

    async def on_incoming_call(self, call):
        async def on_digit(data):
            digit = data["params"]["event"]
            audio = ["https://www.dropbox.com/s/o53k2icx4xul3b2/piano-mp3_C4.mp3?dl=1", "https://www.dropbox.com/s/wa4vtzws5gc8p5e/piano-mp3_D4.mp3?dl=1",
                     "https://www.dropbox.com/s/ys2mexeh1m8dmge/piano-mp3_E4.mp3?dl=1", "https://www.dropbox.com/s/0qcrbmwde6hbyyi/piano-mp3_F4.mp3?dl=1",
                     "https://www.dropbox.com/s/ho18x3an719wpwn/piano-mp3_G4.mp3?dl=1", "https://www.dropbox.com/s/zf976io7w2c1pkd/piano-mp3_A4.mp3?dl=1",
                     "https://www.dropbox.com/s/0egjt8hv6gka7rs/piano-mp3_B4.mp3?dl=1", "https://www.dropbox.com/s/5zqr9ubjvidakk9/piano-mp3_C5.mp3?dl=1"]
            logging.info('digit: ' + digit)
            if(digit == '#'):
                await call.hangup()
            else:
                await call.play_audio(audio[int(digit) - 1], volume = 35)


        result = await call.answer()            
        if result.successful:
            await asyncio.sleep(1)
            await call.play_tts(text='Welcome to phone piano. Enter one through 8 on your dial pad to play notes. Pound to exit', gender = 'male')
      
            call.on('detect.update', on_digit)
            action = await call.detect_digit_async(digits = '12345678#', timeout = 900)
            while (call.active and not action.completed):
                await asyncio.sleep(1)

            await action.stop()
        logging.info('Hanging up..')
        await call.hangup()

consumer = CustomConsumer()
consumer.run()
