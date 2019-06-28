from PIL import Image, ImageFont, ImageDraw
import speech_recognition as sr
import random, textwrap

# Add global variables used in entire application
IMAGE_URL = 'meme.jpg'
FONT_TYPE = 'fonts/opensans.ttf'
SAMPLE_TEXT = 'this is a sample text this is a sample text this is a sample text'
WIDTH = 0
HEIGHT = 0

# Get random meme image from images folder
def get_rand_img():
  image_names = ['freak_out', 'mr_bean', 'obi', 'One', 'sung', 'kate', 'cat', 'LoPan']
  random_num = random.randint(0, len(image_names) - 1)
  image_url = "img/{}.jpg".format(image_names[random_num])
  try:
    img = Image.open(image_url)
    return img
  except IOError as e:
    print('IOError: {0}'.format(e))
    return None

# Get text from computer microphone using Google Speech Recognition
def get_txt_from_speech():
  r = sr.Recognizer()
  with sr.Microphone() as source:
      print("Say something!")
      audio = r.listen(source)
  try:
      # for testing purposes, we're just using the default API key
      # to use another API key, use
      # `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
      # instead of `r.recognize_google(audio)`
      print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
  except sr.UnknownValueError:
      print("Google Speech Recognition could not understand audio")
  except sr.RequestError as e:
      print("Could not request results from Google Speech Recognition service; {0}".format(e))
  raw_text = r.recognize_google(audio)
  initial_txt = raw_text if raw_text!=None else SAMPLE_TEXT
  txt = textwrap.fill(initial_txt, width=WIDTH/15)
  return txt

# Add the text on the image and return final image
def overlay_text_on_image(img, txt):
  draw = ImageDraw.Draw(img)

  # Draw black box at the bottom and add wrapped text
  font = ImageFont.truetype(FONT_TYPE, int(HEIGHT/25))
  draw.rectangle(((WIDTH/10, HEIGHT*(8/10)), (WIDTH*(9/10), HEIGHT*(19/20))), fill='black')
  draw.text((WIDTH/10, HEIGHT*(8/10)), txt, fill='white', font=font)

  return img

if __name__ == '__main__':
  # First get the random image
  img = get_rand_img()

  # Store global variables
  WIDTH, HEIGHT = img.size

  # Second get the text from the user microphone
  txt = get_txt_from_speech()

  # Ensure that both the txt and img are valid
  if img != None and txt != None:
    meme = overlay_text_on_image(img, txt)
    meme.save(IMAGE_URL)
    meme.show()
  else:
    print('Error: Image or text not valid')
