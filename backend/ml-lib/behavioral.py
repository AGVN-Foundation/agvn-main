import torch
from torch.autograd import Variable

from PIL import Image

from config import device
import BAUtils

import warnings

warnings.filterwarnings("ignore")

FILE = 'savedModel.pth'
data = torch.load(FILE, map_location=torch.device('cpu'))

model = BAUtils.net.to(device)
model.load_state_dict(data)
model.eval()
transform = BAUtils.transform('test')

labels = ['assault', 'bullying', 'fun', 'giving blood', 'helping others',
          'riots', 'stealing', 'teamwork', 'vandalism', 'volunteering']


def predict_behavior(img_path):
    try:
        image = Image.open(img_path)
    except Exception:
        return 'invalid path'

    image = transform(image).float()
    image = Variable(image, requires_grad=True)
    image = image.unsqueeze(0)
    image = image.to(device)
    output = model(image)
    _, predicted = torch.max(output, dim=1)
    print(f'Predicted as a case of {labels[predicted.item()]}')

    return labels[predicted.item()]
