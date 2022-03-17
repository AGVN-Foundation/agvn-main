import torch
from torch.autograd import Variable

from config import device
from PIL import Image

import BAUtils

import warnings

warnings.filterwarnings("ignore")

FILE = 'savedModel.pth'
data = torch.load(FILE, map_location=torch.device('cpu'))

model = BAUtils.net.to(device)
model.load_state_dict(data)
model.eval()
transform = BAUtils.transform('test')

labels = ['assault', 'bullying', 'fun', 'giving blood', 'helping others', 'riots', 'stealing', 'teamwork', 'vandalism', 'volunteering']

print("Let's guess your behaviour! (type 'quit' to exit)")

while True:

    img_path = input("Enter an image file path:\n")
    if img_path == "quit" or img_path == 'q':
        break
    try:
        image = Image.open(img_path)
    except Exception:
        print('invalid path')
        continue
    image = transform(image).float()
    image = Variable(image, requires_grad=True)
    image = image.unsqueeze(0)
    image = image.to(device)
    output = model(image)
    _, predicted = torch.max(output, dim=1)
    print(f'Predicted as a case of {labels[predicted.item()]}')
