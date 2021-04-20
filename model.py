import pandas as pd
import numpy as np
from PIL import Image
import torch
from torchvision.models.resnet import resnet18
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
from torch.optim.lr_scheduler import CosineAnnealingLR
from tqdm import tqdm
from torch.utils.data import Dataset
from torchvision import transforms

label_to_expression = {
    1:'Surprise',
    2:'Fear',
    3:'Disgust',
    4:'Happiness',
    5:'Sadness',
    6:'Anger',
    7:'Neutral'
}

transform_test = transforms.Compose([
    transforms.ToTensor(),
])

torch.manual_seed(0)
np.random.seed(0)
cpu = torch.load('static/rafdb_resnet18.pth', map_location=torch.device('cpu'))
cpu.eval()

def pil_loader(path: str) -> Image.Image:
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')

def predictImage(img):
  # img = pil_loader(filepath)
  img = transform_test(img)
  img = img.unsqueeze(0)
  
  with torch.no_grad():
    output = cpu(img)
  return label_to_expression[(int)(output.argmax() + 1)]

